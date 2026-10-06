---
name: antigpt-exec
description: Use when implementing, refactoring, debugging, testing, verifying, changing repository documentation, or delivering non-trivial repository work where local investigation, compatibility, validation, or process growth can pull work away from the authorized objective.
---

# AntiGPT Exec

Apply the AntiGPT Constitution. This Skill adds Execution-specific semantics; it does not redefine the shared governance core.

Load only the references triggered by the current work:

- scope, ownership, repository state, or long-running trajectory → `references/trajectory.md`
- structural replacement, codebase refactoring, dead code, compatibility, or topology change → `references/refactoring.md`
- repository documentation changes, archival, canonical fact ownership, or navigation maintenance → `references/documentation-maintenance.md`
- bug, test failure, unexpected behavior, or failing build → `references/debugging.md`
- tests, verification, qualification, evidence, or CI → `references/testing-and-verification.md`
- commit, PR, merge, or delivery → `references/git-and-delivery.md`
- suspected recurrence of known failure modes → `references/failure-patterns.md`
- need for worked examples → `references/examples.md`

Use bundled scripts for mechanical claims they can actually decide. Semantic judgment remains with the role.

For substantial governance-sensitive prose, run:

```bash
python scripts/check_governance_prose.py <changed-prose>
```

For maintained human-documentation navigation, run:

```bash
python scripts/check_doc_graph.py
```
