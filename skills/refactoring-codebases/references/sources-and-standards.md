# Sources and standards

This Skill is intentionally repository-agnostic. Use current project instructions and ecosystem-specific guidance first when they impose stricter constraints. The sources below inform the general workflow and should be rechecked when platform behavior may have changed.

## OpenAI / Codex

### Build skills

https://learn.chatgpt.com/codex/build-skills

Key guidance used here:

- Skills are reusable workflows with required `SKILL.md` and optional references/scripts/assets.
- Skills use progressive disclosure: name/description first, full `SKILL.md` on activation, supporting resources as needed.
- Keep each Skill focused on one job.
- Instruction-only is the default; prefer scripts when deterministic behavior/tooling justifies them.
- Write clear descriptions with trigger boundaries and test trigger behavior.

### Refactor your codebase

https://learn.chatgpt.com/codex/use-cases/refactor-your-codebase

Key guidance used here:

- Preserve behavior unless functional change is explicitly requested.
- Identify dead code, duplicated paths, oversized modules, stale abstractions, and legacy patterns.
- State current behavior, structural improvement, and validation for each pass.
- Use small reviewable refactoring passes.
- Split framework migrations, dependency upgrades, API changes, and major architecture moves into migration work when appropriate.

### Understand large codebases

https://learn.chatgpt.com/codex/use-cases/codebase-onboarding

Key guidance used here:

- Map request/control flow rather than only summarizing files.
- Identify ownership of business logic, transport, persistence, UI.
- Locate validation, side effects, state transitions, and risky areas before editing.

### Run code migrations

https://learn.chatgpt.com/codex/use-cases/code-migrations

Key guidance used here:

- Migrations use controlled checkpoints and parity validation.
- Inventory legacy assumptions and external contracts.
- Use incremental strategies such as compatibility layers, module-by-module ports, branch-by-abstraction, or strangler-style replacement where appropriate.
- Keep rollback/fallback visible until transition completes.

### Harness engineering

https://openai.com/index/harness-engineering/

Key guidance used here:

- Agent-first repositories benefit from explicit architecture constraints and feedback loops.
- Stable rules can be enforced with linters, structural tests, and other mechanical guardrails.
- Progressive disclosure helps agents load the right context without overwhelming the prompt.

## Agent Skills specification

https://agentskills.io/specification

Key guidance used here:

- `SKILL.md` requires valid YAML frontmatter with `name` and `description`.
- `references/`, `scripts/`, and `assets/` are optional resources.
- Keep `SKILL.md` under 500 lines and move heavy reference material into supporting files.
- Prefer shallow file references from the Skill entry point.

## Refactoring discipline — Martin Fowler

### Refactoring: Improving the Design of Existing Code

https://martinfowler.com/books/refactoring.html

Core principle used here: refactoring is a sequence of small behavior-preserving transformations that cumulatively improve the design while reducing regression risk.

### Definition of Refactoring

https://martinfowler.com/bliki/DefinitionOfRefactoring.html

Used to maintain the semantic boundary between refactoring and general restructuring/behavior change.

### Branch by Abstraction

https://martinfowler.com/bliki/BranchByAbstraction.html

Used only at the migration boundary for large replacements that need old/new implementations to coexist while the system remains releasable.

### Preparatory refactoring / two hats

https://martinfowler.com/articles/preparatory-refactoring-example.html

Used for the distinction between behavior-preserving structural work and adding/changing functionality.

## Google Engineering Practices

### Small CLs

https://google.github.io/eng-practices/review/developer/small-cls.html

Key guidance used here:

- Prefer one self-contained change at a time.
- Small changes are easier to review, reason about, merge, and roll back.
- Separate substantial refactoring from feature/bug changes.
- Pure refactoring should be protected by tests; adding tests first can increase confidence when coverage is missing.

### What to look for in a code review

https://google.github.io/eng-practices/review/reviewer/looking-for.html

Key guidance used here:

- Review design, functionality, complexity, tests, naming, comments, style, and documentation.
- Tests themselves require review.
- Comments generally add the most value when they explain why rather than restating what code does.
- Avoid unnecessary complexity and speculative implementation for unknown future needs.

### The standard of code review

https://google.github.io/eng-practices/review/reviewer/standard.html

Used for the principle that each change should improve or at least not degrade overall code health while still allowing progress.

## Applying external guidance

Do not treat any generic source as a substitute for repository evidence.

Repository-specific constraints, language/tooling conventions, compatibility guarantees, and platform semantics take precedence when they are current and valid.

If a source may have changed since this Skill was authored, verify the current source before relying on platform-specific details.
