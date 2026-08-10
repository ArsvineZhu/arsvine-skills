#!/usr/bin/env python3
"""Read-only repository documentation inventory.

This helper intentionally reports evidence instead of deciding documentation
architecture. It inventories documentation-like files and directories that show
common scope signals. Use repository judgment to decide which scopes are important.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Iterable

DOC_NAMES = {
    "README.md",
    "INDEX.md",
    "AGENTS.md",
    "AGENTS.override.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "GOVERNANCE.md",
    "GOTCHAS.md",
    "KNOWN_ISSUES.md",
    "TROUBLESHOOTING.md",
    "RUNBOOK.md",
    "PLAYBOOK.md",
}

SCOPE_SIGNAL_FILES = {
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "go.mod",
    "pom.xml",
    "build.gradle",
    "build.gradle.kts",
    "Makefile",
    "CMakeLists.txt",
}

SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "target",
    ".next",
    ".cache",
    "__pycache__",
}


def iter_files(root: Path, include_hidden: bool) -> Iterable[Path]:
    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        kept_dirs = []
        for name in dirs:
            if name in SKIP_DIRS:
                continue
            if not include_hidden and name.startswith("."):
                continue
            kept_dirs.append(name)
        dirs[:] = kept_dirs

        for name in files:
            if not include_hidden and name.startswith("."):
                continue
            yield current_path / name


def first_heading(path: Path) -> str | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            for _ in range(80):
                line = handle.readline()
                if not line:
                    break
                stripped = line.strip()
                if stripped.startswith("# "):
                    return stripped[2:].strip()
    except (OSError, UnicodeDecodeError):
        return None
    return None


def line_count(path: Path) -> int | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return sum(1 for _ in handle)
    except (OSError, UnicodeDecodeError):
        return None


def relative(path: Path, root: Path) -> str:
    value = path.relative_to(root).as_posix()
    return value or "."


def build_inventory(root: Path, include_hidden: bool) -> dict:
    markdown_docs: list[dict] = []
    named_docs: list[str] = []
    candidate_signals: dict[str, set[str]] = {}

    for path in iter_files(root, include_hidden):
        rel = relative(path, root)
        name = path.name

        if name in DOC_NAMES:
            named_docs.append(rel)

        if path.suffix.lower() in {".md", ".mdx", ".rst"} or name in DOC_NAMES:
            markdown_docs.append(
                {
                    "path": rel,
                    "lines": line_count(path),
                    "heading": first_heading(path) if path.suffix.lower() in {".md", ".mdx"} else None,
                }
            )

        if name in SCOPE_SIGNAL_FILES or name in {"README.md", "AGENTS.md", "INDEX.md"}:
            parent = relative(path.parent, root)
            candidate_signals.setdefault(parent, set()).add(name)

    root_required = {
        name: (root / name).is_file()
        for name in ("README.md", "INDEX.md", "AGENTS.md")
    }

    candidates = [
        {"path": path, "signals": sorted(signals)}
        for path, signals in sorted(candidate_signals.items())
    ]

    return {
        "root": str(root),
        "root_required_entry_points": root_required,
        "documentation_files": sorted(markdown_docs, key=lambda item: item["path"]),
        "named_governance_files": sorted(named_docs),
        "candidate_scope_signals": candidates,
        "notes": [
            "Candidate scope signals are evidence only; they do not classify important scopes.",
            "Generated, vendored, and hidden directories may be omitted by default.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden directories except known VCS/cache paths")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of a compact text report")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    data = build_inventory(root, args.include_hidden)

    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return 0

    print(f"Root: {data['root']}")
    print("Root entry points:")
    for name, exists in data["root_required_entry_points"].items():
        print(f"  {'OK' if exists else 'MISSING':7} {name}")

    print(f"\nDocumentation-like files: {len(data['documentation_files'])}")
    for item in data["documentation_files"]:
        lines = "?" if item["lines"] is None else str(item["lines"])
        heading = f" — {item['heading']}" if item["heading"] else ""
        print(f"  {item['path']} ({lines} lines){heading}")

    print(f"\nCandidate scope signals: {len(data['candidate_scope_signals'])}")
    for item in data["candidate_scope_signals"]:
        print(f"  {item['path']}: {', '.join(item['signals'])}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
