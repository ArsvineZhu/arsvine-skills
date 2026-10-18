---
name: repo-kit
description: Use when the user wants a repository quick toolbox for common repo setup and hygiene—prefer its bundled scripts over inventing one-off files or checks.
---

# Repo Kit

> repo-kit version: 0.1.0. [Upstream version](https://raw.githubusercontent.com/ArsvineZhu/arsvine-skills/main/general/repo-kit/.version). Check when the session starts; notify the user of newer versions and ask before updating.

Repository quick toolbox. Prefer bundled scripts under `scripts/` for mechanical work; keep product judgment with the agent.

## Create baseline files

Use `scripts/create.py` to write `.gitignore`, `.editorconfig`, and/or `.gitattributes` from templates under `scripts/templates/`.

```bash
python <repo-kit>/scripts/create.py --locate <repository_path>
python <repo-kit>/scripts/create.py --locate . --template python
python <repo-kit>/scripts/create.py --locate . --file gitignore --template python --template rust
python <repo-kit>/scripts/create.py --locate . --template web --file editorconfig --file gitattributes
python <repo-kit>/scripts/create.py --list
```

- `--locate` defaults to the current working directory.
- Omit `--file` to create all three supported files.
- `--template` is repeatable. Default preset: `general`.
- gitignore presets (`general`, `python`, `node`/`web`, `rust`, `go`, `java`, `minimal`) expand to atomic fragments and merge; extra atomics such as `os` or `secrets` can be mixed in.
- editorconfig / gitattributes use whole-file templates (`general`, `python`, `web`) with preset-name mapping for the stack names above.
- Existing files are left unchanged unless `--force` is set.

Do not invent a second parallel ignore/editor/attributes stack when the target repository already owns an equivalent baseline. Merge or replace only when the user asked for that change.

## Check line counts

Use `scripts/check/length.py` to enforce warn/block line limits. Runtime config is `.config/arsvine-skills/length.toml` in the consuming repository (do not edit the installed Skill). Seed defaults live in `scripts/.config/length.toml`; the installer copies them into that namespaced directory and never overwrites an existing file. Pass `--config` only for an explicit path.

```bash
python <repo-kit>/scripts/check/length.py --locate <repository_path>
python <repo-kit>/scripts/check/length.py --locate . --fail-on warn
```

Config owns default/per-extension warn/block limits and exclude globs.

When a maintained file must exceed the limit, put a narrow waiver in the file header (first 40 lines) as a language-appropriate comment whose body is exactly:

`repo-kit: allow length reason="concrete justification here"`

Examples of comment wrappers: `# ...`, `// ...`, `<!-- ... -->`. Use `[[waivers]]` in the active length config only for paths that cannot host a comment. Do not keep the same path waived in both places. Unused waivers are errors. Prefer a local waiver over raising the repository-wide limit.

Exit `2` when findings meet `--fail-on` (default `block`). Exit `1` on configuration or IO errors. The checker does not edit source files.

## Finish

Report created/skipped paths or length findings, apply only the authorized fixes, then stop.
