# Context and Goal Continuity

Long-running work must retain a compact semantic state:

- **Objective** — the outcome the user is trying to reach.
- **Decisions** — accepted choices that still govern the work.
- **Current Work** — the construction or question being handled now.

## Compaction priority

When summarizing or compressing context, preserve these three items before detailed command history, verification logs, abandoned hypotheses, or completed process steps.

## Drift detection

After a long investigation, compare `Current Work` with `Objective`.

If the current activity no longer contributes to the objective, either:

- close the side branch and resume the main work; or
- state the newly discovered blocker and why it changes the main trajectory.

## Decision retention

Keep accepted decisions compact and explicit. Remove superseded decisions from the live state rather than carrying both old and new versions indefinitely.

## Process history

Retain process detail only when it changes the next action, explains a still-live failure, or prevents repeating a costly mistake.
