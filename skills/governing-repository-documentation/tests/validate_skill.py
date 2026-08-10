#!/usr/bin/env python3
"""Static validation for the governing-repository-documentation Skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)


def main() -> int:
    errors: list[str] = []
    text = SKILL.read_text(encoding="utf-8")

    frontmatter = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not frontmatter:
        fail("SKILL.md is missing YAML frontmatter", errors)
    else:
        body = frontmatter.group(1)
        name_match = re.search(r"^name:\s*(.+)$", body, re.M)
        description_match = re.search(r"^description:\s*(.+)$", body, re.M)
        name = name_match.group(1).strip() if name_match else ""
        description = description_match.group(1).strip() if description_match else ""

        if name != ROOT.name:
            fail(f"name {name!r} does not match directory {ROOT.name!r}", errors)
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            fail("name violates lowercase alphanumeric-hyphen format", errors)
        if len(name) > 64:
            fail("name exceeds 64 characters", errors)
        if not description or len(description) > 1024:
            fail(f"description length is invalid: {len(description)}", errors)

    line_count = len(text.splitlines())
    if line_count >= 500:
        fail(f"SKILL.md has {line_count} lines; keep it below 500", errors)

    references = sorted(set(re.findall(r"\]\((references/[^)#]+\.md)\)", text)))
    for reference in references:
        if len(Path(reference).parts) != 2:
            fail(f"deep SKILL.md reference: {reference}", errors)
        if not (ROOT / reference).is_file():
            fail(f"missing reference: {reference}", errors)

    required_contracts = {
        "early question batching": [
            "all reasonably foreseeable blocking questions together",
            "one early message",
        ],
        "human language default": ["user's current language", "single-language"],
        "AI technical English": ["technical English"],
        "two modes": ["Bootstrap mode", "Maintenance mode"],
        "template leakage guard": ["No project-specific template leakage"],
        "important scope entry points": ["Every important scope MUST have"],
        "canonical ownership": ["One canonical owner per important fact"],
        "late question gate": ["no late blocking questions"],
        "verification gate": ["Verification is required before completion"],
        "institutional knowledge governance": [
            "operational knowledge and institutional memory",
            "operational-knowledge.md",
        ],
    }

    lower = text.lower()
    for label, phrases in required_contracts.items():
        if not all(phrase.lower() in lower for phrase in phrases):
            fail(f"missing required contract: {label}", errors)


    operational = ROOT / "references" / "operational-knowledge.md"
    if not operational.is_file():
        fail("missing operational knowledge reference", errors)
    else:
        operational_text = operational.read_text(encoding="utf-8").lower()
        required_roles = [
            "gotcha",
            "known issue",
            "troubleshooting",
            "runbook",
            "playbook",
            "architecture decision record",
            "postmortem",
            "prefer enforcement over remembrance",
        ]
        for role in required_roles:
            if role not in operational_text:
                fail(f"operational knowledge reference missing role/principle: {role}", errors)

    forbidden_project_terms = [
        "heptalogos",
        "native-matrix",
        "embedding.md",
        "functions.md",
        "release-checklist.md",
    ]
    searchable = []
    for path in ROOT.rglob("*"):
        if path.is_file() and path.suffix.lower() in {".md", ".yaml", ".py"} and path != Path(__file__):
            try:
                searchable.append((path, path.read_text(encoding="utf-8").lower()))
            except UnicodeDecodeError:
                pass

    for term in forbidden_project_terms:
        hits = [str(path.relative_to(ROOT)) for path, content in searchable if term in content]
        if hits:
            fail(f"project-specific term {term!r} found in: {', '.join(hits)}", errors)

    placeholder_patterns = [r"\bTBD\b", r"\bTODO\b", r"<INSERT[^>]*>", r"<FILL[^>]*>"]
    for pattern in placeholder_patterns:
        hits = []
        for path, content in searchable:
            if re.search(pattern, content, re.I):
                hits.append(str(path.relative_to(ROOT)))
        if hits:
            fail(f"placeholder pattern {pattern!r} found in: {', '.join(hits)}", errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1

    print(f"PASS: {ROOT.name}")
    print(f"  SKILL.md: {line_count} lines")
    print(f"  references linked: {len(references)}")
    print(f"  reference files present: {len(list((ROOT / 'references').glob('*.md')))}")
    print("  critical workflow contracts: present")
    print("  project-specific leakage scan: clean")
    print("  placeholder scan: clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
