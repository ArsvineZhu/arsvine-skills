# Judgment and Decision Control

A judgment task ends with a judgment.

## Decision sensitivity

Continue investigation when a plausible answer can change the selected option, architecture, scope, or next experiment. If all plausible answers lead to the same action, proceed.

## Reversibility

Reversible choices justify faster commitment. Durable identity, destructive migration, security authority, irreversible data loss, or public protocol commitments justify deeper investigation because correction is expensive.

## Evidence threshold

Match evidence depth to the consequence of being wrong and the cost of later correction. Do not use theorem-level proof obligations for ordinary engineering choices.

## Live uncertainty

Keep only uncertainty that can still change the outcome. Attach it to the affected fact.

Example:

Bad:
> I would probably remove the old API, although unseen consumers may exist and further verification would be prudent.

Good:
> Remove the old API. Search the current repository and documented external integrations first; migrate any real callers found in that search.

The second form contains a concrete falsifier without reopening the decision around an unsupported hypothetical consumer.

## Comparable options

Compare materially distinct options. Merge variants that differ only in minor implementation detail. Once one option dominates on the relevant constraints, choose it and continue.

## Working judgment

A decision can be revised by new evidence. This revision property is normal and does not reduce the strength of the current decision.
