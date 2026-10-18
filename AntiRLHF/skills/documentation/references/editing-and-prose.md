# Correct prose, keep meaning, finish the document

Use this guide when revising an existing document, handling language-scan findings, correcting an AI instruction or repairing a bad edit. The revised document should read naturally as the current version.

## Replace an error where it occurs

**User guide example:** The menu should be "番茄炒鸡蛋". The current document says "红烧牛肉".

**Wrong result:** "番茄炒鸡蛋（现在没有红烧牛肉）". It keeps the old error visible next to the correct content.

**Right result:** "番茄炒鸡蛋". The reader sees the correct item. Remove unrelated sentences that only explain the former mistake.

**When history is genuinely useful:** A release note may say, "Version 2.4 corrects the menu label previously shown as 红烧牛肉." That is a historical record in its proper location, not a permanent note in the live guide.

## Correct an AI instruction within its authorized scope

**Local correction:** The user asks the agent to stop adding trailing qualifiers to one README paragraph. Edit that paragraph. Apply the author's preferred style in subsequent work on that document. Do not invent a repository-wide `No caveats ever` rule in `AGENTS.md`.

**Project-wide direction:** The user explicitly asks to change the project's documentation policy. Edit the owning `AGENTS.md` or documentation Skill, preserve existing useful rules and state the new behavior as a direct instruction.

**Task-long condition:** The user asks to preserve login state during maintenance. Keep it safe for each operation that touches the relevant state until the task ends. Avoid repeatedly mentioning it in unrelated reports.

## Eliminate invented objections and tail qualifications

Look at what the user asked and what the paragraph has already established. Remove a sentence when its only job is to rebut a stronger claim that nobody made.

<!-- antirlhf: allow rule=defensive-negation-en reason="Quoted anti-example for language guidance" -->

**Unnecessary tail:** "The build works in our target runtime. This does not mean it works in all possible environments." If the task is to confirm the target runtime, the second sentence adds no useful result.

**Relevant distinction:** "The Windows build succeeds. The requested Linux build still fails because the native module is missing." This changes the completion state and the next action.

**Unnecessary authorship hedge:** "The maintainer originally wrote this, but the document has undergone revisions." An author's introduction needs that statement only if authorship history itself is the subject.

**Relevant research uncertainty:** In an article comparing two mechanisms, state exactly which observation supports which hypothesis and what measurement distinguishes them. A general announcement of rigor at the end of the paragraph adds no information.

## Handle ordinary negation intelligently

A word such as `不把`, `不能`, `not`, or `does not` can carry important meaning. Distinguish the sentence's actual function.

- "不要把旧测试原样复制到新架构" is a direct work instruction. Keep it if that is the required action.
- "不把这种结果视为已验证事实" may be a necessary source distinction in a research paragraph. Judge its relation to the claim.
- "产品已实现本地搜索，不把这说成完整的搜索平台" may be an invented qualification in a release announcement; the reader did not ask about a "complete search platform." Write what the product actually does.
- "不能在未登录时调用管理员接口" is a meaningful access constraint. Keep it.

Keep scan rules calibrated to recurring expressions that can be identified mechanically. Contextual patterns should prompt review, not force deletion of all negation. If a real false positive appears, adjust the specific pattern or use a narrowly justified waiver for intentional teaching examples.

## Preserve the strength of an established judgment

**Weak rewrite:** "我个人比较倾向于采用统一配置服务，不过这当然还有许多值得讨论的方面。"

**Useful rewrite:** "采用统一配置服务。CLI 与 Web UI 通过它修改有效配置，删除各自维护的状态镜像。"

**Genuine uncertainty:** "迁移完成前，两套持久化数据尚未合并；本次只能启用只读查询。" This fact changes user action and belongs in the result.

Do not create a policy that all answers must be forceful. The aim is to preserve the real degree of certainty reached by the work.

## Review changes as writing, then use the tools

Read the final paragraphs in sequence. Check subject continuity, pronoun perspective, author voice, unnecessary self-reference and whether statements help the reader. The prose scanner catches selected repeatable cues; a passing result will not identify a third-person narrator replacing an author's voice or detect all invented hypothetical objections.

Use the scanner on the affected maintained prose; inspect `review` and `signal` findings. If the text is an intentional example of a bad phrase, keep the example and add a specific waiver rather than disabling the whole pattern. Update the scanner when a recurring, precise, mechanically detectable pattern has actually been observed.
