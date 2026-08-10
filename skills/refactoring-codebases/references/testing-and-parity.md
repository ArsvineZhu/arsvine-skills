# Testing and parity

## Purpose

Use independent evidence to show that structural changes preserved the intended behavior. Passing tests are only useful if the tests are capable of detecting the relevant regressions.

## Establish the baseline

Before risky edits, record relevant results:

- passing checks;
- failing checks;
- flaky/unstable checks;
- skipped/unsupported checks;
- environment limitations.

Do not assume the repository starts green.

Final reporting should distinguish:

- pre-existing failures unchanged;
- new failures introduced;
- pre-existing failures resolved intentionally/incidental;
- checks not run or not reliable.

## Characterization tests

When important existing behavior lacks coverage, add the smallest useful test/evidence that captures current behavior before refactoring.

A characterization test is not an endorsement of the current architecture. It protects behavior while structure changes.

Prioritize behavior that is:

- externally visible;
- financially/security/operationally important;
- complex or stateful;
- easy to change accidentally;
- weakly documented;
- relied upon by multiple consumers.

## Independent behavioral oracles

If implementation and tests both need structural updates, keep at least one reasonably independent oracle when practical:

- public contract test;
- integration/E2E behavior;
- golden file/fixture;
- schema validation;
- CLI output/exit-code check;
- dual-run comparison old vs new implementation;
- deterministic snapshot of an externally meaningful result;
- database/state transition assertion;
- protocol conformance test.

Do not modify every oracle to mirror the new implementation and then treat green tests as strong parity evidence.

## Test quality during refactoring

Do not:

- weaken assertions to make the new structure pass;
- replace behavioral assertions with implementation-detail assertions;
- over-mock the code merely because the new architecture has more seams;
- delete regression tests without proving redundancy/obsolescence;
- test private helper arrangement when public behavior is the real contract.

When refactoring improves a boundary, move tests toward stable behavior where practical.

## Focused vs full verification

Use focused checks after each pass for fast localization. Use broader checks at campaign completion or before crossing a high-risk boundary.

Focused checks can include:

- exact unit/contract tests for changed behavior;
- package typecheck/build;
- targeted integration tests;
- generated output comparison;
- architecture/dependency test.

Full checks can include repository-wide tests, build, lint, typecheck, and E2E according to actual project tooling.

## State and side-effect parity

For stateful code, verify more than final return values:

- writes performed/not performed;
- transaction atomicity;
- order of effects;
- retries/idempotency;
- cleanup;
- emitted events;
- cache changes;
- failure-state behavior.

## Concurrency parity

When relevant, protect:

- ordering guarantees;
- concurrency limits;
- cancellation;
- races/data safety;
- resource cleanup;
- backpressure;
- retry interactions.

A deterministic happy-path test may miss these entirely.

## Performance parity

Only treat performance as a formal parity dimension when evidence says it matters. When it does:

- use existing benchmarks/SLO checks when possible;
- measure before and after under comparable conditions;
- do not over-interpret noisy microbenchmarks;
- report the observed delta and uncertainty.

## Test refactoring

Test code can itself be refactored. Separate pure test-structure cleanup from production behavior changes when doing so makes the parity signal clearer.

If a test is genuinely obsolete because the contract no longer exists, that is a behavior/migration decision—not automatically part of structural refactoring.
