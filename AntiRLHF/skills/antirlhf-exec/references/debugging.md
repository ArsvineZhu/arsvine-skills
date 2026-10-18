# Debug a failure and return to the feature

Use this guide when a real test, command, integration path, or user operation fails. Follow the defect to a repairable owner and resume the original task.

## Trace the observed failure

1. Capture the failing action, input, expected result and actual result. A reproducible symptom is often enough to start; use instrumentation when it distinguishes possible causes.
2. Follow the affected data or control flow from the failure to the component responsible for the behavior. Inspect the recent change and the nearest relevant boundary before examining unrelated systems.
3. Choose a repair that explains the symptom. Patch the responsible behavior or correct a structural owner when multiple consumers share the same defect.
4. Re-run the action or targeted test that demonstrated the failure. Expand to affected integration paths when the repair changes shared state, persistence, transport, or security behavior.
5. Remove experimental instrumentation and resume the unfinished feature.

## Distinguish local defects from structural ones

**Local defect:** a serializer incorrectly handles one optional field; its ownership and data path are otherwise sound. Correct the serializer and cover the missed case.

**Structural defect:** three services update the same cache invalidation state, and each bug fix repairs a different service. Choose one mutation/invalidation owner, make callers use it, and remove duplicate invalidation logic. Adding a fourth fallback repeats the underlying problem.

A failure can be small in its visible symptom and large in its structural cause. Let the observed flow determine how far to change code.

## Example: stale cache after mutation

**Observed:** A user updates an item through the API. A later read returns the old value, but a process restart shows the new value.

**Useful next actions:** Trace the API mutation through persistence and cache invalidation. Establish whether the mutation owner publishes an invalidation event and whether the reader consumes it. Repair the missing transition at that boundary. Re-run update -> read and restart -> read where both are part of the contract.

**Misstep:** Instrument every cache, introduce a generic "cache consistency auditor", add a separate retrying read path, and declare safety because all cache-focused unit tests pass. Those tools can leave two competing ways to get the right answer.

**Different evidence:** If the observed data loss happens before persistence, investigate commit/transaction ownership rather than forcing cache invalidation as the answer.

## Stop the investigation when it has served the repair

Once the repair explains the failure and a relevant check confirms it, continue any remaining authorized behavior. A new observation that changes the cause or exposes another affected integration can reopen the investigation. General curiosity about unrelated parts of the system belongs to a different task.
