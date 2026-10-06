# Token-Economic Development (TED)

Preserve required semantics. Minimize total engineering token cost.

## 1. Governing Rule

Engineering decisions shall optimize the total Token Cost of implementation, verification, review, maintenance, and later change, subject to correctness, required semantics, security, and maintainability.

**Token Cost** includes model context, reasoning, generated output, repeated reading, repeated verification output, rework, and future Agent effort caused by the current design.

Immediate brevity is not the objective. Spending more tokens now is justified when it reliably removes greater repeated token expenditure later.

Scale, abstraction, generality, dependency count, file count, package count, process count, and absence of an immediate consumer shall not be treated as evidence of excess.

## 2. Justified Expansion

Engineering may expand when the expected reduction in repeated work, ambiguity, error, or maintenance burden justifies the added implementation and reasoning cost.

A broad abstraction may be preferable to many local mechanisms when it gives a broad responsibility one coherent owner, removes repeated reasoning, isolates volatile mechanics, preserves an established boundary, or materially simplifies approved future development.

The smallest implementation shall not be preferred merely because it is small.

An established development direction may justify structure before its first consumer exists. Hypothetical usefulness alone does not justify substantial machinery.

No separate justification document, matrix, gate, review stage, or approval ceremony is required unless that mechanism has its own Token-Economic value.

## 3. Reuse and Automation

Generic mechanics shall preferentially use an existing semantic owner, project primitive, Standard Library/runtime/OS capability, protocol implementation, or suitable mature library when doing so reduces total Token Cost without surrendering required semantics or authority.

Product semantic ownership does not require reimplementation of generic infrastructure.

Dependency count is not a quality metric.

Low-cost mature tooling that removes recurring manual work, repeated reasoning, formatting drift, avoidable defects, noisy verification, or command repetition should be adopted proactively when its recurring savings exceed its setup and maintenance cost.

Do not preserve manual work merely to avoid adding tooling.

## 4. Architecture and Continuity

Approved abstractions and semantic boundaries shall be evaluated across the approved development direction, not only the current task.

Lack of an immediate consumer is not a deletion reason.

A bounded implementation step shall not flatten, duplicate, bypass, or localize an established abstraction merely because the local task could be completed with fewer files or less indirection.

Existing code and architecture have no automatic preservation privilege. They may be rewritten when correctness, semantics, approved evolution, maintenance burden, or Token Cost justifies the change.

Development history alone creates no compatibility obligation. Compatibility mechanisms require an actual current obligation.

Historical failures may justify permanent automation or guards when the underlying risk remains relevant and the expected recurring savings justify the maintenance cost. History shall be evidence, not automatic authority.

## 5. Process Discipline

Development process is engineering machinery and shall be evaluated by the same Token-Economic standard as code.

Plans, ADRs, gates, matrices, qualification systems, mandatory TDD stages, review stages, evidence packages, checklists, stabilization phases, and closure procedures shall exist only when they reduce more recurring uncertainty, coordination cost, risk, or rework than they create.

Organizational convention, professional appearance, and procedural completeness are not independent reasons for process.

A single incident shall not automatically become a permanent ceremony.

## 6. Failure and Testing

Failure handling shall match the guarantees and risks that the system is required to address.

Restart, retry, reset, operator intervention, fail-loudly behavior, or stronger recovery may each be correct. Additional recovery layers shall not be created merely because another failure can be imagined.

Tests shall protect meaningful contracts, observed risks, or informative uncertainty.

TDD is optional. A failing test shall not be created merely to demonstrate that unwritten functionality is absent.

Production architecture shall not be created solely for test convenience.

## 7. Verification Economy

Verification shall minimize time, compute, context pollution, and repeated Agent reading while preserving required confidence.

During iteration, run the narrowest check capable of falsifying the current change. Do not rerun the full verification suite after every small edit unless the relevant failure cannot be evaluated at a narrower boundary.

When broad verification exposes a scoped failure, inspect related failures together, correct them at the narrowest useful scope, and return to comprehensive verification at a meaningful integration or acceptance boundary.

Repeatedly slow, noisy, redundant, or poorly scoped verification is an engineering problem.

Verification tooling is ordinary engineering. It may be refactored, extended, or newly created when the expected recurring savings in execution time, compute cost, Token Cost, diagnostic precision, or failure localization exceed its maintenance burden.

Existing tool capabilities shall be used when sufficient. Custom tooling is permitted when they are insufficient and the expected net benefit is positive.

Verification output shall favor concise, deterministic, non-interactive diagnostics. Remove unnecessary ANSI color, progress animation, watch-mode noise, repeated stack traces, duplicate failures, and redundant success output where practical. Present useful diagnostics first and retain complete logs separately when needed.

## 8. Execution Authority

Executors shall implement decided semantics, ownership, boundaries, provider choices, compatibility obligations, security constraints, and failure policies while retaining ordinary implementation judgment.

A material unresolved decision shall be escalated. It shall not be hidden behind a new abstraction, configuration option, registry, fallback, policy layer, or generic framework.

Approved capabilities shall be implemented completely. Token economy shall not be used to justify incomplete behavior or weakened requirements.

## 9. Writing Economy

Documentation and user-facing text shall communicate the needed meaning with the minimum wording consistent with clarity and accuracy.

The writer shall not invent a possible misunderstanding and then deny it as the default structure of explanation.

Negative contrast, including patterns such as “not X, but Y” or “this does not mean”, shall be used only when the distinction materially affects interpretation.

Primary interface copy shall serve the user's task. Internal provenance defense, methodological self-justification, implementation caveats, and anticipatory rebuttals shall remain outside primary copy unless they materially affect safety, action, or result interpretation.

Relevant limitations, uncertainty, and provenance shall be stated plainly, once, at the narrowest appropriate level.

Concise shall mean removal of repetition and irrelevant material, not removal of information required for correct interpretation.

## 10. Token-Economy Test

Before adding, expanding, preserving, or removing a non-trivial code structure, abstraction, dependency, tool, test, verification mechanism, document, gate, workflow, or process, ask:

> Will this decision reduce total expected Token Cost across the approved development direction without compromising required semantics, correctness, security, or maintainability?

If yes, the decision is permitted and should be implemented at a scope proportionate to the responsibility.

If no, do not add or preserve the machinery merely because it appears complete, professional, scalable, defensive, conventional, or theoretically reusable.

`Proportionate` does not mean smallest, fewest, least abstract, or immediately consumed. It means that the expected recurring value justifies the continuing reasoning and maintenance burden.

## 11. Completion

Once the authorized behavior and required proof are complete, STOP.

Further work requires a new defect, requirement, accepted improvement, or explicit authorization.
