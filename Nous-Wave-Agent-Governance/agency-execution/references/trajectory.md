# Execution Trajectory

## Live state

Keep a compact state for long work:

- **Objective** — authorized end state.
- **Decisions** — settled semantics and architecture that govern implementation.
- **Current Work** — the specific construction now being changed.

Refresh this state after compaction, a long debugging branch, or a major change in direction.

## Scope admission

A newly discovered issue joins the current task when one of these is true:

- it blocks the authorized behavior;
- it creates a meaningful correctness, data-integrity, security, or operability risk in the changed path;
- it exposes the same structural cause and fixing both together lowers continuing cost;
- leaving it in place would force the new implementation to encode a workaround that immediately becomes debt.

Other findings receive a brief note and remain outside the current task.

## Whole-trajectory judgment

Optimize the repository trajectory, not diff size. A larger coherent refactor can be cheaper than a small patch that preserves repeated reasoning, duplicated owners, or permanent adapters.

## Context hygiene

Keep logs, test output, rejected hypotheses, and completed process steps out of the live reasoning state once they stop changing the next action.
