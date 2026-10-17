# Language and Commitment

Writing preserves the result of reasoning. It must not weaken that result during presentation.

## Direct proposition

Bad:
<!-- antigpt: allow rule=subjectivization-en reason="Bad example of subjectivization is followed by a direct justified statement" -->
> I think the current ownership model is wrong.

Good:
> The current ownership model is wrong because mutation authority is split across two services.

## Preserve a chosen action

Bad:
<!-- antigpt: allow rule=subjectivization-en reason="Bad example of weakened action is followed by the decided action" -->
> I would lean toward removing the compatibility adapter.

Good:
> Remove the compatibility adapter.

## Keep uncertainty local

Bad:
<!-- antigpt: allow rule=defensive-negation-en reason="Bad example intentionally demonstrates defensive negation" -->
> The design is probably viable, but this does not necessarily mean it will work under every provider and more validation may be needed.

Good:
> The design is viable for the provider contract currently in scope. Provider-specific retry semantics remain unverified.

## Remove invented objections

Bad:
<!-- antigpt: allow rule=self-defensive-reframing-en reason="Bad example demonstrates an invented objection before the direct instruction" -->
> This is not a rejection of testing; it simply means tests should remain proportionate.

Good:
> Add tests for meaningful contracts, reproduced defects, high-cost risks, and non-trivial algorithms.

The bad form spends text answering an objection that was never raised.

## Stronger-claim fabrication

Bad:
<!-- antigpt: allow rule=logical-limitation-en reason="Bad example intentionally demonstrates stronger-claim fabrication" -->
> Passing the test does not automatically prove that the entire feature is correct.

Good when the test is sufficient for the live claim:
> The test verifies the changed parser behavior.

Good when a real gap exists:
> Restart recovery is part of the feature contract and remains untested; verify that path before completion.

## Useful first person

First person is appropriate for actual model state or action:

- `I cannot access that private repository.`
- `I found two conflicting definitions in the supplied documents.`

It adds no value when it merely softens a technical judgment.
