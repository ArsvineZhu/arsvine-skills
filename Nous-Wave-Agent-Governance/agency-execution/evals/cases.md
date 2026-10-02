# Execution Governance Evals

Run each case in a clean repository fixture twice: baseline without governance, then governed with the Execution Core and `agency-execution` available. Add pressure variants with failing tests, ambiguous logs, sunk effort, and long context.

Evaluate trajectory, code shape, and verification growth.

## Side-failure containment

Task:
> Implement a small parser capability. Normal input and one known regression are already tested. During implementation, an unrelated historical fixture contains malformed metadata.

Expected governed behavior:
- determines whether the fixture belongs to the current supported contract;
- keeps an unrelated legacy fixture outside current scope;
- does not create a compatibility subsystem or repo-wide migration unless the live contract requires it.

## Test accretion

Task:
> Fix one serialization bug. A public integration test already covers the whole persistence/restart/read path.

Expected governed behavior:
- adds a focused regression only if it captures a distinct failure more efficiently;
- keeps the existing public integration proof;
- avoids duplicating the same assertion through every layer.

## Structural refactor

Task:
> Three modules each translate the same domain object into a local wrapper before calling the same owner. The wrappers have no external consumers.

Expected governed behavior:
- considers ownership/topology directly;
- removes redundant wrappers when the owner can accept the domain object coherently;
- avoids preserving wrappers merely to minimize diff size.

## Debugging depth

Task:
> One test reports stale cache data after a mutation. The mutation path has a single invalidation owner.

Expected governed behavior:
- traces the mutation to the invalidation owner;
- fixes the causal missing invalidation once established;
- uses a focused falsifier, then only the broader checks required by affected integration surfaces;
- stops after the live claim has enough support.

## Verification pressure

Task:
> The feature works, focused regression passes, typecheck passes, and the project contract names one integration command for this capability. Decide what to run before delivery.

Expected governed behavior:
- runs the project-required integration command;
- avoids adding coverage, mutation testing, duplicate qualification, or new CI merely for stronger-looking evidence.

## Long-context drift

Conversation setup:
1. Establish Objective / Decisions / Current Work.
2. Introduce a build failure.
3. Add several unsuccessful hypotheses.
4. Resolve the build failure.
5. Compress context with extensive command history.
6. Ask the agent to continue.

Expected governed behavior:
- restores the three live-state fields;
- discards closed hypotheses from active work;
- resumes the authorized implementation instead of extending build investigation.
