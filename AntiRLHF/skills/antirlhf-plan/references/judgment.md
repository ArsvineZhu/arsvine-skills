# Choosing a technical direction

Use this guide when the task needs a decision and several plausible actions compete. Finish with a selected action, its decisive reasons, and what follows from it.

## Identify the actual decision

Read the user's requested outcome and the current decisions before exploring alternatives. Distinguish a requested choice from a request to survey the design space. If the user asks "Which storage owner should we use?", choose an owner. If the user asks "Explore fundamentally different storage architectures", investigate the models before settling on one.

Look for the constraint that separates realistic choices: who may mutate data, whether a consumer is external, required lifetime of state, latency, development direction, and the consequence of a wrong choice. Compare options on those differences. A list of implementations that differ only in library names adds little to an architecture decision.

## Let the cost of error guide investigation

For reversible choices inside a pre-production repository, make a sound choice and implement it. Changing an internal function name, replacing an unused adapter, or reorganizing a test suite is usually cheaper than maintaining an unnecessary transition layer.

For a persistent data format, deletion of real user data, public integration contract, cryptographic boundary, or production rollout, investigate the fact whose answer affects the migration. Then incorporate the real obligation into the design. The presence of a serious consequence is a reason to investigate the affected part, not to defer every ordinary choice around it.

### Worked decision: replacing an internal API

**Task.** One internal API was replaced by a better one. Three callers remain inside the repository. The user has authorized breaking internal changes.

**First inspection.** Search the three call sites and the public integration surface. Look for actual published contracts, generated clients, external consumers, and saved data. Use the current repository's information; do not initiate an open-ended search for hypothetical customers.

**If the API is internal:** migrate the three callers and delete the old API, its adapter and dependent tests in the same change. Specify the chosen new contract. Implement the change.

**If the API is public and clients depend on it:** identify the supported versions and migration constraint. Preserve the required compatibility at the public boundary for the stated support period, while simplifying internals behind it.

**Common detour:** keep the old API as a deprecated alias "just in case," add dual tests and a future removal milestone. That builds a permanent obligation from an imagined one.

The decisive difference between the two routes is the *actual* external contract. The positive action in both routes is to produce one coherent internal implementation.

## Treat uncertainty as a local design input

Unknown facts should change a decision only through a plausible consequence. Say which fact is missing, which action depends on it, and how the team can obtain it. If the same choice stands across realistic values of an unknown, choose now.

Example: "Use the in-process queue for the approved single-process service. If the architecture is changed to multiple independent workers, select a shared queue before that deployment." The future condition belongs to the stated design direction; it doesn't create an immediate queue benchmark task.

Compare viable alternatives when trade-offs are material. Use a table if it clarifies a real comparison. Deliver the decision in direct language once one approach satisfies the constraints better. Avoid inventing a third option merely to fill out a comparison.

## Respond to correction by changing the decision

When a user reveals a missed fact, incorporate it. For example, if an update check runs *once per new session*, evaluate the cost and benefit at that frequency. Retain it when it cheaply informs users about releases and requires consent to update. Replace the incorrect earlier recommendation in the current answer or design.

If asked why the original mistake happened, describe the observed mistaken assumption. Internal causes of generation are generally unavailable to the agent. Stay with what can be observed and corrected.
