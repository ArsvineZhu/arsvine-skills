---
name: agency-execution
description: Use when implementing, refactoring, debugging, testing, verifying, or delivering non-trivial repository changes where local investigation, compatibility, validation, or process growth can pull work away from the authorized objective.
---

# Agency Execution

Apply the persistent Execution Core throughout the task.

Load only the references triggered by the current work:

- scope, ownership, or long-running trajectory → `references/trajectory.md`
- structural replacement, cleanup, or topology change → `references/refactoring.md`
- bug, test failure, unexpected behavior, or failing build → `references/debugging.md`
- tests, verification, qualification, evidence, or CI → `references/testing-and-verification.md`
- commit, PR, merge, or delivery → `references/git-and-delivery.md`
- suspected recurrence of known failure modes → `references/failure-patterns.md`
- need for worked examples → `references/examples.md`

For substantial prose, Specs, AGENTS changes, or governance-sensitive documentation, run `scripts/scan_defensive_language.py` on the changed files and review each hit semantically.
