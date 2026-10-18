# Worked planning decisions

Read the closest example when the next choice resembles one of these situations. Transfer the reasoning and actions to the actual facts; do not reproduce the example's conclusion for a different task.

## Research broad enough to design, bounded enough to finish

**User task:** Explore a code search engine that could work alongside an existing code graph. Investigate alternatives and recommend an architecture.

**Context:** The graph can already answer cross-file symbol questions. Semantic retrieval may improve natural-language searches. No external vector database has been chosen.

**Misstep:** Compare ten vector databases before identifying the product's real indexing responsibilities. Produce a catalogue of benchmarks, a future evaluation plan, and no architecture.

**Useful sequence:**

1. Inspect what the existing graph parses, how it reacts to file edits, and which queries it serves. Test one representative repository query.
2. Separate the two retrieval roles: symbol and relationship navigation versus fuzzy semantic recall. Decide whether they need the same update clock and identity model.
3. Propose one coherent design with shared change detection and stable source identity where that serves both indexes; keep distinct indexes if their data and query behavior genuinely differ.
4. Compare alternatives that materially affect the choice, such as one in-process index against a remote search service at the target repository scale.
5. Deliver the chosen architecture and the one measurement that could change an unresolved capacity decision.

**Different context:** If the user explicitly requests a survey of retrieval models rather than an architecture decision, investigate the wider field and synthesize the research. Exploration is the requested outcome in that case.

## Architectural design after a visible but misleading success

**User task:** Consolidate configuration and state management without losing CLI and Web UI capabilities.

**Context:** Existing modules have several representations of the same configuration. A new `UnifiedConfigBridge` appears to make all tests pass, but every caller still owns a converter.

**Misstep:** Declare the architecture complete because the bridge makes old paths interoperable. Add tests for every converter and write a compatibility roadmap.

**Useful sequence:**

1. Trace the CLI write, service load, and Web UI read path. Locate the current mutation authority.
2. Define the canonical configuration and the owner responsible for validation and persistence. Keep genuine transport or offline-file boundaries explicit.
3. Give each caller the owner's contract and remove the redundant converters and bridges. Update the Spec's data flow accordingly.
4. Describe restart and error behavior relevant to actual use. Hand the implementer an owned design, not a compatibility matrix.

**Different context:** A shipped API with active external clients has an actual compatibility boundary. Specify its supported behavior and migration separately from the internal replacement.

## A user correction of a mistaken technical judgment

**User task:** Evaluate the value of automatically checking an installed skill's upstream version.

**Context:** The instruction says "check when the session starts". The agent previously argued that the check causes overhead "on every message" and recommended removing it.

**Misstep:** Produce a long apology and cite the governance rules that the answer supposedly violated. Announce that the agent will always remember the lesson.

**Useful sequence:**

1. Read the actual update instruction. Recognize that a session is a newly started conversation or execution session, not every message.
2. Recalculate the cost and utility at one check per session. Preserve the feature if the one request and optional update notification serve the user.
3. Replace the earlier recommendation with the corrected decision. If the question concerns why the error occurred, report the mistaken assumption and its observable effect.

**Result:** The product decision improves immediately. No retrospective policy recital becomes part of the specification.

## An example that represents a wider failure

**User task:** Improve a governance Skill that keeps adding procedural checks across different project activities. The user mentions a CLI operation that repeatedly verified hashes.

**Misstep:** Rewrite only the CLI hash rule and conclude that the governance problem is fixed.

**Useful sequence:**

1. Use the CLI case to identify the actual shared issue: a routine operation became a chain of proof activities.
2. Examine where the same behavior appears in coding tests, review loops, document editing and explanation style.
3. Put the general direction in the Constitution, the actionable mechanics in the responsible task Skills, and specific examples at the places the agent will need them.
4. Leave the CLI-specific Git guidance with the Exec role. Preserve the wider scope of the user's request.
