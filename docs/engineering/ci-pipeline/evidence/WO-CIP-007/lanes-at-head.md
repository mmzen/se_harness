# WO-CIP-007: the lanes at the head

`VER-CIP-003`'s "run observation" row and its first acceptance scenario: the
pull request's own lanes are the observation, read from the runs API rather
than from a green tick.

Pull request #419, base `main` at `560973cf12452d1c91b5a198c6a74d11af383d49`,
implementation head `e96160aff2270a92a5f66f6bb2ba3de9fe1a747b`.

## Runs at the implementation head

| Run id | Workflow | Event | Conclusion |
| --- | --- | --- | --- |
| 34275597729 | SE Harness Candidate Evidence | pull_request | success |
| 34275597949 | Publication Rehearsal | pull_request | success |
| 34275597679 | Predecessor Evaluator Assessment | pull_request | success |
| 34275597700 | Engineering Harness | pull_request | failure, then green at the record head (below) |
| 34275594117 | PR #419 (CodeQL) | dynamic | success |

One run per workflow per commit: the concurrency groups still hold, and the
renamed group `predecessor-evaluator-assessment-${{ github.ref }}` produced
exactly one run.

## The candidate leg no longer qualifies or tests

`Publication Rehearsal` 34275597949, job **Qualify and replay (candidate)**,
read from `GET /actions/runs/34275597949/jobs`:

| Step | Conclusion |
| --- | --- |
| 5. Resolve the subject | success |
| 6. Qualify the exact candidate without publication credentials | **skipped** |
| 7. Replay the exact recipe twice | success |
| 8. Verify the rebuilt bundle against the record | skipped |
| 9. Prove the qualification left no checkout change | success |
| 10. Retain the candidate-controlled qualification result | success |

Step 6 is the step that ran `qualify complete-candidate`, then
`unittest discover`, then the smoke command; `CIP-ONE-001` guards it with
`if: inputs.mode == 'release-record'` and the runner skipped it. The replay
ran, which is the work the leg keeps. The same job in the **release-record**
leg of the same run shows step 6 `success`, so the guard selects by mode and
does not disable the step:

| Leg | Step 6 | Step 7 | Step 8 |
| --- | --- | --- | --- |
| candidate | skipped | success | skipped |
| release-record | success | success | success |

The leg went from 106 s to 28 s (job `started_at` to `completed_at`:
19:09:11 → 19:10:57 at #413's head `02357f7f`, 20:34:37 → 20:35:05 here), and
the whole rehearsal run from 2 m 34 s to 2 m 11 s, bounded by the
release-record leg that this work order does not touch.

## The one lane that qualifies and tests the head commit

`SE Harness Candidate Evidence` 34275597729, job **Candidate source
evidence**: step 6 "Qualify the complete candidate graph as
candidate-controlled" success, step 9 "Run complete candidate-source
regression" success. One of each, and the two checkout and setup-python steps
appear in the log under their digests
(`actions/checkout@11d5960a326750d5838078e36cf38b85af677262`,
`actions/setup-python@a26af69be951a213d495a4c3e4e4022e16d87065`), which is the
pin form observed at run time.

Counting `qualify complete-candidate` in the repository-owned workflows after
the change: two invocations exist, `candidate-evidence.yml` line 71 and
`release-qualification.yml` line 135, and the second is now reached only in
release-record mode. The suite: `candidate-evidence.yml` line 87
(`scripts/run_tests.py`) and `release-qualification.yml` line 139
(`unittest discover`), the second inside the guarded step.

## The renamed jobs ran under their new names

`SE Harness Candidate Evidence` 34275597729, all eight jobs success:

    Candidate source evidence            20:34:34 -> 20:35:21
    Candidate package evidence           20:35:25 -> 20:35:56
    Upgrade rehearsal (Linux)            20:35:59 -> 20:36:39
    Upgrade rehearsal (Windows)          20:35:59 -> 20:40:32
    Build deterministic integration package  20:40:35 -> 20:40:45
    Verify integration package (Linux)   20:40:48 -> 20:41:00
    Verify integration package (Windows) 20:40:49 -> 20:41:27
    Retain verified integration package  20:41:30 -> 20:41:41

`Upgrade rehearsal (<platform>)` is the renamed `Governance migration
(<platform>)`; both legs passed, the cross-platform digest comparison in
`Build deterministic integration package` passed on the renamed outputs, and
`Retain verified integration package` still runs last. `Predecessor Evaluator
Assessment` 34275597679 ran its single renamed job
`Predecessor evaluator assessment` to success. No lane was missing, and the
renamed jobs are not required status checks — the ruleset requires `validate`
only, measured in `retired-names.md`.

The two removed inline re-checks left no gap: `Candidate package evidence`
keeps "Prove candidate wheel has the portable standard surface", the step that
runs `scripts/check_portable_release_surface.py` and the one place those two
refusals are stated.

## The managed lane

`Engineering Harness` 34275597700 failed at the implementation head, in the
step "Enforce the work-order scope on the pull request's diff", with

    blocked: QGP-G4I-EVIDENCE: No readable evidence for WO-CIP-007, checkpoint
    handoff, and formal snapshot d1fad6639e5c22d8869f6707ccc0b50a3246f931ee6e126507c48f8dac8f51f0
    is available.

The scope predicate `QGP-G4I-PATHS` passed — the diff stays inside the
declared scope — and the block is the handoff evidence this packet had not yet
committed. This file, and the handoff `check` result beside it, are that
evidence; the lane is read again at the record head.

## Runs at the packet head f70973335df543cdcabc145ce7f961a0dec5e36f

The commit that adds this packet and the retained `handoff.json`:

| Run id | Workflow | Event | Conclusion |
| --- | --- | --- | --- |
| 34277506456 | SE Harness Candidate Evidence | pull_request | success |
| 34277506885 | Publication Rehearsal | pull_request | success |
| 34277506364 | Predecessor Evaluator Assessment | pull_request | success |
| 34277506498 | Engineering Harness | pull_request | success |
| 34277502856 | PR #419 (CodeQL) | dynamic | success |

Five of five. The required check `validate` is check-run 102234042105,
`success` at this sha; it is the gate the delegated `DR-WO-COMPLETE` reads.

## Runs at the completion commit and the record head

A file cannot carry the reading of the commit that contains it. The lanes at
the completion commit are quoted in the `implemented` event of `WO-CIP-007`
and in the record-preparation event; the lanes at the record head are quoted
in the verification decision of the record prepared for this work order
(`VREC-CIP-007`, the next free identifier: `VREC-CIP-001` to `-006` are
declared across the remote refs).
