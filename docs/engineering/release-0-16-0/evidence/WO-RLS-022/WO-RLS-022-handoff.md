```toml
artifact = "WO-RLS-022"
checkpoint = "handoff"
formal_snapshot_sha256 = "f5b545be6b4d84bec370221eb244f75b4c08447fd1c4ba526e9354e12370bcda"
rebound_at = "2026-09-07T08:25:31Z"
```

# WO-RLS-022 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The one clean 0.16.0 candidate commit is the commit that transitions this
work order to `implemented` on `release/0.16.0` off `main` at `2e46b49`, with
the packaged bytes of `main`. The census from `v0.15.0` is complete with the
four notes-class exemptions the contract names; the released `WO-RLS-021` and
the approved, waiting `WO-TCM-011` are outside the unit by construction; no
trace commit is needed. Qualification readings, the census at the candidate,
the hosted build of record and the hosted lanes are recorded in the sections
below as they complete.

## Evaluators

- Governing: released `se-harness 0.15.0` outside the checkout, `-I`,
  installed at `C:/Users/hok/se-harness-eval-0150` from the wheel file
  whose SHA-256 `eb09343f…` equals the distribution table of
  `RLS-SEH-024`, on this Windows checkout (LF bytes, `core.autocrlf=input`)
  for every reading, the packet and the handoff check included.
- Candidate: this checkout, branch `release/0.16.0` off `main` at
  `2e46b49`, the merge of the approved packet #368; `pyproject.toml` reads
  0.16.0 (moved by `WO-HUP-016`).
- Build host: the hosted GitHub runner running the pinned linux/amd64
  producer image through Docker inside `release-qualification.yml`
  (`candidate` mode), dispatched on this branch.

## Section 1: the candidate

The approvals of `REL-SEH-027` and `WO-RLS-022` rode PR #368 to `main`
before the cut. Every commit on this branch carries the
`Harness-Work-Order: WO-RLS-022` trailer in its final block, so the census
at the candidate needs no exemption beyond the four notes-class merges
between `v0.15.0` and the cut, which the contract names and whose paths
were verified one by one: #348 and #351 under `docs/notes/` and `docs/rca/`,
#357 under `docs/notes/`, #363 the root `GLOSSARY.md` alone.

## Section 2: readings at `3caa77e8`, the start commit

The packaged bytes and `tests/` are identical at every commit of this
branch, including the candidate; the readings below were taken at the start
commit and hold at the candidate.

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | released 0.15.0, outside the checkout, `-I`, wheel-installed | 1,344 artifacts, 0 errors, 71 pre-existing maintenance warnings, 0 advisories |
| `doctor` | released 0.15.0 | 116 PASS, 0 FAIL, 42 `W013` location warnings on historical records |
| `preflight --work-order WO-RLS-022 --phase start` at `2e46b49`, before the start transition | released 0.15.0 | PASS, no diagnostic |
| `preflight --work-order WO-RLS-022 --phase review` | released 0.15.0 | PASS, no diagnostic |
| `check --checkpoint handoff --from-git 2e46b492` | released 0.15.0 | section 2c |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS (12 distribution-bearing records) |
| `scripts/check_portable_release_surface.py --repository .` / `--wheel` / `--harnessctl` | candidate | PASS / PASS / PASS, the latter two on an explicitly non-promotable ephemeral wheel (`3d28d585…`) built outside the checkout with `pip wheel --no-deps` from a Git export of `main` at `2e46b49`, the way the candidate lane builds it, and installed into a disposable environment for the `--harnessctl` reading; the wheel carries the six `se_harness/engine/` files and no `scripts/` data file |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3), LF checkout | section 2b |
| `python scripts/run_tests.py` | candidate, Linux | the hosted candidate-source lane at this head, section 5 |
| `qualify complete-candidate` | candidate, Linux | the hosted candidate-package lane at this head, section 5 (`RID018` boundary on Windows) |
| `repository_tools.upgrade_rehearsal` 0.15.0 -> 0.16.0 | hosted, Linux and Windows | the governance-migration lanes at this head, section 5 |

### Section 2b: the Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` over this branch at
`3caa77e8`, on a detached worktree of this Windows 11 workstation (CPython
3.13.3, LF checkout), whose `tests/` and packaged bytes are identical at
every branch commit including the candidate: 1,265 tests, 26 skipped, 1
error, the known baseline name present on `main` and outside this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a Windows `PermissionError` on a read-only temporary Git object during
teardown), the same reading `WO-RLS-021` and every work order of this cycle
recorded. No other name differs.

### Section 2c: the handoff check

`check --artifact WO-RLS-022 --checkpoint handoff --from-git 2e46b492`,
released 0.15.0, over this packet: Completed; every `QGP-G4I-*` predicate
passes, the evidence predicate reading this packet's header at the formal
snapshot `f5b545be…`; every changed path inside the declared scope;
`complete: true`. The schema-2 result is retained beside this packet as
`handoff.json`.

## Section 3: census re-run at `3caa77e8`

`harnessctl release-unit . --from v0.15.0 --to 3caa77e8 --contract REL-SEH-027`,
released 0.15.0, with the four exempted commits passed as `--exempt`:
untraced 0, exempted 4; eight work orders traced: the five content members,
the released `WO-RLS-021` through the #350 merge (excluded, as the contract
states by construction), the approved `WO-TCM-011` through the #366 merge
(excluded, as the contract states by construction), and `WO-RLS-022`
through this branch's trailered commits. The comparison reports the
`E-CIP-001` findings the contract predicts at this stage: no
`candidate_commit` is declared, the gates differ by exactly `WO-RLS-021`
and `WO-TCM-011`, and the derivation is incomplete because `WO-RLS-022` is
`in_progress`, the state this reading is taken in, and `WO-TCM-011` is
`approved`, the state it keeps until the adoption that follows this release.

## Section 4: build of record

The reading is the `workflow_dispatch` of `publication-rehearsal.yml` on
`release/0.16.0`, whose commit is the branch head (the pull-request event
builds the merge commit, not the head, as `WO-RLS-019`, `WO-RLS-020` and
`WO-RLS-021` recorded).

### Reading at `3caa77e8` (dispatch run 34100421512)

Two producer runs byte-identical, `state` `exact`, the pinned linux/amd64
image `python@sha256:2856e6af…` and the recipe `0c3f368c…` unchanged since
`v0.12.0`. Wheel `se_harness-0.16.0-py3-none-any.whl`
`a0c4f95c12f0eec0417ecc90ea1cffc50923d264c1262c9e9b63c783cea04fdd`; sdist
`se_harness-0.16.0.tar.gz`
`ac327b2b61d099780378d346abbf636e83e90109f8461276f01af915eabd361f`;
`SOURCE_DATE_EPOCH` 1788769330; source manifest `cd3dba47…`. The same run's
`qualification-candidate-3caa77e8…` artifact carries `complete-candidate`
`passed: true`. These are the readings at the start commit, whose packaged
bytes are those of every commit on this branch; the record binds the digests
of the bound candidate, read the same way at that head (section 4b).

## Section 5: hosted lanes

At `3caa77e8`, push event, three runs, all `success`: Engineering Harness
34100226681 (`validate` check-run 101672736892), SE Harness Candidate
Evidence 34100226649, Governor Transition Assessment 34100226619; the
Publication Rehearsal reading at this head is the dispatch of section 4.
The integration-package jobs do not run on a push to a branch other than
`main` by the lane's own condition; they run on the pull-request event of
PR #369 and are recorded at the candidate (section 5b).

Retained by the candidate-evidence run 34100226649:

| Lane | Reading |
| --- | --- |
| candidate source, Linux | `run_tests.py --workers 4 --scale full` pass; portable surface `--repository` PASS; non-promotable candidate wheel `a6bce829…` built from `3caa77e8` |
| `qualify complete-candidate`, Linux | `passed: true`; `CC001` to `CC004` pass |
| `qualify candidate-package` from the isolated released 0.15.0 verifier | `passed: true`; `CP001`, `CP002` pass |
| `repository_tools.upgrade_rehearsal` 0.15.0 -> 0.16.0, Linux, twice | `overall_result` pass both runs; `semantic_sha256` `36f3c724e45dd5b1…` both |
| the same, Windows, twice | `overall_result` pass both runs; the same `semantic_sha256` |

## Section 4b: build re-verified at the bound candidate

`VREC-SEH-025` and `RLS-SEH-025` bind `c103708a`, the implemented-transition
commit, so the replay was dispatched again on `release/0.16.0` at that exact
head (run 34102296258): two producer runs byte-identical, `state` `exact`,
the same pinned image `python@sha256:2856e6af…` and recipe `0c3f368c…`.
Wheel `a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae`;
sdist `25d08fa133e5bf5418b7ade2af995aaf71634422aef775dc55cbdeb32655d581`;
`SOURCE_DATE_EPOCH` 1788770722; source manifest `8153df95…`; checksums
`ba095024…`. The section-4 digests were the reading at `3caa77e8`, whose
packaged bytes are identical; the archives differ only through the
commit-derived `SOURCE_DATE_EPOCH`. The run's `release-build-replay.json`
`manifest`, with `commit` equal to the bound candidate, is retained
byte-for-byte in canonical form as `RLS-SEH-025-bundle.json` when the record
is prepared and is what the record's distribution table carries; the hosted
`release-candidate-replay.yml` dispatch on this branch must reproduce it
from the bound record.

## Section 5b: at the bound candidate `c103708a`

Eight runs, all `success`. Push event: Engineering Harness 34102295234
(`validate` check-run 101679245748), SE Harness Candidate Evidence
34102295244, Governor Transition Assessment 34102295240. Pull-request event
(PR #369, merge commit): Engineering Harness 34102299389 (`validate`
check-run 101679257663), SE Harness Candidate Evidence 34102299306 with the
integration package built, verified on Linux and Windows and retained,
Governor Transition Assessment 34102299313, Publication Rehearsal
34102299604. The dispatch 34102296258 is section 4b. The evidence packet
commit `be80ecbc` before it read the same way: seven runs on both events,
all `success`, the integration package built, verified and retained on the
pull-request event.

Retained by the candidate-evidence run 34102295244:

| Lane | Reading |
| --- | --- |
| `qualify complete-candidate`, Linux | `passed: true`; `CC001` to `CC004` pass |
| `qualify candidate-package` from the isolated released 0.15.0 verifier | `passed: true`; `CP001`, `CP002` pass |
| `repository_tools.upgrade_rehearsal` 0.15.0 -> 0.16.0, Linux, twice | `overall_result` pass both runs; `semantic_sha256` `b850fc50ac35269b…` both |
| the same, Windows, twice | `overall_result` pass both runs; the same `semantic_sha256` |
| candidate source, Linux | `run_tests.py --workers 4 --scale full` pass; non-promotable candidate wheel `eff6f380…` built from `c103708a` |

## Section 6: the record

`VREC-SEH-025` was prepared at `c103708a` by the quality owner from the
released 0.15.0 evaluator over the six gates of `REL-SEH-027`, the five
verification contracts and the six work-order-keyed handoff packets; it is
`ready` in the commit that follows the candidate, with its evaluator
evidence `VREC-SEH-025-evaluator.json` naming the 0.15.0 wheel `eb09343f…`
and payload `11e4ad03…`. The validator's warning count moved from 71 to 72
with it: one `W013` location warning, because the release domain keeps its
records beside their release as every release domain since 0.10.0 has, the
same warning the 0.15.0 records carry. The verification decision is the
assurance owner's.

## Disclosures

1. `harnessctl check --checkpoint handoff` retains `handoff.json` beside
   the packet itself; a shell redirect of its output onto that same path
   makes the retention fail with `WEX-ECP-010` (a Windows rename onto an
   open file). Re-run without the redirect; nothing else changed. Recorded
   so the next release does not repeat it.
2. On the pull-request event the integration-package jobs run and pass;
   `gh pr checks` lists the push-event rows of the same job names as
   "skipping", because the lane's own condition skips them on a push to a
   branch other than `main`. The two readings are not in conflict.
