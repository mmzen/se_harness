# Verification evidence for WO-VSP-002

Date: 2026-08-13

## Accountable supersession decision

After `VREC-DST-008` was retained in a separate ready-record commit, transitioned through the owner's accountable assurance decision, and retained as verified, the repository owner explicitly instructed `ok for WO-DST-007 supersession then so the graph is clean`. In context, the requested target is ready record `VREC-DST-007`; work order `WO-DST-007` remains implemented and unchanged. This is the separate human decision authorizing the record's `ready -> superseded` transition and normal retention on PR 35. Automation validates and visualizes the decision but does not grant it.

## Source and successor

| Fact | Value |
| --- | --- |
| Source | `VREC-DST-007`, previously `ready` |
| Source candidate | `52e713a9b041a0c8355f2ad8ad8f71c7dd65d1f2` |
| Source work set | `WO-DST-007` |
| Source ready SHA-256 | `c0368b850068997f7ce0fedeae7313e1667f2c3ff03ddda2c3cb7f623afbe75c` |
| Source superseded SHA-256 | `37b839d0715f81b17761e98018570849163774ccc5ec9f59b72b820450d494b0` |
| Successor | `VREC-DST-008`, `verified` |
| Successor candidate | `e5ac607f485b33b8e5e45c8198d52d5bc16f1081` |
| Successor work set | `WO-DOC-011`, `WO-DST-007` |
| Successor SHA-256 | `4613db8a76ef2cb9b9470cc0cef214815dafe4317785ce588963b59b6125d30f` |
| Transition time | `2026-08-13T17:51:56Z` |
| Authorized by | `repository-owner` |
| Declared edge | `VREC-DST-007 --superseded_by--> VREC-DST-008` |

Set inspection confirms the successor work set is a strict superset of the source work set. A repository-wide metadata inspection found no ready or released release record whose `includes_verification` relation references `VREC-DST-007`.

## Transition integrity

A TOML metadata comparison against the ready bytes retained in governance history confirmed exact preservation of `id`, `type`, `title`, `owners`, `created`, `updated`, `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, and `evidence_paths`. Original `verifies_work_order` and `conforms_to` relations are also unchanged.

The bounded record diff adds only the permitted `superseded` status, `superseded_at`, `supersession_authorized_by`, one `superseded_by` relation, and explanatory decision text. The old record is retained and is not deleted, rewritten as verified, or made to identify the newer candidate.

## Commands and results

| Check | Result |
| --- | --- |
| `python -B scripts/validate_engineering_artifacts.py --root .` | PASS: 284 artifacts, 0 errors, 38 classified historical warnings |
| start preflight for `WO-VSP-002` | PASS while `approved`, then PASS while `in_progress`; complete governing manifest inspected |
| review preflight for `WO-VSP-002` | PASS while `implemented`; complete governing manifest inspected |
| `python -B -m unittest tests.test_revision_provenance tests.test_dashboard_webui -v` | PASS: 36 tests, 1 expected Windows symlink skip |
| `python -B -m unittest discover -s tests -p "test_*.py"` | PASS: 148 tests, 3 expected skips |
| `python -B -m se_harness doctor .` | PASS: required, distributed, managed, and self-hosting integrity checks passed; existing location advisories remained nonblocking |
| real-repository `dashboard` to two separate explicit outputs | PASS twice: 284 artifacts, 1016 relations, 0 errors, 39 derived warnings, identical snapshot `4884831908594e6b974e93ca54d137b376a9e632aea0706a917ee8f0f538dfdd` |
| Metadata field and original-relation preservation | PASS |
| Successor status and work-set coverage | PASS |
| Active-release back-reference inspection | PASS: none |
| `git diff --check` | PASS |

## Explorer and anomaly result

The deterministic snapshot contains the declared `superseded_by` edge from `VREC-DST-007` to `VREC-DST-008`. `VREC-DST-007` is historical and no longer produces a stale-ready `W-REV-004` observation. Derived warnings decreased from 40 before this decision to 39 afterward.

The graph is clean for the dashboard candidate lineage, but the repository is not warning-free: one unrelated `W-REV-004` observation remains for historical `VREC-AGR-001`, and formal validation retains 38 pre-existing legacy-architecture and canonical-location compatibility warnings. This decision intentionally does not alter those records.

## Changed and protected paths

The final governance change is limited to `docs/engineering/harness-distribution/verification-records/VREC-DST-007.md`, `docs/engineering/verification-supersession/work-orders/WO-VSP-002.md`, and this evidence file. `VREC-DST-008`, both candidate payloads, source evidence, work orders, release records, managed policy and templates, implementation source, tests, README, screenshots, package metadata, and versioning remain unchanged.

## Authority boundary

This decision supersedes only `VREC-DST-007` and retains the explicit historical edge. It does not verify or release `WO-VSP-002`, change `WO-DST-007`, supersede another record, prepare or approve a release, merge PR 35, build or publish a package, create or move a tag, mutate a GitHub Release, deploy, force push, or rewrite history.
