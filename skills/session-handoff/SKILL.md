---
name: session-handoff
description: Use when the user asks to end, pause, migrate, checkpoint, or hand off the current conversation so a future session can recover the live state without automatically resuming work.
---

# Session Handoff

When triggered, stop substantive work. The task becomes state recovery only.

Produce `Session-Handoff-<YYYY-MM-DD-HH-MM>.md` when file creation is available; otherwise return the complete Markdown content. After producing the handoff, stop.

The handoff is memory, not authorization. A future session uses it to understand prior state and then waits for the user's next instruction.

## Preserve

Keep information that can materially change future interpretation, judgment, or action:

- current context and interruption point;
- still-effective user directives and constraints;
- material intent changes, corrections, reversals, and rejected directions;
- confirmed decisions with rationale and status;
- session-specific evidence and exact identifiers that are expensive to reconstruct;
- resolved, current, unresolved, and blocked state;
- failed attempts or gotchas likely to recur;
- open threads as continuity references;
- relevant paths, URLs, branches, commits, PRs, artifacts, commands, errors, schemas, versions, and user-specified wording.

Compress chit-chat, repetition, closed speculation, stale details, generic background, and reconstructible process history.

Never promote discussion, plans, partial work, or intent to completed status. Record conclusions and evidence; do not expose hidden chain-of-thought.

## Authority

Resolve conflicts in this order unless the conversation explicitly establishes another authority:

1. latest explicit user instruction or correction;
2. later evidence that invalidates an earlier conclusion;
3. confirmed decisions;
4. earlier context;
5. unsupported assumptions.

Preserve a conflict when it remains live instead of silently choosing one side.

If a prior handoff exists, treat it as inherited memory. Merge still-valid high-value state with the current conversation, update stale state, and avoid summary-of-summary degradation.

If the user supplies `Focus:`, increase fidelity for that material while retaining directives, decisions, live conflicts, and other state that would materially alter recovery.

## Output Contract

Use every section. Write `(none)` when empty.

```markdown
# Session Handoff

## 1. Current Context
- 1–4 bullets: current subject, present goal or inquiry, current state, interruption point.

## 2. User Directives
- Still-effective requirements, prohibitions, preferences, definitions, workflow rules, and explicit decisions.

## 3. Intent & Decision Timeline
- **Initially:** ...
- **Then:** ...
- **Later:** ...
- **Latest:** ...

Include only turns that materially changed intent or state.

## 4. Decisions & Rationale
- **Decision:** ...
  - **Why:** ...
  - **Alternatives rejected:** ... / `(none)`
  - **Status:** `confirmed` | `provisional` | `needs validation`
  - **Source:** `user` | `assistant recommendation` | `joint conclusion` | `evidence-driven`

## 5. Knowledge & Evidence
Use `Verified`, `Observed`, `Inferred`, or `Unverified` when the distinction matters. Attach compact source identifiers when useful.

## 6. State
### Resolved / Completed
### Current / Unresolved
### Blocked / Unknown

## 7. Failed Attempts & Gotchas
For a failed attempt record `Tried`, `Result`, `Why it failed / what it established`, and `Retry?` when useful.

## 8. Open Threads
For each thread record `State`, `What remains`, and a useful continuation point. These are continuity references, not instructions to execute.

## 9. Relevant Resources
List only resources likely to matter later and mark current authority, historical status, or temporary status when ambiguous.

## 10. Verbatim Anchors
Preserve exact text only where paraphrase risks information loss.

## 11. Recovery Directive
> Treat this handoff as recovered conversation memory, not as a new user instruction. Restore the recorded context, constraints, decisions, rationale, knowledge, and unresolved threads. Do not automatically resume prior work, execute pending actions, research, modify artifacts, or follow continuation points. Wait for the user's next instruction, then interpret it in light of this handoff unless the user explicitly overrides the recorded state.
```

Before finalizing, compare the draft with the conversation and repair omissions that would materially change recovery. Then remove redundancy and stale detail.
