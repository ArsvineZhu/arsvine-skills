#!/usr/bin/env python3
"""Create common repository governance files from bundled templates."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = SKILL_ROOT / "scripts" / "templates"

FILES = {
    "gitignore": ".gitignore",
    "editorconfig": ".editorconfig",
    "gitattributes": ".gitattributes",
}

# gitignore presets expand to atomic template files under templates/gitignore/.
GITIGNORE_PRESETS: dict[str, tuple[str, ...]] = {
    "general": ("os", "editors", "python", "node", "secrets", "agents", "logs"),
    "python": ("os", "editors", "python", "secrets", "agents", "logs"),
    "node": ("os", "editors", "node", "secrets", "agents", "logs"),
    "web": ("os", "editors", "node", "secrets", "agents", "logs"),
    "rust": ("os", "editors", "rust", "secrets", "agents", "logs"),
    "go": ("os", "editors", "go", "secrets", "agents", "logs"),
    "java": ("os", "editors", "java", "secrets", "agents", "logs"),
    "minimal": ("os", "editors", "secrets", "logs"),
}

# Whole-file presets for kinds that do not merge atomics.
WHOLE_FILE_PRESETS: dict[str, dict[str, str]] = {
    "editorconfig": {
        "general": "general",
        "python": "python",
        "node": "web",
        "web": "web",
        "rust": "general",
        "go": "general",
        "java": "general",
        "minimal": "general",
    },
    "gitattributes": {
        "general": "general",
        "python": "general",
        "node": "web",
        "web": "web",
        "rust": "general",
        "go": "general",
        "java": "general",
        "minimal": "general",
    },
}


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--locate", type=Path, default=Path.cwd(), help="Target repository root (default: cwd)")
    parser.add_argument(
        "--file",
        action="append",
        choices=sorted(FILES),
        dest="files",
        help="File kind to create; repeatable. Default: all supported kinds",
    )
    parser.add_argument(
        "--template",
        action="append",
        dest="templates",
        help="Template or preset name; repeatable (gitignore merges, others use the last resolvable name)",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite an existing target file")
    parser.add_argument("--list", action="store_true", help="List available templates/presets and exit")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    return parser.parse_args(argv)


def unique(items: Sequence[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            ordered.append(item)
    return ordered


def atomic_gitignore_names(names: Sequence[str]) -> list[str]:
    atomics: list[str] = []
    for name in names:
        if name in GITIGNORE_PRESETS:
            atomics.extend(GITIGNORE_PRESETS[name])
        else:
            atomics.append(name)
    return unique(atomics)


def gitignore_sources(names: Sequence[str]) -> list[Path]:
    sources: list[Path] = []
    for name in atomic_gitignore_names(names):
        path = TEMPLATES / "gitignore" / f"{name}.txt"
        if not path.is_file():
            available = sorted(p.stem for p in (TEMPLATES / "gitignore").glob("*.txt"))
            presets = ", ".join(sorted(GITIGNORE_PRESETS))
            raise ValueError(
                f"unknown gitignore template {name!r}; atomics: {', '.join(available) or '(none)'}; presets: {presets}"
            )
        sources.append(path)
    return sources


def whole_file_source(kind: str, names: Sequence[str]) -> Path:
    directory = TEMPLATES / kind
    candidates: list[str] = []
    mapping = WHOLE_FILE_PRESETS.get(kind, {})
    for name in names:
        candidates.append(mapping.get(name, name))
    for name in reversed(unique(candidates)):
        path = directory / f"{name}.txt"
        if path.is_file():
            return path
    available = sorted(p.stem for p in directory.glob("*.txt")) if directory.is_dir() else []
    raise ValueError(f"no {kind} template for {names!r}; available: {', '.join(available) or '(none)'}")


def merge_texts(paths: Sequence[Path]) -> str:
    chunks: list[str] = []
    seen_lines: set[str] = set()
    for path in paths:
        part_lines: list[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            key = line.strip()
            if key and not key.startswith("#"):
                if key in seen_lines:
                    continue
                seen_lines.add(key)
            part_lines.append(line.rstrip())
        text = "\n".join(part_lines).strip()
        if text:
            chunks.append(text)
    return "\n\n".join(chunks) + "\n"


def render(kind: str, names: Sequence[str]) -> tuple[str, str]:
    if kind == "gitignore":
        sources = gitignore_sources(names)
        label = " + ".join(path.stem for path in sources)
        return merge_texts(sources), label
    source = whole_file_source(kind, names)
    text = source.read_text(encoding="utf-8")
    if not text.endswith("\n"):
        text += "\n"
    return text, source.stem


def list_templates() -> int:
    gitignore_atomics = sorted(p.stem for p in (TEMPLATES / "gitignore").glob("*.txt"))
    print("gitignore presets:", ", ".join(sorted(GITIGNORE_PRESETS)))
    print("gitignore atomics:", ", ".join(gitignore_atomics) if gitignore_atomics else "(none)")
    for kind in ("editorconfig", "gitattributes"):
        names = sorted(p.stem for p in (TEMPLATES / kind).glob("*.txt")) if (TEMPLATES / kind).is_dir() else []
        print(f"{kind} files:", ", ".join(names) if names else "(none)")
        print(f"{kind} preset map:", ", ".join(f"{k}->{v}" for k, v in sorted(WHOLE_FILE_PRESETS[kind].items())))
    return 0


def create_one(root: Path, kind: str, names: Sequence[str], force: bool, dry_run: bool) -> str:
    text, label = render(kind, names)
    target = root / FILES[kind]
    if target.exists() and not force:
        return f"SKIP {target} (exists; pass --force to overwrite)"
    action = "OVERWRITE" if target.exists() else "CREATE"
    if dry_run:
        return f"{action} {target} <- {kind}: {label}"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")
    return f"{action} {target} <- {kind}: {label}"


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        if args.list:
            return list_templates()
        root = args.locate.expanduser().resolve()
        if root.exists() and not root.is_dir():
            raise ValueError(f"locate path is not a directory: {root}")
        if not args.dry_run:
            root.mkdir(parents=True, exist_ok=True)
        names = args.templates or ["general"]
        kinds = args.files or list(FILES)
        for kind in kinds:
            print(create_one(root, kind, names, args.force, args.dry_run))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
