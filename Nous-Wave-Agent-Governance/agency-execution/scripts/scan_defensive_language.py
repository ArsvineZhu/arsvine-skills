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
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Sequence


@dataclass(frozen=True)
class Pattern:
    key: str
    severity: str
    regex: re.Pattern[str]
    note: str


SEVERITY_ORDER = {"low": 1, "medium": 2, "high": 3}

PATTERNS: tuple[Pattern, ...] = (
    Pattern(
        "subjectivization-zh",
        "medium",
        re.compile(r"(?:我认为|我觉得|我倾向于?|在我看来|我的倾向是)"),
        "Check whether speaker identity adds information or only weakens a judgment.",
    ),
    Pattern(
        "subjectivization-en",
        "medium",
        re.compile(r"\b(?:I think|I believe|I(?:'|’)d lean toward|I lean toward|in my view|my preference is)\b", re.I),
        "Check whether speaker identity adds information or only weakens a judgment.",
    ),
    Pattern(
        "commitment-weakening-zh",
        "medium",
        re.compile(r"(?:可以考虑|不妨考虑|可能更(?:合适|合理|好)|或许更(?:合适|合理|好)|建议可以)"),
        "Check whether a settled choice has been rewritten as an option or possibility.",
    ),
    Pattern(
        "commitment-weakening-en",
        "medium",
        re.compile(r"\b(?:could consider|might consider|may want to consider|could perhaps|might perhaps|probably the better option)\b", re.I),
        "Check whether a settled choice has been rewritten as an option or possibility.",
    ),
    Pattern(
        "automaticity-framing-zh",
        "medium",
        re.compile(r"(?:天然(?:会|成为|导致|意味着|带来)|自然(?:会|地会|成为|导致|意味着)|自动(?:会|成为|导致|意味着))"),
        "Check whether automaticity was asserted where the reasoning only supports a contingent tendency or direct judgment.",
    ),
    Pattern(
        "automaticity-framing-en",
        "medium",
        re.compile(r"\b(?:naturally|inherently|automatically)\s+(?:becomes?|means?|implies?|leads?\s+to|creates?|produces?)\b", re.I),
        "Check whether automaticity was asserted where the reasoning only supports a contingent tendency or direct judgment.",
    ),
    Pattern(
        "defensive-negation-zh",
        "medium",
        re.compile(r"(?:不自动(?:意味着|代表|说明)|并不意味着|并不代表|不能证明|不足以(?:证明|说明)|单凭.{0,24}(?:不能|不足以)|这并不意味着|这不代表)"),
        "Check whether the text invented a stronger claim and then negated it.",
    ),
    Pattern(
        "defensive-negation-en",
        "medium",
        re.compile(r"\b(?:does not automatically (?:mean|imply|prove)|doesn't automatically (?:mean|imply|prove)|does not necessarily (?:mean|imply|prove)|doesn't necessarily (?:mean|imply|prove)|does not prove|doesn't prove|cannot prove|this does not mean|this doesn't mean)\b", re.I),
        "Check whether the text invented a stronger claim and then negated it.",
    ),
    Pattern(
        "invented-contrast-zh",
        "medium",
        re.compile(r"(?:不是.{0,60}而是|并非.{0,60}而是|并不是.{0,60}而是)"),
        "Check whether the contrast answers a real distinction or a model-invented objection.",
    ),
    Pattern(
        "invented-contrast-en",
        "medium",
        re.compile(r"\bnot\s+.{1,80}\s+but\s+", re.I),
        "Check whether the contrast answers a real distinction or a model-invented objection.",
    ),
    Pattern(
        "research-deferral-zh",
        "high",
        re.compile(r"(?:需要进一步(?:研究|验证|调查|确认)|还需要进一步(?:研究|验证|调查|确认)|有待进一步(?:研究|验证|调查|确认))"),
        "Require a concrete decision that the proposed extra research can change.",
    ),
    Pattern(
        "research-deferral-en",
        "high",
        re.compile(r"\b(?:requires further (?:research|validation|investigation)|needs further (?:research|validation|investigation)|more research is needed|further investigation is needed)\b", re.I),
        "Require a concrete decision that the proposed extra research can change.",
    ),
    Pattern(
        "hypothetical-defeater-zh",
        "medium",
        re.compile(r"(?:潜在(?:的)?外部(?:调用方|消费者|依赖)|未来可能(?:存在|出现)|理论上可能(?:存在|出现)|无法排除.{0,40}可能)"),
        "Check whether an unobserved defeater has enough evidence or consequence to affect the decision.",
    ),
    Pattern(
        "hypothetical-defeater-en",
        "medium",
        re.compile(r"\b(?:potential external consumers?|future consumers? may|there may be unknown consumers?|cannot rule out the possibility)\b", re.I),
        "Check whether an unobserved defeater has enough evidence or consequence to affect the decision.",
    ),
    Pattern(
        "safety-preface-zh",
        "low",
        re.compile(r"(?:为了稳妥起见|为(?:了)?安全起见|谨慎起见|保险起见)"),
        "Check whether caution has a concrete risk basis and changes the action.",
    ),
    Pattern(
        "safety-preface-en",
        "low",
        re.compile(r"\b(?:to be safe|for safety's sake|to err on the side of caution|out of an abundance of caution)\b", re.I),
        "Check whether caution has a concrete risk basis and changes the action.",
    ),
)

TEXT_EXTENSIONS = {
    ".md", ".mdx", ".txt", ".rst", ".adoc",
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs",
    ".rs", ".go", ".java", ".kt", ".kts", ".swift", ".c", ".h", ".cc", ".cpp", ".hpp",
    ".sh", ".bash", ".zsh", ".fish", ".ps1",
    ".toml", ".yaml", ".yml", ".json", ".jsonc", ".xml", ".proto", ".sql",
    ".html", ".css", ".scss", ".less", ".vue", ".svelte",
}

DEFAULT_SKIP_DIRS = {
    ".git", "node_modules", "target", "dist", "build", "coverage", ".next", ".nuxt",
    ".venv", "venv", "vendor", ".idea", ".vscode", ".cache", ".turbo", ".pytest_cache",
}

DEFAULT_SKIP_GLOBS = (
    "**/package-lock.json",
    "**/pnpm-lock.yaml",
    "**/yarn.lock",
    "**/Cargo.lock",
    "**/go.sum",
    "**/poetry.lock",
)

ALLOW_MARKERS = ("agency-scan: allow", "defensive-scan: allow")


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", default=["."], help="Files or directories to scan. Default: current directory.")
    parser.add_argument("--changed", action="store_true", help="Scan files changed from HEAD plus untracked files under the current Git repository.")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--exclude", action="append", default=[], help="Additional path glob to exclude. Repeatable.")
    parser.add_argument("--max-bytes", type=int, default=2_000_000, help="Skip files larger than this many bytes.")
    parser.add_argument("--fail-on", choices=("never", "low", "medium", "high"), default="never", help="Optional non-zero exit threshold. Default: never.")
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


def is_skipped(path: Path, root: Path, extra_globs: Sequence[str]) -> bool:
    try:
        rel = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        rel = path.as_posix()

    if any(part in DEFAULT_SKIP_DIRS for part in path.parts):
        return True

    patterns = DEFAULT_SKIP_GLOBS + tuple(extra_globs)
    return any(fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(path.name, pattern) for pattern in patterns)


def looks_textual(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    return path.name in {"AGENTS.md", "README", "LICENSE", "Makefile", "Dockerfile", "Justfile"}


def iter_files(inputs: Sequence[str], root: Path, changed: bool, excludes: Sequence[str], max_bytes: int) -> Iterator[Path]:
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
    self_path = Path(__file__).resolve()
    for path in candidates:
        try:
            resolved = path.resolve()
            if resolved in seen or resolved == self_path:
                continue
            seen.add(resolved)
            if not resolved.exists() or not resolved.is_file():
                continue
            if is_skipped(resolved, root, excludes):
                continue
            if not looks_textual(resolved):
                continue
            if resolved.stat().st_size > max_bytes:
                continue
            yield resolved
        except OSError:
            continue


def scan_file(path: Path, root: Path) -> list[dict[str, object]]:
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
        if any(marker in line for marker in ALLOW_MARKERS):
            continue
        for pattern in PATTERNS:
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
        files = list(iter_files(args.paths, root, args.changed, args.exclude, args.max_bytes))
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    findings: list[dict[str, object]] = []
    for path in files:
        findings.extend(scan_file(path, root))

    findings.sort(key=lambda item: (str(item["path"]), int(item["line"]), int(item["column"]), str(item["pattern"])))

    if args.format == "json":
        print(json.dumps({"files_scanned": len(files), "findings": findings}, ensure_ascii=False, indent=2))
    else:
        print_text(findings)
        print(f"Files scanned: {len(files)}")

    return exit_code(findings, args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
