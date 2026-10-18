---
name: documentation
description: Author and edit product, developer, research, and agent-facing documentation. Use for author voice, editing existing prose, document structure, navigation, and AntiRLHF's prose checker.
---

# Documentation and authorial voice

Follow the active AntiRLHF Constitution and the active role instructions. Read the document being edited before rewriting it. Identify its author, reader, purpose, and source of facts from the actual document and the user's request.

## Write from the right position

- **Author's README, essay, article or announcement:** write as the author speaking to their readers. Preserve characteristic judgments, humor, emphasis and first-person voice. Change the portion the user asked to change; retain distinctive original writing. Do not introduce an editor, reviewer, or assistant speaking on the author's behalf.
- **User/product documentation:** write for the person using the product. Explain what they can do, how to do it, and what result to expect.
- **Developer documentation:** explain the code's actual behavior, contracts, entrypoints and extension work, using current implementation as the source.
- **Agent instructions (`AGENTS.md`, `SKILL.md`, references):** address the executing agent directly. Say what to read, change, run, preserve, or deliver. For example: `Migrate the callers and delete the obsolete adapter`.
- **Research archive:** distinguish observed incidents, cited findings and proposed explanations in the research discussion itself. Place theory, terminology, and causal hypotheses here instead of adding them as disclaimers to an operational instruction.

Read `references/author-and-audience.md` when editing someone else's authored text, translating it, or writing instructions for another agent. It contains the actual AntiRLHF README voice error and contrasting examples.

## Make an edit that can be used

Read the relevant original passage and its neighbors. Identify the current fact or instruction the changed passage will express. Rewrite it in place, preserve unrelated content, and remove text superseded by the edit. Add new information under the heading where a reader will seek it. Update links and maintained translations affected by the change.

Keep one authoritative home for each maintained procedure or fact; link other documents to it. Keep true migration history in changelogs and research records; a corrected user guide describes the current system directly.

Read `references/editing-and-prose.md` for concrete examples of corrections, invented caveats, scope mistakes, and legitimate uncertainty. Read `references/navigation-and-tools.md` when creating or moving documentation, editing navigation, or applying the bundled checker in a different repository.

## Check the written result

Read the completed paragraph as the intended reader. Remove self-description, unrequested author-provenance claims, imagined objections, and hedges that follow an already supported conclusion. Keep distinctions and uncertainty that change the meaning or next action.

For maintained Markdown and AI instructions, use the existing prose scanner on affected files, then inspect contextual findings in the full paragraph:

```bash
python AntiRLHF/skills/documentation/scripts/check/governance_prose.py --changed
```

When installed in Codex, run the equivalent script at `$HOME/.codex/skills/documentation/scripts/check/governance_prose.py` from the consuming repository. The checker uses project configuration first, then installed configuration, then its bundled default. Review findings with the text's intended audience in mind. A `block` requires correction or a specific justified waiver; `review` and `signal` direct attention to context. Preserve an essential technical distinction even when its phrasing matches a pattern.

When changing documented navigation, run the repository's configured doc-graph checker and follow affected links. Finish with the document in its final form, retaining the author's chosen voice.
