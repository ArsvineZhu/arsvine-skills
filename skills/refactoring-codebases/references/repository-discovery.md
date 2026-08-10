# Repository discovery

## Purpose

Build a behavior- and ownership-oriented model of the relevant codebase before designing structural changes.

A useful model explains how the system works and where responsibility lives. A directory listing alone is not a system model.

## Discovery sequence

### 1. Repository and build boundaries

Identify, where applicable:

- workspaces/monorepo packages;
- applications/services/libraries/SDKs/plugins;
- package/build manifests;
- code generation;
- test projects;
- deployment/runtime units;
- platform-specific variants;
- shared infrastructure/tooling.

Note which boundaries are independently built, published, deployed, or versioned.

### 2. Entry points

Find real entry points, such as:

- application bootstraps;
- CLI commands;
- API routes/controllers;
- event/message consumers;
- scheduled/background jobs;
- plugin registrations;
- library exports;
- UI feature roots;
- extension hooks.

Do not assume conventional filenames are authoritative.

### 3. Trace representative flows

For each important flow, trace:

1. entry;
2. validation/parsing;
3. domain/business policy;
4. state reads/writes;
5. persistence;
6. side effects/external calls;
7. result/error mapping;
8. tests/contracts that observe the flow.

Ask:

- Which module owns the policy?
- Which modules merely transport data?
- Where can state change?
- Where do irreversible side effects occur?
- Which boundaries are stable/public?
- Which dependencies are accidental?

### 4. State and lifecycle

Identify:

- sources of mutable state;
- ownership of caches/stores/sessions;
- initialization and teardown;
- lifecycle callbacks;
- transaction boundaries;
- retry/cancellation behavior;
- concurrency limits;
- global/singleton state;
- hidden temporal coupling.

A refactor that moves code without understanding lifecycle can preserve outputs while breaking runtime behavior.

### 5. Dependency structure

Inspect actual dependency direction:

- package imports;
- cross-layer calls;
- cycles;
- dependency inversion points;
- direct access to another module's internals;
- shared utility hubs;
- cross-cutting providers;
- runtime/dynamic dependencies not visible in static imports.

Distinguish architectural dependency from mere file proximity.

### 6. Public and external surfaces

Inventory surfaces that may have external consumers:

- package exports;
- public classes/functions/types;
- API/CLI contracts;
- plugin interfaces;
- schema/protocol/data formats;
- configuration/env keys;
- persisted records;
- generated client contracts;
- event/topic names;
- filesystem conventions;
- scripts used by automation or operators.

Do not infer "internal" from lack of local callers if the artifact is published or externally consumed.

### 7. Tests and executable evidence

Map relevant:

- unit tests;
- integration/E2E/contract tests;
- fixtures/golden files;
- snapshots;
- schemas;
- type-level constraints;
- examples/smoke tests;
- performance/concurrency tests;
- CI checks;
- structural architecture tests.

Record what behavior each actually protects.

### 8. Historical evidence, selectively

Use Git history, ADRs, issues, comments, or old docs when current code reveals a suspicious constraint whose rationale matters.

History is useful for **why** and chronology. It is weaker than current executable evidence for **what currently happens**.

Do not perform broad archaeology unless risk or contradictory evidence justifies it.

## Evidence hierarchy

When determining current behavior, prefer:

1. reproducible executable behavior;
2. focused tests and machine-readable contracts;
3. current schemas/config/manifests/generated interfaces;
4. implementation code;
5. CI/build/deployment automation;
6. maintained documentation;
7. historical records for intent and rationale.

No single source is infallible. Investigate contradictions.

## Discovery output

A useful discovery model should make it possible to state:

- the important flows;
- ownership boundaries;
- public/external surfaces;
- risky state/side-effect boundaries;
- dependency direction;
- verification surfaces;
- where changes are likely to ripple;
- where structural pain is actually coming from.

If the result is primarily a list of filenames, discovery is incomplete.
