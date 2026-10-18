# Rebuilding tests and reducing total maintenance cost

Use this guide when the authorized change replaces substantial architecture, when old tests keep retired internals alive, or when the user has requested a net reduction in code and ongoing maintenance. A local bug fix normally uses the existing focused testing method in the Exec Skill.

## Begin with the target system's behavior

Suppose a large repository has:

```text
tests/legacy-reader/           120 tests
 tests/legacy-writer/          110 tests
 tests/adapter-matrix/         95 tests
 tests/new-storage/            70 tests
 tests/fixtures-and-mocks/     many bespoke factories and schemas
```

The user asks to replace two old storage pathways with one authoritative storage owner, retain existing capabilities and simplify the repository.

A poor migration starts by opening each of the hundreds of old tests and trying to invent a reason to keep it. Most tests can be defended individually: each covers an input, a mock result or a private call that once existed. The cumulative result preserves the old shape while adding a new one.

Start instead with the new system's **external behaviors and independently failing responsibilities**:

- Create, update, delete and read through supported entrypoints.
- Restart recovery and persistence integrity.
- Authorization and durable identity when they belong to the contract.
- Meaningful transaction conflicts and failure recovery.
- Complex parsers, algorithms or state transitions that merit isolated tests.

The specific contract determines which of these exist. Do not manufacture categories solely to fill a coverage plan.

## Recover valuable cases from old tests

Old tests are useful evidence about defects and boundary inputs. Look at representative tests across each old group and the recorded regressions. Transfer a case when the new owner can still fail meaningfully on it. Examples:

- A valid record with a missing optional field may need one parser-level case under the new model.
- Crash-after-write recovery may require an integration test across persistence and restart.
- A dead internal `LegacyAdapter.getRaw()` mock test has no enduring contract after the adapter is removed.
- Two tests asserting the same normalization with different mocks may collapse into one data-driven case.

The purpose is to retain protection for real behavior, not to transport every assertion into a new wrapper.

## Replace groups, including their supports

When the new suite exercises the behaviors under the new owner, delete the old test directories tied to retired implementations. Remove the fixtures, factory layers, mock adapters, test-only configuration and workflow commands that existed only to support those groups.

Do not keep both sets running for a ceremonial transition when the internal rewrite and migration happen in the same authorized branch. Actual staged deployment or published compatibility may require overlapping checks; that obligation comes from the rollout, not from the age of the old tests.

### Why fewer test names can still be more code

A model might replace 300 tests with 40 tests but introduce a generic scenario DSL, multiple factories, fixture converters and a new validator framework. The test count shrinks while the maintenance structure grows.

Inspect the actual replacement: are most new helpers used because of a real repeated contract, or because the agent created a framework and now must feed it? If the latter, replace the framework with ordinary fixtures, direct calls and a simpler suite.

## Preserve tests for independent failures

A unit test for a complex authorization policy and an end-to-end test that verifies the API actually invokes authorization are not automatically duplicates. One can fail while the other passes. Likewise, persistence restart behavior, encrypted transport and transaction rollback can fail independently even when they all involve a saved record.

Keep tests for distinct contracts or costly regressions. The intended reduction removes repeated statements of the same behavior and machinery attached to retired designs. It does not impose an arbitrary quota on tests.

## Contrast with a small repair

**Task:** Fix one encoder edge case in a stable service.

Use the existing encoder test file. Add a concise regression for the new boundary if current tests miss it. Run that test and the affected integration check when the contract crosses a real boundary. Leave the rest of the suite alone.

The wholesale replacement method belongs to large structural refactors. Applying it to a local bug fix would spend the task's budget redesigning an unrelated test system.

## Hold the reduction objective through implementation

When the user requests reduced code size, evaluate the complete change: production implementation, interfaces, tests, scripts, generated glue and workflow machinery. A diff statistic can expose growth, but the design question is why the new code exists and whether it carries required behavior.

**Example:** Delete 18,000 lines from an old subsystem, add 23,000 lines of generic abstractions and tests, then claim the architecture is simpler. Open the newly created bridge/framework/test-helper code and trace its actual consumers. If it exists to keep legacy structures alive, migrate the consumers and remove it. If it carries new required capabilities, simplify the surrounding implementation while preserving those capabilities.

Finish by running the relevant real entrypoints, checking the important contracts, updating current documentation and removing obsolete support files. Report the actual structural result and its effect on the requested capability and size goals.
