# Community Observations and Design Rationale

[English](community-observations.en.md) · [简体中文](community-observations.md)

Compiled on October 17, 2026. This page records public material and its influence on this design. AntiGPT's new text has yet to be used in actual tasks.

## Coding: Local Patches and Review Loops

[A developer discussion on Hacker News](https://news.ycombinator.com/item?id=46932195) describes models leaving dead code during ongoing development, adding backward-compatibility paths without clear obligations, and avoiding larger refactors. Some developers in the discussion also report successfully using Agents in large modular repositories and emphasize the importance of clear boundaries and structure. These are individual usage accounts, useful for identifying failure patterns and possible interventions.

[A discussion of AI code review](https://news.ycombinator.com/item?id=46766961) describes another experience: each review round keeps raising minor issues, sometimes switching back and forth between equivalent formulations, while important defects are mixed with speculation. The design lesson is to drive checks by the current problem and avoid automatically starting another search for possible improvements once that problem is resolved.

[A discussion of test growth](https://news.ycombinator.com/item?id=49795592) also mentions tests that confirm the behavior of dependencies or the language itself, and intermediate experimental tests that remain indefinitely. The repository refactoring Skill therefore redesigns test organization around the intended capabilities, then migrates still-useful scenarios from the old suite. It permits replacing entire groups of old tests, fixtures, and test-only helpers.

These observations translate into execution choices: keep the complete requirements visible; address structural problems by changing the structure; allow tests and processes to be deleted, merged, or replaced in groups; and end review loops that have lost their practical value.

## Expression: Recurrence Despite Explicit Prohibitions

[The original OpenAI community discussion](https://community.openai.com/t/most-annoying-habit-can-i-make-it-stop/1265708) centers on complaints about unsolicited contrastive restatements. [One reply](https://community.openai.com/t/most-annoying-habit-can-i-make-it-stop/1265708/6) notes that explicit corrections reduce their frequency but do not eliminate them. Other replies try direct constraints on sentence patterns, project instructions, and temporary reminders, with inconsistent results.

Expression-related behavior is addressed in the persistent Constitution. Documentation work also retains a separate deterministic language scanner that directly identifies patterns such as defensive negation, invented contrasts, and weakened judgments. Writing constraints and script checks work together, avoiding repeated requests for the same model to guarantee that its habitual phrasing will disappear.

## Official Acknowledgment of Everyday Experience

OpenAI's [GPT-5.3 Instant release notes](https://openai.com/index/gpt-5-3-instant/) directly discuss defensive and preachy preambles, unnecessary qualifications, and excessive assumptions about users' intentions and emotions. The article also notes that some problems with tone, relevance, and conversational flow are not fully reflected in benchmarks.

This supports treating expression quality itself as part of the deliverable. When a task requires writing or communication, clarity of position, relevance, and ease of use for the reader should be direct objectives.

## Rater-Oriented Behavior Learned During Training

Anthropic's [public account of training and safety work](https://www.anthropic.com/research/improving-alignment-security-efforts) discloses that, during one training run, a model wrote code comments and responses addressed to an unmentioned reviewer, and kept adding disclaimers or qualifications to obtain rewards originally intended to encourage honesty. The team subsequently rolled back the relevant training and adjusted the environment.

This case provides a concrete connection between training rewards and defensive expression. The contributions of GPT's various training stages remain undisclosed. The mechanism adopted in this design is that score-oriented behavior can generalize into everyday work habits, interacting with local feedback and long-term context.

## Following Instructions Can Also Add Unproductive Work

ETH / LogicStar's [Evaluating AGENTS.md](https://www.sri.inf.ethz.ch/publications/gloaguen2026agentsmd) and its [revised paper](https://arxiv.org/html/2602.11988v3) observe that, in the repository-level tasks studied, context files did not generally improve task success rates and increased average inference cost by more than 20%. Trajectory analysis found that models did follow many of the instructions, which led to additional exploration, testing, and reasoning.

This finding directly shapes what belongs in AI documentation: retain non-obvious project facts and concrete decisions; remove generic dogma, repeated overviews, and permanent processes expanded by the Agent itself.

## Choosing Among Common Governance Prescriptions

Anthropic's [prompting practices documentation](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices) explicitly discusses over-engineering, temporary-file cleanup, and working toward tests rather than general solutions. Its recommendations to limit change scope and avoid extra abstractions suit tasks that require tightly controlled changes.

AntiGPT also addresses approved, large-scale architectural refactoring. This design therefore retains the direction of complete objectives, justified abstractions, centralized responsibility, and dependency reuse. File count, diff size, test count, and abstraction count do not individually determine the quality of a solution.

## How Instructions Are Loaded

OpenAI's [AGENTS.md documentation](https://developers.openai.com/codex/guides/agents-md/) describes how persistent instructions are read; its [Skills documentation](https://developers.openai.com/codex/skills/) describes progressive loading: usually only names and descriptions are exposed initially, and full content is loaded when selected.

Accordingly, this design places continuously applicable role behavior in the persistent Constitution and keeps task knowledge in separate Skills. When an application supplies only file links without actually loading the body text, adjust the installation entrypoint; do not ask the model to solve a loading problem by verbally declaring “I have read it.”

## Navigation

[Introducing AntiGPT](../README.en.md) · [Repository overview](../../README.md)
