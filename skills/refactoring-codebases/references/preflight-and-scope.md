# Preflight and scope

## Purpose

Establish a safe refactoring boundary before deep repository exploration or modification. The preflight is intentionally short: it should expose material blockers and repository hazards without turning into the full audit.

## Preflight outputs

Before substantial edits, establish:

- execution mode: assessment or execution;
- repository/worktree status;
- applicable agent instructions and local overrides;
- user-owned or unrelated in-progress changes;
- obvious workspace/package/application boundaries;
- generated, vendored, external, or protected areas;
- likely public/external contract surfaces;
- available validation entry points;
- whether the request contains an explicit behavior-change or migration authorization.

## Interaction discipline

Ask early only when an answer would materially alter scope or cause substantial rework.

Batch foreseeable blocking questions. Do not ask one predictable question, perform a long investigation, and then block on another predictable question.

Prefer conservative defaults:

- observable behavior remains stable;
- public contracts remain stable;
- schema/persistent/protocol formats remain stable;
- major dependency/framework/runtime upgrades are out of ordinary refactoring scope;
- unrelated cleanup remains out of scope;
- generated artifacts are modified through their canonical source/generator.

If these defaults satisfy the request, do not ask for redundant permission.

## Working-tree safety

Inspect version-control state before broad edits.

Determine:

- changed/untracked files;
- whether changes predate the refactor;
- whether target files overlap unrelated user work;
- whether a worktree/branch policy exists;
- whether automation may rewrite broad portions of the tree.

Do not:

- hard reset;
- checkout/revert unrelated files;
- discard untracked user work;
- normalize/reformat unrelated files merely to make the diff cleaner;
- assume a clean tree because no status information was provided.

When target files contain unrelated edits, preserve them and make the smallest compatible change. If safe separation is impossible, raise the conflict before destructive action.

## Instruction hierarchy

Read the repository's applicable `AGENTS.md`, local agent instructions, contribution rules, generated-code policies, and build/test guidance before editing.

Treat instructions as constraints, but verify executable facts against the current repository when instructions appear stale or contradictory. Do not silently ignore a rule because it is inconvenient; surface a genuine conflict.

## Generated and protected content

Identify files that are:

- generated from schemas/codegen/templates;
- vendored or third-party;
- build output;
- synchronized from another source;
- externally maintained;
- security- or compliance-sensitive.

Prefer changing the source of generation. If generated output must be committed, regenerate through the repository's verified workflow.

## Scope classification

### Assessment mode

Use when the requested output is analysis, prioritization, a refactoring plan, or an architecture/technical-debt audit.

Stop before production edits unless the user explicitly requests execution.

### Execution mode

Use when the user asks to refactor, clean up, restructure, or modernize the codebase in place.

Do not introduce an unnecessary second approval gate after the user has already authorized execution.

## Scope boundary tests

A proposed change is likely ordinary refactoring when all are true:

- its purpose is internal structural improvement;
- intended external behavior remains the same;
- public/external consumers do not require migration;
- persistent/protocol/config semantics remain stable;
- deployment/runtime platform does not fundamentally change;
- rollback is conceptually "restore old internals," not "migrate data/consumers back."

If these fail, read `migration-boundary.md`.

## Preflight anti-patterns

Avoid:

- exhaustive repository indexing before asking a known blocking question;
- running the full test suite before knowing whether it is relevant;
- deep Git archaeology as a first step;
- proposing architecture before reading applicable instructions/manifests;
- asking users to decide facts that repository evidence can answer;
- silently assuming breaking-change authorization because the user said "refactor everything."
