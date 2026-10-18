# Execution cases: choose a path and finish it

Use the case that matches the current work. Compare the facts before carrying an action into another repository.

## Feature passes unit tests but fails the actual entrypoint

**Task:** Add an API endpoint that saves user configuration and makes it effective after restart.

**Existing result:** Unit tests for the validation function pass. The new endpoint responds successfully, but the CLI still writes an old configuration file and restart reloads stale data.

**Unhelpful path:** Report green validation tests; add separate tests for each helper; create a compatibility file watcher to keep two data sources in sync.

**Useful path:**

1. Trace endpoint -> configuration owner -> persistence -> service restart -> effective state. Trace the CLI write to the same owner.
2. Choose one mutation and persistence contract. Make the endpoint and CLI use it, retaining a genuine offline-file entrypoint only if the product requires one.
3. Remove the old duplicate write path and its converter. Update the contract-level tests for actual current behavior.
4. Run endpoint -> restart -> read and CLI -> restart -> read. Finish when the requested flows work.

**Alternative evidence:** If CLI offline configuration is an intentional product capability, preserve it as a defined import/load operation with the same validation authority.

## A minor failure during a major feature

**Task:** Finish the new parser and expose it through the CLI.

**Observation:** A legacy fixture fails because its metadata contains malformed bytes. The fixture is from an unused pre-production experiment.

**Unhelpful path:** Audit every fixture, build a compatibility parser, add migration commands, and postpone the CLI feature.

**Useful path:** Verify that the malformed fixture is outside the current supported path. Finish the parser and CLI wiring. Note the unrelated fixture only if the user needs to act on it.

**Different case:** If that input is supported production data, add the case to the actual parser or migrate the data as required by its supported contract. The same symptom now falls inside the feature.

## Large refactor produces a larger new system

**Task:** Consolidate three representations of the same business entity, reduce code and maintenance, and keep all current behavior.

**Existing result:** Old converters are removed. A new generic framework, two adapters per caller, an event router and dozens of tests appear. The replacement is larger than the old implementation.

**Unhelpful path:** Keep the new framework because much work was invested; rename modules, make test helpers reusable, and explain why the new line count is justified.

**Useful path:**

1. Identify where the canonical data owner still fails to provide the shape consumers actually need.
2. Move business conversion or policy into that owner. Keep transport conversion only at genuine external boundaries.
3. Simplify consumer calls. Delete the new unnecessary adapters, duplicated router and obsolete old tests together.
4. Rebuild tests from the actual operations and independent failures. Run the user-visible paths. Compare final total code and complexity with the explicit reduction goal.

**Different case:** Several adapters may be appropriate when real public protocols have independent semantics and lifecycles. Keep those adapters as boundary owners; simplify the shared domain beneath them.

## A test keeps the obsolete architecture alive

**Task:** Replace an internal API used by three in-repository modules; no external compatibility obligation is present.

**Unhelpful path:** Add a deprecated alias, preserve a wrapper for twenty old tests, and create a dual-suite qualification matrix.

**Useful path:** Move the three callers to the chosen interface. Transfer meaningful test scenarios to the new owner. Delete the retired API, its mocks, dedicated fixtures and redundant tests. Run the caller paths once the migration is complete.

**Different case:** If an active external client has a support contract, expose an explicit compatibility boundary for that client while keeping one internal implementation.

## A document correction becomes a permanent warning

**Task:** Replace an incorrect menu item in a user guide and keep an active login during an unrelated maintenance task.

**Unhelpful path:** Change the menu to `Tomato and eggs (no beef)`, add `Never mention beef` to `AGENTS.md`, and repeatedly announce after later lint runs that login is unaffected.

**Useful path:** Write the correct menu item in place. Leave the wrong item out of the user guide. Keep login state intact during commands touching its files or services. Continue the original maintenance task.

**Different case:** A release's known-issues document may legitimately record the old error and when it was fixed. Put that history in the release record, not beside the current menu item.
