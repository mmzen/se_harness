# Release 0.11.0 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.11.0 from the immutable `v0.10.0` baseline (`69ee77a673a25a28535a03ebfaa5c29b454e1f5f`, `RLS-SEH-019`). The packet was derived on 2026-08-29 over `main` at `8db0b96` with the exact public 0.10.0 evaluator outside the checkout.

0.11.0 is an ordinary schema-3 release. The root lock is exact public 0.10.0 (adopted by `WO-HUP-010`) and that released evaluator validates the complete current graph without error.

## Why 0.11.0

One day of governed work on the 0.10.0 root: the root adoption itself (`WO-HUP-010`); one projection command, `check`, with `focus` folded in and then removed (`WO-ECP-015`, `WO-ECP-017`); the scope and handoff checkpoints admitting a work order's own records by construction (`WO-ECP-016`, issue #264); and the execution of the Phase 4 decision — the envelope, bundle, broker, `delegated-workflow` command and the stubbed writing skills removed, the journaled apply kept (`WO-ECP-006`, `ADR-ECP-002`).

Consumers, and this repository after adopting it, obtain these only through a release.

## Release packet

- `REL-SEH-022` (`draft`): the exact 0.11.0 release unit as a six-work-order allow-list, the complete commit census from `v0.10.0` with one named exemption, aggregate-assurance requirements, promotion policy and the latest-marker step.
- `WO-RLS-017` (`draft`): qualify the candidate, run the recipe-bound reproducible build, retain the bundle manifest and evidence, maintain the indexes. No version move: the candidate already reads 0.11.0.
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-020`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-020`.

The authoritative state of every artifact is its own front matter and `[[lifecycle_events]]`, not this index.

## Release unit shape

Six work orders: the five landed since `v0.10.0` and `WO-RLS-017`. Measured over the whole `gates` array at `8db0b96`: seven verification contracts, an eight-requirement union, six work-order-keyed evidence paths:

- `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010/WO-HUP-010-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-015/WO-ECP-015-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-016/WO-ECP-016-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-017/WO-ECP-017-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-006/WO-ECP-006-handoff.md`
- `docs/engineering/release-0-11-0/evidence/WO-RLS-017/WO-RLS-017-handoff.md` (to be written by `WO-RLS-017`)

## Census note

Eight merges sit on the first-parent path since `v0.10.0`. Since `RLS-SEH-019` the derivation follows each merge to its second-parent trailers, so seven trace: `103127c` (#260) to `WO-RLS-016`, released by `RLS-SEH-019` and excluded; the other six to the five members. `47f67de` (#261) merged a documentation pull request with no work order and is the one exemption.
