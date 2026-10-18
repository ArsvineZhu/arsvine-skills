#!/usr/bin/env python3
"""Install the AntiRLHF bundle and independent general Skills from this checkout."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from collections.abc import Sequence
from pathlib import Path

UPSTREAM = "https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main"
START = "<!-- antirlhf-constitution:start -->"
END = "<!-- antirlhf-constitution:end -->"


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", choices=("codex",))
    parser.add_argument("--instructions-file", type=Path)
    parser.add_argument("--skills-dir", type=Path)
    parser.add_argument("--antirlhf", action="store_true", help="Install the complete AntiRLHF Skill bundle")
    parser.add_argument(
        "--skill", action="append", default=[], metavar="NAME", help="Install an independent general Skill; repeatable"
    )
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing files")
    return parser.parse_args(argv)


def skill_dirs(root: Path) -> list[Path]:
    if not root.is_dir():
        return []
    return sorted(path for path in root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def destinations(args: argparse.Namespace, include_antirlhf: bool) -> tuple[Path | None, Path]:
    skills_dir = args.skills_dir or (Path.home() / ".codex" / "skills" if args.profile == "codex" else None)
    if skills_dir is None:
        raise ValueError("provide --profile codex or --skills-dir")
    instructions = None
    if include_antirlhf:
        instructions = args.instructions_file or (
            Path.home() / ".codex" / "AGENTS.md" if args.profile == "codex" else None
        )
        if instructions is None:
            raise ValueError("AntiRLHF requires --profile codex or --instructions-file")
        instructions = instructions.expanduser().resolve()
    return instructions, skills_dir.expanduser().resolve()


def merge_managed_block(existing: str, block: str) -> str:
    start_count, end_count = existing.count(START), existing.count(END)
    if start_count != end_count or start_count > 1:
        raise ValueError("instructions contain malformed or duplicate managed blocks")
    if start_count:
        first, last = existing.index(START), existing.index(END)
        if last < first:
            raise ValueError("instructions contain reversed managed markers")
        existing = existing[:first] + existing[last + len(END) :]
    return block + ("\n\n" + existing.lstrip("\n") if existing.strip() else "\n")


def version(path: Path) -> str:
    value = path.read_text(encoding="utf-8").strip()
    if not value or len(value.splitlines()) != 1:
        raise ValueError(f"expected a single nonempty version in {path}")
    return value


def update_instruction(name: str, installed: str, upstream: str) -> str:
    return (
        f"> {name} version: {installed}. [Upstream version]({UPSTREAM}/{upstream}). "
        "Check when the session starts; notify the user of newer versions and ask before updating."
    )


def stamp_skill(text: str, name: str, note: str) -> str:
    text = re.sub(r"^> " + re.escape(name) + r" version:.*\n?", "", text, flags=re.MULTILINE)
    heading = re.search(r"^# [^\n]+\n", text, re.MULTILINE)
    if heading is None:
        raise ValueError(f"{name}/SKILL.md: missing first-level heading")
    return text[: heading.end()] + "\n" + note + "\n\n" + text[heading.end() :].lstrip("\n")


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


PROJECT_CONFIG_NAMESPACE = Path(".config") / "arsvine-skills"


def project_config_dir(instructions_file: Path | None, skills_dir: Path) -> Path:
    """Namespaced project config: `.config/arsvine-skills/` beside AGENTS.md or skills/."""
    root = instructions_file.parent if instructions_file is not None else skills_dir.parent
    return root / PROJECT_CONFIG_NAMESPACE


def ensure_config_dir(config_dir: Path) -> None:
    """Create the namespaced config directory; fail clearly on path conflicts."""
    dot_config = config_dir.parent
    if dot_config.exists() and not dot_config.is_dir():
        raise ValueError(f"config parent exists and is not a directory: {dot_config}")
    if config_dir.exists() and not config_dir.is_dir():
        raise ValueError(f"config path exists and is not a directory: {config_dir}")
    config_dir.mkdir(parents=True, exist_ok=True)


def skill_config_files(source: Path) -> list[Path]:
    bundled = source / "scripts" / ".config"
    if not bundled.is_dir():
        return []
    return sorted(path for path in bundled.iterdir() if path.is_file() and not path.name.startswith("."))


def seed_project_configs(sources: Sequence[Path], config_dir: Path, dry_run: bool) -> list[str]:
    """Copy Skill-bundled configs into `.config/arsvine-skills/` without overwriting local files."""
    messages: list[str] = []
    if not dry_run:
        ensure_config_dir(config_dir)
    elif config_dir.exists() and not config_dir.is_dir():
        raise ValueError(f"config path exists and is not a directory: {config_dir}")
    elif config_dir.parent.exists() and not config_dir.parent.is_dir():
        raise ValueError(f"config parent exists and is not a directory: {config_dir.parent}")
    for source in sources:
        for path in skill_config_files(source):
            target = config_dir / path.name
            if target.exists():
                messages.append(f"SKIP CONFIG {target} (exists; leaving local file unchanged)")
                continue
            if dry_run:
                messages.append(f"CREATE CONFIG {target} <- {source.name}/scripts/.config/{path.name}")
                continue
            shutil.copy2(path, target)
            messages.append(f"CREATE CONFIG {target}")
    return messages


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo = Path(__file__).resolve().parents[1]
    try:
        antirlhf = skill_dirs(repo / "AntiRLHF" / "skills")
        general = {path.name: path for path in skill_dirs(repo / "general")}
        unknown = sorted(set(args.skill) - set(general))
        if unknown:
            raise ValueError(
                f"unknown general Skill(s): {', '.join(unknown)}; use --antirlhf for the complete AntiRLHF bundle"
            )
        default = not args.antirlhf and not args.skill
        include_antirlhf = args.antirlhf or default
        if include_antirlhf and not antirlhf:
            raise ValueError("AntiRLHF/skills contains no installable Skills")
        instructions_file, skills_dir = destinations(args, include_antirlhf)
        selected_general = list(dict.fromkeys(args.skill)) if args.skill else list(general) if default else []
        sources = list(antirlhf) if include_antirlhf else []
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
        merged = None
        if include_antirlhf:
            # destinations() always returns a Path when include_antirlhf is true.
            assert instructions_file is not None
            merged = instructions_file.read_text(encoding="utf-8") if instructions_file.exists() else ""
            bundle_version = version(repo / "AntiRLHF" / ".version")
            constitution = (repo / "AntiRLHF" / "CONSTITUTION.md").read_text(encoding="utf-8").strip()
            updates = update_instruction("AntiRLHF", bundle_version, "AntiRLHF/.version")
            merged = merge_managed_block(merged, f"{START}\n{constitution}\n\n{updates}\n{END}")
        versions: dict[str, str] = {}
        stamped = {}
        for source in sources:
            if source.name in selected_general:
                installed = version(source / ".version")
                note = update_instruction(source.name, installed, f"general/{source.name}/.version")
                stamped[source.name] = stamp_skill((source / "SKILL.md").read_text(encoding="utf-8"), source.name, note)
            else:
                assert bundle_version is not None
                installed = bundle_version
            versions[source.name] = installed
        config_dir = project_config_dir(instructions_file, skills_dir)
        if instructions_file is not None:
            print(f"INSTRUCTIONS: {instructions_file}")
        print(f"CONFIG DIR: {config_dir}")
        for source in sources:
            print(f"SKILL {source.name}: {source} -> {skills_dir / source.name}")
        if bundle_version is not None:
            print(f"VERSION AntiRLHF {bundle_version}: .version in each of the {len(antirlhf)} installed Skills")
        for name in selected_general:
            print(f"VERSION {name} {version(general[name] / '.version')}: {skills_dir / name / '.version'}")
        if args.dry_run:
            for message in seed_project_configs(sources, config_dir, dry_run=True):
                print(message)
            return 0
        for source in sources:
            install_skill(source, skills_dir / source.name, versions[source.name], stamped.get(source.name))
        for message in seed_project_configs(sources, config_dir, dry_run=False):
            print(message)
        if instructions_file is not None:
            assert merged is not None
            instructions_file.parent.mkdir(parents=True, exist_ok=True)
            instructions_file.write_text(merged, encoding="utf-8")
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print("Installation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
