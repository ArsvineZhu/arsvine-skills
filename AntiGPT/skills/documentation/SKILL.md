---
name: documentation
description: Write, restructure, or maintain product, developer, and AI-facing documentation; correct defensive GPT prose using a deterministic scanner; repair document navigation, author voice, duplicated authority, and append-only or memorial edits. Use for documentation and agent-instruction work.
---

# Documentation

Apply the active AntiGPT Constitution and Plan or Exec Skill. Own the reader-facing document, its structure, and the correction of GPT's persistent writing patterns. Use the included deterministic prose scanner during maintained documentation work.

## Identify author and reader

Before writing, determine who is speaking, who will read it, what the document enables them to do, and the established voice and language. This reasoning shapes the document; it should not be announced in the final copy.

- Product and user documentation: serve the user with capabilities, setup, interaction, and outcomes in the user's language or requested language.
- Developer documentation: explain architecture, APIs, extension points, configuration, and relevant commands at the level useful to contributors. Follow the user's language or requested language.
- AI-facing instructions, AGENTS files, Skills, and operational indexes: use concise technical English. Include actual non-obvious owners, commands, constraints, and authoritative entrypoints. Avoid generic coding advice, historical narration, invented gates, and boilerplate assurances.

Adopt the requested author's perspective. A personal narrative can use first person; technical product documentation usually speaks about the product and its users. Do not prefix each sentence with the author's name or "I" merely because the task says to write from their perspective.

## Edit the target, not the correction history

Correct text **in place**. Replace the superseded sentence or section with the intended current content. When a user removes an incorrect item, erase the item and its obsolete support text. Do not replace it with a parenthetical negation, warning about the old mistake, "formerly" monument, or empty stub.

Do not elevate a correction of one paragraph, document, or task into a permanent cross-repository rule. Repetition or emphasis does not expand the correction's scope. Keep the corrected final artifact clean; avoid repeatedly reporting that the discarded content remains absent.

Put new information into the section it belongs to. Rewrite or remove the old explanation rather than append changes at the bottom. Keep terminal navigation after substantive content, and use in-text links when they serve a specific paragraph.

## Give information a clear owner and route

Maintain one canonical owner for each enduring fact or procedure. Link other pages to it or derive their content from it. Separate current implementation, approved target design, and historical background where useful. Reorganize flat directories and unrelated scripts into semantic groups as the information architecture grows.

Keep human documents discoverable through maintained entrypoints and intelligible parent/related links. Navigation is a reading path, not a collection of exhaustive crosslinks. When a project maintains explicit reciprocal terminal navigation, maintain both ends of changed links. Use `scripts/check/doc_graph.py` for a repository with a `.docgraph.toml` describing those pages; do not impose this navigation convention on a different docs system.

Use descriptive section and file names. Do not invent opaque stage or rule labels such as `R-01` or `S2`. Existing external issue/PR identifiers and real protocol versions remain as they are. Avoid manual inventories of hashes or UUIDs where human navigation already has a descriptive link or path.

## Enforce language with the bundled scanner

Prompted language discipline is imperfect. The tool at `scripts/check/governance_prose.py` checks maintained prose for recognizable defensive negations, fabricated contrasts, unnecessary self-positioning, speculative deferrals, and related patterns. Its configuration is `scripts/config/scanner.toml`.

After authoring or editing prose, run the scanner on the affected maintained files, for example:

```bash
python <documentation-skill-path>/scripts/check/governance_prose.py README.md AGENTS.md docs/
```

Inside a Git working tree, `--changed` scopes the scan to edited and untracked files. The scanner joins soft-wrapped prose within paragraphs, retains quoted prose, skips fenced code, and reports source locations. `--format json` returns findings, waivers, and operational errors.

Use rule severity to choose the next action:

- `block`: inspect the flagged construction and either correct it or give a narrow waiver for a justified use.
- `review`: read the passage in context. Preserve genuine uncertainty, technical distinctions, and authorial opinion; remove unsupported hedging, invented obligations, and self-defence.
- `signal`: a weak cue for attention, such as a cautionary preface. Keep it only when it contributes to the reader's decision.

The configured rules cover defensive conclusions, invented contrasts, judgment weakening, speculative deferral, hypothetical compatibility, correction memorials, and process substituted for implementation. Judge the proposed action against the user's objective; do not infer architecture quality from a count of matched words.

For intentional examples or necessary distinctions, place a named waiver with a concrete reason immediately before the affected prose unit:

```html
<!-- antigpt: allow rule=defensive-negation-en reason="Quoted bad example teaches the failure pattern" -->
```

Consecutive waivers for different rules apply to that same next unit. Unknown, duplicate, unused, or dangling waivers are errors. A quotation or a `Bad:` label alone does not exempt text. Keep examples and their explanations intact; identify their teaching purpose in the waiver.

Keep the existing checker, configurable patterns, and valid waiver support. Improve detections for observed failures; do not replace the checker with a request that the same model merely promises better wording. The check edits no source files; fix the actual prose at its owner.

## Finish as the reader

Read the changed document as its intended audience. The central information must be findable, terminology must match its real meaning, and the reader must be able to navigate onward or back. Use the repository's existing link checker where relevant. Deliver the corrected text and navigation, then stop; no separate writing-quality score or self-evaluation dossier is needed.
