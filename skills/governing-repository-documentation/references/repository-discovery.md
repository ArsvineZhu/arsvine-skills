# Repository discovery and evidence model

## Objective

Understand the repository before designing or rewriting its documentation. Documentation quality depends on reconstructing the actual system, its audiences, and its workflows rather than paraphrasing existing prose.

## Discovery sequence

### Establish repository boundaries

Identify:

- Git root and nested repositories, if any;
- monorepo/workspace boundaries;
- primary applications, services, packages, libraries, SDKs, plugins, tools, and deployment units;
- generated, vendored, archived, fixture, example, and external-code areas;
- documentation roots and publication systems.

Do not assume one repository equals one product.

### Inspect build and execution surfaces

Locate and verify, where relevant:

- package/workspace manifests;
- lockfiles and package-manager conventions;
- build scripts and task runners;
- development/start commands;
- lint, format, type-check, and static-analysis commands;
- unit, integration, end-to-end, and smoke-test commands;
- generation steps;
- release and packaging workflows;
- deployment and operational workflows.

Commands shown in documentation must come from these sources or from verified runtime output.

### Map user-visible and integration surfaces

Look for:

- CLI command definitions and help output;
- HTTP/RPC/IPC APIs;
- event contracts;
- public modules and SDKs;
- plugin/provider/adapter interfaces;
- configuration files and environment-variable readers;
- schemas and serialization formats;
- protocol definitions;
- database migrations or persistent data formats;
- import/export formats.

Prefer machine-readable definitions as factual reference sources when practical.

### Map runtime and architectural behavior

Trace enough implementation to understand:

- startup and lifecycle;
- major control paths;
- data flow;
- persistence and state ownership;
- concurrency or scheduling where important;
- trust/security/sandbox boundaries;
- external integrations;
- extension points;
- failure and recovery behavior.

Do not translate every source file into prose. Extract stable boundaries, contracts, and design intent.

### Inspect existing documentation

Inventory:

- README files;
- INDEX/navigation files;
- AGENTS and override files;
- user guides and tutorials;
- developer/reference/architecture docs;
- community and contribution docs;
- ADRs/design records;
- gotchas, known issues, workarounds, troubleshooting, runbooks, playbooks, and incident/postmortem records;
- examples and templates;
- AI Skills, prompts, and workflows;
- generated documentation.

For each maintained document, determine:

- primary audience;
- purpose;
- scope;
- canonical facts it appears to own;
- inbound navigation path;
- whether it is current, stale, duplicated, historical, or orphaned.


### Look for hidden institutional knowledge

When the task is bootstrap or a sufficiently deep maintenance audit, inspect selectively for high-value knowledge that has not reached the formal documentation system.

Signals include:

- `FIXME`, `HACK`, `WORKAROUND`, `TEMPORARY`, caveat, or warning comments;
- regression tests whose names encode past failures;
- CI exceptions and unexplained ordering constraints;
- scripts with safety checks or non-obvious sequencing;
- issue/incident references attached to still-active code;
- repeated "pitfall", "known limitation", "do not", or "must run from" prose;
- historical notes that explain a still-active architecture or operations rule.

Treat these as investigation leads only. Verify current applicability and recurrence value before promoting them into maintained documentation. Do not copy debugging debris wholesale into a gotchas file.

Use Git history or external issue systems only when the knowledge cannot be resolved from current repository evidence and the expected value justifies the cost.

### Use history selectively

Use Git history when current files do not explain:

- why a design exists;
- whether a document describes removed behavior;
- whether a rename/move recently invalidated links;
- whether a generated artifact is expected to be committed;
- whether a suspicious inconsistency is transitional.

History is evidence about chronology and intent, not the primary source for current behavior.

## Evidence hierarchy

Use the following default precedence when sources disagree:

1. verified executable behavior;
2. tests and formal machine-readable contracts;
3. active configuration/manifests/schemas/generated interfaces;
4. implementation code;
5. active automation and CI/CD;
6. maintained documentation;
7. issue history, commit history, ADRs, and obsolete documentation.

This is not absolute. A test can be stale; implementation can contain dead code; generated files can be unrefreshed. Resolve contradictions instead of blindly following rank.

## Classify implementation status

When useful, classify facts as:

- **Current:** verified behavior or contract in the current repository.
- **Planned:** explicitly designed or tracked but not implemented.
- **Deprecated:** still present but intentionally being retired.
- **Historical:** retained only to explain past decisions or migrations.
- **Unknown:** repository evidence is insufficient.

Never write planned or historical behavior as current.

## Discovery outputs

Before restructuring documentation, you should be able to answer:

- What are the repository's major products and subsystems?
- Who uses or maintains each one?
- What are the important scopes?
- What are the authoritative commands and interfaces?
- Which docs are entry points, reference, explanation, procedures, or historical records?
- Where are duplicated facts maintained?
- What is missing?
- What can be generated instead of manually mirrored?
- Which changes are necessary versus stylistic?

If you cannot answer these, discovery is not complete enough for bootstrap restructuring.

## Optional inventory helper

`scripts/inventory_docs.py` provides a read-only list of documentation files and candidate scope signals. It deliberately does not decide which scopes are important or which files should exist.

Use existing repository tooling when it provides a better inventory.
