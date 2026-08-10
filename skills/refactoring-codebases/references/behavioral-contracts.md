# Behavioral contracts

## Purpose

Define what "preserve behavior" means for a refactoring pass. Observable behavior is broader than return values and happy-path output.

## Contract model

For each material refactoring area, record four things:

1. **Current behavior / invariants** — what must remain true;
2. **Structural problem** — why the current shape is costly or risky;
3. **Transformation** — what internal change is proposed;
4. **Parity evidence** — how stability will be demonstrated.

If any of these are missing, the pass is under-specified.

## Observable behavior surfaces

Consider only those that are relevant to the system, but do not overlook:

- return values and rendered output;
- public signatures and type contracts;
- error classes/codes/messages when relied upon;
- validation semantics;
- ordering;
- idempotency;
- side effects;
- persistence and transaction semantics;
- serialized formats;
- filesystem paths/layout;
- event/topic/protocol behavior;
- timing and retry behavior;
- cancellation semantics;
- resource cleanup;
- lifecycle ordering;
- concurrency limits/ordering/races;
- authentication/authorization effects;
- security/trust boundaries;
- configuration precedence/defaults;
- CLI exit codes/stdout/stderr where contractual;
- logs/metrics/traces that operational automation relies on;
- performance/resource characteristics when they are an established practical contract.

Do not broaden the contract unnecessarily. The goal is to protect real behavior, not freeze every incidental implementation detail.

## Invariants

Some important contracts are best expressed as invariants:

- exactly-once/at-most-once effects;
- monotonic state transitions;
- transaction atomicity;
- cache invalidation guarantees;
- dependency direction;
- deterministic serialization;
- ordering constraints;
- no network call before validation;
- no mutation after cancellation;
- cleanup always occurs after acquisition.

Prefer a direct executable check when an invariant can be tested mechanically.

## Public vs internal contracts

Public/external contracts deserve stronger preservation evidence than internal seams.

Internal interfaces MAY change freely when:

- all consumers are understood;
- behavior remains stable;
- the new boundary is demonstrably better;
- the change does not leak into a hidden external contract.

Public/external contracts SHOULD remain stable by default. If they must change, the work has crossed into migration/behavior-change territory.

## Intentional behavior changes

If the user explicitly authorizes a functional change alongside refactoring:

- separate the behavior-changing change from structural cleanup when practical;
- define old behavior and new behavior explicitly;
- do not use "parity" language for the changed dimension;
- preserve unrelated contracts;
- test the new behavior independently.

Use the "two hats" discipline: know whether the current step is preserving behavior or changing it.

## Non-functional contracts

Performance, memory, startup time, concurrency throughput, or resource consumption are not automatically immutable. They become contract-relevant when repository evidence shows that users, SLOs, tests, operators, or architecture constraints rely on them.

When relevant:

- establish a baseline measurement;
- compare like-for-like;
- account for noise;
- report uncertainty rather than fabricating precision.

## Contract drift warning

Do not "preserve" behavior solely because stale documentation says it exists. Resolve behavior from current evidence. Conversely, do not treat current accidental behavior as intentional public contract without checking consumers/tests/history when that distinction matters.
