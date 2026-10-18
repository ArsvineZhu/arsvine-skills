# Architecture and implementable specifications

Use this guide when choosing responsibilities, data models, module boundaries, plugin mechanisms, external interfaces, or writing a specification for implementation.

## Recover required behavior before drawing components

Trace representative activities from the user's entrypoint to the resulting state or external effect. Identify the entities being represented, who creates and changes them, their lifetime, and who observes them. For existing systems, inspect the actual code and registration/discovery mechanism. For a clean-room design, derive the needed capabilities from the project direction and the requirements.

List a few meaningful workflows in prose as needed, for example:

- A CLI command changes configuration, the service applies it, and the persisted state survives restart.
- An incoming message is normalized, routed to its recipient, and acknowledged with the right failure semantics.
- A caller submits a query, the search engine finds symbols and semantic evidence, and the caller receives ranked results.

Use the workflow to identify boundaries. A class name, directory layout, architecture pattern, or repository test is evidence about the old implementation; it is not an architectural requirement by itself.

## Find the right owner without building a god object

**Repeated business rule.** Three entrypoints each decide whether a message is authorized. Give the policy one owner, have entrypoints call it, and keep the entrypoint-specific transport work at each boundary.

**Different rules that resemble each other.** Three adapters each map different external protocols to the domain message. They may share serialization helpers while retaining independent protocol responsibility. Putting every protocol rule in a universal dispatcher would join unrelated change reasons.

**Same entity represented several ways.** If services repeatedly convert the same domain message into incompatible internal shapes, design one canonical representation at the owner and make the consumers use it. Keep explicit transport conversion at genuine external boundaries. Avoid an additional canonical-object wrapper that simply hides unchanged duplicates.

**Shared library candidate.** Use a mature parser, message queue, cryptographic primitive, or storage driver where it meets the environment and integration needs. Preserve domain rules in the owning module. A new dependency should replace enough custom mechanics to make the resulting system simpler, rather than merely add a framework around simple behavior.

Ownership is visible in the flow of change: a domain-rule change should require editing its owner and updating real consumers when their contract changes. If every policy change edits five unrelated modules, ownership is split. If one universal manager knows all five modules' unrelated business rules, ownership is overcentralized.

## Choose interfaces that express actual responsibilities

An interface is useful when it represents a distinct external boundary, multiple concrete implementations, a stable contract between owners, or an approved extension direction. A plugin registry is useful when components really register dynamically and have an independent lifecycle. A private helper called once does not need a plugin system to look extensible.

Define operation names using domain vocabulary, specify inputs and outputs, and place state mutation behind the chosen owner. Make failure behavior explicit where callers must handle it: retryability, transaction boundary, rollback, conflict, not-found, and loss of connectivity as appropriate. Decide public compatibility from actual consumers and commitments. Internal APIs can be replaced together with their callers when the user authorizes architectural changes.

### Example: configuration owner

**Existing shape:** CLI edits one TOML representation, a server writes a database mirror, and a Web UI caches another mutable copy. Each path validates fields differently.

**Target:** choose the component with mutation authority; give it one canonical domain representation and validation rules. CLI and Web UI submit changes to that authority, read effective state from it, and use their own UI-friendly representations only at the presentation boundary. Persist the canonical state through an owned storage adapter.

**Avoided failure:** introducing `ConfigManager`, `ConfigAdapter`, `ConfigBridge`, and `ConfigCompat` while retaining every old validation and mutation path. These names increase indirection without changing ownership.

**Different legitimate choice:** an offline CLI may need to edit a configuration file while the service is stopped. Define how the service loads and validates that file. Do not require a running service merely to preserve a pure "single API" slogan.

## Write a Spec from the decisions

Record enough material for the implementing agent to create the selected system:

- Required capabilities and observable behavior, including meaningful negative paths.
- Domain entities, data fields, identities, invariants, and ownership of mutation.
- Interfaces, call flow, lifecycle, persistence, and event ordering where relevant.
- Failure and recovery behavior with actual consequences for the system.
- External compatibility, permissions, and operational constraints that are current requirements.
- Interfaces between planned components and any material decision still open.

Use schemas, pseudocode, example interactions, or sequence descriptions when they eliminate implementation ambiguity. Put the open decision next to the part it affects. Write alternatives and rationale in a separate design discussion when future contributors need the history; the implementation Spec should emphasize the selected contract.

## Return to the project goal

If a new finding changes the target design, revise the affected owners and interfaces together. If it only changes the syntax of one helper, finish that detail and return to the larger design. An architecture discussion ends with a coherent system shape and usable implementation guidance.
