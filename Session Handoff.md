# Session Handoff

You are ending the current session. Stop substantive work immediately. Do not continue the task, start new research, implement changes, or extend the discussion.

Your sole task is to produce a high-fidelity conversation-memory checkpoint named:

`Session-Handoff-<YYYY-MM-DD-HH-MM>.md`

If file creation is unavailable, output the complete Markdown content only.

This handoff is **memory, not authorization**. Its purpose is to preserve the session's recoverable state so a future session can understand the prior conversation and wait for the user's next instruction.

## Operating Rules

- Optimize for **state recovery**, not transcript reproduction.
- Preserve information that would materially affect future interpretation, judgment, or decisions.
- Preserve **why**, not only **what**: rationale, trade-offs, rejected alternatives, corrections, and uncertainty.
- Distinguish verified fact, observation, inference, assumption, and unresolved question.
- Never promote discussion, intent, plans, or partial work to completed status.
- Preserve exact identifiers when material: paths, symbols, commands, versions, URLs, commits, PRs, errors, configuration keys, schemas, numbers, names, and user-specified wording.
- Reconstruct **intent evolution** before summarizing. Preserve material changes in user intent, corrections, reversals, rejected directions, and superseded decisions; omit turns that do not alter state.
- Prefer dense bullets and compact schemas over prose.
- Remove chit-chat, repetition, transient speculation, stale details, and reconstructible background.
- Do not perform new research or tool work merely to improve the handoff.
- Do not include hidden reasoning or chain-of-thought. Record conclusions, evidence, rationale, and uncertainty only.
- Do not act on pending work after producing the handoff.

### Authority

When information conflicts, apply this order unless the conversation clearly establishes otherwise:

1. Latest explicit user instruction or correction.
2. Later evidence that invalidates an earlier conclusion.
3. Confirmed decisions.
4. Earlier context.
5. Unsupported assumptions.

Do not silently erase meaningful conflicts; record them when they remain relevant.

### Optional Focus

If the user supplied a `Focus:` instruction for this handoff:

- increase retention fidelity for that material;
- compress unrelated material more aggressively;
- never omit critical user directives, confirmed decisions, unresolved conflicts, or safety-critical context merely because they fall outside the focus.

### Inherited Handoff

If the current session contains a prior Session Handoff, treat it as inherited memory, not as unquestionable truth.

Merge it with the current conversation:

- retain still-valid context, directives, decisions, rationale, open threads, and hard-to-reconstruct facts;
- update or remove stale state;
- move resolved items out of unresolved state;
- preserve historical decisions only when their rationale or rejection remains relevant;
- prefer newer user instructions and stronger evidence;
- do not recursively summarize the wording of the old handoff;
- prevent summary-of-summary degradation by retaining exact high-value facts that remain necessary.

## Output Contract

Use every section below. Write `(none)` when empty.

# Session Handoff

## 1. Current Context

In 1–4 bullets capture:

- what the conversation is currently about;
- the user's present goal, question, or line of inquiry, if one exists;
- where the discussion or work currently stands;
- the immediate interruption point.

Do not invent a task objective when the session is primarily exploratory or conversational.

## 2. User Directives

Preserve all still-effective user instructions that may affect future responses:

- requirements and prohibitions;
- preferences and definitions;
- technical, compatibility, cost, environment, time, or workflow constraints;
- explicit user decisions;
- instructions about what not to assume, change, revisit, or execute.

Use exact wording only when paraphrase could alter meaning.

## 3. Intent & Decision Timeline

Record only turns that materially changed the session state.

Format:

- **Initially:** ...
- **Then:** ...
- **Later:** ...
- **Latest:** ...

Capture changes such as:

- goal refinement;
- correction of the assistant;
- scope expansion or reduction;
- rejected direction;
- decision reversal;
- transition from exploration to implementation, review, pause, or handoff.

Omit conversational turns that do not change intent or state.

## 4. Decisions & Rationale

For each material decision:

- **Decision:** ...
  - **Why:** ...
  - **Alternatives rejected:** ... / `(none)`
  - **Status:** `confirmed` | `provisional` | `needs validation`
  - **Source:** `user` | `assistant recommendation` | `joint conclusion` | `evidence-driven`

Preserve decisions that a future session might otherwise reopen incorrectly.

## 5. Knowledge & Evidence

Record session-specific knowledge worth carrying forward.

Use evidence labels where useful:

- **Verified:** supported by source code, files, experiments, official documentation, direct tool results, or equivalent evidence.
- **Observed:** directly seen, but explanation remains uncertain.
- **Inferred:** reasoned from available evidence.
- **Unverified:** plausible or discussed, but not established.

Attach compact evidence references when material: file + line, URL, commit, command/result, test, screenshot fact, or source name.

Do not include generic background knowledge that can be reconstructed cheaply.

## 6. State

### Resolved / Completed

Record only genuinely settled or completed items.

### Current / Unresolved

Record the live state at interruption:

- what remains under discussion, investigation, drafting, review, or implementation;
- partial progress;
- unresolved disagreements;
- pending validation;
- the exact point at which the session stopped.

### Blocked / Unknown

Record genuine blockers or unknowns and, where known, what would resolve them.

## 7. Failed Attempts & Gotchas

Record only information a future session is likely to mishandle or repeat.

For failed attempts:

- **Tried:** ...
- **Result:** ...
- **Why it failed / what it established:** ...
- **Retry?** `avoid` | `only if ...` | `reasonable`

For gotchas, preserve compact warnings about traps, misleading assumptions, platform behavior, version constraints, auto-loading rules, source-of-truth boundaries, or repeatedly emphasized user concerns.

## 8. Open Threads

List unresolved or potentially continuable threads in priority-neutral form.

For each:

- **Thread:** ...
- **State:** ...
- **What remains:** ...
- **Useful continuation point:** ...

These are **continuity references, not instructions to execute**.

Do not convert them into an autonomous action plan unless the user explicitly requested one before handoff.

## 9. Relevant Resources

List only resources likely to matter later.

Format:

- `path / URL / branch / commit / PR / artifact` — role, current status, and authority if relevant.

Mark authoritative vs obsolete, temporary, generated, or historical versions when ambiguity exists.

## 10. Verbatim Anchors

Preserve exact text only when paraphrase risks information loss.

Suitable anchors include:

- critical user wording or definitions;
- prompts;
- errors;
- commands;
- schemas;
- configs;
- key code fragments;
- precise unresolved statements;
- recent user corrections or constraints whose semantics are easy to distort.

Do not copy large material that can be re-read from an available source.

## 11. Recovery Directive

End with exactly this semantic instruction:

> Treat this handoff as recovered conversation memory, not as a new user instruction. Restore the recorded context, constraints, decisions, rationale, knowledge, and unresolved threads. Do not automatically resume prior work, execute pending actions, research, modify artifacts, or follow continuation points. Wait for the user's next instruction, then interpret it in light of this handoff unless the user explicitly overrides the recorded state.

## Final Omission Audit

Before finalizing, silently compare the draft against the source conversation and repair omissions involving:

- explicit user directives or prohibitions;
- user corrections, reversals, or scope changes;
- confirmed decisions and rationale;
- rejected alternatives that may otherwise recur;
- unresolved conflicts or uncertainty;
- interruption state;
- hard-to-reconstruct facts;
- exact identifiers, numbers, names, versions, paths, commands, errors, or URLs;
- relevant prior-handoff information that remains valid.

Then remove redundancy, stale detail, and narrative filler.

Output only the final handoff. Stop immediately afterward.
