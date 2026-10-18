# Arsvine Skills

[中文](README.zh-CN.md)

I maintain this repository for governance methods and general-purpose Skills developed through research, software development, and everyday work with agents. Its current focus is AntiRLHF.

## AntiRLHF

AntiRLHF is a governance model for agents, developed from my long-term use of Chat, Research Agents, and Coding Agents. Models often complete individual steps yet drift from the objective over long tasks, accumulating local patches, compatibility layers, verification procedures, and defensive explanations.

I organize these recurring problems into constraints on judgment, attention, and task trajectories, then apply them through Skills and checkers for research, development, and writing. The aim is to keep agents working toward actual requirements, solve problems at the appropriate responsibility boundary, and reduce the burden of understanding and changing the result.

A persistent Constitution sets the direction. Four Skills turn it into task-specific practice:

| Skill                                                  | Responsibility                                                                              |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| [AntiRLHF Plan](AntiRLHF/skills/antirlhf-plan/SKILL.md)   | Make decisions, research consequential unknowns, and design at the right level.             |
| [AntiRLHF Exec](AntiRLHF/skills/antirlhf-exec/SKILL.md)   | Carry decisions through implementation and keep the whole user journey working.             |
| [Refactoring](AntiRLHF/skills/refactoring/SKILL.md)     | Reorganize responsibilities, unify data flow, and remove recurring complexity.              |
| [Documentation](AntiRLHF/skills/documentation/SKILL.md) | Write for the reader, maintain coherent documentation, and catch recurring defensive prose. |

Install AntiRLHF as one bundle. The documentation Skill owns its prose and navigation checkers; all four Skills share that capability.

[Governance approach and evolution](AntiRLHF/README.en.md) · [Research notes](AntiRLHF/docs/README.en.md) · [Documentation index](AntiRLHF/INDEX.md)

## Installation

With Python 3.11 or newer, install without cloning:

```bash
curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \
  | python3 - --profile codex --antirlhf
```

From a local checkout:

```bash
python scripts/install.py --profile codex --antirlhf
```

Either path installs the four Skills into `~/.codex/skills/` and prepends the Constitution and a short quoted version/update note as a managed block to `~/.codex/AGENTS.md`, preserving your other instructions.

[Installation and updates](INSTALL.md) covers previews, independent Skills, other harnesses, and `--ref` pinning.

## General Skills

The `general/` directory holds independently installable capabilities:

- [Session Handoff](general/session-handoff/SKILL.md): carry the decisions, context, and unfinished state of a long conversation into the next session.
- [Repo Kit](general/repo-kit/SKILL.md): quick toolbox for common repository setup and hygiene.

```bash
python scripts/install.py --profile codex --skill session-handoff
python scripts/install.py --profile codex --skill repo-kit
```

## Inside the repository

```text
.config/arsvine-skills/   Active project checker configuration
AntiRLHF/
  .version                Bundle version
  CONSTITUTION.md          Persistent governance
  README.md / README.en.md Governance approach and evolution
  INDEX.md                Documentation index
  skills/                 Four bundled Skills (bundled defaults in scripts/.config/)
  docs/                   Research notes and literature
  archive/                Historical governance texts
general/                  Independent Skills, each with .version
scripts/                  install.py, install-remote.py, validate.py
```

## Develop

```bash
python scripts/validate.py
```

Format:

```bash
# Python — install once: uv tool install ruff  (or: uv sync --group dev)
ruff format .
ruff check --fix .

# Markdown / YAML — install once: npm install
npm run format
```

The repository validator checks Skill structure, documentation navigation, all maintained prose (including this README and Skill references), Skill interface text, scanner behavior, and Python compilation. Versions live in `AntiRLHF/.version` and each general Skill's `.version`; the installer records them with the installed Skills and adds a short update note to the AntiRLHF instruction block or the general Skill's own `SKILL.md`.

## Navigation

- [Install](INSTALL.md)
- [AntiRLHF introduction](AntiRLHF/README.en.md)
- [AntiRLHF index](AntiRLHF/INDEX.md)
- [Research notes](AntiRLHF/docs/README.en.md)
