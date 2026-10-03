#!/usr/bin/env python3
"""Scan repository prose for defensive-language patterns that deserve semantic review.

The scanner reports candidates. It does not decide whether a sentence is wrong.
Default exit status is 0. Use --fail-on explicitly when a repository chooses to gate on
selected severities.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence


@dataclass(frozen=True)
class Pattern:
    key: str
    severity: str
    regex: re.Pattern[str]
    note: str
    broad_negation: bool = False


@dataclass(frozen=True)
class ScannerConfig:
    text_extensions: frozenset[str]
    skip_dirs: frozenset[str]
    skip_globs: tuple[str, ...]
    allow_markers: tuple[str, ...]
    patterns: tuple[Pattern, ...]


SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3}

CONFIG_PATH = Path(__file__).with_name("scanner.toml")


def load_config(path: Path = CONFIG_PATH) -> ScannerConfig:
    try:
        config = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, tomllib.TOMLDecodeError) as exc:
        raise RuntimeError(f"cannot load scanner configuration {path}: {exc}") from exc

    if config.get("version") != 1:
        raise RuntimeError(f"unsupported scanner configuration version in {path}")

    scanner = config.get("scanner")
    if not isinstance(scanner, dict):
        raise RuntimeError(f"scanner configuration {path} must contain a [scanner] table")

    def read_string_list(name: str) -> list[str]:
        value = scanner.get(name)
        if not isinstance(value, list) or not value or any(not isinstance(item, str) or not item for item in value):
            raise RuntimeError(f"scanner configuration {path} needs a non-empty string list for {name}")
        return value

    text_extensions = read_string_list("text_extensions")
    skip_dirs = read_string_list("skip_dirs")
    skip_globs = read_string_list("skip_globs")
    allow_markers = read_string_list("allow_markers")

    entries = config.get("patterns")
    if not isinstance(entries, list) or not entries:
        raise RuntimeError(f"scanner configuration {path} must contain a non-empty [[patterns]] list")

    patterns: list[Pattern] = []
    seen_keys: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        if not isinstance(entry, dict):
            raise RuntimeError(f"pattern #{index} in {path} must be a table")

        key = entry.get("key")
        severity = entry.get("severity")
        regex_source = entry.get("regex")
        ignore_case = entry.get("ignore_case", False)
        note = entry.get("note")
        broad_negation = entry.get("broad_negation", False)

        if not isinstance(key, str) or not key:
            raise RuntimeError(f"pattern #{index} in {path} needs a non-empty string key")
        if key in seen_keys:
            raise RuntimeError(f"duplicate pattern key {key!r} in {path}")
        seen_keys.add(key)
        if not isinstance(severity, str) or severity not in SEVERITY_ORDER:
            raise RuntimeError(f"pattern {key!r} in {path} has invalid severity {severity!r}")
        if not isinstance(regex_source, str) or not regex_source:
            raise RuntimeError(f"pattern {key!r} in {path} needs a non-empty regex string")
        if not isinstance(ignore_case, bool):
            raise RuntimeError(f"pattern {key!r} in {path} has non-boolean ignore_case")
        if not isinstance(note, str) or not note:
            raise RuntimeError(f"pattern {key!r} in {path} needs a non-empty note")
        if not isinstance(broad_negation, bool):
            raise RuntimeError(f"pattern {key!r} in {path} has non-boolean broad_negation")

        try:
            regex = re.compile(regex_source, re.IGNORECASE if ignore_case else 0)
        except re.error as exc:
            raise RuntimeError(f"pattern {key!r} in {path} has invalid regex: {exc}") from exc
        patterns.append(Pattern(key, severity, regex, note, broad_negation))

    return ScannerConfig(
        frozenset(text_extensions),
        frozenset(skip_dirs),
        tuple(skip_globs),
        tuple(allow_markers),
        tuple(patterns),
    )



def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan. Default: current directory.")
    parser.add_argument("--changed", action="store_true", help="Scan files changed from HEAD plus untracked files under the current Git repository.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--exclude", action="append", default=[], help="Additional path glob to exclude. Repeatable.")
    parser.add_argument("--max-bytes", type=int, default=2_000_000, help="Skip files larger than this many bytes.")
    parser.add_argument("--fail-on", choices=("never", "low", "medium", "high"), default="never", help="Optional non-zero exit threshold. Default: never.")
    parser.add_argument("--include-broad-negations", action="store_true", help="Include low-severity broad Chinese and English negation-marker candidates.")
    return parser.parse_args(argv)


def git_changed_files(root: Path) -> list[Path]:
    commands = (
        ["git", "diff", "--name-only", "--diff-filter=ACMR", "HEAD"],
        ["git", "ls-files", "--others", "--exclude-standard"],
    )
    files: list[Path] = []
    for command in commands:
        proc = subprocess.run(command, cwd=root, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
        if proc.returncode != 0:
            raise RuntimeError("--changed requires a Git repository with a readable HEAD")
        for line in proc.stdout.splitlines():
            if line.strip():
                files.append(root / line.strip())
    return sorted(set(files))


def is_skipped(path: Path, root: Path, extra_globs: Sequence[str], config: ScannerConfig) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = path.as_posix()

    if any(part in config.skip_dirs for part in path.parts):
        return True

    patterns = config.skip_globs + tuple(extra_globs)
    return any(fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in patterns)


def looks_textual(path: Path, text_extensions: frozenset[str]) -> bool:
    if path.suffix.lower() in text_extensions:
        return True
    return path.name in {"AGENTS.md", "README", "LICENSE", "Makefile", "Dockerfile", "Justfile"}


def iter_files(
    inputs: Sequence[str],
    root: Path,
    changed: bool,
    excludes: Sequence[str],
    max_bytes: int,
    config: ScannerConfig,
) -> Iterator[Path]:
    candidates: Iterable[Path]
    if changed:
        candidates = git_changed_files(root)
    else:
        expanded: list[Path] = []
        for raw in inputs:
            path = Path(raw).expanduser()
            if not path.is_absolute():
                path = (Path.cwd() / path).resolve()
            if path.is_file():
                expanded.append(path)
            elif path.is_dir():
                expanded.extend(p for p in path.rglob("*") if p.is_file())
        candidates = expanded

    seen: set[Path] = set()
    self_paths = {Path(__file__).resolve(), CONFIG_PATH.resolve()}
    for path in candidates:
        try:
            resolved = path.resolve()
            if resolved in seen or resolved in self_paths:
                continue
            seen.add(resolved)
            if not resolved.exists() or not resolved.is_file():
                continue
            if is_skipped(resolved, root, excludes, config):
                continue
            if not looks_textual(resolved, config.text_extensions):
                continue
            if resolved.stat().st_size > max_bytes:
                continue
            yield resolved
        except OSError:
            continue


def scan_file(
    path: Path,
    root: Path,
    patterns: Sequence[Pattern],
    allow_markers: Sequence[str],
) -> list[dict[str, object]]:
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return []

    try:
        display_path = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        display_path = str(path)

    findings: list[dict[str, object]] = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if any(marker in line for marker in allow_markers):
            continue
        for pattern in patterns:
            for match in pattern.regex.finditer(line):
                findings.append(
                    {
                        "path": display_path,
                        "line": line_no,
                        "column": match.start() + 1,
                        "severity": pattern.severity,
                        "pattern": pattern.key,
                        "match": match.group(0),
                        "note": pattern.note,
                        "text": line.strip(),
                    }
                )
    return findings


def print_text(findings: Sequence[dict[str, object]]) -> None:
    if not findings:
        print("No defensive-language candidates found.")
        return

    for item in findings:
        print(
            f"{item['path']}:{item['line']}:{item['column']} "
            f"[{str(item['severity']).upper()}] {item['pattern']}: {item['match']}"
        )
        print(f"  {item['text']}")
        print(f"  REVIEW: {item['note']}")

    counts = {level: 0 for level in SEVERITY_ORDER}
    for item in findings:
        counts[str(item["severity"])] += 1
    print(f"\nCandidates: {len(findings)} (high={counts['high']}, medium={counts['medium']}, low={counts['low']})")
    print("Each hit requires semantic review; presence alone does not establish a defect.")


def exit_code(findings: Sequence[dict[str, object]], fail_on: str) -> int:
    if fail_on == "never":
        return 0
    threshold = SEVERITY_ORDER[fail_on]
    return 2 if any(SEVERITY_ORDER[str(item["severity"])] >= threshold for item in findings) else 0


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path.cwd().resolve()

    try:
        config = load_config()
        patterns = config.patterns
        if not args.include_broad_negations:
            patterns = tuple(pattern for pattern in patterns if not pattern.broad_negation)
        files = list(iter_files(args.paths, root, args.changed, args.exclude, args.max_bytes, config))
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    findings: list[dict[str, object]] = []
    for path in files:
        findings.extend(scan_file(path, root, patterns, config.allow_markers))

    findings.sort(key=lambda item: (str(item["path"]), int(item["line"]), int(item["column"]), str(item["pattern"])))

    if args.format == "json":
        print(json.dumps({"files_scanned": len(files), "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print_text(findings)
        print(f"Files scanned: {len(files)}")

    return exit_code(findings, args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
