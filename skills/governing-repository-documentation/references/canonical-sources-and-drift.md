# Canonical sources and documentation drift

## Canonical ownership

Important facts should have one authoritative owner.

A canonical owner may be:

- a machine-readable contract;
- a generated reference produced from such a contract;
- one maintained human reference document;
- an AGENTS file for an AI-only operational rule;
- an architecture/design record for rationale.

Other documents should summarize, contextualize, and link.

## Canonical-source table

During bootstrap or a substantial maintenance audit, build an internal table similar to:

| Fact class | Repository evidence | Canonical documentation owner | Secondary surfaces |
|---|---|---|---|
| Install/start commands | manifests/scripts | getting-started or root README | local README summaries |
| Configuration | schema/readers | configuration reference | README examples |
| Public API | formal definition/types | generated or human API reference | how-to examples |
| CLI | command definitions/help | CLI reference | quickstart examples |
| Architecture rationale | code + ADR/history | architecture explanation | README summary |
| Agent validation | scripts/CI | closest AGENTS scope | developer guide rationale |
| Current known issue/workaround | implementation + issue evidence | one known-issue/troubleshooting owner | README/FAQ links |
| Deterministic operational procedure | scripts/automation + verified process | runbook or automation docs | playbook/postmortem links |
| Significant decision rationale | code + decision evidence | ADR/decision log | architecture summary |
| Past incident learning | incident evidence | postmortem/incident review | current docs link only when useful |

Do not necessarily commit this table. Use it to make ownership decisions.

## Duplication categories

Not all repetition is harmful.

### Acceptable repetition

- a minimal quickstart command repeated in an entry page for usability;
- a one-sentence architecture summary linking to full explanation;
- a small configuration snippet demonstrating a common case;
- an AGENTS rule referencing the same validation command owned by build tooling.

### Harmful duplication

- several complete configuration tables maintained independently;
- API signatures manually copied into multiple guides;
- root and local AGENTS repeating the same policy verbatim;
- README and developer guide each owning different versions of setup commands;
- translated docs edited independently without a canonical source policy.

When repetition is necessary, minimize the duplicated surface.

## Machine-readable sources

Prefer machine-readable sources for factual reference when they are reliable and part of the repository's maintained workflow.

Examples:

- OpenAPI or equivalent interface specifications;
- JSON Schema or other config/data schemas;
- CLI parser definitions and generated help;
- package manifests;
- public type definitions;
- database schema/migration definitions;
- protocol IDLs.

Do not generate documentation merely because generation is possible. Generated output should solve a real discoverability or usability need.

## Drift detection in maintenance mode

Start from change evidence when available:

- working-tree diff;
- staged diff;
- recent commits relevant to the requested range;
- release diff or version boundary;
- changed public interfaces/configuration.

Map changed implementation surfaces to documentation triggers.

Typical triggers:

| Implementation change | Documentation to inspect |
|---|---|
| Public behavior | README/how-to/reference/examples |
| API contract | API reference, examples, migration notes |
| CLI | CLI reference, quickstart, scripts/examples |
| Configuration/env vars | configuration reference, sample config, deployment docs |
| Schema/data format | schema reference, compatibility/migration docs |
| Important directory boundary | root/local INDEX and README/AGENTS |
| Build/test workflow | development/testing docs and AGENTS |
| Deployment | runbooks/operations docs |
| Skill/agent workflow | SKILL/AGENTS/references and validation guidance |

## Documentation synchronization policy

Encode durable triggers in contribution guidance, AGENTS instructions, CI, review checklists, or release workflows where appropriate.

Do not rely on future maintainers remembering that documentation needs updates.

Keep the rule near the workflow it governs.


## Institutional-knowledge drift

Gotchas, workarounds, runbooks, playbooks, and incident-derived rules have unusually high drift risk because they often describe exceptional behavior.

During maintenance, verify transitions rather than preserving every warning indefinitely:

- known issue fixed -> remove active workaround and resolve/remove current warning;
- gotcha mechanically prevented -> remove or reduce prose warning;
- manual runbook automated -> make automation the executable source and remove duplicated manual step lists;
- postmortem lesson becomes current policy -> move the current rule to ADR/architecture/runbook/playbook/AGENTS as appropriate;
- ADR superseded -> preserve decision history while marking the new current decision;
- temporary compatibility rule expires -> remove it from active docs and AGENTS.

Prefer explicit removal conditions for temporary knowledge.

Do not let issue trackers, commit messages, or postmortems become accidental canonical owners of current procedures.

## Generated and vendored material

Identify generated docs explicitly.

Document:

- source of generation;
- generator command;
- whether output is committed;
- whether direct edits are forbidden;
- validation expectations.

Do not hand-edit vendored/external documentation unless repository policy explicitly requires it.

## Historical material

Historical documents should be visibly historical.

Options include:

- archival directory already used by the repository;
- explicit status header;
- ADR/design-record mechanism;
- removal when no ongoing value exists.

Do not leave obsolete instructions in the active documentation graph where readers can mistake them for current behavior.

## Maintenance minimalism

In maintenance mode, prefer repairing the canonical source and its immediate navigation edges.

Do not restructure the entire documentation hierarchy merely because the audit found cosmetic inconsistencies.

Escalate to structural work only when drift reveals an underlying ownership or discoverability failure.
