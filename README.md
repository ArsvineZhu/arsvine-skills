# Arsvine Skills

[中文](README.zh-CN.md)

I maintain this repository for governance methods and general-purpose Skills developed through research, software development, and everyday work with agents. Its current focus is AntiGPT.

## AntiGPT

AntiGPT is a governance model for agents, developed from my long-term use of Chat, Research Agents, and Coding Agents. Models often complete individual steps yet drift from the objective over long tasks, accumulating local patches, compatibility layers, verification procedures, and defensive explanations.

I organize these recurring problems into constraints on judgment, attention, and task trajectories, then apply them through Skills and checkers for research, development, and writing. The aim is to keep agents working toward actual requirements, solve problems at the appropriate responsibility boundary, and reduce the burden of understanding and changing the result.

A persistent Constitution sets the direction. Four Skills turn it into task-specific practice:

| Skill | Responsibility |
| --- | --- |
| [AntiGPT Plan](AntiGPT/skills/antigpt-plan/SKILL.md) | Make decisions, research consequential unknowns, and design at the right level. |
| [AntiGPT Exec](AntiGPT/skills/antigpt-exec/SKILL.md) | Carry decisions through implementation and keep the whole user journey working. |
| [Refactoring](AntiGPT/skills/refactoring/SKILL.md) | Reorganize responsibilities, unify data flow, and remove recurring complexity. |
| [Documentation](AntiGPT/skills/documentation/SKILL.md) | Write for the reader, maintain coherent documentation, and catch recurring defensive prose. |

Install AntiGPT as one bundle. The documentation Skill owns its prose and navigation checkers; all four Skills share that capability.

[Governance approach and evolution](AntiGPT/README.en.md) · [Documentation index](AntiGPT/INDEX.md)

## Installation

With Python 3.11 or newer, run from this checkout:

```bash
python scripts/install.py --profile codex --antigpt
```

This installs the four Skills into `~/.codex/skills/` and prepends the Constitution and a short quoted version/update note as a managed block to `~/.codex/AGENTS.md`, preserving your other instructions.

[Installation and updates](INSTALL.md) covers previews, independent Skills, and other harnesses.

## General Skills

The `general/` directory holds independently installable capabilities:

- [Session Handoff](general/session-handoff/SKILL.md): carry the decisions, context, and unfinished state of a long conversation into the next session.

```bash
python scripts/install.py --profile codex --skill session-handoff
```

## Inside the repository

```text
AntiGPT/
  .version                Bundle version
  CONSTITUTION.md          Persistent governance
  README.md / README.en.md Governance approach and evolution
  INDEX.md                Documentation index
  skills/                 Four bundled Skills
  docs/                   Observations and background
  archive/                Historical governance texts
general/                  Independent Skills, each with .version
scripts/                  Repository installation and validation
  config/                 Repository tooling configuration
```

## Develop

```bash
python scripts/validate.py
```

The repository validator checks Skill structure, documentation navigation, all maintained prose (including this README and Skill references), Skill interface text, scanner behavior, and Python compilation. Versions live in `AntiGPT/.version` and each general Skill's `.version`; the installer records them with the installed Skills and adds a short update note to the AntiGPT instruction block or the general Skill's own `SKILL.md`.

## Navigation

- [Install](INSTALL.md)
- [AntiGPT introduction](AntiGPT/README.en.md)
- [AntiGPT index](AntiGPT/INDEX.md)
