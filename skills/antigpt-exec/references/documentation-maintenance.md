# Documentation Changes

Documentation changes implement the repository's current information architecture. Existing files and paths have no preservation privilege unless a real external link, tool, publishing system, or user workflow relies on them.

## Authority

Update facts from their current authoritative source. When code, schemas, manifests, generated references, or project decisions own a fact, documentation must agree with that authority.

A stale document does not authorize changing working implementation merely to make the prose true. If the document describes an already-decided contract that implementation violates, report or repair the implementation under that contract.

## Canonical ownership

Keep one canonical owner for each important fact. Replace duplicated authoritative prose with links, projections, generated material, or narrower summaries when that reduces drift.

Move rationale with the semantic owner when a structural change makes the old document location misleading.

## Structure

Move, merge, split, archive, rewrite, or delete documents when that improves current comprehension and information ownership. Do not create `README`, `INDEX`, `AGENTS`, FAQ, runbook, playbook, ADR, or other document types merely to complete a template.

Keep current policy and operational guidance distinguishable from history, postmortems, superseded designs, generated output, and examples.

## Navigation

Maintained human documentation must be intentionally reachable from an appropriate entry point.

When documents declare reciprocal relationships in an explicit `Navigation` section, keep the link in both documents. Ordinary inline references do not require backlinks.

Use repository-relative links for repository content when practical. When moving a maintained document, update inbound navigation and other current references that rely on its path.

## AI-facing instructions

Keep AI operational instructions scoped, concise, and in technical English unless the consuming system establishes another requirement. Remove duplicated parent rules from narrower scopes. Put mechanically enforceable facts in tooling when the check is stable and worth its cost.

## Durable operational knowledge

Keep active gotchas, known issues, workarounds, runbooks, and playbooks only while they describe a live condition or responsibility. Retire resolved workarounds from the active path. Historical incidents may retain explanatory value without owning current procedure.

## Verification

Verify the claims affected by the change: local links and navigation, commands, paths, configuration names, interfaces, examples, installation steps, and AI instruction references.

Use `scripts/check_doc_graph.py` for declared human-document navigation when the repository uses that convention. Mechanical graph validity does not determine whether the information architecture itself is good.
