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

## Owner decisions taken 2026-08-26

Twelve open decisions in this packet were put to the repository owner and
answered. They are recorded where they bind, in the artifact that carries the
consequence, and not summarized here as a substitute for reading it:

- the three increments land in the stated order, all three in scope
  (`INT-DLC-001`);
- the `implemented` retirement is a within-`se-harness-workflow-v3` change with
  no generation bump, accepting that a consumer pinning `v3` sees reachable
  behaviour narrow without a generation signal (`REQ-DLC-002`, `ADR-DLC-001`,
  `WO-DLC-002`);
- `WFL-DEFINITION-COMPLETE` keeps its published identifier, and the resulting
  name-versus-behaviour residue is accepted and disclosed (`REQ-DLC-002`);
- grandfathering is by enumerated frozen vectors, not a cutover date over
  `created` (`REQ-DLC-001`, `SPEC-DLC-003`, `ADR-DLC-002`);
- the generation set is closed at exactly 14 identifiers, with no exceptions and
  no re-measurement window (`REQ-DLC-001`);
- realization is a derived report and never a stored fact, with the three-way
  classification as specified (`REQ-DLC-003`);
- the first increment renders the derivation in `harnessctl inspect` only; the
  dashboard and explorer surfaces are deferred to separately approved work
  (`REQ-DLC-003`, `WO-DLC-002` out of scope, `VER-DLC-001` residual);
- `E022` and `W025` are reserved, with next-free fallback if a concurrent change
  takes them (`REQ-DLC-004`);
- `W025` is emitted once per grandfathered definition on every run; aggregation
  and a verbose-only rendering are both forbidden, and the verdict grows from 50
  warnings to 499 (`REQ-DLC-004`, `SPEC-DLC-003`);
- outcome preservation is an exact-equality gate, and a reduced warning count
  fails (`REQ-DLC-005`); and
- `commit_bound_verification = "required"` on all three work orders
  (`REQ-DLC-005`).

Two questions are deliberately left open for the accountable role rather than
decided here: the declaration packet's field name (`REQ-DLC-001`) and the
`implemented` row's `predecessor_adapter` value (`REQ-DLC-002`). Both sit inside
an implementation agent's authorized envelope.

Every artifact remains `draft`. This packet authorizes no implementation,
lifecycle transition, Git action, or external action. The decisions above are the
repository owner's answers on the packet's content; they are not an approval of
any artifact in it, and no status has moved. The `[assurance]` classifications in
the three work orders now record the engineering owner's decision of 2026-08-26;
the approval of the work orders themselves remains outstanding.
