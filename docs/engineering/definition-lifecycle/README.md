# Definition Lifecycle Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this directory
> or index.

This domain requires that a definition's lifecycle status answer exactly one
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

## Packet contents

The fourteen definitions are `approved`. `WO-DLC-001` is `approved`;
`WO-DLC-002` and `WO-DLC-003` are `draft`.

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

## Definition approval taken 2026-08-26

The repository owner approved the definition packet on 2026-08-26 through the
instruction `i approve the artifact pack`. The fourteen definitions moved
`draft -> approved` in one atomic transition packet, each recording the role that
exercised `DR-DEFINITION-DECIDE` for its artifact type: `product-owner` for the
intent and capability, `requirements-steward` for the five requirements,
`technical-owner` for the three specifications, the two ADRs, and the
architecture, and `assurance-owner` for the verification contract. Every chain is
recorded in the artifact itself; this paragraph is an index entry, not the record.

Acceptance of `ADR-DLC-001` and `ADR-DLC-002` satisfies the `adr_required`
outcome in `ARCH-DLC-001`'s `decision_assessment`.

Approving a definition is `DR-DEFINITION-DECIDE`. It authorizes no
implementation, no work-order start, no Git action, and no external action, and it
does not approve a work order: that is `DR-WO-SELECT`, a different decision right
held by the engineering owner, and nothing is approved by implication.

## Work-order authorization taken 2026-08-26

The engineering owner approved `WO-DLC-001` on 2026-08-26, exercising
`DR-WO-SELECT` on that work order alone. `WO-DLC-002` and `WO-DLC-003` remain
`draft` by the same decision, so increment 1's scope is the only bounded work
authorized in this domain.

`WO-DLC-003` was deliberately not authorized alongside it. `SPEC-DLC-003` permits
its authorization once `REQ-DLC-001` and `REQ-DLC-002` are approved, which they
now are, but the reason that rule gives is that its frozen 449-identifier set must
be measured after the first two increments settle. Authorizing scope built on a
figure that cannot yet be measured would make the authorization weaker than it
looks, so each remaining increment is authorized in its turn.

The `[assurance]` classification on all three work orders records the engineering
owner's decision of 2026-08-26 on the classification only, independently of
whether the work order is approved.

Starting `WO-DLC-001` is a further `DR-WO-START` decision behind
`QG-G3-WORK-AUTHORIZATION`. It has not been taken, and no implementation has
begun.
