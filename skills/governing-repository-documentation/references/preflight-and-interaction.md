# Preflight and interaction discipline

## Purpose

Prevent long-running documentation work from stalling on predictable questions after the user has already left the interaction.

The preflight phase exists to discover decisions, not to perform the documentation audit itself.

## Interaction contract

Before deep work:

1. Announce that a short preflight scan will run first.
2. State that the scan is intentionally bounded and that you will return promptly with any decisions required before the full audit begins.
3. Inspect only enough repository context to identify foreseeable blocking choices.
4. Ask all such choices together in one confirmation message.
5. State defaults for every choice that has a safe default.
6. Wait for the user's confirmation when a real decision remains.
7. Once confirmed, begin the long-running audit and avoid unnecessary interruptions.

Do not simulate progress while waiting for a decision that materially changes architecture.

## What belongs in preflight

Inspect shallow, high-information signals:

- top-level directory listing;
- repository-root README, INDEX, AGENTS, and active overrides;
- documentation-root top level;
- workspace or package manifests;
- obvious package/application/service boundaries;
- obvious localization directories or language-suffixed files;
- existing Skills and agent-instruction locations;
- `git status` and a concise diff/file summary when maintenance mode is likely.

A preflight should generally avoid:

- recursive source-code comprehension;
- full API or schema enumeration;
- full build or test suites;
- exhaustive Markdown reading;
- large generated directories;
- deep Git history;
- broad web research unrelated to an immediate preflight decision.

The limit is semantic rather than chronological: stop once you can identify the foreseeable governance decisions.

## Required early language question

Unless the user already explicitly supplied the answers in the current request, the preflight confirmation MUST ask:

- Which language should human-facing documentation use?
  - Default: the user's current language.
- Should documentation be single-language or multilingual?
  - Default: single-language.
- If multilingual, what translation coverage is desired and which language is canonical?
  - Default canonical language: the selected primary human-documentation language.

Ask these together, not serially.

A compact interaction can present options such as:

- Primary language: `<detected user language>` (default) / another language.
- Localization: single-language (default) / entry points only / user-facing docs / full maintained corpus / custom scope.
- Canonical source for multilingual docs: primary language (default) / another maintained language.

AI-facing operational documentation remains concise technical English regardless of this choice.

## Other questions that belong in the early confirmation

Include a question only when its answer can materially change the architecture or cause substantial rework and repository evidence cannot resolve it safely.

Common examples:

- bootstrap versus maintenance mode when both are plausible and the distinction matters;
- whether an existing but incomplete localization program should be preserved, expanded, or retired;
- whether generated reference documentation is authoritative or merely an artifact when repository evidence is genuinely ambiguous;
- whether historical documents are intentionally preserved as records or should be retired when no policy can be inferred;
- organization-specific publication constraints not encoded in the repository.

Do not ask users to decide facts that can be discovered from the repository.

## Batch questions, do not drip-feed them

A repository documentation task is often autonomous and long-running. Traditional one-question-at-a-time clarification is harmful here when multiple predictable decisions can be identified in advance.

The first confirmation should therefore be a **decision packet**, not a conversational questionnaire.

Bad pattern:

1. Ask language.
2. Explore for twenty minutes.
3. Ask whether multilingual docs are desired.
4. Explore again.
5. Ask whether to preserve the old docs tree.

Required pattern:

1. Short scan.
2. Surface all currently foreseeable material choices together.
3. Establish defaults and user decisions.
4. Execute autonomously.

## No-late-blocking-questions rule

After the preflight confirmation, do not block on ordinary uncertainty.

Continue with a conservative, reversible, evidence-based default when possible. Record the decision and report the uncertainty at the end.

A late question is justified only when **all** of the following are true:

1. New evidence reveals a choice that could not reasonably have been identified during preflight.
2. The plausible options would materially change public documentation architecture, repository policy, or destructive edits.
3. Repository evidence cannot resolve the choice.
4. No safe conservative default exists.

If any condition is false, continue instead of blocking.

## Decision ledger

After preflight, maintain an internal ledger containing at least:

- mode;
- primary human-documentation language;
- localization policy;
- canonical localization source language;
- primary documentation root;
- important-scope classification rule;
- any approved structural constraints;
- conservative defaults chosen for unresolved non-blocking issues.

Do not repeatedly reconsider settled decisions without contradictory evidence.

## Non-blocking uncertainty examples

These normally belong in the final report, not a mid-run question:

- a small internal module's intended long-term status is unclear;
- a historical document might be archival but keeping it temporarily is safe;
- an undocumented internal API's stability is uncertain;
- a borderline directory might or might not justify a local INDEX;
- one example cannot be executed because an optional external dependency is unavailable;
- an external link cannot be verified due to network restrictions.

Use the least destructive interpretation and continue.
