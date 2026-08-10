# Architecture and dependencies

## Purpose

Improve module boundaries and dependency structure without replacing the repository's architecture with a generic pattern catalog.

## Boundary quality

A useful unit has a clear answer to:

- What does it own?
- What does it expose?
- What does it depend on?
- Who is allowed to depend on it?
- Where does state live?
- Where do side effects cross the boundary?
- How is it tested/validated?

A boundary is weak when consumers need internal knowledge to use it correctly.

## Dependency direction

Prefer dependencies that follow ownership and stability:

- domain policy should not depend unnecessarily on UI/transport details;
- core behavior should not directly know deployment plumbing unless the domain requires it;
- infrastructure should enter through explicit seams when substitution or ownership warrants it;
- cross-cutting concerns should have defined entry points rather than ad hoc imports everywhere.

Do not force classic layered architecture when a different architecture is already coherent.

## Cycles

For a dependency cycle, identify why each edge exists.

Common causes:

- misplaced shared types;
- callbacks reaching back into higher layers;
- overly broad modules;
- initialization coupling;
- shared mutable state;
- convenience imports.

Break the weakest/least essential edge, not necessarily the easiest line to move.

Do not create a meaningless `common` package as a dumping ground merely to remove cycles.

## Dependency inversion

Introduce an interface/port only when it creates a real boundary benefit, such as:

- isolating infrastructure from policy;
- supporting multiple implementations that actually exist or are being migrated;
- enabling deterministic tests for an unavoidable external dependency;
- defining a stable package/service contract;
- making ownership/dependency direction explicit.

Do not add an interface simply because "clean architecture" suggests one.

## State ownership

Prefer:

- one authoritative owner for mutable state;
- explicit mutation APIs;
- clear transactional boundaries;
- lifecycle and cleanup rules near the resource owner;
- immutable data across boundaries when practical and beneficial.

Beware refactors that move methods but leave state ownership ambiguous.

## Side effects

Separate pure/domain decisions from irreversible effects when doing so:

- clarifies behavior;
- enables reliable parity tests;
- reduces retry/transaction bugs;
- improves ownership.

Do not scatter side-effect wrappers into excessive layers. One clear boundary is usually better than several ceremonial ones.

## Cross-cutting concerns

For logging, telemetry, auth, feature flags, caching, transactions, or configuration:

- identify the legitimate cross-cutting boundary;
- avoid arbitrary access from every layer;
- preserve operational semantics;
- consider mechanical architecture checks for stable dependency rules.

## Change affinity

Files that repeatedly change together because they implement one coherent concept should normally be close in ownership and navigation.

Do not confuse change affinity with accidental co-change caused by a bad centralized file; first understand why they change together.

## Public vs internal architecture

Internal boundaries may be redesigned aggressively when behavior and all consumers are understood.

Published package/service/plugin boundaries require stronger compatibility discipline. If consumers need coordinated changes, read `migration-boundary.md`.

## Architecture anti-patterns during refactoring

Avoid introducing:

- service/repository/controller layers by default;
- interface-per-class;
- factories with no variation;
- wrappers around every dependency;
- dependency injection containers for simple local construction;
- micro-packages that increase navigation/coupling cost;
- "shared" packages that erase ownership;
- abstraction layers that exist only to make diagrams symmetrical.

## Mechanical guardrails

When dependency direction is objective, stable, and repeatedly violated, consider enforcing it with:

- import-boundary lint rules;
- package visibility rules;
- architecture tests;
- build-system dependency constraints;
- generated dependency graphs checked in CI.

Use guardrails proportionately. Do not build a custom architecture framework for a one-off issue.
