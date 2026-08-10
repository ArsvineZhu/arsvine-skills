# Multilingual documentation

## Principle

Multilingual documentation multiplies maintenance surfaces. Localize only the material users need, with a clear canonical source and synchronization policy.

Do not interpret "multilingual" as "translate every Markdown file".

AI-facing operational documentation remains concise technical English and is excluded from human localization unless the platform explicitly requires otherwise.

## Establish the policy during preflight

When multilingual documentation is requested or already present, establish all of these before restructuring:

- primary human-documentation language;
- canonical source language;
- supported locales;
- translation coverage;
- location/naming strategy;
- synchronization expectations;
- whether translations may lag and how lag is signaled.

Ask these in the early decision packet, not one-by-one later.

## Translation coverage models

Choose the smallest model that satisfies the audience.

### Entry points only

Localize the repository landing page and possibly the first-use guide.

Use when translated discovery and onboarding are valuable but the technical corpus can remain canonical in one language.

### User-facing corpus

Localize README/getting-started/how-to/user troubleshooting material while keeping developer/internal/reference material in the canonical language.

Use when end users need localization but maintainers share a common technical language.

### Selected topic set

Maintain a declared subset of documents in several languages.

Use when only certain products, markets, or workflows require localization.

### Full maintained corpus

Translate nearly all human-facing documentation.

Use only when the project has the maintenance capacity and publication workflow to keep locales synchronized.

## Layout strategies

Do not force a layout when an established localization system exists.

Common strategies include:

### Language-suffixed entry files

```text
README.md
README.<locale>.md
```

Useful for a small number of highly visible entry points.

### Locale directories

```text
<documentation-root>/
├── <locale-a>/
├── <locale-b>/
└── ...
```

Useful for larger parallel corpora.

### Canonical corpus plus localized subset

Keep canonical docs in the normal tree and a clearly named localization area for translated material.

Useful when translation coverage is intentionally partial.

These are abstract patterns. Preserve repository conventions when they are coherent.

## Canonical source rules

Every translated document should have one declared canonical source.

Avoid independent editing of equivalent facts in several languages without a synchronization process.

When practical, maintain a mapping between canonical and translated documents through:

- stable relative paths;
- frontmatter metadata already supported by the documentation system;
- an index/catalog;
- generated localization metadata.

Do not invent a new metadata system if the repository already has one.

## Drift policy

For each supported translation scope, decide whether translations must be:

- synchronous: changes are not complete until required translations are updated;
- bounded-lag: translations may lag but the status must be visible;
- best-effort: only the canonical language is authoritative.

Document the policy where maintainers and AI agents will see it.

For synchronous localization, add documentation synchronization requirements to the relevant AGENTS or contribution workflow.

## Navigation

Users should be able to:

- identify the current language;
- find supported alternatives;
- know which language is authoritative;
- avoid following stale cross-language links.

Do not create a language selector that points to nonexistent translations.

## Translation quality

Preserve:

- commands;
- identifiers;
- API/schema names;
- paths;
- code examples;
- configuration keys;
- error codes.

Translate explanatory prose and human-facing UI concepts according to the selected locale and project terminology.

Avoid literal translation of established technical terms when it reduces clarity.

## AI operational files

Do not create localized copies of `AGENTS.md` or `SKILL.md` for human convenience. If humans need an explanation of those policies, provide a separate human-facing document in the selected language and keep the operational source in technical English.
