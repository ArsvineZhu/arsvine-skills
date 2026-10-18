# Install Arsvine Skills

[中文](INSTALL.zh-CN.md)

Use Python 3.11 or newer. No local clone is required for the remote installer.

## Remote install (no clone)

Fetch the repository archive and run the installer in one step. Flags after `-` are the same as `scripts/install.py`:

```bash
curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \
  | python3 - --profile codex --antirlhf
```

On Windows, use `curl.exe` and `python` the same way. Pin a branch, tag, or commit with `--ref` (default `main`):

```bash
curl -fsSL https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/scripts/install-remote.py \
  | python3 - --ref main --profile codex --antirlhf --dry-run
```

The bootstrap downloads a GitHub zip archive into a temporary directory, runs that tree's `scripts/install.py`, then deletes the temporary checkout unless you pass `--keep-fetch`. Use `--from PATH` to run against an existing checkout instead of downloading.

## Install from a local checkout

From a clone of this repository:

```bash
python scripts/install.py --profile codex --antirlhf
```

## Choose what to install

AntiRLHF installs its Constitution and four Skills together: `antirlhf-plan`, `antirlhf-exec`, `refactoring`, and `documentation`.

```bash
python scripts/install.py --profile codex --antirlhf
```

Install an independent general Skill:

```bash
python scripts/install.py --profile codex --skill session-handoff
python scripts/install.py --profile codex --skill repo-kit
```

Combine the selections:

```bash
python scripts/install.py --profile codex --antirlhf --skill session-handoff --skill repo-kit
```

Without selection flags, the installer installs AntiRLHF and all general Skills. Use `--dry-run` to preview any command. The same selection flags work with `install-remote.py`.

## Destinations

The Codex profile writes Skills to `~/.codex/skills/` and prepends the AntiRLHF managed block to `~/.codex/AGENTS.md`. Existing instructions follow it. General Skills install only into their Skill directories; their version and update note lives in `SKILL.md`.

Skill-bundled defaults under each Skill's `scripts/.config/` are copied into the namespaced harness/project directory `.config/arsvine-skills/` next to `AGENTS.md` (or beside `skills/` when no instruction file is used). Filenames are undecorated (`scanner.toml`, `length.toml`, `docgraph.toml`). Existing files in that directory are left unchanged; a pre-existing `.config/` owned by other tools is left alone aside from creating our subdirectory.

For another harness, provide its persistent instruction file and Skill directory:

```bash
python scripts/install.py --antirlhf \
  --instructions-file /path/to/persistent/instructions.md \
  --skills-dir /path/to/skills
```

Installed Skill directories are replaced with the selected source content. Keep personal edits in the source checkout before reinstalling. Project overrides belong in `.config/arsvine-skills/`, not inside installed Skills.

## Versions and updates

- `AntiRLHF/.version` is the version of the whole AntiRLHF bundle. The installer copies that version into each of its four installed Skill directories as `.version`.
- Each Skill under `general/` owns its own `.version`, copied with the Skill.
- AntiRLHF appends a short `>` version and update note inside its Constitution block, without a separate heading or local path. General Skills carry the equivalent note in their own `SKILL.md`. The note asks the Agent to check once per session when access is available, notify the user of a newer version, and ask before updating.

To update from a checkout, pull the latest content and rerun the same `scripts/install.py` command. To update without a clone, rerun the remote installer against the desired `--ref`. Either path refreshes selected Skills and their version notes. Installing AntiRLHF also refreshes its managed block at the beginning of the instruction file.

## Ask an Agent to install

> Install AntiRLHF with the remote installer (`scripts/install-remote.py` via curl) or from this checkout with `scripts/install.py`. Use this harness's persistent instruction file and Skill directory. Preserve existing unrelated instructions. Include the installed versions and update-notification guidance. Show me the installation result.

## Validate this checkout

```bash
python scripts/validate.py
```

Repository commands live under `scripts/`; this repository's active checker policy lives under `.config/arsvine-skills/`. The documentation Skill owns the reusable prose and navigation checkers. Validation scans the repository’s maintained human and AI-facing documents together. `AntiRLHF/archive/` is excluded from prose scanning.

## Navigation

- [Repository overview](README.md)
- [AntiRLHF introduction](AntiRLHF/README.en.md)
- [AntiRLHF index](AntiRLHF/INDEX.md)
- [Research notes](AntiRLHF/docs/README.en.md)
