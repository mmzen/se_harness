# Release 0.9.0 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.9.0 from the immutable `v0.8.0` baseline (`884b769efdc9eda2959f2c774e6af10748beb88a`, `RLS-SEH-017`). The packet was derived on 2026-08-28 over `main` at `effbcbc`.

0.9.0 is an ordinary schema-3 release. The root lock is exact public 0.8.0 (adopted by `WO-HUP-008`) and that released evaluator validates the complete current graph without error.

## Why 0.9.0

The release that carries the first three steps of the execution-control-plane plan recorded in `ADR-AEX-008`: `harnessctl next` and Git-derived change sets (`WO-ECP-001`), harness-authored evidence packets, identifier allocation and `pr-body` (`WO-ECP-002`), and the managed workflow's mandatory, scope-aware pull-request gate with a digest that covers the change set (`WO-ECP-003`). It also carries the root adoption of 0.8.0 (`WO-HUP-008`), the deletion of the retired governance-migration stage machine (`WO-ECP-011`, closing issue #210) and the interpreter-safety rule kept in code (`WO-REB-030`, closing issue #220).

Two facts make this release the right next step rather than more plan work: consumers, and this repository after adopting it, only obtain the four new commands and the mandatory gate through a release; and `WO-ECP-006`, the delegation class, should stand behind the gate this release ships.

## Release packet

- `REL-SEH-020` (`draft`): the exact 0.9.0 release unit as a seven-work-order allow-list, the complete commit census from `v0.8.0` with nine named exemptions, aggregate-assurance requirements, promotion policy, rollback and observation window.
- `WO-RLS-015` (`draft`): qualify the candidate, run the recipe-bound reproducible build, retain the bundle manifest and evidence, maintain the indexes. No version move: the candidate already reads 0.9.0 (`WO-HUP-008`).
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-018`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-018`.

The authoritative state of every artifact is its own front matter and `[[lifecycle_events]]`, not this index.

## Release unit shape

Seven work orders: the six landed since `v0.8.0` and `WO-RLS-015`. Measured over the whole `gates` array at `effbcbc`: seven verification contracts, a thirteen-requirement union, seven work-order-keyed evidence paths:

- `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-verification.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-011/WO-ECP-011-verification.md`
- `docs/engineering/released-evaluator-boundary/evidence/WO-REB-030-verification.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-001/WO-ECP-001-verification.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-002/WO-ECP-002-handoff.md`
- `docs/engineering/execution-control-plane/evidence/WO-ECP-003/WO-ECP-003-handoff.md`
- `docs/engineering/release-0-9-0/evidence/WO-RLS-015-verification.md` (to be written by `WO-RLS-015`)

## Census note

Every merge on the first-parent path since `v0.8.0` is exempted by name in the contract: the branch commits behind them carry their `Harness-Work-Order:` line as body text followed by a separate `Co-Authored-By` paragraph, which Git does not parse as a trailer, so `harnessctl release-unit` cannot trace them. The membership is therefore established by the contract's allow-list and by each work order's own lifecycle and evidence, as for the 0.8.0 merges. Commits from this packet onward carry both lines in one final trailer paragraph.
