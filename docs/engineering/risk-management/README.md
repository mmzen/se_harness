# Risk Management Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes one governed `risk` artifact: identified anywhere along
the process by anyone, raised by repository policy when its score reaches the
acceptance level, disposed by the owner of the stage it threatens, and
mitigated through ordinary governed work. Owner decisions taken on 2026-08-25
before drafting: the disposer is resolved by stage (no new role); the default
acceptance level is 1 (raise everything); `mitigating` blocks release; the
scale is 5x5.

## Draft definition packet

- `INT-RSK-001`: make risk a first-class governed fact with one accountable disposer.
- `CAP-RSK-001`: identify anywhere, raise by policy, dispose by role, mitigate through governed work.
- `REQ-RSK-001`: the risk artifact and its score.
- `REQ-RSK-002`: raising by the acceptance level.
- `REQ-RSK-003`: disposition rights and lifecycle.
- `REQ-RSK-004`: gates and blocking.
- `REQ-RSK-005`: mitigation traceability and the release list.
- `REQ-RSK-006`: identification mechanics.
- `SPEC-RSK-001`: schema, transitions, predicate, commands, configuration.
- `ARCH-RSK-001` / `ADR-RSK-001`: a new lifecycle family, stage-resolved disposition, a predicate in existing gates.
- `VER-RSK-001`: independent evidence for the risk artifact.
- `WO-RSK-001`: implement the bounded first increment after approval and an explicit start decision.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action.
