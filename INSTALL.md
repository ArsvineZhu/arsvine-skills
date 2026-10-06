# Install Arsvine Skills

Arsvine Skills has two installation surfaces:

1. `AntiGPT/CONSTITUTION.md` belongs in the Harness's persistent user-level instructions.
2. Directories under `skills/` belong in the Harness's Skill directory or native Skill installer.

The Constitution is persistent governance. Role and task Skills remain progressively disclosed and load only when relevant.

## Codex

From a local checkout:

```bash
python scripts/install.py --profile codex
```

Default destinations:

```text
~/.codex/AGENTS.md
~/.codex/skills/
```

The installer inserts or replaces a delimited AntiGPT Constitution block and preserves all other content in the existing `AGENTS.md`.

Preview changes without writing:

```bash
python scripts/install.py --profile codex --dry-run
```

Install selected Skills only:

```bash
python scripts/install.py --profile codex --skill antigpt-plan --skill antigpt-exec
```

## Other Harnesses

Use the Harness's persistent global instruction file and native Skill directory:

```bash
python scripts/install.py \
  --instructions-file /path/to/persistent/instructions.md \
  --skills-dir /path/to/skills
```

Override the selected Skills with repeated `--skill` options.

If a Harness has its own plugin or marketplace installer, native installation may replace the file-copy step. Keep `AntiGPT/CONSTITUTION.md` as the single canonical governance source; do not maintain a second Harness-specific Constitution.

## AI-assisted installation

You can give a capable Coding Agent this repository and ask it to:

> Install Arsvine Skills for this Harness. Put `AntiGPT/CONSTITUTION.md` into the user-level persistent instructions without deleting unrelated existing instructions. Install the desired directories under `skills/` through the Harness's native Skill mechanism. Treat archived governance as historical only. Verify that the installed Skill metadata is discoverable.

## Updating

Re-run the installer. The managed Constitution block is replaced in place, and installed Skill directories are synchronized from the current checkout.

## Navigation

- [Repository overview](README.md)
- [AntiGPT](AntiGPT/README.md)
