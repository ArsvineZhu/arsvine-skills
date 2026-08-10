# Migration boundary

## Purpose

Recognize when structural refactoring has become a migration, behavior change, or coordinated compatibility project that requires a different execution contract.

## Strong migration signals

Treat the work as migration or behavior-change work when it requires one or more of:

- framework replacement or major framework-version transition with semantic changes;
- runtime/language/platform migration;
- major dependency upgrade with breaking contracts;
- public API/CLI break;
- persistent data/schema migration;
- protocol/serialization format change;
- configuration/env semantic change requiring consumer updates;
- auth/security/trust-boundary redesign;
- deployment architecture replacement;
- consumer coordination or compatibility window;
- data backfill/conversion;
- old and new implementations coexisting during rollout.

## Boundary question

Ask:

> Can the desired structural improvement be completed as a series of behavior-preserving transformations while existing consumers continue to work unchanged?

If yes, ordinary refactoring may continue.

If no, the task needs migration semantics.

## What changes in migration mode

Migration requires stronger planning for:

- old→new concept mapping;
- compatibility layers;
- rollout/checkpoints;
- data/consumer transition;
- parity during coexistence;
- rollback/fallback;
- deprecation/removal conditions;
- operational communication.

Do not silently apply these assumptions under the refactoring label.

## Branch by abstraction

For large replacements that must remain releasable:

1. establish an abstraction around the current dependency/boundary;
2. route existing behavior through it;
3. add the replacement implementation;
4. compare/validate implementations;
5. migrate consumers incrementally where possible;
6. remove the old implementation and transitional abstraction only when safe.

Use only when the abstraction creates a genuine migration seam. Do not introduce it for a small direct replacement.

## Parallel/dual-run parity

When old/new implementations can run side-by-side safely, compare outputs/effects before switching ownership. Account for side effects; shadow execution is not safe for every operation.

## Major dependency upgrades

If a dependency upgrade is incidental to refactoring, keep the current supported version unless there is a concrete blocker.

If upgrade is required:

- classify separately;
- inventory breaking changes;
- verify platform/build/runtime assumptions;
- preserve rollback where practical;
- avoid mixing broad code cleanup into the same migration checkpoint.

## Public contract change

If internal structure can only improve by breaking public contracts:

- identify affected consumers;
- explain why an internal compatibility layer is insufficient;
- obtain explicit authorization when required;
- use versioning/deprecation/migration strategy appropriate to the project.

## Handoff output

When stopping a refactoring campaign at the migration boundary, report:

- the desired structural improvement;
- the blocking contract/migration requirement;
- affected surfaces;
- recommended migration strategy/checkpoints;
- what safe refactoring was completed beforehand;
- what remains intentionally unmodified.
