# Architecture and Specification

Architecture work owns the future trajectory of a system. Local implementation shape is an input, not the design authority.

## Start from semantics

Identify the capability, semantic owner, data or policy authority, lifecycle, consumers, failure semantics, and expected evolution that are relevant to the current decision. Let those facts determine topology and interfaces.

Existing modules, file layout, tests, documentation, naming, and internal APIs may be retained when they still express the target structure. Replace them when they distort ownership or continuing cost.

## Solve at the owning level

Before selecting the first workable local implementation, check whether the request exposes a higher-level ownership, model, topology, or abstraction defect.

Signals include:

- one policy implemented in several owners;
- repeated cross-owner edits;
- recurring adapters or conversions;
- duplicated state or mutation authority;
- a third similar local flow;
- compatibility machinery whose only purpose is preserving superseded internal structure;
- repeated fixes that move the symptom while preserving the cause.

Choose the coherent owner-level design when it materially improves the trajectory. Do not minimize edit count as an architectural objective.

## Interfaces

Create an interface, layer, registry, or extension mechanism when it owns a real semantic separation, authority separation, lifecycle, multiple current implementations, or a concrete development direction. A generic pattern name is not a reason to introduce one.

## Specification

A Spec records the decided contract needed by implementation. Include the selected owner, semantics, invariants, interfaces, lifecycle, failure policy, compatibility obligations, security constraints, and unresolved items that truly block implementation.

Keep investigation history, discarded alternatives, generic risk catalogues, and proof narration outside the implementation contract unless they are required to understand a live decision.

## Future direction

Design for the approved trajectory and reasonably foreseeable extension. Give hypothetical future consumers design weight only when a concrete direction or obligation supports them.
