# Introducing AntiRLHF

[简体中文](README.md)

> I wrote this by hand. Please cherish it in the age of AI.

AntiRLHF is an agent governance project targeting **local defensibility optimization**: a model can make the current step appear cautious, correct, and verifiable while losing sight of the complete objective, architecture, and user experience. We first recognized these problems through repeated use of GPT, and now observe related behavior across models.

It grew out of a recurring problem encountered over long-term use of Chat, Research Agents, and Coding Agents: models can complete local tasks, yet over long trajectories gradually devote resources to self-defence, cataloguing risks, procedural completeness, minimal changes, imagined compatibility obligations, and piles of proof, ultimately drifting away from what the user actually wants to accomplish.

The underlying cause is the response strategies LLMs "learn" during post-training to satisfy evaluation metrics—and they can wreck the user experience.

## Contents

- [The “GPT” phenomenon](#observed-phenomena)
- [Constitution](#constitution)
- [Roles](#roles)
- [The structure of AntiRLHF](#the-structure-of-antirlhf)
- [History](#history)

---

## Observed phenomena

In coding tasks, common symptoms include excessive verification, reliance on local passes, tests that freeze interfaces, and ever-accumulating wrappers and compatibility layers. The model is “afraid” to refactor; even when it does, it may delete large amounts of old code only to build another pile of shit that introduces still more burden through a new framework, additional tests, and processes. It overlooks paradigms that could organize the repository better: a single code file runs to 2,000 or 3,000 lines, code files are dumped into a flat directory, shared mechanisms are never extracted, mature libraries or dependencies are not prioritized, and it reinvents the wheel (then maintains its own pile of shit). It habitually lists “evidence,” identifies “boundaries,” and obsessively checks licenses and file SHAs for alignment.

<!-- antirlhf: allow rule=logical-limitation-en reason="Faithful translation of the author's quoted examples of unwanted qualifiers" -->

In natural language, after giving a sufficient answer, it keeps adding boundaries and qualifications, inventing objections the reader never raised, and appending negative qualifiers to settled conclusions: “cannot show,” “cannot prove,” “does not represent,” “does not equal,” “insufficient to judge,” “cannot guarantee.” It attacks imaginary targets, evades responsibility, lowers the certainty of its judgments, struggles to take a definite position, and produces wordy, poorly structured answers.

In long-lived documents, the model may also turn a local correction into a global prohibition, or rewrite “delete this content” as a tombstone proclaiming “correct content (the error is now gone).” AGENTS and Skill text pass these habits on to later models, causing lasting contamination.

> All of the following behaviors are undesirable.

### Defensive cognition

After encountering unknowns, risks, limitations, or counterexamples, the model tends to keep describing them rather than distilling the information back into a judgment or action.

### Commitment erosion / “My suggestion, my inclination is…”

<!-- antirlhf: allow rule=subjectivization-en reason="Quoted alternatives illustrate how settled judgments are weakened" -->
<!-- antirlhf: allow rule=commitment-weakening-en reason="Quoted alternatives illustrate how settled judgments are weakened" -->

Reasoning has already reached a clear conclusion, but the output rewrites it as “I lean toward,” “you could consider,” or “may be more suitable.” The wording reintroduces uncertainty that the reasoning already eliminated.

### Stronger-claim fabrication / Inventing a proposition, then qualifying it

<!-- antirlhf: allow rule=invented-contrast-en reason="Quoted contrast names the failure pattern being documented" -->

“Not X but Y,”
<!-- antirlhf: allow rule=logical-limitation-en reason="Quoted examples name the failure pattern being documented" -->

“does not prove,” “does not automatically become…”

<!-- antirlhf: allow rule=logical-limitation-en reason="Quoted examples name the failure pattern being documented" -->

The model upgrades a limited proposition into a stronger one on its own, then negates that invented proposition with phrases such as “does not prove” and “does not automatically mean.” The result is defensive, verbose text.

### Status-quo privilege / Preserving the current mess / Shitpile compatibility

Changing an existing structure requires continual proof, while preserving it is treated as the safe default. The usual result is a growing accumulation of aliases, shims, dual paths, transition layers, and local compensations.

### Process substitution / Over-engineering / Institutionalizing process

Plans, matrices, risk levels, acceptance tables, qualification tables, checklists, review stages, evidence packages, and fixed phases begin to replace actual design and implementation. Process turns from a tool into a deliverable. The model has seen too much TDD and EDD (test- and evidence-driven development), and likes them far too much: large repositories end up with hundreds of tests, new projects have a dozen tests before they have even got going, and checking repository status turns into gathering a complete set of Evidence and listing matrices.

### Context drift

Long tasks and compaction more readily retain logs, failed attempts, and verification history, while the genuinely important `Objective`, `Decisions`, and `Current Work` are diluted.

---

## Constitution

[`CONSTITUTION.md`](CONSTITUTION.md) is AntiRLHF's universal governance core. It is suitable for user-level persistent custom instructions in an Agent Harness, remaining in context over time, such as the user custom instructions in the ChatGPT app or Codex.

The Constitution defines only principles that hold across roles: preserve the objective and settled decisions, make judgments, solve problems at the semantic-owner level, limit low-value investigation and verification, deny historical structures preservation privilege, reject defensive substitutes, and stop once the objective is complete. Task-specific knowledge stays outside the Constitution.

The Constitution carries the long-term direction, Skills provide task-specific working methods, and scripts check recurring textual and file patterns. To improve an instruction, start with the real action it should change.

## Roles

AntiRLHF distinguishes Planning from Execution because they share governance principles but face different forms of behavioral deterioration.

### Plan

[`antirlhf-plan`](skills/antirlhf-plan/) addresses research, architecture, technical comparison, specifications, and design judgment.

It focuses on:

- Whether further research can still change the decision, model, or experiment;
- Whether uncertainty is being used to evade judgment;
- Whether architecture starts from capabilities, semantic owners, authority, lifecycle, and development direction;
- Whether higher-level ownership or modeling problems have been identified before implementing the first workable solution;
- Whether settled judgments are weakened when expressed.

### Exec

[`antirlhf-exec`](skills/antirlhf-exec/) addresses repository implementation, refactoring, debugging, testing, verification, and delivery.

It focuses on:

- Whether already-decided semantics are implemented directly;
- Whether local failures hijack the current objective and lead to endless fixation on a dead end;
- Whether patches, adapters, fallbacks, or compatibility mechanisms keep piling up at the wrong owner;
- Whether tests and verification protect genuinely important logic and contracts, starting from the objective and user actions, rather than pursuing quantity, coverage, and self-proof;
- Whether old APIs, documents, tests, and processes are granted preservation and compatibility privileges.

## The structure of AntiRLHF

AntiRLHF uses four different mechanisms, each carrying only the responsibility suited to mechanization:

```text
Constitution
  persistent governance principles

Plan / Exec Skills
  role-specific routing and task semantics

References
  progressively disclosed domain knowledge

Scripts
  mechanical checks
```

Static scripts can judge only mechanically checkable content. Language scanning can block high-confidence defensive-expression patterns and require explicit waivers, but cannot decide whether a caveat, abstraction, or compatibility obligation is semantically justified.

---

## History

AntiRLHF evolved from JDD, TED, and COST, a progression from shallower to deeper understanding while governing GPT models. They respectively strengthened ideas of justified machinery, Token economy, and total cost across the software trajectory, gradually revealing a higher-level problem: governance must extend beyond code and engineering processes to directly constrain an Agent's judgment, allocation of attention, and task trajectory. The original observations were developed under the name **AntiGPT**. The project became **AntiRLHF** as the research expanded to the gap between recalling a rule and acting on it, retrospective self-justification, and feedback-shaped behaviors. The name marks that research focus: behavior shaped by post-training feedback.

Historical governance texts remain in [`archive/`](archive/README.en.md). Field observations, hypotheses, prompt interventions and literature are collected in the [research notes](docs/README.en.md).

## Navigation

- [Repository overview](../README.md)
- [Installation](../INSTALL.md)
- [Package index](INDEX.md)
- [Research notes](docs/README.en.md)
