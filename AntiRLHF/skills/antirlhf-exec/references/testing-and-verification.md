# Verification that protects working behavior

Use this guide for focused feature changes, debugging, test selection, and interpreting existing CI results. For redesign of a large suite during structural replacement, load `../../refactoring/SKILL.md` and its `../../refactoring/references/testing-and-reduction.md` from this reference directory's sibling Skill.

## Choose a check for the behavior under change

Start with the operation the user expects to work. Use the existing test or command that can detect a defect in that operation. Add a test when it captures a distinct regression, a meaningful boundary case, a complex algorithm, or an independently failing contract.

A test is worthwhile because of the failure it can reveal and the protection it gives later changes. Test count, assertion count and coverage percentage are signals about coverage; they are not the objective.

### Example: one serialization fix, six possible test layers

**Change:** The persisted representation of an optional field was wrong.

**Current tests:** An integration test already covers create -> persist -> restart -> read. The serializer has a dedicated unit suite.

**Useful action:** Put the field-specific regression in the serializer test if it uniquely catches the defect. Update the existing restart integration test if the public contract requires checking the field across restart. Run both affected checks.

**Wasteful action:** Add independent tests through six service and repository layers to repeatedly assert the same serialized value, along with extra test factories and a CI verification matrix. The apparent increase in coverage may mostly repeat the same contract.

**Different case:** If encryption, transaction recovery and client decoding can fail independently, tests at those boundaries protect distinct risks and should remain.

## Respond to checks with changes in work

A failed check gives an observed defect; locate its owner and fix it. Re-run that check. When a broad suite reports one concrete failure, work on that failure before running the full suite repeatedly.

A passing focused check answers the question it examined. Continue the other unfinished parts of the feature. Once implementation and relevant integration behavior work, finish the task.

If a passing unit test coexists with a failing CLI or API path, implement or repair that path. The user experiences the real entrypoint, not the unit-test count.

## Adjust tests when architecture changes

A test attached to an obsolete private interface may fail after an intentional architectural replacement. Inspect whether it protects a behavior still required. Move valuable scenarios to the current contract or owner, then remove the obsolete test and its fixture. Update production code to preserve real public behavior; do not resurrect private adapters merely to satisfy old mocks.

For a whole-suite reset, read the refactoring guide. It covers designing new tests from target capability, transferring useful scenarios, and deleting groups of obsolete test machinery.

## Use each tool for the question it answers

Linters and type checks catch static defects. Unit checks catch local behavior. Integration tests catch contracts across components. Manual or scripted runs of the actual entrypoint catch missing wiring. Benchmarks matter when performance is a requirement or a design decision. Run the appropriate tools, understand their findings, and finish after they have done their job.
