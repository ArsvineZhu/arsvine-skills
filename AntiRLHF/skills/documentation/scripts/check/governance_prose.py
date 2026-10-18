#!/usr/bin/env python3
"""Scan maintained prose for actionable AntiRLHF language and process cues."""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
import tomllib
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from pathlib import Path

CLASS_ORDER = {"signal": 1, "review": 2, "block": 3}
WAIVER_RE = re.compile(
    r'<!--\s*antirlhf:\s*allow\s+rule=(?P<rule>[a-z0-9-]+)\s+reason="(?P<reason>[^"\n]+)"\s*-->', re.I
)
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
INLINE_RE = re.compile(r"(?P<ticks>`+)(?P<body>.+?)(?P=ticks)")
URL_RE = re.compile(r"\]\([^)]*\)|https?://\S+")
STRUCTURE_RE = re.compile(r"^\s*(?:#{1,6}\s+|[-+*]\s+|\d+[.)]\s+)")


@dataclass(frozen=True)
class Pattern:
    key: str
    klass: str
    regex: re.Pattern[str]
    note: str
    scope: str = "all"


@dataclass(frozen=True)
class Config:
    prose_extensions: frozenset[str]
    code_extensions: frozenset[str]
    skip_dirs: frozenset[str]
    skip_globs: tuple[str, ...]
    patterns: tuple[Pattern, ...]


@dataclass(frozen=True)
class Unit:
    text: str
    positions: tuple[tuple[int, int], ...]
    source: str
    directive: bool = False


CONFIG_NAME = "scanner.toml"
PROJECT_CONFIG_DIR = Path(".config") / "arsvine-skills"


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
    # An installed Codex bundle seeds shared defaults beside ~/.codex/AGENTS.md.
    global_config = Path(__file__).resolve().parents[4] / PROJECT_CONFIG_DIR / name
    if global_config.is_file():
        return global_config.resolve()
    bundled_seed = Path(__file__).resolve().parents[1] / ".config" / name
    if bundled_seed.is_file():
        return bundled_seed.resolve()
    raise ValueError(f"config not found: {candidate}")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."])
    parser.add_argument("--changed", action="store_true", help="Scan changed and untracked Git files")
    parser.add_argument("--include-code", action="store_true", help="Also scan configured source extensions as text")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--fail-on", choices=("never", "signal", "review", "block"), default="block")
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--max-bytes", type=int, default=1_000_000)
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Config path; default: .config/arsvine-skills/scanner.toml",
    )
    return parser.parse_args(argv)


def load_config(path: Path) -> Config:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 2:
        raise ValueError(f"unsupported scanner config version: {data.get('version')!r}")
    scanner = data["scanner"]
    for key in ("prose_extensions", "code_extensions", "skip_dirs", "skip_globs"):
        if not isinstance(scanner[key], list) or not all(isinstance(v, str) and v for v in scanner[key]):
            raise ValueError(f"scanner.{key} must be a list of nonempty strings")
    patterns = []
    keys = set()
    for raw in data["patterns"]:
        key, klass, regex, note = (raw[k] for k in ("key", "class", "regex", "note"))
        if not isinstance(key, str) or not re.fullmatch(r"[a-z0-9-]+", key) or key in keys:
            raise ValueError(f"invalid or duplicate rule key: {key!r}")
        if klass not in CLASS_ORDER or not isinstance(note, str) or not note.strip():
            raise ValueError(f"invalid class or note for {key}")
        if not isinstance(regex, str) or not regex:
            raise ValueError(f"empty regex for {key}")
        if not isinstance(raw.get("ignore_case", False), bool):
            raise ValueError(f"ignore_case must be boolean for {key}")
        compiled = re.compile(regex, re.I if raw.get("ignore_case", False) else 0)
        if compiled.search(""):
            raise ValueError(f"rule {key} matches empty text")
        scope = raw.get("scope", "all")
        if scope not in {"all", "ai"}:
            raise ValueError(f"invalid scope for {key}: {scope!r}")
        keys.add(key)
        patterns.append(Pattern(key, klass, compiled, note, scope))
    if not patterns:
        raise ValueError("configuration must define at least one pattern")
    return Config(
        frozenset(scanner["prose_extensions"]),
        frozenset(scanner["code_extensions"]),
        frozenset(scanner["skip_dirs"]),
        tuple(scanner["skip_globs"]),
        tuple(patterns),
    )


def git_changed(root: Path) -> set[Path]:
    def run(*args: str) -> list[str]:
        proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
        if proc.returncode:
            raise ValueError(proc.stderr.strip() or "git command failed")
        return [name for name in proc.stdout.split("\0") if name]

    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=root, capture_output=True, text=True)
    if top.returncode:
        raise ValueError(top.stderr.strip())
    git_root = Path(top.stdout.strip())
    names = set(run("diff", "--name-only", "--diff-filter=ACMR", "-z", "HEAD"))
    names.update(run("ls-files", "--others", "--exclude-standard", "--full-name", "-z"))
    return {(git_root / name).resolve() for name in names}


def skipped(path: Path, root: Path, config: Config, extra: Sequence[str]) -> bool:
    try:
        relative = path.relative_to(root)
    except ValueError:
        relative = path
    return any(part in config.skip_dirs for part in relative.parts) or any(
        fnmatch.fnmatch(relative.as_posix(), glob) for glob in (*config.skip_globs, *extra)
    )


def iter_files(args: argparse.Namespace, root: Path, config: Config) -> Iterable[Path]:
    allowed = config.prose_extensions | (config.code_extensions if args.include_code else frozenset())
    changed = git_changed(root) if args.changed else None
    seen = set()
    if args.max_bytes <= 0:
        raise ValueError("--max-bytes must be positive")
    for raw in args.paths:
        candidate = (root / raw).resolve()
        if not candidate.exists():
            raise ValueError(f"input does not exist: {raw}")
        for path in sorted(candidate.rglob("*")) if candidate.is_dir() else [candidate]:
            if not path.is_file() or path in seen:
                continue
            seen.add(path)
            if changed is not None and path not in changed:
                continue
            if skipped(path, root, config, args.exclude) or path.suffix.lower() not in allowed:
                continue
            if path.stat().st_size > args.max_bytes:
                raise ValueError(f"input exceeds --max-bytes: {path}")
            yield path


def mask_markup(line: str) -> str:
    chars = list(line)

    def mask(start: int, end: int) -> None:
        chars[start:end] = " " * (end - start)

    for match in INLINE_RE.finditer(line):
        body = match.group("body")
        # Keep quoted natural language visible; identifiers and code are not prose.
        prose = (bool(re.search(r"\s", body)) or bool(re.search(r"[\u3400-\u9fff]{4}", body))) and not re.search(
            r"[={}]|::|=>", body
        )
        if prose:
            mask(match.start(), match.start("body"))
            mask(match.end("body"), match.end())
        else:
            mask(match.start(), match.end())
    for match in URL_RE.finditer(line):
        mask(match.start() + (1 if match.group().startswith("]") else 0), match.end())
    return "".join(chars)


def prose_units(text: str, markdown: bool) -> Iterable[Unit]:
    lines: list[tuple[int, str, str]] = []
    fence = ""
    comment = False
    quote = False

    def unit() -> Unit:
        joined, positions, source = [], [], []
        for number, clean, raw in lines:
            if joined:
                joined.append(" ")
                positions.append((number, 1))
            joined.extend(clean)
            positions.extend((number, col + 1) for col in range(len(clean)))
            source.append(raw)
        return Unit("".join(joined), tuple(positions), "\n".join(source))

    for number, raw in enumerate(text.splitlines(), 1):
        line = raw
        if markdown:
            # Strip blockquote markers without shifting source columns.
            line = re.sub(r"^(\s*>\s*)+", lambda m: " " * len(m.group()), line)
            match = FENCE_RE.match(line.lstrip() if raw.lstrip().startswith(">") else line)
            if fence:
                if match and match[1][0] == fence[0] and len(match[1]) >= len(fence) and not match[2].strip():
                    fence = ""
                continue
            if match and not comment:
                if lines:
                    yield unit()
                    lines = []
                fence = match[1]
                continue
            if "antirlhf:" in line.lower() and "allow" in line.lower() and "<!--" in line:
                if lines:
                    yield unit()
                    lines = []
                yield Unit(line, tuple((number, col + 1) for col in range(len(line))), raw, True)
                continue
            # Mask comment spans, preserving visible prose and its source columns.
            chars = list(line)
            cursor = 0
            while cursor < len(line):
                start = cursor if comment else line.find("<!--", cursor)
                if start < 0:
                    break
                end = line.find("-->", start if comment else start + 4)
                stop = len(line) if end < 0 else end + 3
                chars[start:stop] = " " * (stop - start)
                comment = end < 0
                cursor = stop
            line = "".join(chars)
        is_quote = raw.lstrip().startswith(">") if markdown else False
        if not line.strip() or (lines and (STRUCTURE_RE.match(line) or is_quote != quote)):
            if lines:
                yield unit()
                lines = []
        if not line.strip():
            continue
        quote = is_quote
        lines.append((number, mask_markup(line) if markdown else line, raw))
        if markdown and re.match(r"^\s*#{1,6}\s", line):
            yield unit()
            lines = []
    if lines:
        yield unit()


def finding(
    path: str,
    line: int,
    column: int,
    klass: str,
    rule: str,
    match: str,
    note: str,
    text: str,
    end_line: int | None = None,
) -> dict[str, object]:
    return dict(
        path=path,
        line=line,
        column=column,
        end_line=end_line or line,
        **{"class": klass},
        rule=rule,
        match=match,
        note=note,
        text=text.strip(),
    )


def is_ai_instruction(path: Path) -> bool:
    if path.name in {"AGENTS.md", "CONSTITUTION.md", "SKILL.md"}:
        return True
    return path.parent.name == "references" and path.suffix.lower() == ".md" and not path.name.endswith(".zh-CN.md")


def scan_file(path: Path, root: Path, config: Config) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    text = path.read_text(encoding="utf-8")
    try:
        display = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        display = str(path)
    active = tuple(p for p in config.patterns if p.scope == "all" or is_ai_instruction(path))
    patterns = {p.key: p for p in active}
    findings, waivers = [], []
    pending: dict[str, tuple[str, Unit]] = {}

    def invalid(unit: Unit, rule: str, note: str) -> None:
        line, column = unit.positions[0]
        findings.append(finding(display, line, column, "block", rule, unit.text.strip(), note, unit.source))

    for unit in prose_units(text, path.suffix.lower() in {".md", ".mdx"}):
        if unit.directive:
            match = WAIVER_RE.fullmatch(unit.text.strip())
            if not match or match["rule"] not in patterns or len(match["reason"].strip()) < 8:
                invalid(
                    unit,
                    "invalid-waiver",
                    "Use a known rule and a specific quoted reason of at least eight characters.",
                )
            elif match["rule"] in pending:
                invalid(unit, "invalid-waiver", "Use each rule once for the next prose unit.")
            else:
                pending[match["rule"]] = (match["reason"].strip(), unit)
            continue
        used = set()
        candidates = [(pattern, match) for pattern in active for match in pattern.regex.finditer(unit.text)]
        # A stronger rule owns a contained phrase, including its waiver accounting.
        candidates = [
            (pattern, match)
            for pattern, match in candidates
            if not any(
                CLASS_ORDER[other.klass] > CLASS_ORDER[pattern.klass]
                and stronger.start() <= match.start()
                and stronger.end() >= match.end()
                for other, stronger in candidates
            )
        ]
        for pattern in active:
            matches = [match for owner, match in candidates if owner.key == pattern.key]
            if matches and pattern.key in pending:
                reason, directive = pending[pattern.key]
                waivers.append(
                    dict(
                        path=display,
                        line=unit.positions[0][0],
                        end_line=unit.positions[-1][0],
                        rule=pattern.key,
                        reason=reason,
                        directive_line=directive.positions[0][0],
                    )
                )
                used.add(pattern.key)
                continue
            for match in matches:
                line, col = unit.positions[match.start()]
                end_line = unit.positions[match.end() - 1][0]
                findings.append(
                    finding(
                        display,
                        line,
                        col,
                        pattern.klass,
                        pattern.key,
                        match.group(),
                        pattern.note,
                        unit.source,
                        end_line,
                    )
                )
        for rule, (_, directive) in pending.items():
            if rule not in used:
                invalid(directive, "unused-waiver", "The named rule must match the next prose unit.")
        pending.clear()
    for _, directive in pending.values():
        invalid(directive, "unused-waiver", "A waiver requires a following matching prose unit.")
    return findings, waivers


def should_fail(findings: Sequence[dict[str, object]], threshold: str) -> bool:
    return threshold != "never" and any(CLASS_ORDER[str(item["class"])] >= CLASS_ORDER[threshold] for item in findings)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    root = Path.cwd().resolve()
    findings, waivers, errors = [], [], []
    scanned = 0
    try:
        config = load_config(resolve_config(args.config, root, CONFIG_NAME))
        for path in iter_files(args, root, config):
            try:
                found, waived = scan_file(path, root, config)
                findings.extend(found)
                waivers.extend(waived)
                scanned += 1
            except (OSError, UnicodeError) as exc:
                errors.append(f"{path}: {exc}")
    except (OSError, UnicodeError, ValueError, KeyError, TypeError, re.error) as exc:
        errors.append(str(exc))
    findings.sort(key=lambda x: (str(x["path"]), int(x["line"]), int(x["column"]), str(x["rule"])))
    waivers.sort(key=lambda x: (str(x["path"]), int(x["line"]), str(x["rule"])))
    if args.format == "json":
        print(
            json.dumps(
                dict(files_scanned=scanned, findings=findings, waivers=waivers, errors=errors),
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        for item in findings:
            print(
                f"{item['path']}:{item['line']}:{item['column']} [{str(item['class']).upper()}] {item['rule']}: {item['match']}"
            )
            print(f"  {item['text']}\n  {item['note']}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Files scanned: {scanned}; findings: {len(findings)}; waivers: {len(waivers)}; errors: {len(errors)}")
    return 1 if errors else 2 if should_fail(findings, args.fail_on) else 0


if __name__ == "__main__":
    raise SystemExit(main())
