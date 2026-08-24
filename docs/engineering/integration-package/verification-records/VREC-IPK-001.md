+++
id = "VREC-IPK-001"
type = "verification_record"
title = "Verification candidate for WO-IPK-001"
status = "ready"
owners = ["engineering-owner"]
created = "2026-08-24"
updated = "2026-08-24"
commit = "6d4a727789668395365d885be0c2e829f1aaba2c"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-24T11:58:47Z"
prepared_by = "engineering-owner"
artifact_snapshot_sha256 = "122d096426932e5a0d9ad919596d5369e2c13afdf9caa330da6679c530077b7d"
evidence_paths = ["docs/engineering/integration-package/evidence/WO-IPK-001-verification.md"]
evaluator_evidence_path = "docs/engineering/integration-package/evidence/VREC-IPK-001-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

[relations]
verifies_work_order = ["WO-IPK-001"]
conforms_to = ["VER-IPK-001"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-IPK-001` to candidate commit `6d4a727789668395365d885be0c2e829f1aaba2c`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Commit-bound workflow evidence

- Pull request: [`#132`](https://github.com/mmzen/se_harness/pull/132), branch
  head `cb5cfe048406bb6f4dda08e05b11b44c8269beb0`.
- Exact tested candidate: PR merge commit
  `6d4a727789668395365d885be0c2e829f1aaba2c`, with base parent
  `a57e73e200cf98c67d03c3ef8d50454d56e47740` and branch-head parent
  `cb5cfe048406bb6f4dda08e05b11b44c8269beb0`. The record's `commit`
  field intentionally binds this tested merge commit rather than claiming the
  branch head was the byte-for-byte workflow checkout.
- Candidate workflow: [`SE Harness Candidate Evidence`, run `32724068968`,
  attempt 1](https://github.com/mmzen/se_harness/actions/runs/32724068968),
  `pull_request` event, completed successfully from
  `2026-08-24T11:52:14Z` through `2026-08-24T11:55:35Z`.
- Existing prerequisites passed: candidate source, candidate package,
  Linux/Windows governance migration, and cross-platform migration
  reconciliation.
- [`Build deterministic integration package`](https://github.com/mmzen/se_harness/actions/runs/32724068968/job/97422005855)
  passed and reported a byte-stable wheel from two disposable builds.
- [`Verify integration package (Linux)`](https://github.com/mmzen/se_harness/actions/runs/32724068968/job/97422077703)
  and [`Verify integration package (Windows)`](https://github.com/mmzen/se_harness/actions/runs/32724068968/job/97422077727)
  both passed while installing the same staged wheel and exercising disposable
  repositories. Their reported checkout snapshots were respectively
  `e423779eec07f53450f5ba2b8c2b6d1858fbea0779321cec4448e4941afb5a13`
  and `f7164c8cfee58386772c74f4254643256a78c399603f2c79efe2841ccb67e0ee`;
  platform-specific Git materialization accounts for the different snapshot
  digests, while both jobs reported the same commit, version, and wheel digest.
- [`Retain verified integration package`](https://github.com/mmzen/se_harness/actions/runs/32724068968/job/97422201522)
  passed only after both platform jobs and reverified the final payload
  boundary before upload.

## Retained package evidence

- Integration identity: `0.6.0+pr132.g6d4a72778966`, manifest schema
  `se-harness-integration-package-v1`, and `promotable: false`.
- Wheel: `se_harness-0.6.0+pr132.g6d4a72778966-py3-none-any.whl`, 323391
  bytes, SHA-256
  `f965ef4d8f48c8c31f3d86cb52f928c01a26ff66bf26c757973874155ed6cdfa`.
- Canonical manifest: 1131 bytes, SHA-256
  `26851aa0e2de3a1309f751a04b905d5d8869e4ffe79e4e0c4400eee123ca6fd9`.
- `SHA256SUMS`: 212 bytes, SHA-256
  `84b4bdd225379d9e56e31ae6597bfc54dac1394821da7ff1501c65587770b8dc`.
- One-day staging artifact `9518889658` was named
  `integration-package-staging-6d4a727789668395365d885be0c2e829f1aaba2c`.
  Final three-day artifact `9518909417` was named
  `se-harness-integration-6d4a727789668395365d885be0c2e829f1aaba2c`,
  had GitHub archive digest
  `sha256:41ef159bcc80076fe55bc049cd70b5dccaa87033c8c05b2218b34ba3eb2a4952`,
  and expires at `2026-08-27T11:55:31Z`.
- A separate local download replayed the repository verifier against the final
  three-file payload with the exact commit, repository, PR, ref, run, attempt,
  workflow, and retention expectations; it passed without installation into an
  owner environment.

## Deviation and disposition

The first PR run, `32723593670`, for branch head
`d0cb7e40878166692d53d673b9b753905aeb9953`, passed the deterministic build
and Linux install but failed Windows job `97420732524`. Windows expanded the
runner's `RUNNER~1` temporary-directory alias after virtual-environment
creation, and the candidate correctly rejected the apparently out-of-bound
launcher with mutation guard `MG005`. Final retention was skipped and no VREC
was prepared for that failed candidate. Commit
`cb5cfe048406bb6f4dda08e05b11b44c8269beb0` canonicalized the disposable root
before venv creation and added a regression test; successful run `32724068968`
is the evidence used by this record.

This ready record does not verify itself and does not authorize merge, release,
publication, promotion, evaluator adoption, or installation into a managed
repository. Those remain separate accountable decisions.
