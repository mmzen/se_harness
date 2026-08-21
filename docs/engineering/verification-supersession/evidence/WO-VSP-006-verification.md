# WO-VSP-006 supersession evidence

Date: 2026-08-21

## Authority and preliminary decision review

The accountable owner separately authorized an assurance owner to review and explicitly disposition only `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003`. Review selects verified `VREC-WEX-005` as the direct successor because it covers both `WO-WEX-001` and `WO-WEX-002`, conforms to both `VER-WEX-001` and `VER-WEX-002`, and is the verified aggregate correction that already supersedes intermediate aggregate `VREC-WEX-004`.

No active RLS references any of the three sources. The intended edges preserve work-order coverage without a cycle:

- `VREC-WEX-001 -> VREC-WEX-005`;
- `VREC-WEX-002 -> VREC-WEX-005`; and
- `VREC-WEX-003 -> VREC-WEX-005`.

This governance-only decision is not one of the eight release-bearing 0.6.0 work orders and grants no candidate commit, aggregate capture, VREC or RLS release decision, tag, publication, deployment, or root upgrade.

## Original identities

| Record | Status | Work orders | Contracts | Original file SHA-256 |
| --- | --- | --- | --- | --- |
| `VREC-WEX-001` | `ready` | `WO-WEX-001` | `VER-WEX-001` | `71dc7a1630e8653db364aa01b606187a870b86c41bac299519fa32fa3ec5be4e` |
| `VREC-WEX-002` | `ready` | `WO-WEX-001` | `VER-WEX-001` | `e128b8aa7e2b64d6165c4a9a03399c1713608878329f3d1cb8574ee84c27de21` |
| `VREC-WEX-003` | `ready` | `WO-WEX-002` | `VER-WEX-002` | `7b2ab53d5edc02362d699cf49f37a4b82a3ecf9b8c2f4ede606a3b3c7e16521f` |
| `VREC-WEX-005` | `verified` | `WO-WEX-001`, `WO-WEX-002` | `VER-WEX-001`, `VER-WEX-002` | `67581052979d843464b658baa2c06967ead0bffda007e9a998db8ea42557f0dd` |

## Applied decision and field preservation

At `2026-08-21T14:10:10Z`, the assurance owner transitioned all three sources from `ready` to `superseded`, set `supersession_authorized_by = "assurance-owner"`, added exactly one `superseded_by = ["VREC-WEX-005"]` relation, and retained an attributable lifecycle event. Final hashes are:

| Record | Final file SHA-256 |
| --- | --- |
| `VREC-WEX-001` | `35e3b7694bf3bca993b27d00adac9252f8ffa0d2f0edc182b9eafc2c3419a4ab` |
| `VREC-WEX-002` | `b2eb9a0c25e0be438c183e7b05cc11b8844d5fe63dfb54cb714ad21c19e74803` |
| `VREC-WEX-003` | `d3f4ce409d9a70892dd537ad238dbcbaea3b3d3f801e5ed79b2fdebd9003f896` |

Diff review against `HEAD` confirms that `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, `evidence_paths`, `verifies_work_order`, and `conforms_to` remain byte-for-byte unchanged for every source. Only status, supersession fields and relation, lifecycle event, and explanatory narrative changed. `VREC-WEX-005` remains unchanged at SHA-256 `67581052979d843464b658baa2c06967ead0bffda007e9a998db8ea42557f0dd`.

## Verification

- The isolated released 0.5.0 evaluator passed start preflight for `WO-VSP-006` with the complete 21-file governing manifest.
- Candidate 0.6.0 produced a read-only atomic three-record transition plan with no blockers and exactly the permitted write-field set. It was not permitted to mutate the installed root.
- Because released 0.5.0 predates the `transition` command, the already authorized human decisions were recorded directly from that plan, then checked with the exact external released evaluator.
- Released-evaluator graph validation passed with 597 artifacts, 0 errors, and the existing 44 maintenance warnings; structure, governance, and policy planes have no warnings.
- Released-evaluator inspection reports 597 artifacts, 2,140 relations, 44 maintenance findings, zero decisions required, and no assurance-pending records.
- The complete amended Python 3.14.6 suite passed 369 tests in 184.924 seconds with five conditional platform/privilege skips and zero failures or errors.
- The same suite passed on Python 3.11.9: 369 tests in 187.069 seconds with the same five conditional skips and zero failures or errors.
- The current-version documentation contract, Git-backed release-manifest case, workflow JSON byte-parity case, supersession validation, inspection, and Explorer cases all pass within that suite.
- No active RLS back-reference to a source exists; no cycle or coverage loss exists.
- Released-evaluator review preflight passed for implemented `WO-VSP-006` with the complete 21-file governing manifest.
- Final released-evaluator doctor, graph validation, inspection, Explorer generation, release-distribution validation, and `git diff --check` pass in the repository-wide audit.

This governance-only work has `commit_bound_verification = "not_required"` because it records an already authorized assurance decision and changes no executable or managed behavior.

## Authority boundary

No operational candidate commit, aggregate VREC preparation or transition, RLS preparation or transition, tag, publication, deployment, root-evaluator upgrade, successor mutation, or other lifecycle decision occurred.
