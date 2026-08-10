# Verification and quality gate

## Principle

Documentation is not complete because Markdown renders. Verify claims against the repository and verify the documentation graph itself.

Use existing project tooling first. Add new tooling only when it has clear long-term value.

## Verification layers

### Structure

Check:

- required root entry points exist;
- primary documentation root has README, INDEX, and AGENTS;
- every identified important scope has README and AGENTS;
- local INDEX files exist only where justified;
- moved/renamed docs have updated inbound links;
- maintained docs are reachable from navigation;
- generated/vendor/archive areas are clearly handled.

### Links

Check:

- repository-relative links;
- image/resource paths;
- links in README/INDEX/AGENTS;
- links to moved source/examples;
- important external links when network access is available.

Use the repository's link checker if one exists. `scripts/check_internal_links.py` is a fallback for local path existence and does not fully validate anchors, rendered-site routing, or all Markdown extensions.

### Commands and workflows

Verify commands from authoritative sources and execute representative commands when practical.

Check:

- install/setup;
- start/development;
- build;
- lint/format/type-check;
- tests;
- generation;
- packaging/release;
- deployment/operations.

Do not claim a command passed if it was only found in a manifest.

Distinguish:

- **exists:** command is defined;
- **verified:** command was actually executed successfully;
- **not run:** command was not executed and should not be reported as passed.

### Configuration and environment

Cross-check:

- configuration keys;
- types/defaults;
- precedence;
- environment-variable names;
- secrets handling;
- example configuration.

Prefer schemas or code that actually consumes configuration.

### Interfaces and reference

Cross-check public API/CLI/protocol/schema docs against formal definitions and current implementation.

Check examples against the documented interface.

### Onboarding path

Follow the documented first-use path as far as the environment allows.

Check that:

- prerequisites are sufficient;
- commands are ordered correctly;
- referenced files exist;
- expected results are plausible and preferably observed;
- the path does not jump to undocumented state.

### AI instructions

For every applicable AGENTS chain:

- verify language is technical English;
- verify scope and inheritance;
- verify commands and paths;
- detect duplicated parent rules;
- detect contradictions;
- verify override semantics for the target agent platform;
- check that required documentation synchronization rules are present where needed.

For Skills:

- validate required metadata;
- validate referenced files;
- compile/run scripts when safe;
- verify examples and tool assumptions;
- verify progressive disclosure and trigger scope.


### Operational knowledge and institutional memory

For repositories that maintain gotchas, known issues, workarounds, troubleshooting knowledge, runbooks, playbooks, ADRs, or postmortems, verify:

- active gotchas still reproduce or remain logically applicable;
- resolved defects are not still presented as active known issues;
- workarounds are still necessary, safe, and owned in one current place;
- temporary entries have a meaningful removal condition when practical;
- runbook commands, prerequisites, permissions, verification, rollback, and stop conditions are current;
- playbook branches use current observability signals and link to current mitigations;
- postmortems remain historical and do not own current operational procedure;
- ADR lifecycle/supersession is coherent when ADRs are used;
- high-risk AI-relevant constraints appear in the correct AGENTS scope without long duplicated rationale;
- mechanically preventable mistakes are enforced where justified rather than relying only on prose warnings;
- important institutional knowledge is reachable from the appropriate README/INDEX.

### Language and localization

Check:

- human docs use the selected primary language where required;
- AI operational docs remain technical English;
- translated docs exist only within the chosen localization scope;
- canonical language is identifiable;
- required translation pairs are present;
- cross-language navigation is valid;
- stale translations are marked according to policy.

## Existing tooling preference

Look for existing:

- Markdown linters;
- prose/style linters;
- link checkers;
- documentation site builds;
- doctests;
- schema validators;
- example tests;
- generated-reference checks;
- CI documentation jobs.

Use these before introducing another tool.

## New tooling threshold

A new check is justified only when it is:

- lightweight;
- stable;
- repository-appropriate;
- likely to prevent recurring drift;
- cheap enough to maintain.

Do not introduce a documentation framework, site generator, or CI dependency solely to make one audit look comprehensive.

## Final evidence report

Record what was actually done.

Good:

- `npm run docs:check` — passed.
- internal Markdown link checker — 0 missing local paths.
- onboarding commands verified through service startup; external integration step not run because credentials were unavailable.

Bad:

- "All documentation verified" when only a link scan ran.

## Failure handling

If a verification fails:

1. determine whether documentation or implementation is wrong;
2. fix the documentation when implementation is authoritative;
3. do not silently change application behavior merely to satisfy prose;
4. report an implementation defect separately when the documentation correctly describes an intended contract that the code violates;
5. rerun the relevant verification.

## Completion questions

Before declaring completion, answer yes or explicitly explain why not applicable:

- Can a new user find and complete the first-use path?
- Can a developer find setup, testing, and architecture information?
- Can an advanced user find precise reference for exposed interfaces/configuration?
- Can an operator find deployment/operations material when the project has operational responsibilities?
- Can an AI agent determine repository-wide and local constraints without reading duplicated manuals?
- Can readers navigate maintained docs without guessing filenames?
- Does each important fact have a clear owner?
- Are material claims verified or explicitly marked as unverified?
