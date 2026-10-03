# Execution Examples

## Small failure during feature work

Situation:
A parser feature is nearly complete. One unrelated old fixture contains malformed metadata and fails an exploratory check.

Bad trajectory:
Investigate every historical fixture, add a compatibility parser, create a migration command, add CI coverage, and postpone the parser feature.

Good trajectory:
Determine whether the malformed fixture is part of the supported current contract. If it is unrelated legacy data in a resettable pre-production fixture set, record it and continue the parser feature. If the new parser must consume it, repair the canonical data path or migrate the fixture directly.

## Duplicate tests

Situation:
A public integration test already verifies create → persist → restart → read. A new change fixes a serialization bug in that path.

Bad trajectory:
Add separate tests at unit, repository, service, client, restart, and qualification layers for the same serialized field.

Good trajectory:
Add the smallest regression test that uniquely captures the serialization defect if the public integration test cannot localize it. Keep the existing public test as the end-to-end proof.

## Internal API replacement

Situation:
A pre-production repository has one obsolete internal API with three callers.

Bad trajectory:
Add a deprecated alias, compatibility wrapper, warning log, dual test matrix, and removal plan.

Good trajectory:
Migrate the three callers and delete the obsolete API, its tests, and stale documentation in the same change.

## Debugging

Situation:
A failing test shows stale cache data after one mutation.

Bad trajectory:
Instrument every cache boundary and begin a general cache consistency investigation before checking the mutation path.

Good trajectory:
Trace the mutation path to the invalidation owner. Once the missing invalidation is identified and the fix explains the failure, repair it and run the focused falsifying test. Broaden verification only across the integration surface affected by the invalidation change.
