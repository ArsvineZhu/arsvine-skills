#!/usr/bin/env python3
"""Check local path targets in Markdown links without modifying the repository.

This is a lightweight fallback, not a full Markdown/site link validator. It checks
file/directory existence for common inline Markdown links and images. It skips
external URLs, mail links, data URLs, and anchor-only links. Anchor validity and
site-generator routing are intentionally out of scope.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"^\s*(```|~~~)")
SKIP_SCHEMES = {"http", "https", "mailto", "tel", "data"}
SKIP_DIRS = {".git", ".hg", ".svn", "node_modules", "vendor", "dist", "build", "target", ".next", ".cache", "__pycache__"}


def markdown_files(root: Path, include_hidden: bool):
    for current, dirs, files in os.walk(root):
        kept = []
        for name in dirs:
            if name in SKIP_DIRS:
                continue
            if not include_hidden and name.startswith("."):
                continue
            kept.append(name)
        dirs[:] = kept
        for name in files:
            if name.lower().endswith((".md", ".mdx")):
                if not include_hidden and name.startswith("."):
                    continue
                yield Path(current) / name


def strip_optional_title(raw: str) -> str:
    """Extract the destination from `(path "title")` approximately."""
    raw = raw.strip()
    if raw.startswith("<") and ">" in raw:
        return raw[1 : raw.index(">")]
    # Paths with spaces should normally be angle-bracketed or URL encoded.
    # For the common title form, split before a quoted title.
    match = re.match(r"^(.*?)(?:\s+[\"'].*[\"'])?$", raw)
    return match.group(1).strip() if match else raw


def resolve_local_target(source: Path, destination: str, repo_root: Path) -> Path | None:
    destination = strip_optional_title(destination)
    if not destination or destination.startswith("#"):
        return None

    parsed = urlsplit(destination)
    if parsed.scheme.lower() in SKIP_SCHEMES or parsed.netloc:
        return None

    path_part = unquote(parsed.path)
    if not path_part:
        return None

    if path_part.startswith("/"):
        target = repo_root / path_part.lstrip("/")
    else:
        target = source.parent / path_part

    return target.resolve(strict=False)


def scan_file(path: Path, repo_root: Path) -> list[dict]:
    issues: list[dict] = []
    in_fence = False

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return [{"file": path.relative_to(repo_root).as_posix(), "line": 0, "target": "", "error": str(exc)}]

    for line_no, line in enumerate(lines, 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        for raw in LINK_RE.findall(line):
            target = resolve_local_target(path, raw, repo_root)
            if target is None:
                continue
            try:
                target.relative_to(repo_root)
            except ValueError:
                # A relative link intentionally escaping the repository may be valid.
                # Report it only if the target is missing.
                pass
            if not target.exists():
                issues.append(
                    {
                        "file": path.relative_to(repo_root).as_posix(),
                        "line": line_no,
                        "target": strip_optional_title(raw),
                        "resolved": str(target),
                    }
                )
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", help="Repository root (default: current directory)")
    parser.add_argument("--include-hidden", action="store_true", help="Include hidden directories except known VCS/cache paths")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    if not root.is_dir():
        parser.error(f"not a directory: {root}")

    files = sorted(markdown_files(root, args.include_hidden))
    issues: list[dict] = []
    for path in files:
        issues.extend(scan_file(path, root))

    result = {
        "root": str(root),
        "markdown_files_checked": len(files),
        "missing_local_targets": issues,
        "limitations": [
            "Does not validate Markdown anchors.",
            "Does not understand every site-generator route or Markdown extension.",
            "External URLs are skipped.",
        ],
    }

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Checked {len(files)} Markdown/MDX files")
        if not issues:
            print("No missing local link targets found.")
        else:
            print(f"Missing local targets: {len(issues)}")
            for issue in issues:
                print(f"  {issue['file']}:{issue['line']}: {issue['target']}")

    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
