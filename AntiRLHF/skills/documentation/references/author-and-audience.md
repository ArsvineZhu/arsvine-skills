# Write as the intended author, to the intended reader

Read this guide when editing an authored README, translating someone else's writing, adding a research article, or writing instructions for another agent. Establish the speaking position from the existing document and the task.

## A maintainer's README is the maintainer speaking

The original AntiGPT introduction includes:

> 本文纯手写，在 AI 时代请您珍惜。

This sentence is part of the author's voice. It is personal, pointed and humorous. The author is speaking directly to the reader about a product born from experience with models.

**Wrong edit:**

> 本文最初的观察与观点由维护者亲自撰写，后续内容随研究持续修订。

The replacement invents a third-person narrator and a provenance statement. It changes tone, adds qualifications about authorship, and answers a question the reader never asked. It also changes what the author chose to say.

**Right edit for an AntiGPT → AntiRLHF rename:** Preserve the original sentence. Rename the product where required, update genuinely changed capabilities and links, and edit the specific explanation of the project's wider scope in the author's existing style. Keep the author's emphatic description of model behavior. If the user explicitly requests a rewrite of that sentence, follow their intended tone rather than imposing a neutral editorial voice.

### Before changing original prose

Read the surrounding paragraph and ask what communicative job it performs: argument, joke, direct criticism, instruction, explanation, or transition. Preserve that job when changing technical facts. A slogan may carry deliberate emotional force; a technical definition may depend on exact terms. Treat neither as disposable filler.

Do not rewrite an author's first-person judgments as findings by a reviewer. Do not append phrases that describe the assistant's caution, diligence or source attribution when the author is making a point.

## Product and developer documents have different readers

**Product guide:** Address the person who wants to perform an action. "Open Settings, choose the provider, save the connection. The new provider appears in the selection list." Provide prerequisites where the operation actually depends on them.

**Developer guide:** Address a contributor implementing or maintaining the program. "The provider registry loads driver definitions at startup. Add the driver in `drivers/` and register its exported constructor." Derive these facts from current code.

**Research archive:** Write as the project researchers documenting observed incidents, published studies and hypotheses. Use citations for external findings. Keep causal uncertainty in the part of the article actually discussing causation. It does not belong as a blanket afterthought in the project introduction or a Constitution paragraph.

## Agent-facing text must instruct the agent

A Skill description is discovery metadata: use a short third-person-style capability description such as "Refactor repository ownership, data paths, tests and tooling for substantial structural changes."

The body of `SKILL.md`, `AGENTS.md`, and agent references is instruction text. Address the executing agent and name the object of its work:

| Indirect description | Direct instruction |
|---|---|
| Prevent the agent from inventing new compatibility machinery. | Migrate the active callers and delete retired internal adapters. |
| This skill encourages careful testing. | Run the test that exercises the changed behavior; add a regression for a distinct missed failure. |
| The document guards against context drift. | After compaction, restore the Objective, Decisions and unfinished Current Work. |
| AntiRLHF seeks to improve architectural judgment. | Trace the mutation path and choose the component that owns the state change. |

The direct versions give another model actions it can perform. Explanations of the Skill's philosophical purpose belong in the README or research archive when a human reader needs them.

## Translating an author's document

Carry across viewpoint, humor, certainty, technical terms and intended force. Literal translation may be awkward; preserve the meaning and voice instead of replacing them with official-sounding qualifiers. Preserve authored quotations as quotations. If the Chinese source speaks as the author, its English counterpart should also speak as the author.

Translating an operational Skill is different: retain imperative commands, file paths and conditions. A Chinese review edition should represent the English instructions faithfully and use direct second-person or imperative language, rather than talking about what "the Agent" is supposed to do from outside.

## Finish with a reader check

Read the edited section as if it were written and published by its intended author. Verify that the reader receives the promised information, tone and action without needing the assistant's editing history. Then check affected links and language patterns using the existing documentation tools.
