```toml
artifact = "WO-DST-022"
checkpoint = "handoff"
formal_snapshot_sha256 = "3ff0291c232c60dcc6ad47557413bb224d54fd573f076fc612ccb9be41bbad50"
rebound_at = "2026-08-29T18:21:41Z"
```

# WO-DST-022 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`plan_install(mode="upgrade")` classifies prior-lock managed and fragment
paths absent from the managed set: `remove` when the tracked bytes match the
recorded digest, `customized` when they differ (`DST-UPR-001`); apply
deletes removed files with directory pruning inside the one
pre-write-snapshot transaction (`DST-UPR-002`, `DST-UPR-003`), keeps the
lock and the replay clean (`DST-UPR-004`), refuses over a customized copy
before any write (`DST-UPR-005`), and records `remove` in the transaction
evidence (`DST-UPR-006`); the 0.10.0-to-0.11.0 fifteen-path pair is pinned
in conformance tests (`DST-UPR-007`); the installation note documents the
rule and the manual remediation (`DST-UPR-008`); `SPEC-DST-001` and
`SPEC-ECP-007` carry the amendment records. Issue #271.

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  Windows for `doctor` (0 FAIL), `preflight`, `transition --apply`,
  `evidence` and the handoff check; the 0.10.0-shipped canonical snapshot
  rule binds this packet natively on the CRLF worktree.
- Candidate: this checkout, branch `wo/dst-022-upgrade-remove` off `main`
  at `d3b5a3f`; the suite and both validators run candidate source.

## Change

- `se_harness/installer.py`: `_plan_leaving_set` classifies leaving-set
  entries after the managed-set loop, upgrade mode only; leaving-set paths
  resolve through `safe_destination` and fail closed; `apply_changes`
  executes removals only when updates are allowed, snapshots them,
  deletes or rewrites (fragment remainder), prunes emptied directories no
  further than the target root, and keeps prior lock entries for removals
  it did not execute; `_upgrade_evidence_bytes` admits `remove` to the
  evidence plan, schema id unchanged.
- Single drop point (analysis, `VER-DST-022`): the written lock's `files`
  is built only in `apply_changes` from the plan's changes; the only branch
  that drops a prior entry without replacing it is the `remove` branch fed
  by `_plan_leaving_set`, and paths never planned (leaving-set seed,
  missing file, blockless fragment) leave the lock through the same
  rebuild. No second lock-rebuild site exists (`grep -n "files\["
  se_harness/installer.py`).
- `docs/notes/harness-installation-and-upgrades.md`: the removal rule and
  the fifteen orphan paths a 0.11.0 root must delete by hand.
- No managed or hash-locked root file moved.

## Tests

`tests/test_standard_repository_lifecycle.py`, six new cases over the
fifteen retired 0.10.0 skill paths written as fixtures: the `remove` plan
and deletion with pruning and no-op replay; the `customized` refusal with
every byte retained; silent retirement of a leaving-set seed entry and a
missing path; fragment-block removal preserving the owner remainder and
deleting a block-only file; `remove` actions in the transaction evidence
under the unchanged schema id; restoration of every deleted file after an
interrupted apply.

## Readings

- `validate_engineering_artifacts.py --root .`: 1157 artifacts, 0 errors,
  484 warnings (advisory `W-AUT-*` maintenance readings on pre-existing
  artifacts; the four new definitions contribute none).
- `validate_release_distributions.py --root .`: PASS, 8 distribution-bearing
  records.
- Suite (Windows workstation, `scripts/run_tests.py`): 1134 tests, 1 error,
  26 skipped; the error is
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  a `PermissionError` deleting a fixture `.git` tree, reproduced identically
  on an unmodified control worktree at `main` `d3b5a3f`, so it is the
  workstation baseline, not this change. `tests/test_standard_repository_lifecycle.py`
  alone: 29 tests, OK. The Linux lane settles the suite hosted.
- In-tree `doctor` exits 1 on candidate-versus-released skew alone, the
  expected boundary evidence.

## Hosted lanes

All thirteen lanes of pull request #276 pass at its head `b871758`. The
owner merged the pull request on 2026-08-29 as `edcef3e`; the push-event
runs on `main` for that commit read Engineering Harness success, Governor
Transition Assessment success and Publication Rehearsal success, with SE
Harness Candidate Evidence still in progress at the time of this
recording and settled readings quoted in the verification decision.
