# Topic documentation

## Principle

Create topic documentation from actual repository capabilities and reader needs. Do not create a fixed set of filenames merely because similar repositories have them.

For each topic, answer:

- Who needs this?
- What task or question does it serve?
- What facts does it own canonically?
- What implementation evidence verifies those facts?
- Should this be a standalone document, a section, generated reference, or link to an existing source?

## Architecture and explanation

Architecture documentation should communicate stable structure that is expensive to reconstruct repeatedly from source code.

Cover only relevant concerns such as:

- system boundaries;
- component responsibilities;
- dependency direction;
- startup/lifecycle;
- control and data flow;
- state and persistence ownership;
- concurrency/scheduling model;
- external integrations;
- extension points;
- trust, security, or sandbox boundaries;
- failure handling and recovery;
- important invariants;
- non-obvious design trade-offs.

Avoid file-by-file tours and prose mirrors of implementation.

Use architecture decision records or equivalent history only when the decision rationale has continuing maintenance value.

## API and interface reference

Prefer formal interface definitions as factual sources when available.

Verify:

- names and routes;
- signatures;
- parameters;
- request/response shapes;
- return values;
- error behavior;
- events;
- defaults;
- constraints;
- authentication/authorization expectations;
- compatibility/versioning;
- examples.

If OpenAPI, protobuf, schema files, public types, generated docs, or another machine-readable contract are authoritative, do not manually duplicate the entire contract. Human docs should add organization, semantics, examples, constraints, or decision guidance.

## CLI reference

Verify against command definitions and executable help when practical.

Document:

- command hierarchy;
- required/optional arguments;
- flags;
- defaults;
- environment/config interactions;
- exit behavior important to automation;
- examples for common tasks.

Avoid copied help output when generated help is already accessible and current; link or generate reference where appropriate.

## Configuration and environment

Document only verified configuration sources.

Cover relevant aspects:

- configuration locations;
- precedence and merging;
- defaults;
- required values;
- accepted values and types;
- environment variables;
- secrets and sensitive values;
- platform-specific differences;
- reload/restart behavior;
- example configuration.

Never commit real credentials, tokens, private endpoints, or secrets into examples.

Prefer schema-generated tables when a stable schema already owns these facts.

## Development

A developer guide should make a new contributor productive.

Verify and explain:

- prerequisites;
- repository setup;
- dependency installation;
- development/start commands;
- build;
- lint/format/type-check;
- testing;
- debugging;
- code generation;
- dependency updates;
- local services or fixtures;
- common contribution flow.

Do not repeat every root README command if a canonical developer guide already owns the full workflow.

## Testing

Testing documentation should explain the test strategy and how to execute it.

Cover applicable layers:

- unit;
- integration;
- end-to-end;
- smoke;
- contract;
- performance;
- snapshot/golden;
- documentation or example validation.

Explain fixtures, local dependencies, filtering, expected environment, and minimum validation after common change classes.

## Extension/plugin development

When the repository exposes an extension surface, document:

- extension boundary;
- lifecycle;
- supported interfaces;
- registration/discovery;
- configuration;
- compatibility/versioning;
- security/trust assumptions;
- packaging/distribution when applicable;
- minimal working example;
- validation and troubleshooting.

Do not infer extension contracts from internal implementation APIs unless they are intentionally supported.

## Data formats, protocols, and schemas

Document semantics not obvious from the formal schema:

- ownership;
- versioning;
- compatibility;
- required invariants;
- producer/consumer responsibilities;
- migration behavior;
- validation;
- examples.

Avoid manually copying large field tables when a schema generator can remain authoritative.

## Deployment and operations

Operational docs should be executable and environment-aware.

Cover only applicable concerns:

- prerequisites;
- deployment topology;
- configuration/secrets;
- startup/shutdown;
- health checks;
- migrations;
- backups/restores;
- observability;
- upgrades/rollbacks;
- incident-relevant failure states;
- resource or platform constraints.

Separate operator procedures from architecture explanation when mixing them makes either hard to use.

## Security

Security documentation may include:

- vulnerability reporting process;
- supported security-update versions;
- threat/trust boundaries;
- secret handling;
- permission model;
- secure deployment requirements;
- security-sensitive development rules.

Do not expose secrets or unsafe operational details unnecessarily.

Repository security policy files should match the hosting platform's discovery conventions when applicable.

## Release and migration

Release documentation should describe the real release workflow and validation gates.

Migration documentation should clearly state:

- source state/version;
- target state/version;
- prerequisites;
- irreversible steps;
- compatibility windows;
- rollback options;
- verification.

Do not retain obsolete release checklists as current process documentation.

## Troubleshooting

Prefer the structure:

`Symptom -> Possible cause -> How to confirm -> Resolution`

Include only problems that can still occur or historical issues explicitly needed during migration/support.

Avoid generic advice such as "restart and try again" unless it is an evidence-based resolution.


## Operational knowledge and institutional memory

Use [operational knowledge](operational-knowledge.md) for detailed role selection and lifecycle rules covering gotchas, known issues, workarounds, troubleshooting, runbooks, playbooks, architecture decision records, postmortems, and FAQ material.

Key boundaries:

- gotcha = durable non-obvious trap before/during normal work;
- known issue = current unresolved defect or limitation;
- troubleshooting = symptom-first diagnosis and resolution;
- runbook = repeatable procedure to achieve a known outcome;
- playbook = investigation/decision guidance under uncertainty, often linking to runbooks;
- ADR = rationale and consequences of a significant decision;
- postmortem = historical incident learning and follow-up, not current procedure ownership.

Do not create all of these document types for every repository. Derive them from real operational responsibilities and recurring knowledge.

## Examples and templates

Treat examples as maintained interfaces.

Verify that they:

- use current APIs and configuration;
- reference existing files and commands;
- contain no secrets;
- declare prerequisites;
- are minimal enough to maintain;
- can be tested or executed when the repository supports that workflow.

Prefer executable examples over decorative pseudocode when feasible.
