# Important repository scopes

## Purpose

Define where local `README.md` and `AGENTS.md` are required without creating documentation in every implementation directory.

## Core rule

Every important scope must provide:

- `README.md` for humans;
- `AGENTS.md` for AI coding agents.

The repository root is always important.

The primary documentation root is always important and additionally requires `INDEX.md`.

## Scope signals

A directory is likely important when several of these signals apply:

- It is an independently understandable application, service, package, library, SDK, plugin, provider family, adapter family, toolchain, or deployment unit.
- It has its own manifest, build, test, release, or deployment workflow.
- It exposes a public or extension interface.
- It owns durable data, schemas, migrations, protocols, or generated artifacts.
- It has a distinct security, trust, sandbox, compatibility, or operational boundary.
- It has maintainers or ownership separate from adjacent code.
- Agents or developers are expected to enter the directory directly and perform work there.
- It contains multiple subcomponents whose relationship is not obvious from names alone.
- It already has substantial local documentation or local working conventions.

No single signal automatically makes a directory important.

## Strong non-signals

Do not classify a directory as important merely because it:

- contains source files;
- has many files;
- corresponds to one namespace;
- exists under `src/`;
- contains tests mirroring source layout;
- contains generated output;
- contains third-party/vendor code;
- contains a few internal helpers;
- has a name that sounds architectural.

## Boundary test

Ask four questions:

1. **Identity:** Can this directory be described as a coherent subsystem or working area in one sentence?
2. **Autonomy:** Does a developer or agent need local knowledge to modify it safely?
3. **Discoverability:** Would a newcomer benefit materially from an entry point here?
4. **Durability:** Is this boundary likely to remain meaningful as individual files change?

If the answer is mostly no, do not create local entry-point files.

## Nested scope test

A child scope is justified when it adds meaningful local context beyond the parent.

A local README should not merely repeat the parent's module list.

A local AGENTS file should not merely repeat repository-wide commands and rules.

Nested scopes should reduce cognitive load, not multiply maintenance surfaces.

## Documentation root

Treat the main documentation directory as an important scope even when it is not executable code.

Its local files serve different purposes:

- `README.md`: explain the documentation set, intended audiences, reading paths, and maintenance model;
- `INDEX.md`: catalog maintained documentation;
- `AGENTS.md`: tell AI agents how to edit, validate, localize, and navigate documentation in that subtree.

## Examples of generic scope patterns

These patterns are illustrative categories, not required directory names:

- one deployable backend service within a monorepo;
- a public SDK package;
- a plugin ecosystem root;
- a command-line application package;
- a documentation site source tree;
- a build/release tooling area with its own workflows;
- a schema/protocol package consumed by several components.

Do not copy example names into a target repository.

## Borderline scopes

When a scope is borderline:

- prefer the parent scope if local documentation would be only a few repeated lines;
- create a local README when human discoverability has clear value;
- create a local AGENTS file when modification constraints or validation differ materially;
- avoid asking the user mid-run unless the decision changes public repository architecture significantly and no conservative choice exists.

Record uncertain borderline decisions in the final report when useful.
