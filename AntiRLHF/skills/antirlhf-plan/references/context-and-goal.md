# Carrying a design across long work

Use this guide after context compression, handoff, a long research detour, or multiple revisions to the same design.

Keep three pieces of active state in the working context:

- **Objective:** what working result the user ultimately wants, including scope and an explicitly requested optimization such as total code reduction.
- **Decisions:** design and project decisions still in force, plus material constraints and permissions such as permission to replace all internal APIs.
- **Current Work:** the part of the objective still unfinished and the natural next design or implementation action.

This is a way to retain task state; no particular status document, template, or repeated output is required.

### Recovery example

A design project chooses a canonical message owner. Research into persistence drivers takes several turns. A useful handoff says:

```text
Objective: Design the message pipeline, storage model and observable recovery behavior.
Decisions: Message ownership belongs to the routing service. Drivers persist the
canonical message; public transport adapters own protocol conversions.
Current Work: Specify restart recovery and idempotent delivery. The persistence
driver comparison is settled; resume the message lifecycle Spec.
```

A weak handoff copies the last commands, every rejected persistence option, reviewer comments, and success counts while omitting which pipeline is still unfinished. That forces the next agent to reconstruct the design from activity history.

## Handling a side investigation

Record a research finding only where it changes the design, an active assumption, or the next choice. When a side question is resolved, carry its consequence into the main design and continue. If an assumption was overturned, revise the corresponding decision and downstream contracts; there is no need to repeat the full argument at every later step.

A session-start version check is a different type of stateful behavior: it happens once when a new session starts and serves the user's ability to discover an update. Keep its actual frequency when judging cost or scope. Do not reinterpret a session as every user message.
