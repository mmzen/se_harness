# Release 0.7.0 Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the integration and qualification of SE Harness 0.7.0 from the immutable `v0.6.0` baseline, whose tag object is `03cae3d30ea1e3933a92c9e87683b0144f8ccc77` and whose released candidate commit is `3b339e9fc70cc634e6dc6bda07ea6a9b1a465798`. The packet was last re-derived against `main` commit `73b7b5437637bc2ac2d9af2c8c9295b4d4475d68`, tree `4497eb9c94eef17ff8a214c46dafa8a8c4fdfbfc`.

0.7.0 is the first **ordinary** release of this repository. The root lock is schema 3 at exact public 0.6.0, and that released evaluator validates the complete current graph without error. No predecessor-bootstrap contract, derived compatibility view, or expected-red managed lane applies, so `REL-SEH-014` declares no `[bootstrap]` table. The predecessor-bootstrap rules in `docs/notes/developing-se-harness.md` remain a historical description of the 0.6.0 release only.

## Release packet

- `REL-SEH-014` (`approved`): exact 0.7.0 release unit, baseline and exclusions, `WO-TCM-001`'s coverage and its accepted limitation, `WO-AEX-005`'s admission, aggregate-assurance requirements, promotion gates, human approval triggers, and rollback policy.
- `WO-RLS-010` (`approved`): bounded versioning, integration, qualification, recipe-bound reproducibility, package acceptance, index maintenance, retained evidence, and aggregate-VREC preparation work.
- `REL-SEH-012`, `REL-SEH-013`, and `WO-RLS-009`: rejected predecessors, retained as immutable history and all terminal. `REL-SEH-012` named a thirty-three-gate allow-list; `REL-SEH-013` carried the corrected thirty-four-gate unit and was approved before being retired with `WO-RLS-009`.
- Proposed aggregate verification record after an approved and committed candidate: `VREC-SEH-013`.
- Proposed release record after verified aggregate assurance and separately authorized preparation: `RLS-SEH-013`.

Both were approved in one atomic transition at 2026-08-25T11:53:28Z: `REL-SEH-014` by the release owner and `WO-RLS-010` by the engineering owner. The owner had approved the identical thirty-four-work-order unit once before, as `REL-SEH-013` at 2026-08-25T11:38:12Z, but that contract is rejected and its approval was not reused as authority; the decision was put again and taken on the successors' own terms. Their authoritative state is the front matter and `[[lifecycle_events]]` of each artifact, not this index. Start preflight is now unblocked, and the governance commit carrying this packet was a separate authorization from the approval.

## Release unit shape

The release unit is thirty-four work orders: the thirty-three release-bearing work orders measured after `v0.6.0`, plus `WO-RLS-010` itself. It aggregates nineteen verification contracts, forty-one requirements, and thirty-five work-order-keyed evidence paths (thirty-four existing plus one `WO-RLS-010` retains). `REL-SEH-014` names every member explicitly; the set is an allow-list, not an inference from dates, branches, or merge order.

`WO-HUP-002` is excluded because it adopted exact public 0.6.0 as this repository's own root evaluator, the same class of change that `REL-SEH-007` excluded by name as `WO-HUP-001`. `WO-AEX-006` through `WO-AEX-008` are excluded because they are approved, not started, and must proceed sequentially after `WO-AEX-005`; the owner decided on 2026-08-25 to ship 0.7.0 without waiting for them. The plugin-distribution exploration note is excluded because the owner decided it needs no artifact or work order.

## Why the contract was re-issued twice

`REL-SEH-012` was approved at 2026-08-25T10:28:10Z. `WO-AEX-005` reached `implemented` at 2026-08-25T10:29:40Z, ninety seconds later, and its authorized bytes are inside the packaged surface, so the approved allow-list stopped describing the release unit almost immediately. An approved allow-list is not widened in place. The 0.6.0 history is the precedent: `REL-SEH-008`, `REL-SEH-009`, and `REL-SEH-010` were each rejected and re-issued as that unit grew from nine to fourteen gates under `REL-SEH-011`. The release owner therefore rejected `REL-SEH-012` and issued `REL-SEH-013` with the thirty-four-gate unit, which the owner approved.

The second succession is about the work order, not the unit. `WO-RLS-009`'s aggregate scope had been amended to match the new unit, but the owner never approved that amendment, and the governing evaluator refuses an `approved` to `approved` transition (`WEX201`), so no re-approval event could be recorded on it. Shown three measured routes, the owner chose to reject `WO-RLS-009` and issue `WO-RLS-010`. Because `REL-SEH-013` named `WO-RLS-009` in `gates`, that left an approved contract naming a rejected member, and an approved contract is not repaired in place either — so `REL-SEH-013` and `WO-RLS-009` were rejected in one atomic transaction at 2026-08-25T11:47:44Z and re-issued as `REL-SEH-014` and `WO-RLS-010`. `WO-RLS-010` declares `REQ-DST-006`, `SPEC-DST-001`, `ARCH-DST-001`, `ADR-DST-001`, and `VER-DST-001` rather than a release contract, so a later contract succession will break no graph edge pointing at it. No work was started under any rejected artifact: no start preflight, no version move, no build, no candidate commit.

## `WO-TCM-001`: covered, with an accepted limitation

`WO-TCM-001` was `in_progress` with no verified coverage when this packet was drafted, while its authorized bytes were already on `main`. On 2026-08-25 the owner accepted it into the release unit and authorized its transition; the engineering owner applied `in_progress` to `implemented` at 2026-08-25T10:21:06Z. Admitting it raised the unit from thirty-two work orders to thirty-three and the requirement union from thirty-seven to forty. The verification-contract and keyed-evidence counts did not move, because `VER-TCM-001` and the combined TCM evidence file already serve both TCM work orders.

Coverage is now closed but qualified. `VREC-TCM-002` binds candidate commit `f7b69d0ad40321caa0520f9fed137be8e32bcf1f` and was verified at 2026-08-25T10:51:11Z, reaching `main` through the true merge of pull request #151. The record discloses, permanently, that `VER-TCM-001`'s manual-assessment conditions are not evidenced: the two independent reviewer judgments over rendered corpus output do not exist and no retained manual review form covers them. The owner verified with that gap as accepted residual risk. So `WO-TCM-001` holds verified coverage that is **not** a claim of conformance to `VER-TCM-001`'s semantic and operator-comprehension conditions, and `VREC-SEH-013` must not restate it as unqualified. Recording those judgments would need a successor record binding a new manual review form, which is later governed work outside this release unit.

## `WO-AEX-005`: admitted, and inert

`WO-AEX-005` is `implemented` as of 2026-08-25T10:29:40Z and verified by `VREC-AEX-005` at 2026-08-25T10:39:01Z against `VER-AEX-001` and `VER-AEX-004`. Two parts of it reach adopting repositories and are the reason it must be in the unit: the managed work-order template gains an optional `[agentic_delegation]` table with its guidance paragraph, and the distributed managed validator gains the rules that check it. The table is optional and declarative — it records a maximum delegation, starts no work, and grants no standing authority.

Its four new runtime modules (`agent_contract.py`, `delegated_authority.py`, `repository_state.py`, `runtime_state.py`) are reachable only from each other. `se_harness/cli.py` references none of them and no command path invokes `delegated_authority`, so they are inert in 0.7.0 and activate only when `WO-AEX-006` through `WO-AEX-008` land. Publishing 0.7.0 ships governed, verified, tested, unreachable scaffolding, and the release notes must not describe delegated execution as available.

## Firsts this release exercises

- First ordinary complete-graph release under the schema-3 root.
- First `[distribution] schema = 2` recipe-bound release record.
- First release built through recipe-bound replay (`WO-RLO-004`), rehearsed credential-free on both runner platforms (`WO-RLO-005`), and assessed through portable governor succession (`WO-HUP-004`).
- First release carrying the declared hash-bound text classes (`WO-HBI-001`, `WO-HBI-002`), declared byte rules (`WO-HBI-003`, `WO-HBI-004`), the `qualify` and `migrate` command namespaces (`WO-REB-018`, `WO-REB-020`), the agent and skill contracts (`WO-AEX-001` through `WO-AEX-004`), the optional work-order delegation surface (`WO-AEX-005`), and the managed technical-communication route (`WO-TCM-001`, `WO-TCM-002`).

## What is not authorized

`WO-RLS-010`'s approval authorizes start preflight and then only the declared versioning, integration, qualification, recipe-bound reproducible-build, index-maintenance, and retained-evidence work inside its six scoped paths. Nothing has been started under it: no start preflight, no version move, no build, no candidate commit.

Everything else remains a separate action-time decision and none of it is authorized by the approvals recorded here: the candidate commit, the version bump, a promotable build, `VREC-SEH-013` or `RLS-SEH-013` preparation or transition, tag creation or movement, GitHub or PyPI publication, Pages deployment, `release/0.7` maintenance-line mutation, credential use, external policy change, and root-evaluator upgrade.
