# Refactoring diagnostics

## Purpose

Diagnose structural problems by maintenance cost, not by fashion. Code smells are prompts for investigation, not automatic refactoring commands.

## Responsibility and cohesion

Investigate:

- modules that own unrelated policies;
- functions/classes with multiple conceptual phases that change for different reasons;
- business logic mixed with transport/persistence/rendering/infrastructure;
- "utils/common/helpers" modules that accumulate unrelated behavior;
- logic located far from the component/domain that owns it;
- data structures manipulated by many distant modules with no clear owner.

Improvement target:

- one coherent reason to change per unit at the appropriate scale;
- clear domain/component ownership;
- related behavior and tests located near that owner.

Do not split merely to make units smaller.

## Coupling

Investigate:

- bidirectional dependencies;
- cycles;
- deep reach into another module's internals;
- global mutable state;
- cross-layer shortcuts;
- overly broad shared context objects;
- hidden dependencies through globals/service locators;
- modules that require many unrelated collaborators to test.

Ask whether coupling is essential to the domain or accidental to the current implementation.

## Abstraction quality

Smells:

- wrappers with no semantic boundary;
- interfaces with only one implementation and no substitution/testing/ownership benefit;
- generic abstractions parameterized by many flags;
- duplicated abstractions representing the same concept differently;
- abstractions whose callers constantly bypass them;
- stale layers preserved after their original reason disappeared;
- abstractions created from superficial syntax duplication.

Prefer an abstraction when it owns a stable concept, policy, boundary, or variation point.

## Duplication taxonomy

Before deduplicating, classify:

### Duplicated syntax

Similar lines, but no shared reason to change. Often safe to leave alone.

### Duplicated algorithm

Same computation repeated. May justify consolidation if semantics are truly shared.

### Duplicated domain rule / policy

Same business decision encoded in multiple places. High-value target because divergent copies create inconsistent behavior.

### Duplicated protocol/config knowledge

Same external contract or configuration semantics manually repeated. Prefer one canonical owner or generated source.

### Coincidental similarity

Looks the same now but belongs to different domains/evolution paths. Sharing may create harmful coupling.

## Control-flow complexity

Investigate:

- deep nesting;
- repeated condition ladders;
- boolean flags that multiplex distinct modes;
- implicit fallthrough;
- error handling interleaved with business steps;
- temporal coupling;
- callbacks/promises that obscure execution order;
- state machines encoded as scattered booleans;
- retry/cleanup logic duplicated across paths.

Prefer making phases and state transitions explicit when that reduces reasoning cost.

Do not extract every branch into a tiny helper if it makes the narrative harder to follow.

## State ownership

Smells:

- multiple modules mutate the same state directly;
- unclear source of truth;
- caches updated from unrelated layers;
- setters whose side effects are unknown;
- mutation coupled to read operations;
- hidden singleton state;
- state transitions requiring callers to remember ordering rules.

Improvement target: one obvious owner for mutation and explicit transition boundaries.

## Interface quality

Investigate:

- broad parameter bags unrelated to one responsibility;
- booleans changing function personality;
- inconsistent error models;
- functions both returning and mutating overlapping data;
- callers depending on hidden side effects;
- internal interfaces exposing implementation details;
- multiple equivalent interfaces for the same concept.

Do not break public contracts solely for internal elegance.

## Naming and concepts

Look for:

- one domain concept with multiple names;
- one name used for different concepts;
- names that reflect obsolete implementation;
- vague names such as `manager`, `processor`, `helper`, `data` without context;
- inconsistent terminology across related modules.

Rename when it materially improves the model. Avoid broad churn for stylistic consistency alone.

## Physical organization and change affinity

Place code by coherent ownership, responsibility, dependency direction, and change affinity—not by superficial technical shape.

Beware global folders that scatter one domain across:

- `controllers/`;
- `services/`;
- `repositories/`;
- `validators/`;
- `utils/`.

A feature/domain-oriented layout may improve locality, but it is not a universal requirement. Preserve an existing coherent convention unless there is a concrete benefit to change.

## Size metrics

Long files/functions/classes are signals to ask:

- Are there multiple responsibilities?
- Is the unit difficult to understand in one mental model?
- Do unrelated changes collide here?
- Are dependencies tangled?
- Is testing difficult?
- Would extraction create a stable semantic boundary?

If the answer is no, size alone is not sufficient justification.

## Testability

Poor testability may reveal:

- hidden dependencies;
- mixed side effects and policy;
- global state;
- overly broad units;
- unstable seams.

Do not redesign solely to enable mocking. Prefer stable behavioral boundaries and real dependencies where practical.

## Finding template

A useful diagnostic finding states:

- **Observation** — concrete evidence;
- **Cost/risk** — why it matters;
- **Likely cause** — structural mechanism;
- **Candidate improvement** — not yet a mandate;
- **Evidence needed** — what must be verified before editing.
