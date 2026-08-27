# Release 0.7.1 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.7.1 from the immutable `v0.7.0` baseline, whose released candidate commit is `374554d01f9a2e4601dc5b58279a01de2c7b6523` (`RLS-SEH-015`). The packet was derived on 2026-08-27 against `main` at `f605e580e6366a739dc020559cac35a89e1ffc39`.

0.7.1 is an ordinary schema-3 release, like 0.7.0. The root lock is exact public 0.6.0 and that released evaluator validates the complete current graph without error; `REL-SEH-018` declares no `[bootstrap]` table.

## Why 0.7.1

The repository owner's standing direction of 2026-08-27: the released-evaluator upgrade must be simple and straightforward, so the archive-digest gate `MG004` and the work-order binding `MG007` go. `WO-REB-027` implemented that on `main` with verified coverage; it is the payload of this release, and it is what lets this repository adopt a released evaluator by `pip install` and `harnessctl upgrade . --apply` (the 0.7.0 adoption, `WO-HUP-006`, was rejected on that direction). Three verified repairs to ordinary-record release mechanics that landed after the 0.7.0 candidate, `WO-REB-024` through `WO-REB-026`, ride along.

## Release packet

- `REL-SEH-018` (`draft`): the exact 0.7.1 release unit as a five-work-order allow-list, the complete commit census from `v0.7.0` with six named exemptions, aggregate-assurance requirements, promotion gates, human approval triggers, and rollback policy.
- `WO-RLS-013` (`draft`): move the candidate identity to 0.7.1 together with its governance-migration scenario, qualify the candidate, run the recipe-bound reproducible build, retain the bundle manifest and evidence, maintain the indexes.
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-015`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-016`.

The authoritative state of every artifact is its own front matter and `[[lifecycle_events]]`, not this index.

## Release unit shape

Five work orders: the four verified since `v0.7.0` and `WO-RLS-013`. Measured over the whole `gates` array at `f605e58`: four verification contracts (`VER-DST-001`, `VER-REB-004`, `VER-REB-006`, `VER-REB-011`), a six-requirement union (`REQ-DST-006`, `REQ-REB-011`, `REQ-REB-012`, `REQ-REB-015`, `REQ-REB-027`, `REQ-REB-028`), five work-order-keyed evidence paths (four existing plus the one `WO-RLS-013` retains).

The commit census (`harnessctl release-unit . --from v0.7.0 --to f605e58`) traces `WO-REB-027` from the merge commit of pull request #198 and reports six first-parent commits without a `Harness-Work-Order` trailer: the merge commits of pull requests #184, #183, #185, #186, #188 and #197. Each is named and exempted in the contract with its reason; the derivation with those exemptions is complete. The contract names no `candidate_commit` because the candidate does not exist before `WO-RLS-013` runs, so `QGP-G5P-RELEASE-UNIT` passes unmeasured, as it did for `REL-SEH-017`.

## Candidate version and scenario

`pyproject.toml`, `se_harness/__init__.py` and the README install line move to 0.7.1 in the same change as the governance-migration scenario `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.1.json`, written by `python -m repository_tools.predecessor_facts write-scenario` from the 0.7.0 pair; the 0.7.0 pair is retired because the lane derives exactly one scenario from the root and the candidate version. The tests that pin the candidate version follow.

## Evidence

`evidence/WO-RLS-013-verification.md`, then the aggregate record's evaluator evidence and the release record's bundle and evaluator evidence, all retained under `evidence/`.
