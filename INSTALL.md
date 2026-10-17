# Install Arsvine Skills

[中文](INSTALL.zh-CN.md)

Use Python 3.11 or newer. Run these commands from a local checkout of this repository.

## Choose what to install

AntiGPT installs its Constitution and four Skills together: `antigpt-plan`, `antigpt-exec`, `refactoring`, and `documentation`.

```bash
python scripts/install.py --profile codex --antigpt
```

Install an independent general Skill:

```bash
python scripts/install.py --profile codex --skill session-handoff
```

Combine the selections:

```bash
python scripts/install.py --profile codex --antigpt --skill session-handoff
```

Without selection flags, the installer installs AntiGPT and all general Skills. Use `--dry-run` to preview any command.

## Destinations

The Codex profile writes Skills to `~/.codex/skills/` and prepends the AntiGPT managed block to `~/.codex/AGENTS.md`. Existing instructions follow it. General Skills install only into their Skill directories; their version and update note lives in `SKILL.md`.

For another harness, provide its persistent instruction file and Skill directory:

```bash
python scripts/install.py --antigpt \
  --instructions-file /path/to/persistent/instructions.md \
  --skills-dir /path/to/skills
```

Installed Skill directories are replaced with the selected source content. Keep personal edits in the source checkout before reinstalling.

## Versions and updates

- `AntiGPT/.version` is the version of the whole AntiGPT bundle. The installer copies that version into each of its four installed Skill directories as `.version`.
- Each Skill under `general/` owns its own `.version`, copied with the Skill.
- AntiGPT appends a short `>` version and update note inside its Constitution block, without a separate heading or local path. General Skills carry the equivalent note in their own `SKILL.md`. The note asks the Agent to check once per session when access is available, notify the user of a newer version, and ask before updating.

To update, obtain the latest repository content and rerun the same installation command. This refreshes selected Skills and their version notes. Installing AntiGPT also refreshes its managed block at the beginning of the instruction file.

## Ask an Agent to install

> Install AntiGPT from this repository as a complete four-Skill bundle. Use the installer with this harness's persistent instruction file and Skill directory. Preserve existing unrelated instructions. Include the installed versions and update-notification guidance. Show me the installation result.

## Validate this checkout

```bash
python scripts/validate.py
```

Repository commands and configuration live under `scripts/`. The documentation Skill owns the reusable prose and navigation checkers. Validation scans the repository’s maintained human and AI-facing documents together. Historical JDD, TED, and COST source texts are excluded; their maintained archive introductions are included.

## Navigation

- [Repository overview](README.md)
- [AntiGPT introduction](AntiGPT/README.en.md)
- [AntiGPT index](AntiGPT/INDEX.md)
