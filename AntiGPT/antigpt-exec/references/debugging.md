# Bounded Debugging

Debugging exists to restore the authorized behavior with a reliable causal understanding.

## Find enough cause

Trace the failure until the repair target is clear and the proposed fix explains the observed behavior. Use the cheapest observation that can distinguish the live hypotheses.

A full causal history is unnecessary once additional detail cannot change the repair or validation strategy.

## Escalate structurally

Repeated fixes in different locations, recurring shared-state failures, or a workaround that must cross multiple semantic owners indicate a structural problem. Reconsider the architecture at that point instead of stacking another patch.

## Side findings

A side finding enters scope only under the admission rules in `trajectory.md`. Record other findings briefly and return to the current objective.

## Experimental instrumentation

Add temporary instrumentation when it can discriminate between live causes. Remove it after the cause is established unless it has continuing operational value.

## Validation

Use the smallest check that can falsify the proposed repair. Broaden verification when the changed path crosses integration surfaces whose failure would matter to the live claim.
