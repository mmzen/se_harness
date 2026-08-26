# Definition Lifecycle Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain proposes that a definition's lifecycle status answer exactly one
question. Today it answers three at once: does this artifact govern, which schema
generation is it, and has it been built. Measured against the graph at `c189b58`,
the generation reading is right for 14 of 28 `implemented` architectures and wrong
for the other 14; the realization reading is stored in a terminal field that 49
of 104 `implemented` requirements can already falsify; and 449 of 630 definitions
carry a status with no recorded decision at all.

Three increments follow, in order: replace the generation proxy with an explicit
declaration, terminate the reachable lifecycle at `approved` and derive
realization from work-order and verification coverage, then require a recorded
decision chain for every status past `draft`. No artifact byte changes in any of
them, and no decision is fabricated for any existing record.

## Draft definition packet

- `INT-DLC-001`: make a definition's lifecycle status mean exactly one thing.
- `CAP-DLC-001`: read authority, generation, and realization from three independent sources.
- `REQ-DLC-001`: declared architecture-generation exemption, replacing the status proxy.
- `REQ-DLC-002`: terminate the definition lifecycle at `approved`.
- `REQ-DLC-003`: derive realization from work-order and verification coverage.
- `REQ-DLC-004`: require a recorded decision for every definition state past `draft`.
- `REQ-DLC-005`: preserve every existing governing record and diagnostic outcome.
- `SPEC-DLC-001`: the declared generation exemption, on the `SPEC-LRE-001` model.
- `SPEC-DLC-002`: lifecycle termination and the read-only realization derivation.
- `SPEC-DLC-003`: the mandatory decision chain and its declared pre-contract set.
- `ARCH-DLC-001`: one question per mechanism, with the dependency direction fixed.
- `ADR-DLC-001`: declaration over inference, in three ordered increments, with no data migration.
- `ADR-DLC-002`: enumerated frozen vectors rather than a cutover date over `created`.
- `VER-DLC-001`: independent evidence, measured as paired base-and-candidate runs.
- `WO-DLC-001` / `WO-DLC-002` / `WO-DLC-003`: the three increments, one each, in that order.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action. The `[assurance]`
classifications in the three work orders are proposed for the engineering owner's
decision, not records of a decision taken.
