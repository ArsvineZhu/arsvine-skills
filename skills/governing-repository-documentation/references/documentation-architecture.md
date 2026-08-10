# Documentation architecture

## Goal

Organize documentation around reader needs, repository boundaries, and canonical information ownership. Do not optimize for file count or superficial symmetry.

## Information classes

Use these classes to reason about content. They are not mandatory directory names.

### Entry and navigation

Answers:

- What is this repository or scope?
- Where do I start?
- Where is a topic documented?

Typical owners: `README.md`, `INDEX.md`, documentation landing pages.

### Tutorial and getting started

Learning-oriented material that leads a newcomer through a successful first experience. Keep choices and explanations minimal enough that the path remains reliable.

### How-to

Goal-oriented procedures for readers who already have enough context to accomplish a specific task.

### Reference

Information-oriented descriptions of facts and contracts: APIs, CLI, configuration, schemas, formats, compatibility, options, and public interfaces.

### Explanation and architecture

Understanding-oriented material: boundaries, lifecycle, data flow, invariants, design intent, trade-offs, and conceptual models.

### Contribution, maintenance, release, and operations

Working material for contributors and operators: development, testing, release, deployment, incident response, maintenance, governance, and troubleshooting.

### Operational knowledge and institutional memory

Hard-won knowledge that is expensive or dangerous to rediscover: gotchas, current known issues and workarounds, diagnostic playbooks, procedural runbooks, architecture decisions, and incident lessons.

Treat these as semantic roles rather than mandatory filenames. Read [operational knowledge](operational-knowledge.md) before designing this part of the corpus.

The distinction between these classes is useful because mixing their jobs produces bloated README files, narrative API reference, tutorials overloaded with architecture theory, and operational notes that become stale or impossible to find.

## Mandatory generic anchors

Use this abstract topology unless an existing coherent documentation system provides equivalent established locations:

```text
repository-root/
├── README.md
├── INDEX.md
├── AGENTS.md
├── <documentation-root>/
│   ├── README.md
│   ├── INDEX.md
│   ├── AGENTS.md
│   └── <topic documentation derived from repository needs>
└── <important-scope>/
    ├── README.md
    ├── AGENTS.md
    └── <local documentation only when justified>
```

This is a role model, not a filename template for topic documentation.

## Responsibilities by anchor

### Root README

Human landing page. Communicates identity, value, prerequisites, shortest verified start path, and links to deeper documentation.

### Root INDEX

Repository map. Explains major areas and where authoritative documentation or important subsystems live.

### Root AGENTS

Repository-wide operational rules for AI coding agents.

### Documentation-root README

Explains the documentation corpus: audiences, reading paths, categories, contribution/maintenance expectations, and localization model.

### Documentation-root INDEX

Authoritative catalog of maintained documentation. Organize by reader goal or subject, not raw filesystem order.

### Documentation-root AGENTS

AI instructions specific to documentation work: language policy, canonical sources, validation, generation rules, and local workflows.

### Important-scope README

Human explanation of the scope's purpose, responsibilities, boundaries, entry points, local workflows, and deeper docs.

### Important-scope AGENTS

Concise local AI constraints and validation rules, inheritance-aware relative to ancestors.

## Topic documents are derived, not prescribed

Create a topic document only when repository evidence establishes a durable topic and audience need.

Possible concerns include architecture, configuration, API, CLI, protocol/data format, extension development, testing, deployment, operations, security, release, troubleshooting, migration, contribution, gotchas, known issues, runbooks, playbooks, decision records, or incident learning. These are examples of concerns and knowledge roles, not required files.

Decide whether to merge or split based on:

- distinct audience;
- distinct maintenance owner;
- distinct canonical facts;
- document size and navigability;
- change frequency;
- whether readers commonly need one topic without the other.


## Institutional-knowledge placement principle

Place hard-won knowledge at the narrowest stable scope that owns it, then expose it through navigation. Do not centralize every trap merely to make one large `GOTCHAS.md`, and do not scatter cross-cutting operational rules across many local files.

Prefer this ownership hierarchy:

1. machine enforcement for preventable mistakes;
2. nearest canonical current document for active behavior/procedure;
3. nearest applicable AGENTS scope for concise AI operational constraints;
4. ADR or postmortem for durable historical rationale/learning;
5. issue/commit history only as evidence, not as the maintained documentation system.

A historical source may explain why a current rule exists, but it should not silently become the current owner of the rule.

## Preserve coherent existing systems

Do not replace a mature documentation site, generated reference system, or stable information architecture merely to match this Skill's examples.

Map required roles onto existing locations when they are equivalent and discoverable.

Restructure when there is concrete evidence of:

- missing entry points;
- orphan content;
- conflicting ownership;
- misleading hierarchy;
- severe discoverability problems;
- mixed audiences causing maintenance problems;
- obsolete architecture that no longer matches the repository.

## Canonical ownership model

For each important fact, identify one owner.

Example ownership pattern:

| Fact | Canonical owner | Other documents |
|---|---|---|
| First-run path | Getting-started content or root README if short | Link or brief summary |
| Full configuration semantics | Configuration reference or schema | Link; avoid copied tables |
| API contract | Machine-readable API definition or API reference | Usage examples link back |
| Architecture rationale | Architecture/explanation doc | README gives only summary |
| Agent validation rules | Closest applicable AGENTS file | Human docs may explain rationale |
| Documentation catalog | Documentation INDEX | README links to catalog |

Do not create several canonical-looking owners for the same fact.

## Navigation graph

A healthy documentation graph usually supports these paths:

```text
root README
  -> root INDEX
  -> documentation README / INDEX
  -> topic documentation
  -> important-scope README
  -> source/examples only when useful
```

Topic documents should link back to an appropriate index or parent when that improves navigation.

Navigation should not require readers to infer meaning from raw filenames.

## Avoid empty architecture

Do not create empty tutorial/how-to/reference/explanation directories merely to exhibit a framework.

Improve content first. Let structure emerge from real material and reader needs.
