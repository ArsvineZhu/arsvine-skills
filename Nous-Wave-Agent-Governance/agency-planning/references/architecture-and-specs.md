# Architecture and Spec Work

Architecture work is responsible for the future trajectory of the system, not merely the smallest local patch.

## Start from ownership and direction

Identify the product capability, semantic owner, data authority, lifecycle, consumers, and expected evolution. Let these determine topology and interfaces.

Existing modules, file layout, tests, documents, and naming are migration inputs. Preserve them when they remain the best structure; replace them when they distort ownership or continuing cost.

## Refactor at the owning level

Repeated cross-owner work, recurring adapters, duplicated decisions, and a third similar flow are signals to reconsider topology. Prefer one coherent owner over several local compensations.

## Spec purpose

A Spec records the decided contract needed by implementation. It should contain decisions, semantics, invariants, interfaces, failure policy, and unresolved items that truly block implementation.

Do not turn a Spec into a transcript of every option considered, every caveat discovered, or every method used to gain confidence.

## Real uncertainty

Mark an item unresolved only when implementation materially depends on its resolution. Keep non-blocking research questions in the appropriate research record or future-work note.

## Future use

Architect for the approved development direction and reasonably foreseeable extension. Hypothetical future consumers receive design weight only when a concrete trajectory or obligation supports them.
