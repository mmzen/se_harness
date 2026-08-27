# Release 0.7.0 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.7.0 from the immutable `v0.6.0` baseline, whose tag object is `03cae3d30ea1e3933a92c9e87683b0144f8ccc77` and whose released candidate commit is `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`. The current packet was derived on 2026-08-26 against `main` at `be2f0cfec18b86d273400466cdf1c8c691d92f75`, tree `fd9bccb5631bef0279ae92c40353b818016cd277`.

0.7.0 is the first **ordinary** release of this repository. The root lock is schema 3 at exact public 0.6.0, and that released evaluator validates the complete current graph without error. No predecessor-bootstrap contract, derived compatibility view, or expected-red managed lane applies, so `REL-SEH-017` declares no `[bootstrap]` table.

## Release packet

- `REL-SEH-017` (`draft`): the exact 0.7.0 release unit as a fifty-three-work-order allow-list, the reported commit census, baseline and exclusions, the disclosed limitations carried from `REL-SEH-015`, aggregate-assurance requirements, promotion gates, human approval triggers, and rollback policy.
- `WO-RLS-012` (`draft`): the remaining qualification of the final candidate, the recipe-bound reproducible build, the bundle manifest, index maintenance, and retained evidence, with its aggregate census deferred to the contract.
- `WO-RLS-011` (`implemented`): moved the candidate identity to 0.7.0 and retained the first qualification evidence; its candidate `f76da5727e86fc53375bfa5cafcfcbf168c7456e` is on `main`. It is a member of the unit, covered by the planned aggregate record; the workflow contract admits no rejection from `implemented`.
- `REL-SEH-012` through `REL-SEH-015`, `WO-RLS-009`, and `WO-RLS-010`: rejected predecessors, retained as immutable history and all terminal.
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-014`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-014`.

The authoritative state of every artifact is its own front matter and `[[lifecycle_events]]`, not this index.

## Why `REL-SEH-015` was rejected and `REL-SEH-016` is not reused

`REL-SEH-015` froze a thirty-six-gate allow-list at 2026-08-25T12:57:58Z and declared any later `implemented` work order with packaged-surface bytes a stop condition. Sixteen such work orders reached `main` with verified coverage: `WO-RLO-006`, `WO-REB-023`, `WO-AEX-006` through `WO-AEX-008`, `WO-AUT-001`, `WO-AUT-002`, `WO-CIP-001` through `WO-CIP-005`, `WO-RLO-007`, and `WO-TST-001` through `WO-TST-003`. The release owner rejected the contract at 2026-08-26T20:48:50Z.

A first successor, `REL-SEH-016`, was approved on a thirty-eight-gate unit on the branch of pull request #169, where `VREC-SEH-013` was verified and `RLS-SEH-013` prepared. The owner decided on 2026-08-26 that the attempt had failed and closed #169 unmerged. Nothing from it reaches `main`; because identifiers are shared across branches, `REL-SEH-016`, `VREC-SEH-013`, and `RLS-SEH-013` are treated as spent, and this packet uses `REL-SEH-017`, `VREC-SEH-014`, and `RLS-SEH-014`.

## Release unit shape

Fifty-three work orders: the thirty-five historical members `REL-SEH-015` named, the sixteen verified since, `WO-RLS-011`, and `WO-RLS-012`. Measured over the whole `gates` array at `be2f0cf`: twenty-four verification contracts, sixty-five requirements, fifty-eight work-order-keyed evidence paths (fifty-seven existing plus the one `WO-RLS-012` retains). On the fifty-one-member historical basis the same measurement gives twenty-three contracts and sixty-four requirements; the contract states the whole-`gates` basis so an aggregate record cannot mix the two.

The contract keeps the allow-list form. The commit census (`harnessctl release-unit . --from v0.6.0 --to be2f0cf`) traces nine work orders and reports ninety-three untraced commits, because the trailer convention post-dates most of the history; the owner chose on 2026-08-26 to report the census as evidence rather than enforce it, so the contract names no `candidate_commit` and `QGP-G5P-RELEASE-UNIT` passes unmeasured.

Forty-five implemented, unreleased work orders are excluded by name-class: documentation, revision-provenance, publication-history, verification-supersession, work-order-lifecycle, root-evaluator adoption, RCA, and historical release-disposition work whose execution scope names no packaged-surface path. `REL-SEH-017` lists them.

## Disclosed limitations

Carried unchanged from `REL-SEH-015`: `VER-TCM-001`'s two reviewer judgments do not exist (`VREC-TCM-002`); `VER-ADS-001`'s Scenario 8 classifications were not run and both ADS records were verified with the hosted Linux figure pending. `WO-AEX-005`'s scaffolding is no longer inert now that Phase 4 is in the unit. `VREC-SEH-014` must not restate any of this coverage as unqualified.

## What is not authorized

Nothing in this packet is approved. `WO-RLS-012`'s approval, `REL-SEH-017`'s approval, work start, the candidate commit and its push, `VREC-SEH-014` and `RLS-SEH-014` preparation and transition, the tag, GitHub or PyPI publication, Pages deployment, `release/0.7` maintenance-line mutation, credential use, external policy change, and root-evaluator upgrade are each a separate later decision.
