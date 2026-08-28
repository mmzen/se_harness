# Release 0.8.0 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.8.0 from the immutable `v0.7.1` baseline (`58efcaa1dfbb8f5921e82c72b6cc40add0c9a36c`, `RLS-SEH-016`). The packet was derived on 2026-08-28 against `main` at `ff0e3376e0eb9d7622828a5a843f244988860ec8`.

0.8.0 is an ordinary schema-3 release. The root lock is exact public 0.7.1 and that released evaluator validates the complete current graph without error.

## Why 0.8.0

The first release after the 2026-08 complexity audit. It carries the P0 repairs that landed under it — the retired predecessor-bootstrap bridge (`WO-REB-028`, `WO-REB-029`), the fresh-consumer `doctor` fix (`WO-HBI-005`), one workflow kernel (`WO-ECP-005`, `WO-ECP-009`), the real upgrade rehearsal (`WO-ECP-010`), the string-form pin retarget (`WO-AUT-003`) — plus the adoption of 0.7.1 as root (`WO-HUP-007`) and the host-independent candidate export (`WO-RLO-008`). The kernel and gate-contract changes are interface changes, which is why this is 0.8.0 and not 0.7.2.

## Release packet

- `REL-SEH-019` (`draft`): the exact 0.8.0 release unit as a ten-work-order allow-list, the complete commit census from `v0.7.1` with fifteen named exemptions, aggregate-assurance requirements, promotion gates, human approval triggers, and rollback policy.
- `WO-RLS-014` (`draft`): qualify the candidate, run the recipe-bound reproducible build, retain the bundle manifest and evidence, maintain the indexes. No version move: the candidate already reads 0.8.0.
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-016`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-017`.

The authoritative state of every artifact is its own front matter and `[[lifecycle_events]]`, not this index.

## Entry condition

`VREC-REB-026` and `VREC-REB-027` (covering `WO-REB-028` and `WO-REB-029`) were `ready` at drafting and were verified by the assurance owner on 2026-08-28 on this packet's branch; every member now holds verified coverage. Their decision reasons over-state one re-measurement (the evidence documents were appended after their candidates, prefix preserved); `REL-SEH-019`'s entry criteria carry the correction.

## Release unit shape

Ten work orders: the nine landed since `v0.7.1` and `WO-RLS-014`. Measured over the whole `gates` array at `ff0e337`: nine verification contracts, a twelve-requirement union, eleven work-order-keyed evidence paths:

- `docs/engineering/artifact-authoring/evidence/WO-AUT-003-verification.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-005/WO-ECP-005-verification.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-009/WO-ECP-009-verification.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-010/WO-ECP-010-verification.md`
- `docs/engineering/hash-bound-integrity/evidence/WO-HBI-005-verification.md`
- `docs/engineering/release-orchestration/evidence/WO-RLO-008/WO-RLO-008-verification.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-028-verification.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-029-verification.md`
- `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-007-verification.md` (and `WO-HUP-007-evaluator-upgrade.json`)
- `docs/engineering/release-0-8-0/evidence/WO-RLS-014-verification.md` (retained by `WO-RLS-014`)

The commit census (`harnessctl release-unit . --from v0.7.1 --to ff0e337`) traces `WO-HUP-007`, `WO-RLO-008` and the tail of `WO-RLS-013` from trailers and reports fifteen first-parent merge commits without one; each is named and exempted in the contract with its reason.

## Evidence

`evidence/WO-RLS-014-verification.md`, then the aggregate record's evaluator evidence and the release record's bundle and evaluator evidence, all retained under `evidence/`.
