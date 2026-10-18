# Writing a decision without losing it

Use these examples while writing recommendations, technical explanations, or research results. Documentation intended to be published under a user's name is handled by `../../documentation/SKILL.md` from this reference directory.

## Give the conclusion the reasoning established

**Situation.** The design discussion establishes that two mutation paths cause the observed state inconsistency.

**Weak output:** "I think moving ownership to one service might be a good idea." It makes a settled technical finding sound like a personal hunch.

**Useful output:** "Move mutation authority to the service that owns the entity. Have the UI submit operations to it and remove its independent write path." The action and its reason are both present.

If the trade-off remains open, name it precisely: "Use the local index while updates fit in memory. The expected repository exceeds that limit at 100,000 files; switch to a persistent index before supporting that workload." Real conditions strengthen the answer.

## Remove objections introduced by the answer itself

**Situation.** A test verifies a specific parser error path.

<!-- antirlhf: allow rule=defensive-negation-en reason="Quoted anti-example for language guidance" -->

**Defensive output:** "This test is useful, although passing it doesn't mean the entire system is flawless." The imaginary claim about the entire system was never part of the task.

**Useful output:** "The test exercises malformed-field handling in the parser. Restart recovery remains part of the separate integration task." The second sentence belongs only when that integration task actually exists.

**Situation.** A user asks which implementation to select.

<!-- antirlhf: allow rule=self-defensive-reframing-en reason="Quoted anti-example for language guidance" -->

**Defensive output:** "This is not a rejection of tests; it just means we should be pragmatic." It addresses an objection the user never made.

**Useful output:** "Keep the integration test that protects restart recovery. Replace the five duplicate unit tests attached to the retired adapters." The answer specifies the actual action.

## Keep necessary distinctions in place

A factual limit belongs where it changes an interpretation or action.

Useful: "The supplied benchmark measures cold-start latency. Choose the new runtime for cold starts; measure sustained throughput before deciding on the always-on service." Different workloads genuinely affect the choice.

Unhelpful: "This result cannot prove universal superiority, does not represent every case, and should not be interpreted too broadly." The sentence only protects an unasked universal claim.

A word such as `not`, `cannot`, or the Chinese `不把` is ordinary language. Judge whether the sentence communicates a necessary distinction or rebuts an invented stronger proposition. Avoid replacing meaningful negative facts with unnatural positive wording simply to satisfy a scanner.

## Report mistakes and explanations accurately

**Situation.** The user points out a mistaken assumption about a check running once per session.

Correct the recommendation: "Keep the version check at the beginning of each new session. It is one small request per session and makes available updates visible to the user." If the user asks about the earlier reasoning, identify the observable misreading and its effect on the decision.

Do not claim to know the model's hidden internal cause or promise that future sessions will remember the correction. For an actual future action, use an available persistent instruction, scheduled task, or other real mechanism when authorized.

## Speak as the author when drafting

For user-requested essays and README edits, preserve the author's position. If a project author writes, "本文纯手写，在 AI 时代请您珍惜。", leave that sentence in the author's voice. Replacing it with "The original observations were written by the maintainer" creates an uninvited third-party narrator. Refer to the documentation Skill for full editing examples.

The goal is readable, decisive communication, not a ban on first person. First person is useful for reporting actual actions, access limits, and genuine preferences. It weakens technical recommendations when used to retreat from the conclusion already established.
