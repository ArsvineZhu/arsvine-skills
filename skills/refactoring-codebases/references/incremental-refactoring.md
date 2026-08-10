# Incremental refactoring

## Purpose

Turn a broad structural goal into a sequence of reviewable passes that preserve working software and make regressions easy to localize.

## Campaign vs pass

### Refactoring campaign

The campaign holds the global view:

- target scope;
- structural problems;
- desired direction;
- behavior/compatibility constraints;
- risk hotspots;
- dependency order;
- deferred migration/feature work;
- pass sequence.

### Refactoring pass

A pass is one coherent improvement that can be independently understood and validated.

A good pass usually has one primary verb/object, such as:

- remove obsolete resolver;
- consolidate tax policy;
- isolate persistence from domain calculation;
- split orchestration from rendering;
- make state transition ownership explicit;
- break dependency cycle between A and B;
- move side effects behind existing service boundary.

Avoid vague passes such as "clean architecture" or "modernize src".

## Pass contract

Every pass should state:

- **Goal**;
- **Scope**;
- **Problem/evidence**;
- **Behavior/invariants preserved**;
- **Transformation**;
- **Risk**;
- **Focused validation**;
- **Deferred/non-goals**.

## Sequencing

A common safe order is:

1. establish missing behavior protection;
2. remove verified dead code and obsolete branches;
3. clarify names/ownership where ambiguity blocks reasoning;
4. consolidate duplicated domain knowledge;
5. simplify control/state flow;
6. repair dependency boundaries;
7. perform larger file/module moves after dependencies are understood;
8. remove transitional compatibility code introduced during intermediate steps.

This is a heuristic, not a mandatory recipe. Dependency structure may require another order.

## Preparatory refactoring

Sometimes the target change is hard because the code has no safe seam. Use a small preparatory pass to create one while preserving behavior.

Examples:

- introduce a parameter before moving ownership;
- centralize construction before replacing a dependency;
- add a stable internal interface before splitting a module;
- isolate side effects before simplifying policy;
- add characterization coverage before extraction.

The preparatory pass should have value as a stepping stone and remain behavior-preserving.

## Validation cadence

After each meaningful pass:

- run focused checks;
- inspect the diff;
- confirm no unexpected contract expansion;
- keep the build/test state no worse than baseline;
- record any newly discovered dependency or risk.

Do not stack several risky transformations before checking anything.

## Pass size

Prefer the smallest **coherent** unit, not the smallest line count.

A pass can span many files when one conceptual move requires coordinated imports/tests. Conversely, a 20-line change can be too broad if it changes unrelated concerns.

## Intermediate states

A multi-pass campaign may temporarily contain transitional code. Make it explicit:

- why it exists;
- which later pass removes it;
- whether both paths must remain behaviorally equivalent;
- what validation protects the transition.

Do not let temporary adapters/shims become permanent through forgetfulness.

## Long-running campaigns

For work spanning multiple sessions or modules, maintain a durable execution plan if the repository's workflow supports one. Record:

- target end-state;
- pass status;
- preserved contracts;
- validation results;
- discoveries/decisions;
- deferred work.

Do not create a repository artifact for a small one-session refactor unless it provides real coordination value.

## Convergence

After each pass, reassess remaining findings.

Stop when:

- major maintenance costs in scope are addressed;
- next changes are mostly stylistic or speculative;
- expected benefit is low relative to churn/risk;
- further improvement requires migration/behavior change;
- evidence is insufficient for safe continuation.

Refactoring is economic: the goal is cheaper, safer future change—not aesthetic completion.
