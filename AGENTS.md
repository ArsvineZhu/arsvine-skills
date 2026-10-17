# Repository Instructions

This repository governs itself with AntiGPT.

- Read `AntiGPT/CONSTITUTION.md` before non-trivial work.
- Use `AntiGPT/skills/antigpt-plan` for non-trivial research, architecture, technical comparison, specification, and design judgment.
- Use `AntiGPT/skills/antigpt-exec` for non-trivial repository implementation, refactoring, debugging, testing, verification, and delivery.
- Treat `AntiGPT/archive/` as historical material. Archived documents may explain lineage; they do not define current policy.
- Keep `CONSTITUTION.md`, `SKILL.md`, AI-facing references, agent instructions, and executable governance text in concise technical English.
- Human-facing documentation uses English entrypoints and Chinese authoritative editions. Preserve the handwritten Chinese `AntiGPT/README.md` and translate it into `AntiGPT/README.en.md`.
- AntiGPT installs its four Skills together; `general/` contains independent Skills. The documentation Skill owns reusable checkers; root `scripts/` owns repository installation and validation.
- Use `AntiGPT/skills/refactoring` for structural refactoring and `AntiGPT/skills/documentation` for documentation work.
- Prefer structural correction and canonical ownership over compatibility layers, duplicate policy, local compensation, or minimum-diff preservation.
- Preserve user work and repository state that the current task does not authorize changing.
- Development work uses a branch and lands through Squash Merge.

- Run `python scripts/validate.py` for repository validation. The repository uses its own documentation checker on maintained human documents, AI references, Skills, and interface metadata. Keep teaching examples in scope with specific waivers. Historical JDD/TED/COST source texts are excluded; archive introductions are maintained prose.
