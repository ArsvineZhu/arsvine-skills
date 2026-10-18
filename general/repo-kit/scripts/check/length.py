#!/usr/bin/env python3
"""Check repository files against configurable line-count warn/block limits."""

from __future__ import annotations

import argparse
import fnmatch
import re
import sys
import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

CONFIG_NAME = "length.toml"
PROJECT_CONFIG_DIR = Path(".config") / "arsvine-skills"
SEVERITY = {"warn": 1, "block": 2}
HEADER_LINES = 40
WAIVER_RE = re.compile(r'repo-kit:\s*allow\s+length\s+reason="([^"\n]+)"', re.I)


def resolve_config(explicit: Path | None, project: Path, name: str) -> Path:
    """Resolve project config at `.config/arsvine-skills/` (Skill scripts/.config is install seed only)."""
    if explicit is not None:
        path = explicit.expanduser()
        path = path if path.is_absolute() else (project / path)
        if not path.is_file():
            raise ValueError(f"config not found: {path}")
        return path.resolve()
    candidate = project / PROJECT_CONFIG_DIR / name
    if candidate.is_file():
        return candidate.resolve()
    raise ValueError(f"config not found: {candidate}")


@dataclass(frozen=True)
class Limits:
    warn: int
    block: int


@dataclass(frozen=True)
class Waiver:
    path: str
    reason: str
    source: str  # "inline" | "config"


@dataclass(frozen=True)
class Config:
    default: Limits
    extensions: dict[str, Limits]
    exclude: tuple[str, ...]
    waivers: dict[str, Waiver]


@dataclass(frozen=True)
class Finding:
    path: str
    lines: int
    level: str
    limit: int
    note: str


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locate", type=Path, default=Path.cwd(), help="Repository root to scan (default: cwd)")
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Config path; default: .config/arsvine-skills/length.toml",
    )
    parser.add_argument("--fail-on", choices=("never", "warn", "block"), default="block")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    return parser.parse_args(argv)


def load_config(path: Path) -> Config:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1:
        raise ValueError(f"unsupported length config version: {data.get('version')!r}")
    limits = data.get("limits") or {}
    default_raw = limits.get("default") or {}
    default = Limits(int(default_raw.get("warn", 400)), int(default_raw.get("block", 800)))
    if default.warn <= 0 or default.block <= 0 or default.warn > default.block:
        raise ValueError("limits.default warn/block must satisfy 0 < warn <= block")
    extensions: dict[str, Limits] = {}
    for ext, raw in (limits.get("extensions") or {}).items():
        key = ext if ext.startswith(".") else f".{ext}"
        item = Limits(int(raw["warn"]), int(raw["block"]))
        if item.warn <= 0 or item.block <= 0 or item.warn > item.block:
            raise ValueError(f"limits.extensions.{ext} warn/block must satisfy 0 < warn <= block")
        extensions[key.lower()] = item
    exclude = tuple(str(item) for item in data.get("exclude") or [])
    waivers: dict[str, Waiver] = {}
    for raw in data.get("waivers") or []:
        rel = str(raw["path"]).replace("\\", "/").lstrip("./")
        reason = str(raw.get("reason") or "").strip()
        if len(reason) < 8:
            raise ValueError(f"config waiver for {rel!r} needs a reason of at least eight characters")
        if rel in waivers:
            raise ValueError(f"duplicate config waiver path: {rel}")
        waivers[rel] = Waiver(rel, reason, "config")
    return Config(default, extensions, exclude, waivers)


def excluded(rel: str, patterns: Sequence[str]) -> bool:
    posix = rel.replace("\\", "/")
    parts = frozenset(posix.split("/"))
    for pattern in patterns:
        if fnmatch.fnmatch(posix, pattern):
            return True
        # Python fnmatch does not treat ** as recursive; honor **/dir/** by path part.
        if pattern.startswith("**/") and pattern.endswith("/**"):
            name = pattern[3:-3]
            if name and ("/" not in name) and name in parts:
                return True
        trimmed = pattern[3:] if pattern.startswith("**/") else pattern
        if trimmed.endswith("/**"):
            trimmed = trimmed[:-3] + "/*"
        if trimmed != pattern and fnmatch.fnmatch(posix, trimmed):
            return True
    return False


def iter_files(root: Path, config: Config) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root).as_posix()
        if excluded(rel, config.exclude):
            continue
        yield path


def read_text(path: Path) -> str | None:
    try:
        data = path.read_bytes()
    except OSError:
        return None
    if b"\x00" in data[:8192]:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def count_lines(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def comment_body(line: str) -> str | None:
    """Return the body of a comment line, or None when the line is not a comment."""
    stripped = line.strip()
    if not stripped:
        return None
    if stripped.startswith("<!--") and stripped.endswith("-->"):
        return stripped[4:-3].strip()
    for prefix in ("#", "//", "--"):
        if stripped.startswith(prefix):
            return stripped[len(prefix) :].strip()
    if stripped.startswith("*") and not stripped.startswith("**"):
        return stripped[1:].strip()
    return None


def inline_waiver(rel: str, text: str) -> Waiver | None:
    matches: list[re.Match[str]] = []
    for line in text.splitlines()[:HEADER_LINES]:
        body = comment_body(line)
        if body is None:
            continue
        match = WAIVER_RE.fullmatch(body)
        if match:
            matches.append(match)
    if not matches:
        return None
    if len(matches) > 1:
        raise ValueError(f"{rel}: multiple inline length waivers in the first {HEADER_LINES} lines")
    reason = matches[0].group(1).strip()
    if len(reason) < 8:
        raise ValueError(f"{rel}: inline length waiver needs a reason of at least eight characters")
    return Waiver(rel, reason, "inline")


def limits_for(path: Path, config: Config) -> Limits:
    return config.extensions.get(path.suffix.lower(), config.default)


def resolve_waiver(rel: str, inline: Waiver | None, config: Config) -> Waiver | None:
    configured = config.waivers.get(rel)
    if inline and configured:
        raise ValueError(f"{rel}: remove the config waiver; an inline waiver already exists")
    return inline or configured


def scan(root: Path, config: Config) -> tuple[list[Finding], list[dict[str, object]]]:
    findings: list[Finding] = []
    used_waivers: list[dict[str, object]] = []
    for path in iter_files(root, config):
        rel = path.relative_to(root).as_posix()
        text = read_text(path)
        if text is None:
            continue
        lines = count_lines(text)
        limits = limits_for(path, config)
        waiver = resolve_waiver(rel, inline_waiver(rel, text), config)
        if lines > limits.block:
            if waiver:
                used_waivers.append(
                    {
                        "path": rel,
                        "reason": waiver.reason,
                        "source": waiver.source,
                        "lines": lines,
                        "limit": limits.block,
                    }
                )
                continue
            findings.append(Finding(rel, lines, "block", limits.block, f"exceeds block limit {limits.block}"))
        elif lines > limits.warn:
            if waiver:
                used_waivers.append(
                    {
                        "path": rel,
                        "reason": waiver.reason,
                        "source": waiver.source,
                        "lines": lines,
                        "limit": limits.warn,
                    }
                )
                continue
            findings.append(Finding(rel, lines, "warn", limits.warn, f"exceeds warn limit {limits.warn}"))
        elif waiver:
            raise ValueError(f"{rel}: unused {waiver.source} length waiver (file is within limits)")
    used_paths = {str(item["path"]) for item in used_waivers}
    unused = sorted(path for path in config.waivers if path not in used_paths)
    if unused:
        raise ValueError("unused config waiver path(s): " + ", ".join(unused))
    findings.sort(key=lambda item: (SEVERITY[item.level], -item.lines, item.path))
    return findings, used_waivers


def should_fail(findings: Sequence[Finding], threshold: str) -> bool:
    return threshold != "never" and any(SEVERITY[item.level] >= SEVERITY[threshold] for item in findings)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        root = args.locate.expanduser().resolve()
        if not root.is_dir():
            raise ValueError(f"locate path is not a directory: {root}")
        config = load_config(resolve_config(args.config, root, CONFIG_NAME))
        findings, waivers = scan(root, config)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        if args.format == "json":
            import json

            print(json.dumps({"errors": [str(exc)], "findings": [], "waivers": []}, ensure_ascii=False, indent=2))
        else:
            print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        import json

        payload = {
            "findings": [item.__dict__ for item in findings],
            "waivers": waivers,
            "errors": [],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item.path}: {item.lines} lines [{item.level.upper()}] {item.note}")
        print(f"Files with findings: {len(findings)}; active waivers: {len(waivers)}")
    return 2 if should_fail(findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
