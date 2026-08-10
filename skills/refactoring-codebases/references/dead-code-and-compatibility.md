# Dead code and compatibility

## Purpose

Remove obsolete code confidently without deleting behavior that is reached dynamically or by external consumers.

## Dead-code evidence

Static "find references" is one signal, not final proof.

Check relevant reachability channels:

- direct imports/calls;
- exports/public package surface;
- dynamic imports/module loading;
- reflection;
- registries/service locators;
- decorators/annotations discovered at runtime;
- dependency injection bindings;
- plugin/provider discovery;
- configuration names/strings;
- route/event/topic registration;
- serialization/deserialization hooks;
- CLI command registration;
- scripts/build/release tooling;
- code generation/templates;
- tests/fixtures/examples used as executable consumers;
- external consumers of a published library/service;
- backwards-compatibility contracts.

## Confidence classes

### High confidence dead

Evidence indicates no reachable internal or external path, no public contract, and no dynamic registration.

Delete and validate.

### Likely dead but uncertain

Static references absent, but dynamic/public/plugin behavior is plausible.

Investigate before deletion. Prefer deprecation/instrumentation when external reachability cannot be established safely.

### Intentionally dormant

Fallback, feature-flagged, compatibility, disaster-recovery, platform-specific, or staged code may be rarely executed but still required.

Document/verify its activation condition rather than deleting from usage frequency alone.

## Compatibility shims

A shim should have a clear reason and lifecycle.

Ask:

- Who still needs it?
- What old contract does it preserve?
- Can usage be measured or searched?
- What condition permits removal?
- Is the compatibility window still active?

Do not keep a shim indefinitely because "someone might use it."

Do not remove it merely because the repository itself no longer does.

## Feature flags and old paths

Before deleting a flagged branch:

- confirm rollout state;
- check whether the flag can still change at runtime/config;
- verify operational fallback requirements;
- check tests/experiments/deployment config;
- remove the flag definition/config/documentation together when appropriate.

## Public exports

For libraries/SDKs, an exported symbol may have zero repository-internal callers and still be heavily used externally.

Treat published surface as a contract unless there is evidence or explicit authorization to break/deprecate it.

## Dynamic-name hazards

Search not only symbol names but stable strings:

- registry keys;
- route names;
- event names;
- config values;
- plugin identifiers;
- serialized type tags;
- command names.

Renaming can be breaking even when types compile.

## Removal validation

After deletion:

- build/typecheck;
- run focused tests;
- search for stale references/config/docs;
- verify generated artifacts if relevant;
- run startup/plugin discovery/smoke paths where static analysis is insufficient.

## Archive vs delete

Source control already preserves history. Do not keep dead implementation files commented out or move them into `legacy/` merely for nostalgia.

Archive only when the repository has a real operational/legal/reference reason distinct from version-control history.
