#!/usr/bin/env python3
"""Install the AntiGPT bundle and independent general Skills from this checkout."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Sequence

ANTIGPT_SKILLS = ("antigpt-plan", "antigpt-exec", "documentation", "refactoring")
UPSTREAM = "https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main"
START = "<!-- arsvine-skills:antigpt-constitution:start -->"
END = "<!-- arsvine-skills:antigpt-constitution:end -->"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("codex",))
    parser.add_argument("--instructions-file", type=Path)
    parser.add_argument("--skills-dir", type=Path)
    parser.add_argument("--antigpt", action="store_true", help="Install the complete four-Skill AntiGPT bundle")
    parser.add_argument("--skill", action="append", default=[], metavar="NAME", help="Install an independent general Skill; repeatable")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    return parser.parse_args(argv)


def destinations(args: argparse.Namespace, include_antigpt: bool) -> tuple[Path | None, Path]:
    skills_dir = args.skills_dir or (Path.home() / ".codex" / "skills" if args.profile == "codex" else None)
    if skills_dir is None:
        raise ValueError("provide --profile codex or --skills-dir")
    instructions = None
    if include_antigpt:
        instructions = args.instructions_file or (Path.home() / ".codex" / "AGENTS.md" if args.profile == "codex" else None)
        if instructions is None:
            raise ValueError("AntiGPT requires --profile codex or --instructions-file")
        instructions = instructions.expanduser().resolve()
    return instructions, skills_dir.expanduser().resolve()


def merge_managed_block(existing: str, block: str) -> str:
    start_count, end_count = existing.count(START), existing.count(END)
    if start_count != end_count or start_count > 1:
        raise ValueError("existing instructions contain malformed or duplicate Arsvine managed blocks")
    if start_count:
        first, last = existing.index(START), existing.index(END)
        if last < first:
            raise ValueError("existing instructions contain reversed Arsvine managed markers")
        if first == 0:
            return block + existing[last + len(END):]
        existing = existing[:first] + existing[last + len(END):]
    return block + ("\n\n" + existing if existing else "\n")


def version(path: Path) -> str:
    value = path.read_text(encoding="utf-8").strip()
    if not value or len(value.splitlines()) != 1:
        raise ValueError(f"expected a single nonempty version in {path}")
    return value


def update_instruction(name: str, installed: str, upstream: str) -> str:
    return (
        f"> {name} version: {installed}. [Upstream version]({UPSTREAM}/{upstream}). "
        "Check once per session; notify the user of newer versions and ask before updating."
    )


def stamp_skill(text: str, name: str, note: str) -> str:
    text = re.sub(r"^> " + re.escape(name) + r" version:.*\n?", "", text, flags=re.MULTILINE)
    heading = re.search(r"^# [^\n]+\n", text, re.MULTILINE)
    if heading is None:
        raise ValueError(f"{name}/SKILL.md: missing first-level heading")
    return text[:heading.end()] + "\n" + note + "\n\n" + text[heading.end():].lstrip("\n")


def install_skill(source: Path, target: Path, installed: str, skill_text: str | None) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=f".{source.name}-", dir=target.parent) as temp_dir:
        staged = Path(temp_dir) / source.name
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        (staged / ".version").write_text(installed + "\n", encoding="utf-8")
        if skill_text is not None:
            (staged / "SKILL.md").write_text(skill_text, encoding="utf-8")
        if target.exists():
            shutil.rmtree(target)
        shutil.move(str(staged), str(target))


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo = Path(__file__).resolve().parents[1]
    try:
        general = {path.name: path for path in sorted((repo / "general").iterdir())
                   if path.is_dir() and (path / "SKILL.md").is_file()}
        unknown = sorted(set(args.skill) - set(general))
        if unknown:
            raise ValueError(f"unknown general Skill(s): {', '.join(unknown)}; use --antigpt for the complete AntiGPT bundle")
        default = not args.antigpt and not args.skill
        include_antigpt = args.antigpt or default
        instructions_file, skills_dir = destinations(args, include_antigpt)
        selected_general = list(dict.fromkeys(args.skill)) if args.skill else list(general) if default else []
        sources = [(repo / "AntiGPT" / "skills" / name) for name in ANTIGPT_SKILLS] if include_antigpt else []
        sources.extend(general[name] for name in selected_general)
        for source in sources:
            if not (source / "SKILL.md").is_file():
                raise ValueError(f"missing Skill: {source}")
            target = skills_dir / source.name
            if target.is_symlink() or (target.exists() and not target.is_dir()):
                raise ValueError(f"Skill destination must be a directory, not a file or symlink: {target}")
            if target == source or target in source.parents or source in target.parents:
                raise ValueError(f"Skill destination overlaps its source: {target}")
            if instructions_file is not None and (instructions_file == target or target in instructions_file.parents):
                raise ValueError(f"instructions file must be outside installed Skill directories: {instructions_file}")
        bundle_version = None
        if include_antigpt:
            merged = instructions_file.read_text(encoding="utf-8") if instructions_file.exists() else ""
            bundle_version = version(repo / "AntiGPT" / ".version")
            constitution = (repo / "AntiGPT" / "CONSTITUTION.md").read_text(encoding="utf-8").strip()
            updates = update_instruction("AntiGPT", bundle_version, "AntiGPT/.version")
            merged = merge_managed_block(merged, f"{START}\n{constitution}\n\n{updates}\n{END}")
        versions = {}
        stamped = {}
        for source in sources:
            if source.name in selected_general:
                installed = version(source / ".version")
                note = update_instruction(source.name, installed, f"general/{source.name}/.version")
                stamped[source.name] = stamp_skill((source / "SKILL.md").read_text(encoding="utf-8"), source.name, note)
            else:
                installed = bundle_version
            versions[source.name] = installed
        if instructions_file is not None:
            print(f"INSTRUCTIONS: {instructions_file}")
        for source in sources:
            print(f"SKILL {source.name}: {source} -> {skills_dir / source.name}")
        if bundle_version is not None:
            print(f"VERSION AntiGPT {bundle_version}: .version in each of the four installed Skills")
        for name in selected_general:
            print(f"VERSION {name} {version(general[name] / '.version')}: {skills_dir / name / '.version'}")
        if args.dry_run:
            return 0
        for source in sources:
            install_skill(source, skills_dir / source.name, versions[source.name], stamped.get(source.name))
        if instructions_file is not None:
            instructions_file.parent.mkdir(parents=True, exist_ok=True)
            instructions_file.write_text(merged, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print("Installation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
