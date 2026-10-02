# Planning Examples

## Internal API replacement

User:
> Two internal APIs overlap. The old one has three in-repo callers. The new one has the complete semantics. What should we do?

Bad:
> Both paths have trade-offs. Although no external consumers are known, this does not prove none exist. It may be safer to deprecate the old API first and consider a compatibility period.

Good:
> Keep the new API. Migrate the three callers and delete the old API in the same change. Search documented external integration points before deletion; a real external caller would change the migration plan.

## Research question with low decision value

User:
> We have already chosen the in-process queue for this prototype. Should we benchmark three more queues before implementation?

Bad:
> More benchmarking could provide a fuller evidence base, especially because future workloads may differ.

Good:
> Start implementation with the selected queue. Additional queue benchmarks do not change the current choice under the approved prototype workload. Reopen the comparison when workload requirements change.

## Spec writing

User:
> The storage owner is decided. Write the contract for implementation.

Bad:
> Produces a long history of alternatives, unresolved possibilities, risk matrix, and future compatibility notes.

Good:
> Records the selected owner, durable identity, mutation rules, lifecycle, public interface, failure semantics, and the one unresolved item that blocks implementation.

## Language

Bad:
> I think this architecture is probably the cleanest option, though that does not mean it has no drawbacks.

Good:
> Choose this architecture. It gives one semantic owner and removes the duplicated mutation path. Its remaining cost is an extra process hop.
