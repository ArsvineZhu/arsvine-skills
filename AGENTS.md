# Repository Instructions

This repository governs itself with AntiRLHF.

- Read `AntiRLHF/CONSTITUTION.md` before non-trivial work.
- Use `AntiRLHF/skills/antirlhf-plan` for non-trivial research, architecture, technical comparison, specification, and design judgment.
- Use `AntiRLHF/skills/antirlhf-exec` for non-trivial repository implementation, refactoring, debugging, testing, verification, and delivery.
- Treat `AntiRLHF/archive/` as historical material. Archived documents may explain lineage; they do not define current policy.
- Keep `CONSTITUTION.md`, `SKILL.md`, AI-facing references, agent instructions, and executable governance text in concise technical English.
- Human-facing documentation uses English entrypoints and Chinese authoritative research editions. Keep the maintainer’s perspective in `AntiRLHF/README.md`; maintain its English translation.
- AntiRLHF installs its four Skills together; `general/` contains independent Skills. The documentation Skill owns reusable checkers; root `scripts/` owns repository installation and validation.
- Use `AntiRLHF/skills/refactoring` for structural refactoring and `AntiRLHF/skills/documentation` for documentation work.
- Prefer structural correction and canonical ownership over compatibility layers, duplicate policy, local compensation, or minimum-diff preservation.
- Preserve user work and repository state that the current task does not authorize changing.
- Development work uses a branch and lands through Squash Merge.

- Run `python scripts/validate.py` for repository validation. Check maintained human documents and AI-facing instructions with the existing prose scanner. Keep research writing within the same documentation graph. Historical governance source texts remain outside the active policy scope.
