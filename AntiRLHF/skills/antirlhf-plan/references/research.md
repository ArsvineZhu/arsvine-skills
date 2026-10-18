# Research that changes understanding or decisions

Use this guide for literature reviews, technical investigations, scientific questions, and exploratory architecture research. The result may be a new model, a choice, a set of findings, or an experiment design. Investigate deeply when discovery itself is the task.

## Begin with the question the research must answer

Write the actual open question in working context. For a design choice, identify the alternatives and the facts on which the choice depends. For exploratory research, identify what needs to be understood or discovered; several lines of inquiry may be justified even before a final design is possible.

Find primary sources where possible: specifications for required behavior, current source code for library semantics, technical papers for research claims, and real user reports for experienced failures. Distinguish the source's finding from your interpretation. Preserve the user's supplied material as the basis for their question; add external sources when the user asks for investigation or external verification helps the decision.

## Follow an investigation to a useful result

When new evidence reveals an architectural problem, update the working model and follow the question it opens. When new papers repeat an already established finding, move toward synthesis. Keep important disagreement and mechanisms that could change the answer. Do not keep searching solely to increase the source count.

A search can be useful even without changing the immediate design if the user asked to map an emerging area, examine competing theories, or gather research material. The stopping point is a sufficiently developed account of that requested subject.

### Example: researching a new code retrieval architecture

**Task.** Decide whether a code graph and semantic search should share an indexing pipeline.

**Useful investigation:** inspect how each tool extracts symbols, tracks code changes, stores relationships, ranks results, and serves agent queries. Determine whether they share a durable source of truth and which part has to change when a file is edited. Try representative cross-file queries if the choice depends on retrieval quality.

**Decision:** if graph edges and semantic chunks have independent update costs and retrieval roles, allow separate indexes while sharing the file-change source and stable symbol identity where feasible. If both tools duplicate the same parser, examine reusing one parsing layer. Design by *real shared responsibility*, not by the label "unified retrieval system."

**Unproductive continuation:** enumerate every retrieval benchmark, introduce a multi-stage evaluation platform, then stop before deciding the indexing ownership. A particular experiment is useful only if it can distinguish the live alternatives.

## Design an experiment to discriminate

When evidence cannot settle a material choice, design an observation that would actually change it. For algorithm or architecture questions, keep the variable relevant to the hypothesis and compare outcomes on the same task conditions. For an implementation already selected, use a targeted experiment only if the unknown affects whether it can satisfy the requirements.

Example: a local vector index may work well enough for small repositories. Before proposing an external database, measure update cost, memory, and query latency at a representative repository size. Decide what result would trigger the external option. No standing evaluation platform is necessary for a single design question.

## Report research in a useful form

Lead with discoveries and their implications. Give concrete source links and dates where the claim depends on them. Record disagreements that change the working model, relevant limitations near the result they qualify, and next experiments when they serve an open question. Put background context after the result rather than substituting a long account of research effort for the result.

When the user wants a research archive rather than an immediate design, preserve important hypotheses and source provenance *in the archive*. Write operational Agent instructions separately as direct actions.
