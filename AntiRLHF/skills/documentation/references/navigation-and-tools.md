# Maintain document links and use the bundled checkers

Use this guide when moving documents, changing navigation, installing the documentation Skill into another repository, or investigating an actual scanner/link-check issue.

## Edit documents at their authoritative location

Keep current documentation in its current-topic directory. Place historical commentary in an archive or research area when that is what the document represents. If an API or workflow is replaced, update its current usage section and links; delete outdated instructions from the live guide.

After moving a file, update local Markdown links that refer to it and follow the important entrypoint links as a reader. Translate user-visible navigation where the project maintains multiple language editions. Retain semantic names rather than anonymous document IDs.

Some repositories maintain an explicit doc graph with reciprocal Navigation links. Check whether the current project declares this convention before adding reciprocal links. Contextual references and citations can remain ordinary one-way links.

## Run the existing prose checker

From the AntiRLHF repository root:

```bash
python AntiRLHF/skills/documentation/scripts/check/governance_prose.py --changed
```

Scan named files when reviewing a particular article:

```bash
python AntiRLHF/skills/documentation/scripts/check/governance_prose.py path/to/file.md
```

When installed in Codex, the script lives at `~/.codex/skills/documentation/scripts/check/governance_prose.py`. The project-specific configuration is `.config/arsvine-skills/scanner.toml`; the script falls back to the user's installed configuration and then the Skill's bundled config. Use `--config` when deliberately selecting a particular rule set.

`block` is a narrow failure class, `review` requires contextual reading, and `signal` is a weaker cue. The scanner can detect a form of defensive wording; it cannot establish what the author meant. Review the paragraph for its reader and actual claim.

For an intentional quoted anti-example, put a specific waiver directly before the affected prose:

```html
<!-- antirlhf: allow rule=defensive-negation-en reason="Quoted wording shown as an anti-example" -->
```

Use waivers for examples and necessary expressions, not as a way to avoid rewriting actual defensive prose. The script also reports unused or malformed waivers.

## Run navigation checks where configured

For repositories with `.config/arsvine-skills/docgraph.toml`:

```bash
python AntiRLHF/skills/documentation/scripts/check/doc_graph.py
```

The checker reads the configured maintained document set, tests Navigation targets, checks required reciprocal links and entrypoint reachability. Fix the missing link in the owning document or adjust the project configuration when navigation responsibility changes.

Outside this repository, resolve the same script relative to the installed `documentation/SKILL.md`. A consuming repository must provide its own docgraph configuration if it opts into this convention.

## Finish as a reader would

Open the changed entrypoint, follow the links touched by the edit, and read the changed section as the intended audience. Leave the correct current content in place, with research history and editor notes located only where they are actually part of the deliverable.
