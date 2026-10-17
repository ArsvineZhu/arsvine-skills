---
name: antigpt-exec
description: Use when implementing, refactoring, debugging, testing, verifying, changing repository documentation, or delivering non-trivial repository work where local investigation, compatibility, validation, or process growth can pull work away from the authorized objective.
---

# AntiGPT Exec

Apply the AntiGPT Constitution in coding, debugging, refactoring, testing, documentation changes, and delivery. Load the refactoring or documentation Skill for their substantive task methods.

Load only the references triggered by the current work:

- scope, ownership, repository state, or long-running trajectory → `references/trajectory.md`
- structural replacement, codebase refactoring, dead code, compatibility, or topology change → `references/refactoring.md`
- repository documentation changes, archival, canonical fact ownership, or navigation maintenance → `references/documentation-maintenance.md`
- bug, test failure, unexpected behavior, or failing build → `references/debugging.md`
- tests, verification, qualification, evidence, or CI → `references/testing-and-verification.md`
- commit, PR, merge, or delivery → `references/git-and-delivery.md`
- suspected recurrence of known failure modes → `references/failure-patterns.md`
- need for worked examples → `references/examples.md`

## Finish the capability

Keep the full intended behavior and explicit engineering goals visible. Work on the highest-impact missing part of the result before polishing already-functioning components. Connect actual producers, state, interfaces, and consumers as the required capability demands. Use real execution paths early enough for their behavior to inform implementation.

A green test suite describes only what those tests exercised. The task stays open while promised capabilities or integration behavior are missing. A local failure, check, or speculation does not displace the objective unless it materially blocks it.

## Change the whole owning structure

Repair wrong authority, data shapes, duplicated policy, and dependency direction at their owners. Migrate affected producers and consumers together; delete the displaced route, wrapper, fallback, and associated temporary machinery. Allow a large coherent diff. Use established libraries and a shared implementation where they replace repeated work. Do not create a new generic framework merely to preserve the previous structure in another form.

When the user sets an explicit code-size or complexity reduction goal, design for a net reduction across production code, tests, scripts, and supporting machinery. Observe net change while implementing. If removal of old code is being outweighed by new layers, reconsider the target architecture before continuing. The requested functionality remains intact.

## Reconstruct bloated tests

For a whole-repository cleanup, derive the required testing structure from desired behavior, meaningful risks, and the new architecture first. Then mine old tests for useful scenarios and invariants. Move those into the new suite and delete superseded tests, fixtures, mocks, harnesses, and test-only adapters in coherent groups. Do not preserve an old test merely because it passes or can be described as protecting something.

For focused changes, keep concise regression and integration checks that discriminate real failures. Temporary diagnostic tests may be removed once their purpose ends. Never design production architecture around a convenience assertion or a coverage metric. Do not replace failing product behavior with changed expectations simply to obtain a PASS.

## Prevent governance from multiplying

A check or workflow executed during development becomes a permanent project requirement only if a current obligation justifies maintaining it. Avoid additional acceptance stages, evidence folders, version inventories, defensive fallback chains, and status tracking invented by the agent. Remove requirements whose underlying mechanisms no longer exist.

Use exact SHA, UUID, or other machine references only at concrete operations or contracts that require them. Normal editing, reading, compiling, and commit preparation must not trigger extra SHA capture or equality checks. A gate invented by the agent cannot justify further identifier tracking. Prefer paths, names, branches, and the objects already returned by tools. No self-invented labels such as `R-01` for plans or task stages.

## Apply constraints without ceremony

Preserve login credentials and other user-owned state where the task calls for it. A local instruction remains limited to its original scope. Fix errors in their owning context; do not create commemorative comments, negative-form documentation, or AGENTS-wide prohibitions from a correction. Mention such constraints to the user when their status affects the result or the user's action.

## Observe and deliver

Use focused falsifiers during iteration; widen verification for changed integration, state, security, or public surfaces when warranted. Inspect real behavior when substitutes cannot answer the task. Use the installed documentation Skill's deterministic prose scanner when editing maintained human-facing or AI-facing prose, and its navigation checker where a maintained navigation graph exists.

Briefly state what now works, important structural removals, and real remaining blockers. Report material checks without replaying their logs or enumerating unrelated SHAs. Stop after the authorized work is complete.
