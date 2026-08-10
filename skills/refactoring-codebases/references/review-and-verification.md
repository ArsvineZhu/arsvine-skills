# Review and verification

## Purpose

Verify both dimensions of a refactor:

1. preserved behavior/contracts;
2. actual structural improvement.

A green test suite is not enough if the refactor added unnecessary complexity. A cleaner architecture is not enough if behavior drifted.

## Per-pass diff review

After each material pass, inspect the diff deliberately.

Ask:

- Does every changed file belong to this pass?
- Is there accidental formatting/churn?
- Did a public/exported surface change?
- Did coupling move rather than decrease?
- Did the new abstraction gain a clear semantic owner?
- Are there temporary shims/adapters that need a removal plan?
- Did state/side-effect ownership become clearer?
- Did tests become weaker or more implementation-coupled?
- Are comments/docs now stale?
- Did dead code or duplicate paths remain after the move?

## Architectural review

Evaluate:

- responsibility boundaries;
- cohesion;
- dependency direction;
- state ownership;
- side-effect boundaries;
- interface width/clarity;
- testability;
- change locality;
- number/quality of concepts a maintainer must understand.

Do not declare success because there are more files/classes/interfaces.

## Validation evidence

Use commands that actually exist in the repository. Prefer existing automation over inventing new ad hoc checks.

Possible evidence:

- focused tests;
- package/repository test suites;
- typecheck/compiler;
- lint/format;
- build;
- schema/contract compatibility;
- code generation/check-generated;
- integration/E2E/smoke tests;
- architecture/import tests;
- benchmarks/performance checks;
- concurrency/stress checks.

## Baseline comparison

Report results relative to the pre-refactor baseline.

Good reporting distinguishes:

- `PASS` now and before;
- pre-existing `FAIL` unchanged;
- new regression;
- flaky/inconclusive;
- not run due to environment/credentials/time/tooling.

Never convert "not run" into "pass."

## Verification depth by risk

### R1 — Local structural

Examples: local rename/extract/simplification with strong tests and no contract exposure.

Use focused tests/type/lint as appropriate.

### R2 — Cross-module internal

Examples: internal interface change, package move, dependency-cycle repair.

Add cross-module build/tests and broader import/consumer checks.

### R3 — Contract-adjacent/stateful/dynamic

Examples: serialization, persistence, concurrency, plugin loading, public exports, external integrations, security-sensitive boundaries.

Require stronger independent parity evidence and broader validation.

### R4 — Migration/breaking

Not ordinary refactoring. Use migration workflow and explicit compatibility/rollback checkpoints.

Risk labels are reasoning aids, not mandatory repository metadata.

## Review the tests

Tests can be wrong.

Check:

- Would the test fail if the protected behavior broke?
- Are assertions meaningful?
- Did the refactor weaken or bypass the oracle?
- Are mocks hiding real integration behavior?
- Were snapshots updated blindly?
- Did test changes merely mirror implementation changes?

## Completion review

Before final completion, inspect for:

- stale imports/exports;
- orphan files;
- duplicate old/new implementations;
- obsolete compatibility code;
- stale comments/TODOs;
- changed public surface;
- architecture rule regressions;
- unrelated cleanup;
- unexplained large diffs.

## Convergence review

Ask whether the next candidate pass has demonstrable value.

Stop when remaining work is primarily:

- personal style preference;
- speculative future-proofing;
- broad naming churn;
- pattern uniformity with no change-cost benefit;
- migration/feature work outside scope.

## Final report quality

A useful report says what changed and what evidence supports it.

Avoid vanity metrics such as "reduced 3 files" unless they correlate to a real structural benefit.

Prefer statements like:

- one owner now defines tax rounding instead of three divergent copies;
- domain logic no longer imports transport infrastructure;
- plugin registration remains compatible and is covered by startup discovery test;
- three baseline test failures remain pre-existing; no new relevant failures were introduced.
