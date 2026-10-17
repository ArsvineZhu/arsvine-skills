---
name: refactoring
description: Reconstruct or substantially simplify a code repository, including its owners, data shapes, duplicated logic, bloated tests, obsolete compatibility, scripts, and process. Use when replacing architecture, consolidating mechanisms, or reducing code and test complexity across a repository.
---

# Repository Refactoring

Apply the active AntiGPT Constitution and Plan or Exec Skill. This Skill owns the method for coherent repository-wide redesign, including the test suite and toolchain. Do the requested refactor; avoid turning it into a separate audit project.

## Start from the intended system

Read current product requirements, active repository authority, and representative paths through the existing system. Determine what the system must do, which capabilities already exist, the consumers that rely on them, and the approved development direction. Discover the responsibilities and boundaries that make the present implementation difficult to change.

Identify the desired replacement topology before accumulating local fixes. Focus on behavior owners, data representations, mutation authority, dependency direction, and actually shared infrastructure. Use mature dependencies for generic mechanics when appropriate.

## Make structural replacements directly

Replace duplicate owners, repeated translation shapes, unnecessary state mirrors, competing configuration paths, test-only interfaces, and speculative compatibility together with their callers. Reuse common project primitives rather than recreating a policy or helper in each module. An abstraction is useful when it removes duplicated reasoning or isolates a meaningful variation. Multi-file refactoring is ordinary work.

Look at directory shape and code placement. Group scripts by purpose when repeated prefixes indicate separate domains. Keep a clear owner for shared code, using `lib`, `shared`, or a specific domain module as appropriate. Move adjustable operational policy into the relevant established configuration, and leave implementation constants and protocol rules in code. Avoid proliferating tiny wrappers, generic registries, and incidental configuration frameworks.

When a mechanism is removed, also remove the compatibility shims, residual branches, unused commands, fixtures, obsolete documentation, and instructions that only served that mechanism. Leave a deliberate legacy path only for a real current consumer or migration obligation.

## Rebuild a bloated test suite from the target design

For substantial refactors, **do not begin by individually deciding whether each old test deserves to stay**. That defaults to preserving almost everything. Use this direction instead:

1. Reconstruct the new suite around required user-visible or public behavior, contracts between meaningful owners, complex state transitions, and failure modes with material consequences.
2. Read old suites as a source of useful scenarios, boundary inputs, and previously observed defects. Transfer the valuable assertions into the new structure; their former file, mock, fixture, and helper identity has no preservation status.
3. Replace and delete old groups together: tests for retired APIs, duplicated checks across layers, snapshots of implementation details, mock-only reproductions of already-covered behavior, redundant harnesses, and temporary debugging suites.
4. Keep tests for genuinely independent failures and contract differences. Combine repeated behavioral cases where one clear test surface covers them. Continue to use existing tests temporarily during migration when doing so helps catch regressions.

This is a replacement of the **testing architecture**, not a line-by-line deletion contest. Do not carry the remainder of the old suite forward simply because it still passes. Do not require an individual written defence of every deleted test. Protect the behavior and useful scenarios, not the historical suite's shape.

When repairing a single localized defect, prefer the existing meaningful verification and add a focused regression only when it captures an uncovered, relevant failure. Remove one-off diagnostic code after use unless it has continuing operational value.

## Respect an explicit reduction objective

When asked to materially reduce code volume or complexity, carry that goal through design and implementation. Compare the resulting structure with the starting point, including new production code, test code, scripts, configuration, and workflow machinery. Replace redundant mechanisms instead of rebuilding them under new names. If net growth contradicts the objective, redesign the costly replacement while the work is still underway; do not leave this discovery until the final report.

A smaller count is meaningful only when the required functionality, maintainability, and actual constraints remain satisfied. The user decides the priority of the reduction goal. Do not silently demote it to a mere optional metric.

## Keep the tooling proportional

Consolidate duplicated validation entrypoints. Remove extra gates, evidence ledgers, manual alignment commands, and obsolete scripts introduced by the old design. Preserve useful deterministic tools with an actual job. In particular, do not discard a prose-language scanner because it is a check: it directly catches repeated model-generated wording defects that prompting alone may miss.

Exact hashes and UUIDs stay in real storage, API, and Git operations that need them. Do not introduce periodic SHA alignment, lists of revision identifiers, or trace inventories for routine editing and testing. Use semantic names for the refactor's work areas and documents.

## Finish the replacement

Apply the new shape to all relevant consumers and delete superseded machinery. Update canonical instructions and documentation to describe the current system directly; do not leave negative-form memorials of removed mistakes. Exercise the relevant real usage paths and checks according to the changed behavior. Report the result, significant structural changes, and remaining actual gaps, then stop.
