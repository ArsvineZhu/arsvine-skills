# AGENTS guidelines

## Role

`AGENTS.md` is operational context for AI coding agents. It is not a user guide, architecture textbook, or duplication layer for all repository knowledge.

Write it in concise technical English.

## Required scopes

The repository root and every important scope must have an `AGENTS.md`.

The primary documentation root is an important scope and must have its own `AGENTS.md`.

When a platform-specific override file is already intentionally active, preserve its semantics and do not invent conflicting duplicate instructions. Maintain the baseline `AGENTS.md` when repository policy requires it, but make clear which file is effective for the target platform.

## Root AGENTS content

Include repository-wide operational facts that materially change agent behavior, for example:

- repository layout at the level needed to choose a working area;
- package manager or workspace rules;
- canonical build/test/lint/type-check/format commands;
- generated-file policies;
- protected or externally managed areas;
- architecture boundaries that must not be crossed casually;
- compatibility or public-contract constraints;
- security/trust restrictions;
- required documentation synchronization rules;
- minimum verification before completion.

Exclude:

- marketing or project introduction prose;
- full architecture explanations;
- complete API/configuration reference;
- exhaustive file lists;
- style rules already enforced reliably by formatters/linters unless the agent needs to know how to invoke them;
- generic software-engineering advice.

## Local AGENTS content

A local file should contain only what is relevant to that scope beyond inherited repository rules:

- scope boundary and local ownership;
- where an agent should start reading;
- local modification constraints;
- local commands when different or more specific;
- local invariants;
- generated/protected files;
- local verification requirements;
- documentation that must change when behavior changes.

Do not repeat ancestor rules merely for completeness.

## Inheritance discipline

Before writing a local AGENTS file:

1. Read every applicable ancestor instruction file.
2. Identify what is already inherited.
3. Write only local additions, refinements, or explicit exceptions.
4. Check the root-to-leaf chain for contradiction and unnecessary repetition.

The effective instruction chain should remain compact enough to preserve agent context for the actual task.

## Codex-specific discovery semantics

When the target agent is Codex, verify current official behavior before relying on details that may change.

As of the source set recorded with this Skill, Codex:

- reads global guidance first;
- walks from project root toward the current working directory;
- checks one instruction candidate per directory;
- prefers `AGENTS.override.md` over `AGENTS.md` in the same directory;
- concatenates guidance root-to-leaf so deeper guidance has later precedence;
- applies a configured combined-size limit.

Therefore:

- place repository-wide rules at the root;
- place specialized rules near the code they govern;
- do not create local files that only duplicate parent text;
- treat `AGENTS.override.md` as an intentional override mechanism, not a decorative filename;
- do not assume the same discovery semantics for a non-Codex agent platform without verification.

## Normative language

Use `MUST`, `MUST NOT`, `SHOULD`, and `MAY` only when the distinction matters.

Good rules are observable:

- `MUST run <verified command> after changing the public schema.`
- `MUST NOT edit generated files under <verified path>; update the generator source instead.`
- `SHOULD keep local changes inside this package unless a public contract requires a cross-package change.`

Weak rules are vague:

- "Be careful."
- "Write clean code."
- "Make sure everything works."

## Documentation synchronization rules

Use AGENTS files to encode durable synchronization triggers, such as:

- changing a public API requires checking its reference docs;
- changing CLI behavior requires checking CLI docs and examples;
- changing configuration requires checking configuration reference and sample config;
- moving an important scope requires updating repository and documentation indexes;
- changing a Skill or agent workflow requires validating its references and operational instructions.

Do not list every document in every AGENTS file. Point to the canonical documentation policy when a broader explanation is needed.


## Projecting institutional knowledge into AGENTS

When a gotcha, incident lesson, or known constraint materially affects AI editing behavior, project only the actionable rule into the nearest applicable AGENTS scope.

Use this precedence:

1. prevent the mistake mechanically when practical;
2. keep durable human rationale in the appropriate gotcha/architecture/operational document;
3. add a concise `MUST`/`MUST NOT`/validation rule to AGENTS only when the agent must act differently;
4. link to the detailed human explanation when useful.

Do not copy long incident narratives, workaround histories, or complete runbooks into AGENTS.

If a temporary workaround becomes an AGENTS rule, give it a verifiable scope and ensure the human canonical source contains the condition for removing it. Maintenance audits must remove the AGENTS projection when the workaround is no longer required.

## Human rationale

If a rule needs extensive rationale, put the explanation in human-facing architecture/development documentation and link to it from AGENTS when helpful.

Keep the operational instruction itself short.

## Verification

Before completing an AGENTS change, verify:

- language is technical English;
- commands and paths exist;
- scope is explicit;
- no parent rule is needlessly repeated;
- no local rule contradicts an ancestor unintentionally;
- override semantics match the target agent platform;
- the root-to-leaf instruction chain remains reasonably compact;
- rules describe current repository behavior, not aspirational policy unless explicitly marked.
