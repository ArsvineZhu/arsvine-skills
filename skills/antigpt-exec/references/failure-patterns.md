# Execution Failure Patterns

These patterns describe recurring trajectory failures. Detect the behavior, then restore the authorized objective.

## Investigation sink

A small defect produces a growing chain of traces, experiments, instrumentation, speculative causes, and unrelated cleanup.

Correction: identify the causal explanation required for a reliable fix. Stop investigating when the fix target and falsifying check are clear.

## Test accretion

Every discovered behavior receives another test even when stronger tests already protect the same failure.

Correction: name the concrete failure each test can catch. Remove tests with no unique contract, defect, risk, or algorithmic value.

## Evidence accretion

Passing behavior is followed by repeated proof runs, screenshots, logs, qualification records, or status documents whose only purpose is to strengthen the feeling of certainty.

Correction: match evidence to the live claim and risk. Stop once the claim has enough support.

## Compatibility accretion

Aliases, dual readers, adapters, fallback parsers, migration layers, or deprecation paths appear for consumers that have not been shown to exist.

Correction: identify the current obligation. In pre-production work, migrate real producers and consumers together and delete obsolete paths unless project authority requires compatibility.

## Patch accretion

Local workarounds preserve a topology that repeatedly creates the same problem.

Correction: move to the semantic owner. Refactor the structure when repeated local compensation costs more than the structural change.

## Tool-driven architecture

Production code changes to satisfy coverage, mocks, lints, duplication metrics, CI shape, or qualification convenience.

Correction: preserve product semantics and coherent ownership. Change the tool, test, or verification strategy when the production design is already sound.

## Process substitution

The executor creates plans, matrices, checklists, gates, evidence packages, or closure rituals instead of finishing the authorized capability.

Correction: use process only when it removes a concrete coordination, risk, or uncertainty burden.

## Completion avoidance

The requested behavior works and the necessary evidence exists, yet work continues through extra cleanup, additional validation, speculative hardening, or documentation expansion.

Correction: stop. Resume only for a real defect, requirement, accepted improvement, or explicit authorization.

## Context drift

After compaction or a long debug branch, the agent remembers commands and failures more strongly than the original goal.

Correction: restore `Objective`, `Decisions`, and `Current Work`; discard closed branches from active reasoning.
