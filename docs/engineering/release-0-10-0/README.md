# Release 0.10.0 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.10.0 from the immutable `v0.9.0` baseline (`8adfe1bdeb19b4e6014b7f13afd7da5789846750`, `RLS-SEH-018`). The packet was derived on 2026-08-29 over `main` at `3139f24`.

0.10.0 is an ordinary schema-3 release. The root lock is exact public 0.9.0 (adopted by `WO-HUP-009`) and that released evaluator validates the complete current graph without error.

## Why 0.10.0

The release that repairs the three defects the 0.9.0 adoption exposed on the day it landed: the released evaluator refused `evidence` and `check` on Windows (`WO-ECP-012`, issue #254); the managed pull-request gate was red by construction from a work order's completion to its merge and never enforced on a packet-only pull request (`WO-ECP-013`, issue #255, the `scope` checkpoint); and the formal snapshot depended on the checkout's line endings, so a packet bound on Windows could never pass the hosted lane (`WO-ECP-014`, issue #256). It also carries the root adoption of 0.9.0 itself (`WO-HUP-009`) and the `harnessctl check` reference.

Consumers, and this repository after adopting it, obtain the state-independent gate and the Windows repairs only through a release.

## Release packet

- `REL-SEH-021` (`draft`): the exact 0.10.0 release unit as a five-work-order allow-list, the complete commit census from `v0.9.0` with four named exemptions, aggregate-assurance requirements, promotion policy, rollback and observation window.
- `WO-RLS-016` (`draft`): qualify the candidate, run the recipe-bound reproducible build, retain the bundle manifest and evidence, maintain the indexes. No version move: the candidate already reads 0.10.0 (`WO-HUP-009`).
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-019`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-019`.

The authoritative state of every artifact is its own front matter and `[[lifecycle_events]]`, not this index.

## Release unit shape

Five work orders: the four landed since `v0.9.0` and `WO-RLS-016`. Measured over the whole `gates` array at `3139f24`: five verification contracts, a six-requirement union, five work-order-keyed evidence paths:

- `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009/WO-HUP-009-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-012/WO-ECP-012-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-013/WO-ECP-013-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-014/WO-ECP-014-handoff.md`
- `docs/engineering/release-0-10-0/evidence/WO-RLS-016-verification.md` (to be written by `WO-RLS-016`)

## Census note

The four merges on the first-parent path since `v0.9.0` are GitHub merge commits without a trailer and are exempted by name in the contract; the branch commits behind each carry the `Harness-Work-Order:` trailer in one final paragraph and are parseable, but `harnessctl release-unit` walks the first-parent path only. `WO-RLS-015` is traced through the 0.9.0 release-record commits that follow the tag and is not a member: `RLS-SEH-018` released it.
