# Testing and Verification

Verification is an information tool. Its depth follows contract importance, observed risk, failure cost, and the live claim.

## A test earns its cost

Keep or add a test when it uniquely protects at least one of these:

- a meaningful public or internal contract;
- a reproduced defect with recurrence risk;
- a high-cost failure mode;
- non-trivial algorithmic or state-transition logic;
- a material uncertainty that the test resolves.

A test with no unique failure to catch is a candidate for deletion.

## Overlap

Prefer one strong public or integration proof plus focused regression tests for distinct risks. Do not duplicate the same behavior across several layers merely to increase confidence metrics.

## Iteration

Run the narrowest informative falsifier while editing. Broaden checks after the changed scope stabilizes or when the integration surface makes a narrow result insufficient for the live claim.

## Tools and metrics

Coverage, mutation score, duplication checks, lint, static analysis, CI, benchmarks, and qualification systems are tools with their own costs. Use them where their information changes engineering decisions or protects meaningful failure modes.

Do not redesign production code solely to satisfy a metric or make a test harness convenient.

## Evidence

Record evidence that supports a claim another person or later agent must rely on. Avoid evidence packages whose contents duplicate logs or checks already available from the canonical command.

## Completion

When the authorized behavior is implemented and the required confidence for the live claim has been reached, stop verification and finish the task.
