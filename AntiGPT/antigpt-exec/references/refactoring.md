# Refactoring and Structural Replacement

Refactoring is ordinary implementation when the current structure obstructs the authorized design.

## Follow semantic ownership

Move behavior to the component that owns its semantics. Remove adapters that exist only because ownership is split incorrectly.

Repeated cross-owner edits, repeated conversion code, recurring compatibility shims, and a third similar flow are strong signals to reconsider topology.

## Pre-production replacement

For pre-production internal APIs, schemas, protocol shapes, fixtures, and module paths:

1. identify real current producers and consumers;
2. migrate them together;
3. update canonical tests and documentation;
4. delete the superseded route in the same change.

Add compatibility machinery only for a documented current obligation.

## History

History informs risk and migration effort. It does not grant a structure permanent authority.

## Libraries and dependencies

Use mature libraries for generic mechanics when they reduce implementation and maintenance burden without surrendering product semantics. Dependency count is an input to judgment, not a standalone quality metric.

## Refactor scope

Include surrounding structural work when it directly produces a coherent owner or eliminates an immediate workaround. Leave unrelated aesthetic cleanup for another task.
