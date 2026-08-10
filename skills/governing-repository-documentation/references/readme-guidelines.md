# README guidelines

## Role

A README is an entry point for a repository or important scope. It should help a reader understand what the scope is, why it matters, how to start, and where deeper documentation lives.

A README is not a complete manual.

## Root README

The repository-root README should normally answer, in this order where appropriate:

1. What is the project?
2. Who is it for and what problem does it solve?
3. What are its major capabilities?
4. What is its maturity/support status when relevant?
5. What prerequisites are required?
6. What is the shortest verified path to first success?
7. Where is complete documentation?
8. Where can users get help or report issues?
9. How can contributors get started, when applicable?

The first-use path should be executable and minimal. If setup is complex, link to a dedicated getting-started guide rather than embedding the whole guide.

## Important-scope README

A local README should answer:

- What does this scope own?
- What does it explicitly not own when the boundary is easy to misunderstand?
- What are the important entry points?
- How is the scope organized at a useful level?
- How does it interact with adjacent scopes?
- How do I use, develop, test, or validate it?
- Where are deeper reference or architecture documents?

Do not enumerate every file. Explain durable structure and workflows.

## Documentation-root README

The documentation-root README should explain the documentation system itself:

- audiences;
- recommended reading paths;
- documentation categories;
- canonical source and localization policy;
- contribution/maintenance expectations;
- relationship between the README and the documentation INDEX.

It should not duplicate the INDEX catalog.

## Content to move out of README

Move detailed material to dedicated documentation when it becomes substantial:

- complete API reference;
- exhaustive CLI flags;
- complete configuration tables;
- internal architecture detail;
- long troubleshooting catalogs;
- full deployment runbooks;
- release procedures;
- large extension-development guides.

Keep a short summary and link.

## Commands and examples

Every command shown in README must be checked against current repository scripts, manifests, tooling, or verified execution.

Avoid:

- placeholder package names;
- framework-default commands the repository does not expose;
- examples that depend on undocumented state;
- real credentials or secrets;
- screenshots that substitute for required textual instructions.

Prefer the shortest example that proves the project works.

## Links

Use stable repository-relative links for repository content when practical.

The README should link to:

- root INDEX;
- documentation landing/index;
- support/contribution/security information when it exists and is relevant.

Do not create a dense link dump. Let INDEX own exhaustive navigation.

## Language

Root and local README files are human-facing and follow the established human-documentation language/localization policy.

Keep code identifiers, commands, product names, and authoritative technical names unchanged.

## Maintenance test

A good README remains useful after internal file reorganization because it describes capabilities, boundaries, and stable workflows rather than implementation trivia.

If a README requires frequent edits for private refactors that do not affect users or contributors, it probably contains too much low-level detail.
