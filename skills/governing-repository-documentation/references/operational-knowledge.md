# Operational knowledge and institutional memory

## Purpose

Repositories accumulate knowledge that is not captured adequately by API reference, architecture diagrams, or ordinary how-to guides: recurring traps, hidden constraints, workarounds, diagnostic paths, recovery procedures, incident lessons, and the rationale behind durable decisions.

Treat this material as **operational knowledge and institutional memory**. Govern it deliberately so future maintainers and AI agents do not have to rediscover expensive lessons by trial and error.

Do not turn this category into a filename checklist. The goal is to preserve high-value knowledge in the smallest durable form with a clear owner and lifecycle.

## Core principle

**Prefer enforcement over remembrance.**

If a failure can be prevented reliably by code structure, types, validation, tests, linting, CI, generation rules, permissions, or automation, prefer that enforcement over a prose warning.

Documentation is still useful for:

- rationale that explains the constraint;
- recovery paths that cannot be fully automated;
- diagnostic judgment;
- temporary workarounds;
- cross-cutting operational context;
- knowledge that is expensive to reconstruct.

A warning that exists only because the system permits an avoidable mistake is often a signal to improve the system.

## Knowledge-role model

Use the semantic role first. Choose filenames and directory layout second.

| Role | Primary question | Typical content | Avoid using it for |
|---|---|---|---|
| Gotcha | "What non-obvious trap must I know before changing or using this?" | counterintuitive behavior, hidden constraints, dangerous assumptions, recurring traps | generic tips, ordinary setup, unresolved bug lists |
| Known issue | "What currently broken or limited behavior has not been resolved?" | active defect/limitation, affected scope, impact, workaround, removal condition | historical incidents, permanent design constraints |
| Troubleshooting | "Given this symptom, how do I diagnose and resolve it?" | symptoms, causes, checks, resolutions | architecture rationale, broad operational response coordination |
| Runbook | "How do I perform this known procedure safely and repeatably?" | deterministic operational/maintenance steps, verification, rollback, escalation | open-ended diagnosis or architecture explanation |
| Playbook | "How do I investigate and decide what to do in this class of situations?" | triage, branching diagnosis, decision criteria, escalation, links to runbooks | repeating every mitigation procedure inline |
| Architecture Decision Record | "Why did we choose this significant design?" | context, options, decision, consequences, status | current step-by-step operations, debugging diaries |
| Postmortem / incident review | "What happened, why, what was learned, and what changed?" | impact, timeline, contributing causes, response, lessons, follow-up actions | current operational procedure or active workaround owner |
| FAQ | "Which recurring simple questions deserve a short direct answer?" | genuinely repeated questions with links to canonical detail | a substitute for navigation or missing reference docs |

Repository conventions may use different names. Preserve an established coherent vocabulary when its semantics are clear.

## Placement decision sequence

When you find a piece of hard-won knowledge, classify it in this order:

1. **Can the failure be prevented mechanically?**
   - Add or strengthen enforcement where justified.
   - Keep only the minimum explanatory documentation still needed.
2. **Is this a current unresolved defect or limitation?**
   - Use the known-issue role.
3. **Is the reader starting from an observable symptom?**
   - Use troubleshooting.
4. **Is the path a known, repeatable procedure with a specific outcome?**
   - Use a runbook.
5. **Does the reader need to investigate, branch, classify, or decide under uncertainty?**
   - Use a playbook.
6. **Is it a durable, non-obvious trap that remains relevant even when the system is otherwise healthy?**
   - Use a gotcha.
7. **Is the durable value primarily why a significant decision was made?**
   - Use an ADR or equivalent decision record.
8. **Is the durable value primarily learning from a past incident?**
   - Use a postmortem/incident-review role.
9. **Is it a simple recurring question rather than a deeper knowledge class?**
   - Consider FAQ, but first verify that better navigation would not solve the problem.
10. **Is it purely local implementation context?**
   - Prefer a nearby code comment, test, assertion, type, or implementation note instead of repository-level prose.

One event can produce several durable artifacts, but each artifact must own a different job. For example, an incident may produce a historical postmortem, a new ADR, a current runbook update, and a new automated guard. Do not make the postmortem own all four roles indefinitely.

## Gotchas

### What qualifies

Capture a gotcha only when at least one of these is true:

- recurrence is reasonably likely;
- the correct behavior is counterintuitive;
- rediscovery is expensive;
- the wrong action can cause material damage, data loss, security exposure, compatibility breakage, or substantial wasted time;
- the trap has caused repeated investigations or regressions;
- an AI agent is likely to infer the wrong action from nearby code or conventions;
- a workaround or constraint must remain for a non-trivial period;
- the knowledge spans multiple files or modules and cannot be expressed locally.

Do not capture:

- one-off debugging notes with no recurrence value;
- ordinary syntax or framework behavior readers can obtain from upstream documentation;
- facts already enforced transparently and adequately by tooling;
- temporary task notes that belong in issue tracking;
- speculative warnings without evidence.

### Recommended entry shape

A durable gotcha should usually make these points discoverable:

- **Trap:** what a reasonable maintainer is likely to do wrong;
- **Why it is non-obvious:** the hidden constraint or misleading assumption;
- **Impact:** what goes wrong;
- **Correct handling:** the safe path;
- **Enforcement/detection:** tests, lint, CI, assertions, or validation when available;
- **Scope:** where the rule applies;
- **Reference:** canonical design, issue, or implementation evidence when useful.

Do not force all fields into a rigid template if a short paragraph is clearer.

### Relationship to AGENTS

A gotcha can contain detailed human rationale. `AGENTS.md` should contain only the concise actionable projection when AI agents need the constraint.

Pattern:

```text
Human knowledge: detailed explanation of the trap and rationale
        ↓
AGENTS: short MUST/MUST NOT rule + exact validation + optional link
        ↓
Automation: enforce mechanically where practical
```

Do not paste the entire gotcha into every descendant AGENTS file.

## Known issues and workarounds

A known issue represents **current unresolved reality**, not historical memory.

A useful entry should make clear, when applicable:

- affected component, platform, version, or scenario;
- observable behavior;
- impact/severity relevant to readers;
- how to confirm the issue;
- safe workaround, if one exists;
- limitations or risks of the workaround;
- upstream or internal tracking reference when appropriate;
- condition under which the entry should be removed or changed.

Treat workarounds as temporary liabilities unless the repository explicitly adopts them as permanent behavior.

When the underlying issue is fixed:

- remove the workaround from active how-to, troubleshooting, and operations docs;
- remove or mark the known issue resolved according to repository policy;
- retain historical evidence only when it has continuing explanatory value;
- migrate durable rationale to architecture/ADR if that is the surviving knowledge.

Do not maintain the same workaround independently in several documents.

## Troubleshooting

Troubleshooting is symptom-oriented diagnostic knowledge.

Prefer:

`Symptom -> Likely causes -> How to confirm -> Resolution -> Verification`

For complex problems, link from troubleshooting into a playbook rather than embedding a large decision tree repeatedly.

If a symptom has one deterministic remediation and no meaningful diagnostic branching, the resolution may link directly to a runbook.

Do not confuse a gotcha with troubleshooting:

- **Gotcha:** warns before or during normal work about a non-obvious trap.
- **Troubleshooting:** starts after an observable failure or unexpected result.

## Runbooks

A runbook codifies a known procedure to achieve a specific outcome consistently.

Use runbooks for repeatable tasks such as deployment, rollback, backup/restore, migration, credential rotation, recovery, release operations, maintenance, or other repository-specific operational procedures when those responsibilities actually exist.

A runbook should make the following discoverable where relevant:

- purpose and scope;
- prerequisites and required permissions/tools;
- safety warnings and destructive boundaries;
- ordered steps;
- expected signals/output after important steps;
- verification of the final state;
- rollback or recovery path;
- stop conditions;
- escalation path when the runbook cannot proceed safely.

For risky procedures, prefer explicit checkpoints and observable verification over narrative prose.

### Runbook automation

When a procedure becomes stable and deterministic, consider automation.

If automated:

- keep the automation source canonical for executable behavior;
- document how to invoke it safely;
- document prerequisites, permissions, validation, rollback, and failure handling that automation cannot express sufficiently;
- avoid maintaining a second manual step list that drifts from the script.

## Playbooks

A playbook is decision-oriented guidance for investigating or responding to a class of situations where the correct path depends on evidence gathered during execution.

Use playbooks for scenarios such as incident triage, failed releases, compatibility regressions, unexplained performance degradation, security-response classes, or other multi-branch operational situations **only when the repository actually owns such responsibilities**.

A playbook should usually include:

- trigger / entry criteria;
- scope and likely impact dimensions;
- required tools, permissions, or observability sources;
- first triage checks;
- decision branches based on observable evidence;
- escalation/stop conditions;
- communication expectations when operationally relevant;
- links to runbooks for known mitigations;
- exit criteria and handoff/follow-up expectations.

Keep diagnostic branching in the playbook and deterministic mitigation in runbooks. This separation reduces duplication and makes both easier to validate.

## Architecture decision records

Use an ADR or equivalent decision record for architecturally significant decisions whose rationale will matter after the original discussion disappears.

A useful ADR generally captures:

- context/problem;
- relevant requirements and constraints;
- considered options when meaningful;
- decision;
- consequences/trade-offs;
- status/lifecycle;
- links to superseding or superseded decisions when applicable.

Do not use ADRs as design guides or runbooks. They explain **why a significant decision exists**.

Prefer preserving accepted decision history. When a new decision replaces an old one, use the repository's ADR lifecycle convention rather than rewriting history so the old choice appears never to have existed.

## Postmortems and incident reviews

A postmortem is historical learning, not the canonical owner of current operational instructions.

Use it when an incident is significant enough that preserving the event, contributing causes, response quality, and follow-up learning has durable value.

A useful incident review may contain:

- impact and affected users/systems;
- incident timeline;
- detection and response;
- contributing conditions and root causes where established;
- what worked and what failed in the response;
- corrective/preventive actions;
- owners/tracking for follow-up actions when the repository/team process supports it;
- links to resulting ADRs, runbooks, tests, automation, or current docs.

Keep the review evidence-based and learning-oriented. Avoid blame-focused writing.

When incident lessons become current rules, promote them into the proper current owner:

- durable architecture rationale -> ADR / architecture docs;
- deterministic mitigation -> runbook;
- diagnostic response -> playbook / troubleshooting;
- recurring trap -> gotcha;
- preventable mistake -> test/lint/CI/automation;
- AI-specific operational constraint -> closest applicable AGENTS file.

The postmortem remains historical evidence and should not become the only place where current maintainers can find required procedures.

## FAQ

FAQ is optional and often overused.

Create or retain it only when:

- the same simple questions recur across users or maintainers;
- each answer can remain short;
- the answer can link to a canonical source for detail;
- the repetition is not primarily caused by poor navigation or unclear primary documentation.

If readers ask "Where is X documented?", repair navigation before adding an FAQ entry.

## Knowledge locality and hierarchy

Place institutional knowledge at the narrowest stable scope that owns it.

- repository-wide trap -> repository documentation knowledge surface;
- subsystem-specific trap -> that important scope's documentation;
- operational procedure owned by one service/deployment unit -> near that operational scope;
- cross-cutting incident-response process -> central operations documentation;
- local implementation quirk -> code/test/comment unless cross-cutting or costly to rediscover.

Do not centralize every gotcha merely for discoverability. Use `INDEX.md`, local README links, or a documentation catalog to expose distributed knowledge.

Conversely, do not scatter cross-cutting operational policy across many local files.

## Choosing a physical layout

Choose layout from knowledge volume, ownership boundaries, and reader workflows.

### Small corpus

Prefer sections inside existing maintained documents when only a few entries exist.

Example role mapping:

```text
docs/
├── README.md
├── INDEX.md
├── AGENTS.md
├── TROUBLESHOOTING.md   # if symptom-oriented knowledge is substantial
└── MAINTENANCE.md       # may include a small number of procedures/gotchas
```

The names are examples, not requirements.

### Medium corpus

Separate only roles that have distinct owners or maintenance cycles.

```text
docs/
├── README.md
├── INDEX.md
├── AGENTS.md
├── engineering/
│   ├── README.md
│   ├── AGENTS.md
│   └── <gotchas / known limitations / maintenance knowledge as justified>
├── operations/
│   ├── README.md
│   ├── AGENTS.md
│   └── <runbooks / playbooks / troubleshooting as justified>
└── decisions/
    ├── README.md
    ├── AGENTS.md
    └── <decision records>
```

Create local `INDEX.md` only when those collections become complex enough to need one.

### Large corpus

Use collections when search, ownership, or lifecycle requires them, for example separate runbook, playbook, decision, or incident-history collections. Every important documentation sub-scope still follows the repository's README/AGENTS rules, and complex collections should be reachable from the documentation index.

Do not add empty category directories in anticipation of future knowledge.

## Lifecycle and state

Operational knowledge decays quickly. During maintenance, verify whether each active warning or procedure is still true.

Use status only when it communicates real lifecycle information. Typical semantics include:

- **Active:** currently applicable;
- **Temporary:** current but expected to be removed when a known condition changes;
- **Deprecated:** still relevant during transition but not for new usage;
- **Resolved:** issue/workaround no longer active;
- **Historical:** retained only for chronology, rationale, or learning.

Do not force status metadata onto every entry.

For temporary knowledge, prefer an explicit **removal condition** over a vague statement such as "remove later".

Examples of removal conditions:

- remove when the upstream defect is fixed and the minimum supported version includes the fix;
- remove after the migration window closes;
- remove once CI prevents the unsafe operation;
- replace after the new deployment workflow becomes canonical.

## Knowledge promotion and retirement

Institutional knowledge should move as reality changes.

Typical transitions:

```text
incident observation
    -> postmortem
    -> durable lesson identified
        -> ADR / gotcha / playbook / runbook / automation

known issue
    -> workaround
    -> fix lands
        -> remove active workaround
        -> preserve only durable rationale/history if useful

gotcha
    -> repeated failure
    -> mechanical guard added
        -> remove or reduce warning
        -> keep only rationale if still useful

manual runbook
    -> stable repeated procedure
    -> automation
        -> automation becomes executable source
        -> documentation retains invocation/safety/verification
```

Do not preserve obsolete active warnings merely because they once prevented a real incident.

## Discovery signals for hidden institutional knowledge

During bootstrap or a deep maintenance audit, look selectively for knowledge trapped outside the formal documentation system.

Useful signals include:

- `FIXME`, `HACK`, `WORKAROUND`, `TEMPORARY`, warning, or caveat comments;
- tests named after regressions or incidents;
- unusual CI ordering requirements or commented exceptions;
- scripts that contain safety checks or non-obvious sequencing without explanation;
- issue or incident references in code/comments;
- repeated troubleshooting sections across READMEs;
- "pitfall", "warning", "known limitation", "lesson", "do not", or "must run from" prose;
- commit history when a suspicious constraint lacks current rationale;
- archived incident notes or design discussions when they explain a still-active rule.

These are discovery signals, not instructions to copy text into docs. Validate recurrence value and current applicability before promoting anything.

Do not perform broad issue-tracker or deep Git archaeology unless the task scope, risk, or unresolved evidence justifies it.

## Canonical ownership relationships

Avoid making historical or diagnostic material own current facts accidentally.

| Knowledge | Canonical current owner | Historical/supporting surfaces |
|---|---|---|
| Current deterministic procedure | runbook or automation | postmortem may explain origin |
| Incident diagnosis decision path | playbook | troubleshooting may link to it |
| Current defect/workaround | known-issue owner | issue tracker may track work |
| Durable hidden constraint | gotcha + enforcement where possible | incident/commit may explain origin |
| Significant design rationale | ADR / architecture decision log | postmortem may reference it |
| Current AI constraint | nearest applicable AGENTS | human gotcha/architecture explains rationale |
| Past incident | postmortem | current docs link only when useful |

Issue trackers, commit messages, and chat logs are evidence and work coordination, not reliable substitutes for maintained repository documentation.

## Validation

Before treating operational knowledge as governed, check:

- every active gotcha still applies;
- active known issues are still unresolved;
- workarounds remain necessary and safe;
- runbook commands and prerequisites still exist;
- playbook branches point to current signals and mitigations;
- current procedures are not owned only by historical postmortems;
- ADR status and supersession links are coherent when ADRs are used;
- high-risk agent-relevant gotchas are projected into the correct AGENTS scope without excessive duplication;
- automatable rules are not left as prose-only warnings without justification;
- obsolete warnings have been removed from active navigation;
- important operational knowledge is discoverable from the appropriate README/INDEX.
