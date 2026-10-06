#!/usr/bin/env python3
"""Install the AntiGPT Constitution and selected Arsvine Skills."""
from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Sequence

START = "<!-- arsvine-skills:antigpt-constitution:start -->"
END = "<!-- arsvine-skills:antigpt-constitution:end -->"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("codex",))
    parser.add_argument("--instructions-file", type=Path)
    parser.add_argument("--skills-dir", type=Path)
    parser.add_argument("--skill", action="append", default=[], help="Install only this Skill; repeatable")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def destinations(args: argparse.Namespace) -> tuple[Path, Path]:
    if args.profile == "codex":
        instructions = args.instructions_file or Path.home() / ".codex" / "AGENTS.md"
        skills_dir = args.skills_dir or Path.home() / ".codex" / "skills"
        return instructions.expanduser(), skills_dir.expanduser()
    if not args.instructions_file or not args.skills_dir:
        raise ValueError("provide --profile codex or both --instructions-file and --skills-dir")
    return args.instructions_file.expanduser(), args.skills_dir.expanduser()


def managed_block(constitution: str) -> str:
    body = constitution.strip()
    return f"{START}\n{body}\n{END}"


def merge_managed_block(existing: str, block: str) -> str:
    start_count = existing.count(START)
    end_count = existing.count(END)
    if start_count != end_count or start_count > 1:
        raise ValueError("existing instructions contain malformed or duplicate Arsvine managed blocks")
    if start_count == 1:
        start = existing.index(START)
        end = existing.index(END, start) + len(END)
        merged = existing[:start].rstrip() + "\n\n" + block + existing[end:]
    else:
        prefix = existing.rstrip()
        merged = (prefix + "\n\n" if prefix else "") + block + "\n"
    return merged.rstrip() + "\n"


def install_skill(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"SKILL {source.name}: {source} -> {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{source.name}-", dir=target.parent) as temp_dir:
        staged = Path(temp_dir) / source.name
        shutil.copytree(source, staged)
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staged), str(target))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo = Path(__file__).resolve().parents[1]
    constitution_path = repo / "AntiGPT" / "CONSTITUTION.md"
    skills_root = repo / "skills"

    try:
        instructions_file, skills_dir = destinations(args)
        constitution = constitution_path.read_text(encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    available = sorted(path.name for path in skills_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    selected = args.skill or available
    unknown = sorted(set(selected) - set(available))
    if unknown:
        print(f"error: unknown Skill(s): {', '.join(unknown)}", file=sys.stderr)
        return 1

    block = managed_block(constitution)
    try:
        existing = instructions_file.read_text(encoding="utf-8") if instructions_file.exists() else ""
        merged = merge_managed_block(existing, block)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"CONSTITUTION: {constitution_path} -> {instructions_file}")
    else:
        instructions_file.parent.mkdir(parents=True, exist_ok=True)
        instructions_file.write_text(merged, encoding="utf-8")

    for name in selected:
        try:
            install_skill(skills_root / name, skills_dir / name, args.dry_run)
        except OSError as exc:
            print(f"error installing {name}: {exc}", file=sys.stderr)
            return 1

    if not args.dry_run:
        print(f"Installed Constitution -> {instructions_file}")
        print(f"Installed Skills -> {skills_dir}: {', '.join(selected)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
