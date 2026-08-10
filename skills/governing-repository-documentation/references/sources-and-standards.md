# Sources and standards

## Purpose

Use these sources as external guidance for Skill mechanics and general documentation practice. They do not override the user's explicit requirements, repository-local policy, or verified repository behavior.

Platform behavior and standards can change. When internet access is available and a platform-specific detail matters, verify the current official source instead of relying indefinitely on this snapshot.

Last reviewed: 2026-08-10.

## Agent Skills

### OpenAI: Build skills

https://learn.chatgpt.com/docs/build-skills

Relevant principles:

- Skills package reusable instructions, resources, and optional scripts.
- Skill loading uses progressive disclosure.
- `SKILL.md` contains required metadata and instructions; scripts, references, assets, and OpenAI metadata are optional.
- Descriptions affect implicit invocation and should have clear scope/boundaries with important trigger terms early.
- Keep each Skill focused on one job.
- Prefer instructions over scripts unless deterministic behavior or external tooling is needed.
- Use imperative steps with explicit inputs and outputs.
- Test triggering behavior.

### Agent Skills open specification

https://agentskills.io/specification

Relevant constraints:

- directory name must match Skill `name`;
- name uses lowercase letters/numbers/hyphens and has a 64-character limit;
- description is required and has a 1024-character limit;
- referenced resources should remain focused and load on demand;
- progressive disclosure recommends keeping `SKILL.md` below 500 lines;
- use relative references from the Skill root and avoid deep reference chains;
- optional `scripts/`, `references/`, and `assets/` directories have conventional roles.

## AGENTS.md and Codex

### OpenAI: Custom instructions with AGENTS.md

https://learn.chatgpt.com/docs/agent-configuration/agents-md

Relevant Codex behavior at review time:

- project instructions are discovered from the project root toward the current working directory;
- `AGENTS.override.md` takes precedence over `AGENTS.md` within the same directory;
- at most one candidate instruction file per directory is included;
- root-to-leaf guidance is concatenated so deeper guidance is later in the effective prompt;
- combined project instructions have a configurable size limit;
- specialized rules should live near the code they govern;
- concise behavioral rules are preferred, while formatting/lint rules are better enforced by CI when possible.

Do not assume another AI coding platform uses identical discovery semantics.

## Documentation architecture

### Diátaxis

https://diataxis.fr/

Relevant principles:

- distinguish tutorials, how-to guides, reference, and explanation by user need;
- documentation architecture should emerge from improving real content rather than creating empty four-part structures;
- mixing different documentation jobs is a common source of poor documentation.

This Skill uses these as conceptual information classes, not mandatory directories.

## Repository entry documentation

### GitHub Docs: About the repository README file

https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes

Relevant principles:

- README is a primary repository landing surface;
- it commonly explains project purpose, value, getting started, help, and maintainers/contributors;
- longer documentation belongs outside the README;
- repository-relative links are supported and useful.

### GitHub Docs: Community health files

https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file

Relevant principles:

- `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, governance, and community files have specific jobs;
- these files should be created when the repository needs those jobs, not merely for checklist symmetry.

## Technical writing

### Google developer documentation style guide

https://developers.google.com/style

Useful areas include headings, lists, accessibility, global audiences, links, examples, and terminology.

Relevant principles adopted here:

- prioritize project-specific rules first;
- use descriptive hierarchical headings;
- match list/table form to information structure;
- prefer clear and consistent terminology;
- write for accessibility and global readers.

The Skill does not require Google-specific house style. Use it as secondary writing guidance after repository and user requirements.

## Operational knowledge, runbooks, and playbooks

### AWS Well-Architected: Use runbooks to perform procedures

https://docs.aws.amazon.com/wellarchitected/latest/framework/ops_ready_to_support_use_runbooks.html

Relevant principles:

- a runbook is a documented process for a specific outcome;
- procedures should be repeatable and maintained as the process evolves;
- useful runbooks cover error handling, required tools/permissions, exceptions, and escalation;
- stable procedures are candidates for automation.

### AWS Well-Architected: Use playbooks to investigate issues

https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_ready_to_support_use_playbooks.html

Relevant principles:

- a playbook guides investigation and scoping of an incident or issue;
- playbooks should define required tools/permissions, communication/escalation where applicable, and diagnostic steps;
- once a known root cause is identified, a playbook can point to a runbook for mitigation;
- operational knowledge should not remain only as team muscle memory.

This Skill generalizes these roles beyond AWS-specific operations and does not require cloud infrastructure.

## Incident learning

### Google SRE: Postmortem Culture — Learning from Failure

https://sre.google/workbook/postmortem-culture/

Relevant principles:

- postmortems preserve incident impact, causes, response, and follow-up learning;
- conclusions should be evidence-based;
- follow-up actions need clear ownership in organizations that use an ownership process;
- widely discoverable incident learning reduces repeated rediscovery;
- postmortems are historical learning artifacts, not substitutes for current operational procedures.

## Architecture decisions

### Google Cloud: Architecture decision records overview

https://docs.cloud.google.com/architecture/architecture-decision-records

### AWS Prescriptive Guidance: Architectural decision record process

https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html

Relevant principles:

- ADRs capture significant decisions, their context, and consequences;
- they preserve why a design exists, not merely how it is implemented;
- decision records should have an explicit lifecycle when the repository adopts an ADR process;
- superseding a decision should preserve useful history rather than silently rewriting it.
