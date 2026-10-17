#!/usr/bin/env python3
"""Run the canonical validation for this repository."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOTS = (ROOT / "AntiGPT" / "skills", ROOT / "general")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
FIELD_RE = re.compile(r"^([A-Za-z0-9_-]+):\s*(.+?)\s*$", re.MULTILINE)
RESOURCE_RE = re.compile(r"`((?:references|scripts|agents|assets)/[^`]+)`")


def validate_skills() -> list[str]:
    errors: list[str] = []
    seen_names: set[str] = set()
    directories: list[Path] = []
    for skills_root in SKILLS_ROOTS:
        if not skills_root.is_dir():
            errors.append(f"{skills_root.relative_to(ROOT)}: missing Skill directory")
            continue
        directories.extend(skills_root.iterdir())
    for directory in sorted(directories):
        if not directory.is_dir():
            continue
        skill = directory / "SKILL.md"
        if not skill.is_file():
            errors.append(f"{directory.relative_to(ROOT)}: missing SKILL.md")
            continue
        text = skill.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(text)
        if not match:
            errors.append(f"{skill.relative_to(ROOT)}: missing YAML frontmatter")
            continue
        fields = dict(FIELD_RE.findall(match.group(1)))
        name = fields.get("name")
        description = fields.get("description")
        if name != directory.name:
            errors.append(f"{skill.relative_to(ROOT)}: name {name!r} must match directory {directory.name!r}")
        if not description:
            errors.append(f"{skill.relative_to(ROOT)}: missing description")
        if name in seen_names:
            errors.append(f"duplicate Skill name: {name}")
        if name:
            seen_names.add(name)
        for resource in RESOURCE_RE.findall(text):
            if not (directory / resource).exists():
                errors.append(f"{skill.relative_to(ROOT)}: missing referenced resource {resource}")
        agent = directory / "agents" / "openai.yaml"
        if agent.exists():
            agent_text = agent.read_text(encoding="utf-8")
            if "display_name:" not in agent_text or "short_description:" not in agent_text:
                errors.append(f"{agent.relative_to(ROOT)}: incomplete interface metadata")
    return errors


def run(label: str, command: list[str]) -> int:
    print(f"== {label} ==")
    proc = subprocess.run(command, cwd=ROOT)
    if proc.returncode != 0:
        print(f"FAILED: {label} (exit {proc.returncode})")
    return proc.returncode


def main() -> int:
    errors = validate_skills()
    if errors:
        print("== Skill structure ==")
        for error in errors:
            print(f"ERROR: {error}")
        return 2
    print("== Skill structure ==\nOK")

    commands = [
        ("Documentation scanner tests", [sys.executable, "-m", "unittest", "discover", "-s", "AntiGPT/skills/documentation/tests", "-p", "test_*.py"]),
        ("Documentation graph", [sys.executable, "AntiGPT/skills/documentation/scripts/check/doc_graph.py", "--config", "scripts/config/.docgraph.toml"]),
        (
            "Maintained repository prose",
            [
                sys.executable,
                "AntiGPT/skills/documentation/scripts/check/governance_prose.py",
                ".",
                "--exclude", "AntiGPT/archive/JDD.md",
                "--exclude", "AntiGPT/archive/TED.md",
                "--exclude", "AntiGPT/archive/TED.zh-CN.md",
                "--exclude", "AntiGPT/archive/COST.en.md",
                "--exclude", "AntiGPT/archive/COST.zh-CN.md",
            ],
        ),
    ]
    metadata = sorted(str(path.relative_to(ROOT)) for skills_root in SKILLS_ROOTS for path in skills_root.glob("*/agents/openai.yaml"))
    if metadata:
        commands.append(("Skill interface prose", [sys.executable, "AntiGPT/skills/documentation/scripts/check/governance_prose.py", "--include-code", *metadata]))
    for label, command in commands:
        if run(label, command) != 0:
            return 2

    py_files = sorted(
        str(path.relative_to(ROOT))
        for directory in (ROOT / "scripts", *SKILLS_ROOTS)
        for path in directory.rglob("*.py")
    )
    if run("Python compile", [sys.executable, "-m", "py_compile", *py_files]) != 0:
        return 2

    print("Repository validation OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
