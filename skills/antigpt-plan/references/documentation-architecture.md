# Documentation Architecture

Treat repository documentation as an information system. Design it around readers, authoritative knowledge, and navigation instead of a filename template.

## Model the information

Identify only the dimensions that affect the current repository:

- audiences and the tasks they need to complete;
- canonical owners of important facts;
- current, historical, generated, and operational information;
- human-facing and AI-facing instruction surfaces;
- navigation relationships;
- localization requirements that actually exist.

Do not require `README`, `INDEX`, `AGENTS`, or any other document type merely for symmetry. Create a document when it owns a real information responsibility.

## Canonical ownership

Give each important fact one canonical owner. Other documents may link, summarize, project, or generate from that owner. Avoid several authoritative-looking copies of commands, configuration, contracts, architecture facts, or policies.

When the authoritative fact already lives in code, schema, manifest, generated reference, or another machine-readable source, prefer projection or a precise link over manually duplicating it.

## Current and historical knowledge

Keep current authority easy to distinguish from history, superseded design, examples, experiments, postmortems, and generated material. Historical documents may preserve rationale without remaining on the active authority path.

## Human and AI surfaces

Human-facing documentation optimizes comprehension, task completion, and navigation.

AI-facing instructions optimize scope, authority, precise behavior, trigger quality, and context cost. Keep operational AI instructions concise and use technical English unless the consuming system establishes another requirement.

## Navigation

Readers should reach maintained human documentation through intentional links rather than filename guessing. Use explicit navigation sections where reciprocal relationships are useful.

A declared navigation edge may be mechanically checked for reciprocity. Ordinary inline citations and contextual references do not create backlink obligations.

## Localization

Introduce multilingual structure only when the repository actually serves multiple language audiences. Establish a canonical source language or another clear ownership rule when translations are maintained. Avoid translating AI instructions merely for visual symmetry.
