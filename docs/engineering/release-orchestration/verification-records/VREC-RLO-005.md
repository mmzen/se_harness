+++
id = "VREC-RLO-005"
type = "verification_record"
title = "Verification candidate for WO-RLO-005"
status = "ready"
owners = ["quality-owner"]
created = "2026-08-25"
updated = "2026-08-25"
commit = "cb0bce500bac128664add986300aaa41d053bd3e"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-08-25T06:27:58Z"
prepared_by = "quality-owner"
artifact_snapshot_sha256 = "a8d84aecf65f77788583aab9500c774c0cb492902be384d66b905be5dde178fa"
evidence_paths = ["docs/engineering/release-orchestration/evidence/WO-RLO-005-verification.md"]
evaluator_evidence_path = "docs/engineering/release-orchestration/evidence/VREC-RLO-005-evaluator.json"
evaluator_evidence_sha256 = "fcfc14471cc373fce07ece222f6c03b2152dad2cf4cd5ae6e04cf147c4171962"

[relations]
verifies_work_order = ["WO-RLO-005"]
conforms_to = ["VER-RLO-005"]
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RLO-005` to candidate commit `cb0bce500bac128664add986300aaa41d053bd3e`. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

The repository owner authorized preparation on 2026-08-25 with the statement `you can set
WO-RLO-005 and WO-HBI-004 as implemented, and prepare the verification record(s)`.
`WO-RLO-005` was already `implemented`, so no lifecycle transition was needed and none was
made. Every field above was produced by the released `0.6.0` evaluator's
`capture-verification` run from outside the checkout, at commit
`cb0bce500bac128664add986300aaa41d053bd3e` with a clean worktree.

## What the candidate evidence covers

`WO-RLO-005` adds a repository-owned, credential-free rehearsal of the publication
mechanics that runs on both hosted runner types, and a fail-closed check that the rehearsal
has not drifted from the publication orchestrator. `.github/workflows/publish-pypi.yml` is
not modified by the packet: it is blob `902bb1978181b74918ad57370f77317e15c7bde3` at the
candidate, and the digest pinned in `tests/test_publication_rehearsal.py` is
`2d3c3b775946d7667d9a175b0bb85446ff90db029d021e155a9b12105ff1f51e` over 38213 bytes.

The lane exists because release qualification failed on `windows-2022` in a way no required
gate caught. It has now measured three distinct conditions of that kind at integration time,
and the two that survived to this candidate's predecessor were fixed under `WO-HBI-003` and
`WO-HBI-004`, on their own branches and under their own authorization, rather than absorbed
here.

Measured for this candidate:

- Local, in a `core.autocrlf=true` checkout at `7918a1b`, which the later commits change by
  prose only: full suite 932 tests, OK, 22 skipped, against 811 tests OK in a control at
  plain `main`; `check-divergence` `EXACT` at exit 0; governing validator PASS at 830
  artifacts, 0 errors and 50 maintenance warnings, matched by the candidate validator;
  governing `preflight --phase review` PASS; governing `doctor` exit 0 over 87 checks with 0
  `FAIL`; `validate_release_distributions.py` PASS.
- Hosted, on both runner types, twice: runs
  [32775622117](https://github.com/mmzen/se_harness/actions/runs/32775622117) and
  [32776424455](https://github.com/mmzen/se_harness/actions/runs/32776424455). In each, the
  divergence job reports `EXACT` and both the `ubuntu-latest` and the `windows-2022` leg
  report `REHEARSED` with 21 mechanics executed, 2 excluded, a candidate unit suite that
  passed at 932 tests, byte-identical distribution sets, and a real teardown.

## Assurance-relevant limits of the candidate

The bound evidence file states twelve disclosures. The ones that bear directly on an
assurance decision:

- The rehearsal is derived evidence. It takes no lifecycle transition and grants no
  permission.
- Five orchestrator jobs are excluded by construction and are never rehearsed:
  `github_release`, `observe`, `pages_build`, `pages_deploy` and `pypi`. The
  credential-bearing publication path is therefore unrehearsed by design.
- Two mechanics are excluded on every platform in every run — the predecessor-view
  qualification and the recipe-bound build replay — so neither is proven by this candidate.
  `RLS-SEH-012` declares distribution schema 1.
- The divergence check reads one orchestrator. `.github/workflows/release-candidate-replay.yml`
  is outside it.
- No Linux figure is local, and no local figure comes from CPython 3.11; the hosted legs
  report 10 skips where this workstation reports 22.
- The in-tree `doctor` reports 28 `FAIL` with a `FAIL` set identical to the control's at
  plain `main`, so that skew is inherited boundary state; the governing run has none.
- The detailed hosted figures in the bound evidence come from the run at head `ec3fbf1`,
  one commit behind this candidate; the tip's own run is recorded beside it rather than
  presented as the same run.

Verifying this record would accept the evidence as recorded, including every disclosure in
it. It would authorize no merge, tag, release, publication or deployment, and it would not
change `WO-RLO-005`.
