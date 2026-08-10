# Audience and language policy

## First classify the audience

Every maintained document should have a dominant audience and job. A document may serve secondary readers, but trying to serve everyone equally usually produces poor structure.

Use these broad audience classes.

## General users

Human-facing end users need successful outcomes with minimal implementation detail.

Write in the selected primary human-documentation language.

Prefer:

- common vocabulary;
- complete procedures;
- clear prerequisites and expected results;
- concrete examples;
- links to deeper technical material.

Avoid unnecessary English, internal abstractions, unexplained acronyms, and implementation trivia.

Keep identifiers, commands, product names, API names, protocol names, and established technical terms in their authoritative form when translation would reduce precision.

## Advanced users, developers, maintainers, and operators

Write in the selected human-documentation language, but use established technical English terms where they are clearer and cheaper than forced translation.

Optimize for precision and searchability.

Examples of content that usually remains verbatim:

- command names and flags;
- source identifiers and types;
- package names;
- API names;
- error codes;
- configuration keys;
- environment variables;
- protocol/schema field names.

Do not translate identifiers into pseudo-identifiers.

## AI agents

AI-facing operational documentation MUST use concise technical English regardless of the human-documentation language.

This includes, when present:

- `AGENTS.md`;
- `AGENTS.override.md`;
- `SKILL.md`;
- agent workflow instructions;
- repository-stored system or developer prompts;
- AI-specific operational policies.

AI-facing text should prefer:

- explicit scope;
- imperative instructions;
- exact constraints;
- invariants;
- decision rules;
- verified commands;
- explicit validation requirements;
- normative terms such as MUST, MUST NOT, SHOULD, and MAY when useful.

Avoid:

- marketing language;
- long narrative background;
- repeated architecture explanations;
- vague encouragement;
- facts readily inferable from nearby code;
- human onboarding prose copied into agent context.

## Mixed documents

Do not mix human tutorial prose and AI instructions in the same document unless the repository has a strong established reason.

Prefer a human document for explanation and an AGENTS/Skill file for operational rules, linked when appropriate.

Human readers need rationale and context. AI agents need scope, rules, and verification. These are related but different documentation products.

## Default policy

When the user does not choose another policy:

- human documentation uses the user's current language;
- localization is single-language;
- AI-facing operational documentation uses technical English.

Do not silently infer a different human language from source-code comments or package names when the user has explicitly selected one.

## Existing repository conventions

If the repository already has a deliberate language policy that conflicts with the default, surface that during preflight rather than silently rewriting the corpus.

Repository evidence can answer questions such as:

- whether an English corpus is intentionally public-facing;
- whether localized docs are generated from a canonical source;
- whether separate locale branches or sites exist.

The user decides policy when the evidence and requested change conflict materially.
