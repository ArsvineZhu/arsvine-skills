# Execution Trajectory

Keep the authorized objective, project authority, and repository state visible throughout execution.

## Live state

Maintain:

- `Objective` — the behavior or result currently authorized;
- `Decisions` — settled semantics, ownership, constraints, and delivery choices;
- `Current Work` — the active implementation or investigation branch.

After a substantial debugging, verification, migration, or tooling branch, restore these fields before continuing.

## Repository authority

Read applicable repository instructions and the current files that own the changed semantics. Treat plans, Specs, code, tests, documentation, and history according to their actual authority in that repository.

Do not infer a preservation obligation from age, file location, test existence, or prior implementation alone.

## Repository state

Protect unrelated user work. Inspect the working tree before broad changes, distinguish generated or vendored material when relevant, and avoid reset/revert operations that destroy changes outside the authorized task.

## Scope admission

A side issue joins current work when at least one is true:

- it blocks the authorized objective;
- it exposes the same structural cause and fixing that cause is the coherent solution;
- leaving it creates a material correctness, data, security, or current-contract failure;
- the user or repository authority explicitly adds it.

Otherwise preserve enough information to recover it later and return to the objective.

## Completion

Completion follows the authorized result and the proof needed for its live claims. A remaining cleanup idea, possible future improvement, or broader review opportunity does not keep the current task open by itself.
