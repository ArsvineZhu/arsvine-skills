# Behavioral validation scenarios

These scenarios are maintainership tests for the Skill. They are not runtime instructions and are intentionally not linked from `SKILL.md`.

Run them with a fresh agent context when changing the Skill. Compare behavior without the Skill and with the Skill enabled. A real pressure test is stronger than static inspection.

## Scenario 1: Early decision batching

### Prompt

> Audit and reorganize all documentation in this large monorepo. I may be away from the computer while you work.

### Pressure

The repository has mixed English and Chinese human docs, partial localization, and no explicit statement about whether the user wants one or both languages maintained.

### Expected behavior with Skill

- Announces a short bounded preflight before deep work.
- Performs only shallow inspection sufficient to detect the language/localization issue and obvious repository scopes.
- Returns promptly with one decision packet.
- Asks primary human-documentation language and localization scope together, with defaults.
- Includes mode only if materially ambiguous.
- Does not start a long source/API audit before this confirmation.

### Failure conditions

- Asks only language, then begins deep work and later asks about localization.
- Performs exhaustive repository analysis before asking.
- Silently chooses a language despite the unresolved mixed corpus.

## Scenario 2: Late uncertainty should not block

### Prompt

> Continue the full documentation audit using the decisions we already confirmed.

### Pressure

Midway through the audit, an old internal design note has unclear archival value.

### Expected behavior with Skill

- Uses a conservative reversible choice, such as preserving and marking/reclassifying it when safe.
- Records the uncertainty for the final report.
- Does not stop execution unless the choice is destructive/material, unresolved by evidence, and lacks a safe default.

### Failure conditions

- Stops and asks whether to delete one ambiguous historical note.

## Scenario 3: Maintenance mode minimalism

### Prompt

> Check docs after this week's code changes and fix anything stale.

### Pressure

The repository already has a coherent documentation site, but its file naming differs from the Skill's examples.

### Expected behavior with Skill

- Selects maintenance mode.
- Starts from changed implementation surfaces.
- Preserves coherent existing information architecture.
- Repairs drift and navigation without imposing a new tree.

### Failure conditions

- Renames or reorganizes the documentation corpus merely to match generic conventions.
- Creates many new topic files unrelated to the changes.

## Scenario 4: No project-specific template leakage

### Prompt

> Bootstrap documentation for a small library with a CLI and configuration file.

### Pressure

A previous project used many specialized documents for unrelated features.

### Expected behavior with Skill

- Creates only topic documentation justified by this repository.
- Uses mandatory generic entry points and derives other docs from actual capabilities.
- Does not reuse filenames or categories from unrelated projects.

### Failure conditions

- Creates documents for absent capabilities because they appeared in a prior repository or example.

## Scenario 5: Important-scope discrimination

### Prompt

> Make sure important directories are documented.

### Pressure

The repository contains 80 internal source directories, 4 independently built packages, a documentation root, generated output, and vendor code.

### Expected behavior with Skill

- Treats root and documentation root as important.
- Classifies the independently meaningful packages as likely important after evidence review.
- Requires README and AGENTS in important scopes.
- Does not create README/AGENTS in all 80 implementation directories or generated/vendor areas.

### Failure conditions

- Equates directory count with documentation scopes.

## Scenario 6: AGENTS inheritance and context discipline

### Prompt

> Add AGENTS files throughout the monorepo so Codex knows how to work in each package.

### Pressure

The root already defines package manager, test command, formatting, and public API rules. One package has only a different integration-test command.

### Expected behavior with Skill

- Reads ancestor instructions before writing local ones.
- Local AGENTS adds the scope boundary and package-specific integration-test rule without copying all root rules.
- Verifies current Codex override/discovery behavior before relying on `AGENTS.override.md`.
- Keeps AI-facing instructions in technical English.

### Failure conditions

- Copies the full root AGENTS into every package.
- Uses localized human prose in operational AGENTS files.

## Scenario 7: Canonical ownership and conflicting docs

### Prompt

> README says one configuration default, docs say another, and the schema says a third. Fix the documentation.

### Pressure

The easiest action is to pick one prose document and update the others.

### Expected behavior with Skill

- Investigates executable/configuration/schema evidence.
- Determines which source is authoritative/current.
- Establishes one canonical documentation owner.
- Removes or minimizes duplicated tables in secondary docs.
- Reports unresolved implementation inconsistency instead of inventing behavior.

### Failure conditions

- Trusts the newest-looking prose without verifying repository behavior.

## Scenario 8: Verification claims

### Prompt

> Finish the docs work and tell me whether everything is correct.

### Pressure

The environment lacks credentials for an external integration and cannot execute one example end-to-end.

### Expected behavior with Skill

- Runs available checks.
- Distinguishes commands found from commands actually executed.
- Reports the blocked external integration as unverified.
- Does not claim complete verification.

### Failure conditions

- Says all examples pass when one was not executed.

## Scenario 9: Multilingual scope containment

### Prompt

> I want Chinese and English documentation.

### Pressure

The repository has 50 developer/internal documents and only 5 user-facing entry/how-to documents.

### Expected behavior with Skill

- Uses preflight to ask translation coverage and canonical language in the same decision packet.
- Does not assume all 50 documents must be translated.
- Keeps AGENTS, Skills, and AI operational policies in technical English.
- Encodes a synchronization policy for the selected translated subset.

### Failure conditions

- Automatically doubles every Markdown file.
- Creates translated AGENTS or SKILL files for human convenience.

## Scenario 10: Institutional knowledge is not a filename checklist

### Prompt

> We have recurring engineering traps and operational procedures. Add GOTCHAS, PLAYBOOK, RUNBOOK, KNOWN_ISSUES, FAQ, and postmortem docs everywhere they might be useful.

### Pressure

The repository is a medium-sized library with one deployment tool, two recurring developer traps, one current known limitation, and no incident-response responsibilities.

### Expected behavior with Skill

- Models the underlying knowledge roles before choosing filenames.
- Captures the two durable non-obvious traps as gotcha knowledge at the narrowest stable scope.
- Captures the unresolved limitation as a known issue with a workaround/removal condition if one exists.
- Creates or extends a runbook only for the real repeatable deployment procedure.
- Does not create playbooks, incident postmortems, or FAQ merely for symmetry.
- Preserves a compact documentation topology and links the knowledge from appropriate indexes/READMEs.

### Failure conditions

- Creates every named document because the prompt listed them.
- Treats all troubleshooting notes as gotchas.
- Creates incident-response material for a repository with no such responsibility.

## Scenario 11: Gotcha versus enforcement

### Prompt

> Developers keep forgetting that generated protocol files must not be edited directly. Put it in GOTCHAS.md so people remember.

### Pressure

The repository can reliably detect direct edits in CI and the generator source is known.

### Expected behavior with Skill

- Prefers machine enforcement over relying only on memory.
- Keeps concise human rationale only if it remains useful.
- Projects the actionable constraint into the closest applicable AGENTS file when AI agents could make the same mistake.
- Does not duplicate a long explanation across README, AGENTS, and GOTCHAS.

### Failure conditions

- Adds only a warning paragraph and leaves an automatable failure unenforced.
- Copies the full gotcha into multiple AGENTS files.

## Scenario 12: Playbook versus runbook

### Prompt

> Document what to do when production requests start timing out.

### Pressure

Diagnosis has several branches; once the root cause is known, each mitigation is a deterministic procedure.

### Expected behavior with Skill

- Uses a decision-oriented playbook for investigation/triage.
- Uses or links deterministic runbooks for known mitigations.
- Avoids duplicating the full mitigation procedure into every diagnostic branch.
- Includes stop/escalation criteria when the diagnosis cannot be completed safely.

### Failure conditions

- Calls every operational document a runbook.
- Produces one giant procedure that mixes diagnosis, decision-making, and mitigation without boundaries.

## Scenario 13: Historical learning versus current guidance

### Prompt

> We had a serious outage last year and there is a long incident write-up. Make sure future maintainers do not repeat it.

### Pressure

The incident's immediate workaround is obsolete, but it caused one durable architectural decision and one new operational check.

### Expected behavior with Skill

- Keeps the postmortem historical rather than presenting obsolete remediation as current guidance.
- Promotes the durable architectural rationale into an ADR or current architecture documentation when appropriate.
- Promotes the current operational check into the relevant runbook/AGENTS/automation surface.
- Links historical evidence without making the postmortem the canonical owner of current procedures.

### Failure conditions

- Treats the old postmortem as the current operations manual.
- Deletes all incident history and loses decision rationale.

## Scenario 14: Knowledge lifecycle and stale workaround

### Prompt

> Audit our docs for stale engineering knowledge.

### Pressure

A known issue was fixed months ago, a workaround remains in three documents, and a gotcha is now prevented by a linter.

### Expected behavior with Skill

- Verifies whether the issue and gotcha still apply.
- Removes or archives obsolete active warnings from current navigation.
- Removes duplicated workaround instructions.
- Keeps historical evidence only where it has continuing explanatory value.
- Updates canonical sources and synchronization rules so stale warnings do not remain active.

### Failure conditions

- Keeps all warnings indefinitely because they were once true.
- Deletes history that still explains an architectural decision.
