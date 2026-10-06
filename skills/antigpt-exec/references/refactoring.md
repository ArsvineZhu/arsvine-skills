# Structural Change

Refactoring is ordinary implementation when the current structure obstructs the authorized objective or target architecture.

## Target structure

Find the semantic owner of behavior, policy, state, mutation, lifecycle, and side effects. Repair ownership, topology, authority, or dependency direction when they cause the local problem.

Repeated cross-owner edits, duplicated policy, recurring conversions, a third similar flow, shared mutable state without one owner, and compatibility machinery around superseded internals are signals to reconsider structure.

Change as many files as a coherent structural correction requires. Diff size is not an optimization target.

## Real obligations

Preserve obligations that actually exist in the current task: product behavior, public or external contracts, persistent data, protocols, security properties, operational guarantees, and explicitly authorized compatibility.

Internal APIs, module paths, file layout, wrappers, fixtures, tests, and abstractions may change together when all relevant consumers are understood.

Performance, logs, ordering, concurrency, serialization, configuration, or filesystem shape become preservation obligations only when current users, automation, project authority, or the task relies on them.

## Replacement

When a new internal structure supersedes an old one:

1. identify real current producers and consumers;
2. migrate them coherently;
3. update canonical tests and documentation that describe the changed structure;
4. delete the superseded path and transitional machinery when their obligation ends.

A compatibility layer requires a current compatibility obligation. Development history alone does not create one.

## Deletion and reachability

Establish the forms of reachability the repository actually uses. Static references may be enough for ordinary code. Inspect registries, reflection, configuration, generated consumers, plugin discovery, serialization hooks, scripts, or documented external consumers when those mechanisms exist in the target system.

Do not perform a universal dynamic-consumer ritual in repositories that have no such mechanism.

## Dependencies and abstractions

Prefer the existing semantic owner, project primitive, standard/runtime capability, or mature dependency when it cleanly owns generic mechanics.

Introduce interfaces, ports, registries, wrappers, or dependency injection when they create a real ownership or substitution seam. Avoid layers whose only purpose is pattern conformity, test convenience, or preserving an obsolete shape.

## Verification

Verify the real obligations touched by the structural change. Keep an independent behavioral oracle when implementation and test structure change together and the affected contract makes parity material.

Use focused falsifiers during editing. Broaden only across the integration, state, concurrency, persistence, security, or public surfaces affected by the change.
