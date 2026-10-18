# Changing architecture at the right owner

Use this guide for a substantial module, data-model or internal API replacement. Work through an actual call path; do not infer ownership from a convenient class name.

## Trace the behavior before consolidating it

Choose a representative operation, then follow:

```text
external entrypoint -> input conversion -> domain decision -> state mutation
                    -> persistence/event -> consumer-visible result
```

Some paths have no external input, persistence, or events. Include only what the real system uses. Locate where a rule is decided and whether another module decides the same rule again. Record the concrete consumers affected by a replacement, including configuration, dynamic registration and plugin discovery when relevant.

A useful ownership design gives each responsibility an authoritative answer. Examples: one component decides whether a user has permission to mutate a record; a driver is responsible for one external protocol; storage is responsible for durable writes; a UI owns presentation state.

## Three similar-looking situations with different solutions

### Same business rule is duplicated

**Before:** HTTP, CLI and an internal scheduler each implement `canPublish(record, actor)` with slightly different error handling. Changing the policy requires editing three files; users receive inconsistent outcomes.

**Change:** Move `canPublish` and its policy data into the domain service that owns publishing. Have each entrypoint obtain an actor and normalized request, then call that service. Remove the three local policy implementations. Test the policy at its owner and the real entrypoints' wiring where it can fail independently.

**Result:** A new publishing rule changes one owner. HTTP still owns HTTP status mapping; CLI still owns terminal output; the scheduler still owns its job lifecycle.

### Different responsibilities share some syntax

**Before:** Three adapters parse different external protocols. They each contain a few similar `decodeHeader` lines.

**Bad consolidation:** Create a universal `ProtocolManager` that knows every external protocol, dispatches all messages and owns every adapter's error semantics.

**Better:** Keep protocol adapters independently responsible for their protocols. Extract a shared decoding primitive only if it is genuinely the same operation and its API is simpler than duplicating the code. A mature codec library may serve better than a custom shared module.

**Result:** A change in one protocol does not require editing the universal manager or disturbing unrelated integrations.

### Same entity circulates as multiple private models

**Before:** The router, storage service and CLI each keep different mutable copies of the same domain message. Every boundary converts fields and mirrors state; changes need multiple adapters.

**Change:** Choose a canonical domain message owned by the messaging service. Give storage and other consumers the owner's contract. Convert to protocol-specific shapes where data actually enters or leaves an external protocol. Delete internal mirrors and their private conversion utilities after consumers have migrated.

**Result:** One rule defines message identity and lifecycle. Transport shapes remain transport concerns. There is no new `CanonicalMessageBridge` that simply wraps three unchanged internal representations.

## A real integration boundary can justify an adapter

Suppose an old public client still sends protocol v1 while new clients use v2. A boundary adapter can translate the published v1 shape to the current internal domain model. Keep the contract and supported lifetime explicit. Internal components use the current model; public compatibility stays at the external edge. The existence of a real v1 client explains the adapter. The existence of twenty tests attached to an obsolete internal API does not.

## Module and file structure

Group files by the responsibilities that change together and the interfaces by which others use them. Large files sometimes contain several unrelated owners; split them along those responsibilities. Many tiny files can create unnecessary indirection when they exist only to introduce names or forward a call. Do not treat a numeric file-size limit or a mandatory directory depth as the architecture.

When several modules need the same generic mechanics, first inspect what the language standard library or a mature dependency already provides. Choose a dependency based on real API suitability, maintenance needs, licensing obligations that actually apply, and integration cost. Use it to *replace* homemade machinery. A simple pure helper may be cheaper than importing a framework.

### Example with directories

Before:

```text
src/
  cli-config.ts        # validates configuration independently
  api-config.ts        # repeats validation with slightly different defaults
  web-config.ts        # writes a separate cache
  convert-config.ts
  convert-config-v2.ts
  config-bridge.ts
```

Possible target when the three paths represent **one configuration owner**:

```text
src/config/
  model.ts             # canonical fields and validation
  service.ts           # effective state and mutation authority
  persistence.ts       # saved representation
src/cli/config.ts      # input/output for terminal users
src/api/config.ts      # HTTP boundary
src/web/config.ts      # presentation boundary
```

The exact number of files follows actual responsibilities. If the service also owns file persistence and has one small implementation, keep it in one file. Remove the converters and bridge when their contracts are absorbed by the owner. The target example is a shape to reason from, not a layout to copy into every project.

## Complete the replacement across consumers

1. Implement the chosen owner and contract.
2. Migrate each real caller and storage or transport boundary that depends on the changed shape.
3. Search the repository for the retired interface and test-only adapters. Remove obsolete code and update meaningful tests under the new owner.
4. Update current developer documentation, configuration and examples that reference the old structure.
5. Execute the real operation through the changed entrypoints and resolve any wiring failure.

During an authorized architectural reset, old internal shapes have no continuing claim to preservation merely because they were already built. Real data, public contracts, and unrelated user modifications retain their actual obligations.
