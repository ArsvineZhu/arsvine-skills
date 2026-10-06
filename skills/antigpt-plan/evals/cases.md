# Planning Governance Evals

Run each case in a fresh context twice: baseline without the governance package, then governed with the Planning Core and `antigpt-plan` available. Repeat selected cases under long-context pressure.

Evaluate semantic behavior, not keyword counts.

## Internal API choice

Prompt:
> A pre-production repository has two overlapping internal APIs. The old API has three in-repo callers. The new API expresses the complete semantics. There are no documented external consumers. Decide what to do.

Expected governed behavior:
- chooses the new API;
- migrates known callers and deletes the obsolete route;
- performs a bounded search for real external obligations;
- does not invent a deprecation period or compatibility layer.

Failure signals:
- `I lean toward`, `could consider`, or equivalent commitment erosion;
- hypothetical external consumers dominate the decision;
- research continues after it can no longer change the action.

## Research stop condition

Prompt:
> We selected an in-process queue for a research prototype. Current workload is tiny and queue replacement is localized behind one interface. Should we benchmark three more queue libraries before implementing the experiment?

Expected governed behavior:
- proceeds with the selected queue;
- explains why extra comparison has low decision value now;
- states what future observation would reopen the choice.

## Working model

Prompt:
> We need a model for estimating retrieval usefulness. Several second-order effects are unknown. Build a formula we can use for experiments this week.

Expected governed behavior:
- proposes a falsifiable working model;
- identifies only assumptions capable of changing the experiment;
- avoids replacing the model with a catalogue of caveats.

## Language commitment

Prompt:
> We have confirmed the old adapter has no callers and exists only for a superseded internal API. Give the architecture decision in two sentences.

Expected governed behavior:
- direct deletion decision;
- no self-positioning, invented objection, or defensive negation.

## Compaction pressure

Conversation setup:
1. Establish objective: consolidate ownership of durable session state.
2. Establish decision: Runtime owns lifecycle; persistence owns mechanics.
3. Introduce a test failure in timestamp serialization.
4. Spend several turns investigating the failure.
5. Provide a compressed summary dominated by logs and test details.
6. Ask: `Continue the architecture work.`

Expected governed behavior:
- reconstructs Objective / Decisions / Current Work;
- closes or scopes the timestamp branch;
- resumes ownership consolidation.

## Higher-level redesign pressure

Prompt:
> A feature request can be implemented by adding a fourth adapter beside three existing adapters. All four translate the same domain policy into local shapes. Decide the architecture before implementation.

Expected governed behavior:
- identifies duplicated ownership rather than treating the fourth adapter as the default shape;
- considers moving the policy to its semantic owner;
- chooses the owner-level design when it removes the repeated translation coherently;
- does not prefer the smallest diff merely because it is immediately implementable.

## Documentation architecture

Prompt:
> This small repository has a root README, one architecture document, one AGENTS file, and several historical design notes. Redesign the documentation structure.

Expected governed behavior:
- starts from audiences, canonical information ownership, authority, and navigation;
- archives superseded history outside the active authority path when it retains explanatory value;
- does not manufacture README/INDEX/AGENTS files in every directory for symmetry.
