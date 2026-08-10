---
name: governing-repository-documentation
description: Use when auditing, creating, restructuring, repairing, or maintaining repository documentation; when README, INDEX, AGENTS, user/developer/reference docs, multilingual docs, Skills, gotchas, known issues, runbooks, playbooks, institutional knowledge, or documentation drift need repository-wide governance; or before a documentation-focused release audit.
---

# Governing Repository Documentation

## Overview

Build and maintain a repository documentation system that is discoverable, evidence-based, audience-aware, internally consistent, and resistant to drift.

Treat documentation as an information architecture, not a collection of Markdown files. Inspect the repository before designing the target structure, assign canonical ownership for important facts, keep AI operational instructions compact, and verify documentation against implementation before completion.

## Non-negotiable contracts

### Preflight before deep work

Before a long repository audit, perform only a short, explicitly announced preflight scan. Use it to discover obvious repository structure and identify decisions that could block or materially redirect the work.

Then ask **all reasonably foreseeable blocking questions together in one early message**. Do not begin a long autonomous pass and later stop on a question that could have been identified during preflight.

Read [preflight and interaction](references/preflight-and-interaction.md) before the first user confirmation.

### Language policy before restructuring

Before editing human-facing documentation, establish:

- the primary human-documentation language;
- whether localization is single-language or multilingual;
- if multilingual, the translation scope and canonical source language when not already clear.

Unless the user already supplied these decisions in the current request, ask for them in the preflight confirmation.

Defaults when the user accepts defaults or does not specify an alternative:

- primary human-documentation language: the user's current language;
- localization: single-language;
- canonical human-documentation language: the primary human-documentation language.

AI-facing operational documentation is **not localized by this policy**. `AGENTS.md`, `AGENTS.override.md`, `SKILL.md`, repository-stored agent workflows, system/developer prompts, and AI-specific operational policies MUST use concise technical English.

Read [audience and language](references/audience-and-language.md). If multilingual documentation is requested or already maintained, also read [multilingual documentation](references/multilingual-documentation.md).

### Repository reality is the source of truth

Do not document behavior from filenames, conventions, old prose, screenshots, or assumptions when the repository can be inspected.

Prefer evidence in this order when resolving current behavior:

1. executable behavior and verified command output;
2. tests and machine-readable contracts;
3. current configuration, manifests, schemas, and generated interfaces;
4. implementation code;
5. current automation and CI/CD;
6. maintained documentation;
7. history and design records for intent or chronology.

When evidence conflicts, investigate. Do not silently pick the most convenient source.

Read [repository discovery](references/repository-discovery.md) before the full audit.

### No project-specific template leakage

Do not infer a universal documentation tree from another repository, a screenshot, a previous project, or a fixed list of topic filenames.

The only mandatory generic entry points defined by this Skill are:

- repository root: `README.md`, `INDEX.md`, `AGENTS.md`;
- primary documentation root: `README.md`, `INDEX.md`, `AGENTS.md`;
- each important repository scope: `README.md`, `AGENTS.md`.

All other topic documents MUST be derived from the repository's actual capabilities, audiences, workflows, and maintenance needs.

### Important scopes require local entry points

An important scope is a directory that forms a meaningful working, ownership, deployment, extension, or architectural boundary.

Every important scope MUST have:

- a human-facing `README.md`;
- an AI-facing `AGENTS.md`.

Do not classify every source directory as important. Read [important scopes](references/important-scopes.md) before deciding where local entry points belong.

### One canonical owner per important fact

Assign a canonical documentation owner for important commands, configuration, interfaces, compatibility statements, workflows, and operational facts. Other documents should summarize and link instead of maintaining independent copies.

Read [canonical sources and drift](references/canonical-sources-and-drift.md) whenever duplicated or stale documentation is present, and always in maintenance mode.

### Operational knowledge and institutional memory

Treat recurring traps, hidden constraints, workarounds, known issues, troubleshooting knowledge, runbooks, playbooks, architecture decisions, and incident lessons as governed documentation roles rather than ad hoc notes.

Do not create one file for every role automatically. Classify the knowledge first, place it at the narrowest stable scope, keep historical learning separate from current operational guidance, and **prefer enforcement over remembrance** when a rule can be made mechanical.

Read [operational knowledge](references/operational-knowledge.md) whenever the repository contains recurring engineering traps, workarounds, operational procedures, incident knowledge, or unexplained constraints.

## Modes

This Skill supports two modes.

### Bootstrap mode

Use when documentation is absent, fragmented, structurally incoherent, substantially stale, or explicitly being redesigned.

Bootstrap mode MAY:

- establish the root and documentation entry points;
- define important documentation scopes;
- create, merge, split, move, rename, archive, or remove documentation;
- establish canonical ownership;
- rebuild navigation;
- introduce missing documentation categories supported by repository evidence.

Structural change is allowed, but must remain evidence-driven and proportionate.

### Maintenance mode

Use for routine drift repair, release preparation, documentation review after code changes, or repositories with an already coherent documentation architecture.

Maintenance mode follows a minimal-change policy:

- preserve stable paths and information architecture unless they cause a concrete correctness or discoverability problem;
- focus on changed behavior and affected documentation;
- repair drift and broken navigation;
- avoid broad renames or tree redesign for stylistic preference.

Infer the mode during preflight when the request and repository state make it clear. If the choice is ambiguous and would materially change the work, include it in the single early confirmation. Otherwise state the inferred mode and continue.

## Workflow

### Phase 0: Announce and run bounded preflight

Tell the user that you will perform a short preflight scan before the full audit, and that you will return immediately with any decisions required before long-running work begins.

During preflight inspect only enough to identify blocking decisions and obvious structure. Typical inputs:

- repository root listing;
- root `README.md`, `INDEX.md`, `AGENTS.md`, and override instructions if present;
- primary documentation directory and its top-level contents;
- workspace/package manifests;
- obvious application/package/service boundaries;
- existing localization layout;
- Skill and agent-instruction roots;
- current repository status or a short change summary when maintenance mode is likely.

Do **not** use preflight to perform the full source scan, exhaustive API inventory, full test suite, deep Git archaeology, or complete documentation rewrite.

### Phase 1: Establish the decision ledger

After preflight, ask all foreseeable blocking decisions together.

The confirmation MUST establish or explicitly default:

- documentation mode when materially ambiguous;
- primary human-documentation language;
- localization strategy;
- canonical source language if multilingual;
- any repository-specific governance choice that cannot be inferred safely and would cause substantial rework if guessed.

Record the result as an internal decision ledger. Do not reopen settled decisions without new contradictory evidence.

After this confirmation, follow the **no late blocking questions** rule in [preflight and interaction](references/preflight-and-interaction.md).

### Phase 2: Discover repository reality

Perform the full evidence-based audit.

Map, as applicable:

- applications, packages, libraries, services, plugins, adapters, providers, SDKs, tooling, and deployment units;
- build, development, test, lint, type-check, generation, packaging, release, and operational workflows;
- configuration and environment-variable sources;
- APIs, CLIs, IPC, protocols, schemas, serialization, and public extension points;
- examples, fixtures, templates, and generated artifacts;
- CI/CD and release automation;
- agent instructions, prompts, Skills, and AI workflows;
- existing documentation and navigation;
- operational knowledge signals such as recurring warnings, workarounds, regression notes, runbooks/playbooks, known issues, decisions, and incident records;
- changed areas relevant to maintenance mode.

Use [repository discovery](references/repository-discovery.md). The optional read-only helper `scripts/inventory_docs.py` may accelerate inventory; it does not replace judgment.

### Phase 3: Build the documentation model

Before editing, identify:

- repository audiences;
- important scopes;
- current documentation owners;
- missing topics;
- duplicated facts;
- contradictions;
- stale or historical material;
- orphan documents;
- machine-readable sources that should own factual reference data;
- required user journeys and agent workflows;
- institutional knowledge that is expensive to rediscover;
- temporary knowledge that requires an explicit retirement condition.

Classify documentation needs by purpose: entry/navigation, tutorial/getting started, how-to, reference, explanation/architecture, contribution/maintenance/operations, and operational knowledge/institutional memory. These are information classes, not mandatory directory names.

Read [documentation architecture](references/documentation-architecture.md), [important scopes](references/important-scopes.md), and [operational knowledge](references/operational-knowledge.md) when relevant.

### Phase 4: Design the minimum sufficient target architecture

Define the smallest documentation topology that satisfies actual repository needs.

Required generic anchors:

- root `README.md`: human landing page;
- root `INDEX.md`: repository map;
- root `AGENTS.md`: repository-wide AI working rules;
- documentation-root `README.md`: documentation landing page and reading guidance;
- documentation-root `INDEX.md`: authoritative documentation catalog;
- documentation-root `AGENTS.md`: local AI instructions for documentation work;
- `README.md` and `AGENTS.md` in every important scope.

Create local `INDEX.md` only where navigational complexity justifies it.

Do not create empty categories or topic documents because a checklist contains their names. `GOTCHAS`, `KNOWN_ISSUES`, `RUNBOOK`, `PLAYBOOK`, `FAQ`, ADR, and postmortem are semantic roles, not mandatory files.

For structural design, read:

- [documentation architecture](references/documentation-architecture.md);
- [README guidelines](references/readme-guidelines.md);
- [INDEX and navigation](references/index-and-navigation.md);
- [AGENTS guidelines](references/agents-guidelines.md).

### Phase 5: Repair and write documentation

Execute the target architecture according to mode.

For every document:

- identify primary audience and job;
- identify canonical facts it owns;
- verify commands, paths, interfaces, configuration, and examples;
- remove unrelated responsibilities;
- link to canonical sources instead of copying them;
- preserve useful stable paths when practical;
- distinguish current, planned, deprecated, and historical behavior;
- keep project-specific details grounded in repository evidence.

Load the relevant reference before writing that document type:

| Task | Reference |
|---|---|
| Root or local README | [README guidelines](references/readme-guidelines.md) |
| Root/docs/local INDEX and navigation | [INDEX and navigation](references/index-and-navigation.md) |
| Root/local AGENTS or overrides | [AGENTS guidelines](references/agents-guidelines.md) |
| Architecture, API, CLI, config, development, testing, operations, security, release, extension, or troubleshooting docs | [topic documentation](references/topic-documentation.md) |
| Gotchas, known issues, workarounds, runbooks, playbooks, ADRs, incident reviews, or institutional knowledge | [operational knowledge](references/operational-knowledge.md) |
| Human-facing prose or large rewrite | [writing quality](references/writing-quality.md) |
| Multilingual docs | [multilingual documentation](references/multilingual-documentation.md) |
| Duplicate/stale facts or generated references | [canonical sources and drift](references/canonical-sources-and-drift.md) |

### Phase 6: Audit AI-facing documentation and Skills

Treat AI-facing instructions as operational context, not human manuals.

For `AGENTS.md` and related files:

- keep scope explicit;
- state invariants, constraints, commands, and verification requirements;
- avoid inherited duplication;
- keep repository-to-leaf instruction chains compact;
- use technical English;
- verify platform-specific discovery semantics before relying on overrides.

For Skills:

- verify required metadata and entry files;
- verify triggers, scope, inputs/outputs, workflow, tool assumptions, failure conditions, references, scripts, and validation;
- use progressive disclosure;
- avoid auxiliary-file proliferation without runtime or maintenance value.

Read [AGENTS guidelines](references/agents-guidelines.md). For Skill format questions, consult current platform documentation and [sources and standards](references/sources-and-standards.md).

### Phase 7: Verify

Verification is required before completion.

Check, as applicable:

- internal links and referenced paths;
- important external links;
- commands and task targets;
- configuration and environment-variable names;
- API/CLI/schema references;
- examples and onboarding flow;
- README/INDEX navigation paths;
- `AGENTS.md` scope, inheritance, duplication, and contradictions;
- Skill references/scripts/assets;
- stale names and removed components;
- orphan maintained documents;
- version/platform/compatibility claims;
- documentation language policy;
- multilingual parity within the chosen translation scope;
- active gotchas, known issues, workarounds, runbooks, playbooks, and incident-derived current guidance for staleness and correct ownership.

Prefer existing repository tooling. Use `scripts/check_internal_links.py` only as a lightweight fallback for local Markdown path checks.

Read [verification and quality](references/verification-and-quality.md) before declaring completion.

### Phase 8: Report

Provide a concise final report with:

#### Documentation architecture

State the resulting entry points, important scopes, navigation model, audience/language policy, canonical ownership model, and AI-instruction layering.

#### Changes

Summarize significant additions, rewrites, splits, merges, moves, renames, archives, and removals.

#### Issues resolved

Summarize stale documentation, conflicts, duplication, missing coverage, invalid commands, broken navigation, broken links, undocumented behavior, and agent-instruction problems that were actually fixed.

#### Verification performed

List checks and commands actually executed and their results. Never imply an unexecuted check passed.

#### Remaining uncertainty

List unresolved behavior, missing product decisions, unverifiable claims, incomplete implementation, or intentionally deferred work. Non-blocking uncertainty belongs here rather than causing unnecessary mid-run stops.

## Completion gate

Do not declare success until the repository substantially satisfies all applicable conditions:

- a new user can enter through the root README and reach a verified first-use path;
- the root INDEX provides a useful repository map;
- the documentation INDEX exposes maintained documentation without requiring manual tree browsing;
- every important scope has useful human and AI entry points;
- developers can find verified development and testing procedures;
- relevant audiences can find configuration, interfaces, extension, deployment, operations, security, release, and troubleshooting information when those capabilities exist;
- AI instructions are actionable, scoped, concise, and non-duplicative;
- Skills and agent workflows are internally valid when present;
- canonical owners for important facts are clear;
- durable operational knowledge is discoverable, correctly classified, and not trapped only in comments, historical incident notes, or maintainers' memory;
- obsolete gotchas/workarounds are removed from active guidance, and current high-risk constraints are enforced or projected into the correct operational surface;
- major contradictory or duplicated descriptions are reconciled;
- critical commands, paths, interfaces, configuration, and examples are verified;
- the chosen language/localization policy is applied consistently;
- unresolved ambiguity is explicitly reported.

## Red flags

Stop and correct course if you notice any of these behaviors:

- deep repository exploration before the early confirmation;
- asking one predictable question, doing long work, then asking another predictable blocking question;
- creating topic documents from a generic filename checklist;
- copying another repository's documentation tree;
- creating README/AGENTS files in every implementation directory without scope analysis;
- treating `README.md`, `INDEX.md`, and `AGENTS.md` as interchangeable;
- duplicating commands or configuration tables across several canonical-looking files;
- rewriting coherent documentation architecture during maintenance mode without a concrete need;
- translating AI-facing operational instructions away from technical English;
- documenting planned behavior as current behavior;
- changing application behavior merely to make stale documentation true;
- creating GOTCHAS/PLAYBOOK/RUNBOOK/KNOWN_ISSUES/FAQ files merely because the names sound useful;
- using a postmortem as the canonical current runbook;
- preserving obsolete workarounds as active guidance after the underlying issue is fixed;
- leaving a high-risk, mechanically preventable mistake as prose-only institutional memory without justification;
- declaring verification success without evidence.
