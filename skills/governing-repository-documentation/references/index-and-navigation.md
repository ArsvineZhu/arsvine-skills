# INDEX and navigation

## Role separation

`README.md` and `INDEX.md` have different jobs.

- README: orient, explain, and help the reader start.
- INDEX: map, catalog, and route the reader to authoritative material.

Do not duplicate the same prose in both files.

## Root INDEX

The root `INDEX.md` is a repository map.

It should expose, as applicable:

- major top-level areas;
- important scopes;
- applications/services/packages and their roles;
- documentation locations;
- examples or tooling areas;
- generated/vendor/archive areas;
- areas that should not be edited directly;
- stable entry points for deeper navigation.

Describe boundaries and destinations, not every file.

A reader should be able to answer "where does this concern live?" after scanning the root INDEX.

## Documentation INDEX

The primary documentation-root `INDEX.md` is the authoritative catalog of maintained documentation.

Organize it by reader goal, audience, or topic, for example conceptually:

- start using the project;
- accomplish common tasks;
- understand architecture;
- develop and test;
- look up interfaces/configuration;
- extend the system;
- deploy or operate it;
- troubleshoot;
- find active gotchas, known limitations, runbooks, or playbooks when they exist;
- contribute or release;
- understand architecture decisions and historical incident learning when maintained.

Do not force categories that have no documents.

## Local INDEX

Create a local INDEX only when a scope contains enough documentation or subcomponents that README navigation becomes unwieldy.

A local INDEX is justified when it solves a real discovery problem.

Do not create:

- one-line indexes;
- automatically mirrored file listings with no semantic grouping;
- an INDEX in every important scope merely for symmetry.

## Navigation graph requirements

Every maintained document should be discoverable from an appropriate entry point.

Check for:

- orphan documents with no inbound navigation;
- links to obsolete or renamed docs;
- several competing "main" indexes;
- loops that never lead back to a higher-level map;
- duplicated catalogs that drift independently.

## Link style

Prefer repository-relative links for repository content when practical.

Use descriptive link text. Avoid bare "here" links when the destination can be named.

When moving a document:

1. update inbound links;
2. update indexes;
3. preserve stable public links when the documentation platform supports redirects or aliases;
4. verify downstream references in examples, issue templates, and agent instructions.

## Generated indexes

Use generated navigation only when the repository already has or clearly benefits from a stable generation workflow.

Do not introduce a generator just to avoid maintaining a small semantic index.

Generated indexes should not replace curated explanations of why scopes matter.

## Navigation quality test

A strong navigation system allows three common readers to succeed without opening the raw file tree:

- a new user looking for first use;
- a developer looking for a subsystem or development procedure;
- an operator or advanced user looking for a precise reference, active limitation, runbook, playbook, or troubleshooting path.

If any of these requires guessing filenames, navigation is incomplete.
