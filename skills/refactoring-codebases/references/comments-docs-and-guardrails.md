# Comments, documentation, and guardrails

## Purpose

Keep rationale and operational constraints accurate after refactoring, and convert stable objective rules into mechanical safeguards when worthwhile.

## Comments

Preserve **rationale**, not stale text.

Useful comments explain information that code cannot communicate clearly, such as:

- why a non-obvious design exists;
- compatibility constraints;
- fragile external assumptions;
- concurrency/lifecycle invariants;
- safety/security boundaries;
- intentionally unusual code;
- temporary workarounds and removal conditions;
- algorithmic reasoning that would otherwise be difficult to reconstruct.

Avoid comments that only narrate obvious code.

When a refactor makes a comment obsolete:

- update it;
- relocate it to the new owner;
- remove it if the code now expresses the idea sufficiently.

Do not mechanically preserve every historical comment.

## TODO/HACK/FIXME

Re-evaluate nearby markers during refactoring:

- resolved by this pass → remove/update;
- still valid → preserve with current context;
- reveals a larger unrelated issue → defer explicitly rather than expanding scope;
- encodes a dangerous recurring invariant → consider a mechanical guardrail.

## Documentation updates

A refactoring pass should update narrowly related documentation when structural facts change, such as:

- module/package locations;
- developer navigation;
- build/test commands;
- generated-file ownership;
- extension points;
- internal architecture boundaries that docs intentionally describe;
- AGENTS instructions affected by moved paths/commands/local rules.

Do not turn a code refactor into a repository-wide documentation rewrite. Hand off broad documentation-governance problems separately.

## Agent instructions

When a structural rule affects future coding agents, keep `AGENTS.md` guidance concise and operational:

- exact scope;
- MUST/MUST NOT rule when necessary;
- canonical command/validation;
- link to detailed rationale if useful.

Do not paste architecture essays into every local agent file.

## Prefer enforcement over remembrance

When an objective, stable, recurring rule can be enforced at reasonable cost, consider:

- type constraints;
- tests;
- lint rules;
- import/dependency checks;
- build-system visibility;
- schema validation;
- generated-code checks;
- CI assertions.

Examples:

- forbidden dependency direction;
- generated files must not be edited directly;
- schema/type naming invariants;
- public API compatibility checks;
- required cleanup/registration patterns when statically detectable.

Mechanical enforcement is especially valuable when the same violation repeatedly returns.

## Guardrail decision test

Add a guardrail when most are true:

- rule is objective and machine-detectable;
- false positives can be kept low;
- violation has real maintenance/reliability cost;
- recurrence is plausible;
- the rule is expected to remain stable;
- existing tooling can enforce it simply.

Avoid a custom linter for a subjective one-off preference.

## Guardrails and exceptions

If a legitimate exception exists:

- make it explicit and narrow;
- prefer an auditable suppression mechanism;
- document why it exists;
- avoid disabling the rule globally.

## Generated architecture artifacts

Dependency graphs, API lists, or metrics may help diagnostics, but generated artifacts should not become hand-maintained duplicates of source truth.
