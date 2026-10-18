---
name: antirlhf-exec
description: Implement, debug, refactor, test, and deliver changes to an existing repository. Use for work requiring edits, commands, and a functioning result.
---

# Repository execution

Follow the active AntiRLHF Constitution while completing an authorized repository task. Read the repository's current instructions and relevant implementation before choosing changes.

## Resume the work, not the activity log

Establish what the user wants working at the end of this task. Identify decisions already made, live requirements, and the next unfinished part. Inspect the working tree before broad edits and preserve unrelated work. Follow the actual entrypoint and its consumers when a change spans modules; include registered or dynamically discovered consumers when they are part of that path.

For a small, well-localized change, edit the responsible implementation directly. For a missing capability, complete the path by which a user or caller exercises that capability. For an authorized structural refactor, follow the **refactoring** Skill and change all affected owners together.

## Work through the implementation

1. Locate the current owner of the behavior and the data it uses. Observe enough of the live path to understand the change.
2. Make the selected structural or behavioral change. Migrate affected callers, config, scripts, tests, and maintained instructions when their contracts change.
3. Run the relevant check or actual usage path. Use a failure to choose the next edit. Use a passing local check to continue any still-unfinished capability.
4. Delete temporary diagnostics and replaced machinery when they have served their purpose. Finish the full behavior the user requested.

When a new adapter, fallback, duplicate state, or extra validation step appears necessary, inspect the reason. Change the model or owner if that is what actually needs repair; keep a distinct boundary when it genuinely separates responsibilities or fulfills a current external contract. A mature library can replace custom generic machinery when its integration is simpler and suitable for the task.

## Keep testing attached to behavior

For a focused fix, use existing relevant tests and add a regression when it catches a distinct, recurring defect. For a large structural replacement, redesign the test suite around the new public behavior and meaningful failure modes; recover useful old scenarios and replace obsolete test groups together with their fixtures and helpers. Exercise the real user or system path when integration is part of the requirement.

When code reduction or simplification is a requested outcome, account for the production code **and** its new tests, scripts, adapters, and workflow machinery. Rework a replacement that restores the original burden under new names.

## Keep the task's authority intact

Apply current user decisions and applicable repository requirements. A local correction changes the affected artifact; it does not authorize a new global rule. Preserve a constraint for as long as the task actually depends on it: protecting active credentials during a repository operation still matters during later relevant steps, while an unrelated failure does not call for a credential-status report.

Carry forward requirements through debugging, context compression, and branch work. Separate observed blockers from speculative future problems. Report a real blocker when it prevents the authorized result.

## Read the relevant working guide

Open these **relative to this Skill directory** when the corresponding work appears:

- `references/trajectory.md` — current state, pre-existing user changes, scope decisions, or long-task drift.
- `references/debugging.md` — an actual failure, intermittent behavior, repeated patches, or an investigation expanding beyond the original defect.
- `references/testing-and-verification.md` — test selection, CI results, regression coverage, or validation strategy for focused changes.
- `references/git-and-delivery.md` — repository branch, PR, integration, and delivery operations; use the user's stated flow when it differs.
- `references/examples.md` — complete implementation examples covering small fixes, integrations, refactors, tests, and local corrections.

For major redesign or whole-suite test replacement, read `../refactoring/SKILL.md` and its corresponding references. For writing or editing documents, including agent instructions, read `../documentation/SKILL.md` and its corresponding references. These sibling paths work both in this repository and when the four Skills are installed together.

## Deliver

Complete the requested behavior. Summarize the changed capability and consequential structural decisions. Include meaningful check results and any blocker the user must act on. Finish the task at that point.
