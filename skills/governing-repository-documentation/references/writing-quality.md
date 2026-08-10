# Technical writing quality

## Write for a defined job

Before drafting a section, identify what the reader should understand or accomplish after reading it.

Remove information that belongs to a different job or link to its canonical owner.

## Titles and headings

Use descriptive, scannable headings.

For human technical documentation:

- keep one clear document title;
- maintain logical heading hierarchy;
- avoid skipping levels;
- use task-oriented headings for procedures;
- use concept-oriented headings for explanations;
- avoid decorative numbering unless the repository style requires it.

Preserve stable anchors or update inbound links when changing commonly linked headings.

## Procedures

A procedure should state:

- prerequisites;
- ordered steps;
- exact commands/inputs where needed;
- expected results;
- validation;
- important failure conditions or alternatives.

Use numbered lists when sequence matters.

Do not bury required steps inside explanatory paragraphs.

## Lists and tables

Use lists for sequences or simple sets.

Use tables when readers need to compare multiple properties across items.

Keep list items parallel in grammar and level of detail.

Avoid giant tables when the underlying data can be generated or queried more reliably.

## Examples

Examples should be:

- correct;
- minimal;
- representative;
- copyable when intended for execution;
- explicit about prerequisites;
- free of secrets and private data.

Show expected output when it helps readers verify success.

Do not use examples to define behavior that the reference documentation contradicts.

## Terminology

Use one term for one concept.

Maintain project naming, capitalization, and authoritative identifiers consistently.

Do not invent translations for established technical identifiers.

When a term is specialized and necessary, define it once in the appropriate human-facing document.

## Clarity

Prefer concrete statements over vague qualifiers.

Weak:

- "Usually configure this appropriately."
- "Run the relevant tests."

Strong:

- state the exact condition;
- name the canonical configuration source;
- give the verified command or link to the maintained testing procedure.

Do not over-explain obvious syntax at the cost of the actual workflow.

## Accessibility and global audiences

For human-facing docs:

- do not rely on color or visual position alone to convey meaning;
- use descriptive link text;
- provide useful alt text for meaningful images when supported;
- keep sentences and headings easy to scan;
- avoid culture-specific idioms when they reduce clarity;
- preserve code and identifiers exactly.

When localizing, write naturally for the target language rather than preserving awkward source-language sentence structure.

## Screenshots

Use screenshots only when the visual interface is itself important.

Do not use screenshots as the sole source for:

- commands;
- paths;
- configuration values;
- text that readers must copy;
- critical procedural steps.

Screenshots drift quickly. Prefer textual instructions with screenshots as optional support.

## Comments and inline documentation

Code comments and docstrings are not substitutes for repository documentation.

Use inline documentation for behavior closest to an API or implementation when that is the language/framework convention.

Use repository docs for cross-cutting workflows, architecture, user journeys, and information that spans modules.

## Concision versus completeness

Concision means removing duplication and irrelevant detail, not omitting prerequisites or validation.

A short document that leaves readers unable to complete a task is not high quality.

A long document that mixes tutorial, reference, architecture, and troubleshooting without navigation is also not high quality.
