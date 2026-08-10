---
name: refactoring-codebases
description: Use when planning, auditing, or executing systematic multi-file or repository-wide refactoring of an existing codebase while observable behavior should remain stable; especially for technical debt, dead code, duplicated logic, oversized modules, stale abstractions, tangled dependencies, unclear ownership, or architecture cleanup. Do not use as the primary workflow for feature work, bug fixes, framework/runtime migrations, major dependency upgrades, or trivial local edits.
---

# Refactoring Codebases

## Overview

Improve the internal structure of an existing codebase without silently changing the contract being preserved.

Treat repository-wide refactoring as a **campaign of small, evidence-backed passes**, not as a giant rewrite. Build both a behavioral model and a structural model before making broad changes. Optimize for lower change cost, clearer ownership, stronger cohesion, simpler dependencies, and safer future modification—not for aesthetic uniformity or arbitrary metrics.

## Core contracts

### Preserve observable behavior by default

Refactoring changes internal structure. It does not implicitly authorize product behavior changes, public API breaks, persistent-format changes, protocol changes, security-boundary changes, or migrations.

For every material pass, identify:

- **Behavior/invariants to preserve**;
- **Structural problem**;
- **Transformation**;
- **Parity evidence**.

Read [behavioral contracts](references/behavioral-contracts.md) before risky or cross-module edits.

### Separate refactoring from migration and feature work

Do not hide a rewrite, framework/runtime migration, major dependency upgrade, public-contract break, schema transition, or product behavior change inside "cleanup."

When the safe solution crosses that boundary, classify it explicitly and use [migration boundary](references/migration-boundary.md).

### Protect repository state

Before substantial editing:

- read applicable repository/local agent instructions;
- inspect working-tree state;
- identify unrelated user changes;
- identify generated, vendored, external, and protected areas;
- discover actual build/test/type/lint tooling;
- do not reset, revert, overwrite, or normalize unrelated work.

Read [preflight and scope](references/preflight-and-scope.md).

### Global diagnosis, incremental execution

A repository-wide request authorizes repository-wide **analysis**, not one repository-wide unverified rewrite.

Use two levels:

- **Refactoring campaign** — repository/subsystem-wide diagnosis, priorities, target direction, dependencies between passes;
- **Refactoring pass** — one coherent structural improvement with explicit behavior and verification.

Read [incremental refactoring](references/incremental-refactoring.md).

### Evidence before deletion

"No static callers" is not sufficient evidence that code is dead.

Check dynamic loading, registries, configuration, reflection, decorators, dependency injection, serialization hooks, generated consumers, scripts, plugin discovery, and external/public consumers when relevant.

Read [dead code and compatibility](references/dead-code-and-compatibility.md) before deleting uncertain code or compatibility paths.

### Metrics are signals, not verdicts

File length, function length, cyclomatic complexity, dependency counts, and duplicate-line detectors can identify places worth investigation. They do not prescribe a refactor by themselves.

Do not split a coherent 1,000-line algorithm merely because it is long. Do not extract a shared abstraction merely because two short fragments look similar.

Read [refactoring diagnostics](references/refactoring-diagnostics.md).

### Improve code health, not pattern density

Do not optimize for:

- one class/type per file;
- universal controller/service/repository layers;
- interfaces for every implementation;
- dependency injection everywhere;
- maximum directory symmetry;
- maximum abstraction reuse;
- arbitrary function/file size limits;
- design-pattern count.

Prefer the simplest structure that creates real improvement in understanding, ownership, change locality, verification, or extensibility.

## Modes

### Assessment mode

Use when the user asks to audit, analyze, prioritize, or plan a substantial refactor.

Produce the repository model, behavioral risks, refactoring map, prioritized campaign, and proposed passes. Do not modify production code unless explicitly asked.

### Execution mode

Use when the user asks to perform the refactor.

Do the same analysis necessary for safety, then execute passes incrementally. If the user already authorized execution, do not perform a long analysis and then stop merely to ask whether implementation may begin.

Infer mode from the request when clear. Ask only when ambiguity would materially change the work and no conservative default exists.

## Workflow

### Phase 0 — Bounded preflight

Before deep exploration, inspect only enough to establish safety and scope:

- working-tree/repository status;
- applicable `AGENTS.md` or equivalent instructions;
- root/workspace manifests;
- obvious package/application/service boundaries;
- generated/vendor/protected areas;
- existing validation entry points;
- obvious public/external surfaces;
- current change scope when the task follows recent work.

Use conservative defaults unless the user has explicitly authorized otherwise:

- behavior changes: **not authorized**;
- breaking public-contract changes: **not authorized**;
- major migration: **separate work**;
- major dependency upgrade: **separate work**;
- unrelated cleanup: **out of scope**.

Ask foreseeable blocking questions early and together. Do not spend a long time exploring and then block on a question that a short preflight could have exposed.

Read [preflight and scope](references/preflight-and-scope.md).

### Phase 1 — Establish the refactoring ledger and baseline

Record internally:

- task mode and scope;
- behavior/contracts that must remain stable;
- public/external surfaces;
- generated/protected areas;
- validation commands and available observability;
- pre-existing test/build/type/lint failures;
- migration/behavior-change exclusions;
- important uncertainties.

Do not assume the baseline is green. Distinguish **pre-existing failures** from regressions introduced by the refactor.

For risky areas with weak protection, establish the smallest useful characterization/parity evidence before structural transformation.

Read [behavioral contracts](references/behavioral-contracts.md) and [testing and parity](references/testing-and-parity.md).

### Phase 2 — Discover repository reality

Build a concrete model of the relevant system. Trace behavior rather than merely summarizing filenames.

Map, as applicable:

- entry points and request/control flows;
- business/domain ownership;
- transport/UI boundaries;
- validation boundaries;
- state ownership and state transitions;
- side effects and external integrations;
- persistence and transaction boundaries;
- concurrency/async boundaries;
- dependency direction and cycles;
- public and internal interfaces;
- configuration and generation flows;
- tests, fixtures, contracts, and operational checks;
- package/build/deployment boundaries that constrain structure.

For each important flow, identify where it starts, who owns the policy, where state mutates, where side effects occur, what crosses boundaries, and which tests protect it.

Read [repository discovery](references/repository-discovery.md).

### Phase 3 — Diagnose structural problems

Create a refactoring map based on evidence.

Evaluate relevant dimensions:

- responsibility and cohesion;
- coupling and dependency direction;
- abstraction quality;
- control-flow complexity;
- state and side-effect ownership;
- duplication of knowledge/policy;
- interface quality;
- dead/obsolete code;
- naming and conceptual consistency;
- physical locality and change affinity;
- testability and verification friction;
- architecture rules that repeatedly drift.

For each finding, state the maintenance cost or risk it causes. Do not classify personal style preference as structural debt.

Read [refactoring diagnostics](references/refactoring-diagnostics.md) and [architecture and dependencies](references/architecture-and-dependencies.md).

### Phase 4 — Prioritize the campaign and define passes

Prioritize by **value × risk × dependency order**, not discovery order.

Consider value:

- frequency of future change;
- cognitive load;
- duplicated policy/knowledge;
- defect risk;
- change locality;
- ability to unlock later simplification;
- impact on important developer workflows.

Consider risk:

- public/external exposure;
- test/parity quality;
- persistence and data integrity;
- concurrency;
- dynamic loading;
- security/trust boundaries;
- number of consumers;
- operational criticality;
- rollback difficulty.

Each proposed pass MUST identify:

- goal and scope;
- structural problem;
- behavior/invariants preserved;
- intended transformation;
- affected dependencies;
- risk level;
- focused validation;
- explicitly deferred work.

Use [incremental refactoring](references/incremental-refactoring.md).

### Phase 5 — Execute one pass at a time

For each pass:

1. Reconfirm the behavior/invariants to preserve.
2. Make the smallest coherent transformation.
3. Update affected imports, types, tests, generated-source inputs, references, and narrowly relevant documentation.
4. Run the narrowest meaningful validation.
5. Inspect the diff and architecture impact.
6. Resolve regressions before continuing.
7. Remove transitional leftovers that are no longer required.
8. Continue only when the pass is stable enough to build upon.

Keep the repository buildable/testable between meaningful passes whenever practical.

If a pass expands substantially beyond its stated purpose, stop expanding it and split the remaining work.

### Phase 6 — Review for structural quality and guardrails

After each material pass, review more than test results:

- Did ownership become clearer?
- Did coupling actually decrease, or only move?
- Did an abstraction gain a stable semantic purpose?
- Did the change introduce unnecessary indirection?
- Did tests become more implementation-coupled?
- Did comments become stale?
- Did compatibility shims become permanent by accident?
- Is there a recurring architecture rule that should be mechanically enforced?

Prefer tests, types, lint rules, structural checks, validation, or generation constraints over prose-only warnings when the rule is objective, stable, and worth enforcing.

Read [comments, docs, and guardrails](references/comments-docs-and-guardrails.md) and [review and verification](references/review-and-verification.md).

### Phase 7 — Final verification

Run the repository checks that actually apply and are available, such as:

- focused tests;
- relevant full test suites;
- type checking;
- linting/format checks;
- builds;
- schema/contract validation;
- generated-artifact checks;
- integration/E2E/smoke tests;
- performance or concurrency checks when those characteristics are contract-relevant.

Compare final results with the recorded baseline.

Inspect the final diff for:

- accidental behavior changes;
- stale references/imports/comments;
- unintended public-surface changes;
- transitional compatibility code that can now be removed;
- duplicate implementations left behind;
- misplaced responsibilities;
- speculative abstractions;
- unrelated churn.

Never claim a check passed unless it was actually executed successfully.

Read [review and verification](references/review-and-verification.md).

### Phase 8 — Report

Report concisely:

#### Refactoring map

Summarize the important structural problems found and their priority.

#### Passes completed

For each material pass, state:

- original problem;
- structural improvement;
- behavior/contracts preserved;
- validation performed.

#### Architecture impact

Describe meaningful changes to ownership, cohesion, dependency direction, state/side-effect boundaries, interfaces, testability, and physical organization.

#### Verification

List checks actually run and results, including baseline failures that remained unchanged.

#### Deferred work

List findings intentionally excluded because they are lower value, too risky, migrations, behavior changes, insufficiently evidenced, or unrelated.

#### Remaining risk

State any behavior, integration, performance, concurrency, compatibility, security, or external-consumer risk that could not be fully verified.

## Reference loading guide

| Situation | Read |
|---|---|
| Scope, working tree, user-change safety, early questions | [preflight and scope](references/preflight-and-scope.md) |
| Mapping an unfamiliar repository/subsystem | [repository discovery](references/repository-discovery.md) |
| Defining what "behavior preserved" means | [behavioral contracts](references/behavioral-contracts.md) |
| Smells, duplication, naming, complexity, file/module diagnosis | [refactoring diagnostics](references/refactoring-diagnostics.md) |
| Module boundaries, dependency direction, ownership, state | [architecture and dependencies](references/architecture-and-dependencies.md) |
| Campaign/pass decomposition and sequencing | [incremental refactoring](references/incremental-refactoring.md) |
| Characterization tests, parity, baseline failures, oracles | [testing and parity](references/testing-and-parity.md) |
| Dead code, compatibility paths, dynamic consumers | [dead code and compatibility](references/dead-code-and-compatibility.md) |
| Framework/runtime/API/schema/major dependency transition | [migration boundary](references/migration-boundary.md) |
| Comments, narrow docs updates, mechanical architecture rules | [comments, docs, and guardrails](references/comments-docs-and-guardrails.md) |
| Diff review, verification, completion claims, convergence | [review and verification](references/review-and-verification.md) |
| External standards or rationale for this Skill | [sources and standards](references/sources-and-standards.md) |

## Stop and handoff conditions

Stop the current pass and investigate or ask for help when:

- intended behavior cannot be established with sufficient confidence;
- an unexpected public/external contract is discovered;
- a breaking change becomes necessary;
- the work becomes a framework/runtime/schema/platform migration;
- dynamic/external reachability makes deletion unsafe;
- security/trust-boundary implications are unclear;
- unrelated user changes materially conflict with the pass;
- repeated verification failures lack an understood cause.

When a safe, conservative, reversible choice exists, prefer it and continue. Record non-blocking uncertainty for the final report instead of needlessly stopping long-running work.

## Convergence rule

Refactoring has no natural aesthetic endpoint. Stop the campaign when the next proposed cleanup has weak demonstrated maintenance value relative to its risk, review cost, and churn.

Do not continue merely because more stylistic consistency or abstraction is possible.

## Completion gate

Do not declare completion until the applicable conditions hold:

- preserved behavior/contracts are identified and supported by evidence;
- no accidental breaking change is known;
- important structural problems in scope were improved or explicitly deferred;
- responsibilities and ownership are clearer;
- dependency direction is no worse and preferably simpler;
- duplicated domain knowledge is reduced where appropriate;
- state/side-effect ownership is clearer where it was problematic;
- dead code was removed only with sufficient reachability evidence;
- no speculative architecture was introduced without demonstrated value;
- relevant tests/types/builds/docs/references are synchronized;
- verification results are reported truthfully against baseline;
- residual risks and migration/behavior-change follow-ups are explicit.

## Red flags

Correct course if you notice any of these:

- repository-wide edits before understanding behavior and ownership;
- one giant rewrite instead of reviewable passes;
- changing public contracts because internal code becomes cleaner;
- major dependency/framework upgrades hidden inside cleanup;
- deleting code from static-reference analysis alone;
- rewriting implementation and every test oracle together, then calling that parity;
- splitting files solely because of line count;
- extracting abstractions from coincidental duplication;
- creating interfaces/layers/DI without a concrete boundary benefit;
- moving code by technical shape while weakening domain ownership;
- resetting unrelated working-tree changes;
- weakening tests to make a refactor pass;
- treating pre-existing failing checks as refactor regressions without baseline comparison;
- treating equal return values as full parity when ordering, side effects, concurrency, persistence, or security semantics matter;
- adding prose warnings for stable objective rules that could reasonably be enforced mechanically;
- continuing low-value cleanup after the campaign has converged;
- claiming verification that was not executed.
