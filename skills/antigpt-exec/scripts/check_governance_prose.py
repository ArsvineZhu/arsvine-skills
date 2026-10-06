#!/usr/bin/env python3
"""Find mechanically recognizable AntiGPT prose failures.

The checker intentionally covers a narrow surface. It gates high-confidence forms,
reports softer review signals, and leaves semantic judgment to the agent or reviewer.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11
    tomllib = None

CLASS_ORDER = {"signal": 1, "review": 2, "block": 3}
WAIVER_RE = re.compile(
    r"<!--\s*antigpt:\s*allow\s+rule=(?P<rule>[a-z0-9-]+)\s+reason=\"(?P<reason>[^\"]+)\"\s*-->",
    re.IGNORECASE,
)
FENCE_RE = re.compile(r"^\s*(```|~~~)")
INLINE_CODE_RE = re.compile(r"`[^`]*`")
MARKDOWN_URL_RE = re.compile(r"\]\((?:https?://|mailto:)[^)]+\)")
RAW_URL_RE = re.compile(r"https?://\S+")


@dataclass(frozen=True)
class Pattern:
    key: str
    klass: str
    regex: re.Pattern[str]
    note: str


@dataclass(frozen=True)
class Config:
    prose_extensions: frozenset[str]
    code_extensions: frozenset[str]
    skip_dirs: frozenset[str]
    skip_globs: tuple[str, ...]
    patterns: tuple[Pattern, ...]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan")
    parser.add_argument("--changed", action="store_true", help="Scan changed and untracked Git files only")
    parser.add_argument("--include-code", action="store_true", help="Also scan configured source-code extensions")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on", choices=("never", "signal", "review", "block"), default="block")
    parser.add_argument("--exclude", action="append", default=[], help="Additional glob to exclude")
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument("--config", type=Path, default=Path(__file__).with_name("scanner.toml"))
    return parser.parse_args(argv)


def load_config(path: Path) -> Config:
    if tomllib is None:
        raise RuntimeError("Python 3.11+ is required because scanner.toml uses tomllib")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 2:
        raise RuntimeError(f"unsupported scanner config version: {data.get('version')!r}")
    scanner = data["scanner"]
    patterns = []
    for raw in data.get("patterns", []):
        klass = raw["class"]
        if klass not in CLASS_ORDER:
            raise RuntimeError(f"unknown pattern class {klass!r}")
        flags = re.IGNORECASE if raw.get("ignore_case", False) else 0
        patterns.append(Pattern(raw["key"], klass, re.compile(raw["regex"], flags), raw["note"]))
    return Config(
        frozenset(scanner["prose_extensions"]),
        frozenset(scanner["code_extensions"]),
        frozenset(scanner["skip_dirs"]),
        tuple(scanner["skip_globs"]),
        tuple(patterns),
    )


def git_changed(root: Path) -> set[Path]:
    def run(*args: str) -> list[str]:
        proc = subprocess.run(["git", *args], cwd=root, text=True, capture_output=True)
        if proc.returncode != 0:
            raise RuntimeError(proc.stderr.strip() or "git command failed")
        return [line for line in proc.stdout.splitlines() if line]

    names = set(run("diff", "--name-only", "--diff-filter=ACMR", "HEAD"))
    names.update(run("ls-files", "--others", "--exclude-standard"))
    return {(root / name).resolve() for name in names}


def skipped(path: Path, root: Path, config: Config, extra: Sequence[str]) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = path.as_posix()
    if any(part in config.skip_dirs for part in path.parts):
        return True
    return any(fnmatch.fnmatch(rel, glob) for glob in (*config.skip_globs, *extra))


def iter_files(args: argparse.Namespace, root: Path, config: Config) -> Iterable[Path]:
    allowed = set(config.prose_extensions)
    if args.include_code:
        allowed.update(config.code_extensions)
    changed = git_changed(root) if args.changed else None
    seen: set[Path] = set()
    for raw in args.paths:
        candidate = (root / raw).resolve() if not Path(raw).is_absolute() else Path(raw).resolve()
        paths = candidate.rglob("*") if candidate.is_dir() else [candidate]
        for path in paths:
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            if changed is not None and path.resolve() not in changed:
                continue
            if skipped(path, root, config, args.exclude):
                continue
            if path.suffix.lower() not in allowed:
                continue
            try:
                if path.stat().st_size > args.max_bytes:
                    continue
            except OSError:
                continue
            yield path


def visible_lines(text: str, markdown: bool) -> Iterable[tuple[int, str]]:
    in_fence = False
    fence_token = ""
    for line_no, line in enumerate(text.splitlines(), start=1):
        if markdown:
            fence = FENCE_RE.match(line)
            if fence:
                token = fence.group(1)
                if not in_fence:
                    in_fence = True
                    fence_token = token
                elif token == fence_token:
                    in_fence = False
                    fence_token = ""
                continue
            if in_fence:
                continue
        cleaned = INLINE_CODE_RE.sub("", line)
        cleaned = MARKDOWN_URL_RE.sub("]()", cleaned)
        cleaned = RAW_URL_RE.sub("", cleaned)
        yield line_no, cleaned


def finding(path: str, line: int, column: int, klass: str, rule: str, match: str, note: str, text: str) -> dict[str, object]:
    return {"path": path, "line": line, "column": column, "class": klass, "rule": rule, "match": match, "note": note, "text": text.strip()}


def scan_file(path: Path, root: Path, config: Config) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return [], []
    try:
        display = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        display = str(path)

    patterns = {p.key: p for p in config.patterns}
    findings: list[dict[str, object]] = []
    waivers: list[dict[str, object]] = []
    pending: dict[str, object] | None = None

    for line_no, line in visible_lines(text, path.suffix.lower() in {".md", ".mdx"}):
        waiver_match = WAIVER_RE.fullmatch(line.strip())
        if line.strip().lower().startswith("<!-- antigpt: allow"):
            if not waiver_match:
                findings.append(finding(display, line_no, 1, "block", "invalid-waiver", line.strip(), "Waivers require rule=<id> and a quoted non-empty reason.", line))
                pending = None
                continue
            rule = waiver_match.group("rule")
            reason = waiver_match.group("reason").strip()
            if rule not in patterns or len(reason) < 8:
                findings.append(finding(display, line_no, 1, "block", "invalid-waiver", line.strip(), "Waiver rule must exist and reason must be specific.", line))
                pending = None
                continue
            if pending is not None:
                findings.append(finding(display, int(pending["line"]), 1, "block", "unused-waiver", str(pending["rule"]), "A waiver must apply to the next non-empty prose line.", str(pending["source"])))
            pending = {"rule": rule, "reason": reason, "line": line_no, "source": line, "used": False}
            continue
        if not line.strip():
            continue

        for pattern in config.patterns:
            matches = list(pattern.regex.finditer(line))
            if not matches:
                continue
            if pending is not None and pending["rule"] == pattern.key:
                pending["used"] = True
                waivers.append({"path": display, "line": line_no, "rule": pattern.key, "reason": pending["reason"]})
                matches = []
            for match in matches:
                findings.append(finding(display, line_no, match.start() + 1, pattern.klass, pattern.key, match.group(0), pattern.note, line))
        if pending is not None:
            if not pending["used"]:
                findings.append(finding(display, int(pending["line"]), 1, "block", "unused-waiver", str(pending["rule"]), "A waiver applies only when the next non-empty prose line matches that rule.", str(pending["source"])))
            pending = None

    if pending is not None:
        findings.append(finding(display, int(pending["line"]), 1, "block", "unused-waiver", str(pending["rule"]), "A waiver must apply to the next non-empty prose line.", str(pending["source"])))
    return findings, waivers


def should_fail(findings: Sequence[dict[str, object]], threshold: str) -> bool:
    if threshold == "never":
        return False
    level = CLASS_ORDER[threshold]
    return any(CLASS_ORDER[str(item["class"])] >= level for item in findings)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path.cwd().resolve()
    try:
        config = load_config(args.config)
        files = list(iter_files(args, root, config))
    except (OSError, RuntimeError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    findings: list[dict[str, object]] = []
    waivers: list[dict[str, object]] = []
    for path in files:
        file_findings, file_waivers = scan_file(path, root, config)
        findings.extend(file_findings)
        waivers.extend(file_waivers)
    findings.sort(key=lambda x: (str(x["path"]), int(x["line"]), int(x["column"]), str(x["rule"])))

    if args.format == "json":
        print(json.dumps({"files_scanned": len(files), "findings": findings, "waivers": waivers}, ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item['path']}:{item['line']}:{item['column']} [{str(item['class']).upper()}] {item['rule']}: {item['match']}")
            print(f"  {item['text']}")
            print(f"  {item['note']}")
        if not findings:
            print("No governance-prose findings.")
        print(f"Files scanned: {len(files)}; findings: {len(findings)}; waivers: {len(waivers)}")

    return 2 if should_fail(findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
