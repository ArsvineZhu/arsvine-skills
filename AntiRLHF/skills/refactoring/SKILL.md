---
name: refactoring
description: Rebuild existing code architecture, ownership, data paths, tests, and supporting tooling. Use for substantial refactoring, code reduction, consolidation, or replacement of an obsolete design.
---

# Repository refactoring

Follow the active AntiRLHF Constitution and the active planning or execution instructions. Start from the behavior and architecture the user wants **after** the change. The current files are material to inspect, reuse, replace, or remove.

## Choose the scale from the requested result

A localized defect with a sound owner needs a focused change. Repeated patches across modules, duplicate sources of truth, a deprecated internal interface, or an approved architecture reset call for a coherent structural replacement. Follow the boundary of the responsible system rather than treating the size of the existing diff as a constraint.

For architectural work, read `references/structure-and-ownership.md` before changing owners. For test-suite replacement or explicit total-code reduction, read `references/testing-and-reduction.md` before reorganizing tests and tooling. These are operational guides with worked cases, not additional approval gates.

## Build the target structure

1. Trace representative real usage paths: entrypoint, data producers, domain decisions, state mutations, and consumers. Include CLI, API, adapters, registration and discovery paths where they participate in the requested capability.
2. Describe who owns each business rule, state transition, and external side effect. A component owns a responsibility when callers can rely on it without reimplementing or interpreting that responsibility elsewhere.
3. Choose the target data and interface shape. Distinguish *the same business rule repeated in several places* from *different responsibilities that happen to use similar code*. Combine the former at the actual owner; keep the latter independent. Extract common mechanics only where shared ownership pays for itself.
4. Migrate affected producers and consumers to the selected shape. Update configuration and maintained documents where their meanings change. Remove retired wrappers, duplicate paths, interfaces, tests, and tooling with the structures they supported.
5. Exercise the changed capability through the path that actually uses it. Repair implementation defects in their new owner.

Use existing libraries when they own a well-understood generic concern and fit the environment. Keep domain semantics in the project. Resist both extremes: scattering the same rule across modules and putting unrelated policy into a universal manager.

## Rebuild the tests that belong to the result

During substantial refactoring, derive the replacement checks from the behavior the new system must expose. Read existing tests for meaningful boundary inputs, regressions and independent failures; transfer those scenarios to the new owner or contract. Delete groups tied to retired internals along with their dedicated mocks, fixtures and adapters. Keep distinct tests where they protect independently failing behavior.

During a local fix, preserve the useful suite and modify only the checks affected by the change. When a test fails because it encodes an obsolete internal shape, examine the actual contract before changing production code to appease it.

## Keep the replacement coherent through completion

An explicit simplification goal covers production files, test files, scripts, configuration and supporting workflows. If a new framework, generic interface, or test harness restores the removed complexity, simplify the new structure while the refactor is still under way. Judge the result by required capability and maintenance structure, using size or performance targets when the user specified them.

Finish with working entrypoints, current documentation, relevant checks and removal of obsolete structures. Deliver the resulting code and behavior.
