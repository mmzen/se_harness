# WO-CIP-007: run-list readings before and after

`VER-CIP-003`, first acceptance scenario and the "run observation" row: read the
run list of the base commit's last pull request and of this pull request's head,
and record both counts of qualifications and suite runs.

## What is counted

Two commands, wherever a job invokes them:

- `python -m se_harness qualify complete-candidate` — `candidate-evidence.yml`
  line 67 (job `candidate-source`) and `release-qualification.yml` line 123
  (job `qualify`, both modes).
- the full suite — `scripts/run_tests.py` in `candidate-evidence.yml` line 83
  and `python -m unittest discover -s tests -p 'test_*.py'` in
  `release-qualification.yml` line 127.

`REQ-CIP-008`'s measure counts the invocations **for the pull request's head
commit**. The rehearsal's `rehearse-record` leg qualifies the commit bound by
the selected release record, not this pull request's commit, and `ADR-CIP-001`
keeps that qualification inside the definition the release executes
(`CIP-ONE-001` exempts release-record mode; `WO-CIP-007` places those steps out
of scope). Both figures are given below.

## Before: pull request #413 at head 02357f7f3a5d614c6c40fd2fe168d3e7180c5128

This work order's branch started from `main` at
`fae52e1b6c570bf1cdba892728029fa38416c947`, the merge of #413. The pipeline
files carry one change between `a68caf70` (the commit the three definitions
were measured on) and `fae52e1b`: the suite-timings cache step added to
`candidate-source` under `WO-TST-004`. No rule of `SPEC-CIP-003` reads it, so
#413's run list is a faithful reading of the state the definitions describe.

`main` then moved three times, to `560973cf12452d1c91b5a198c6a74d11af383d49`
(the merge of #414), and this branch merged it in. The before-reading stands
unchanged, measured:

    git diff --stat fae52e1b 560973cf -- .github/

is empty — no workflow file moved on `main` — as are the same diffs over
`scripts/`, `repository_tools/release_distribution.py` and the five test
modules this work order changes.

#414 is not a comparable reading. It is the top of a three-deep stack, so its
head commit `afebfcbc` carried two `pull_request` runs of every repository-owned
workflow at the same second (candidate evidence 34271428281 and 34271428505,
both success; the rehearsal 34271428832 with 34271428639 cancelled), which
doubles every count for a reason no rule of `SPEC-CIP-003` addresses. The
before-figures below therefore come from #413, an unstacked pull request whose
base was `main`.

Runs at that head, read with `gh run list --commit 02357f7f…`:

| Run id | Workflow | Event | Conclusion |
| --- | --- | --- | --- |
| 34267273745 | SE Harness Candidate Evidence | pull_request | success |
| 34267274299 | Publication Rehearsal | pull_request | success |
| 34267274145 | Governor Transition Assessment | pull_request | success |
| 34267273565 | Engineering Harness | pull_request | success |
| 34267267478 | CodeQL | dynamic | success |

Jobs that ran a counted command, read from
`GET /repos/mmzen/se_harness/actions/runs/{id}/jobs`:

| Run id | Job | Step | Command | Commit qualified or tested |
| --- | --- | --- | --- | --- |
| 34267273745 | Candidate source evidence | Qualify the complete candidate graph as candidate-controlled | `qualify complete-candidate` | 02357f7f (the head) |
| 34267273745 | Candidate source evidence | Run complete candidate-source regression | `scripts/run_tests.py` | 02357f7f (the head) |
| 34267274299 | Rehearse the qualification of this candidate / Qualify and replay (candidate) | Qualify the exact candidate without publication credentials | `qualify complete-candidate`, then `unittest discover` | 02357f7f (the head) |
| 34267274299 | Rehearse the qualification of the release record / Qualify and replay (release-record) | Qualify the exact candidate without publication credentials | `qualify complete-candidate`, then `unittest discover` | the commit bound by the selected record |

Before, per pull request:

- qualifications of the head commit: **2**; suite runs of the head commit: **2**.
- qualifications in total: 3; suite runs in total: 3.

The candidate leg also replayed the recipe ("Replay the exact recipe twice"),
which no other lane performs; that is the work the leg keeps.

## After: pull request #419 at head e96160aff2270a92a5f66f6bb2ba3de9fe1a747b

Runs and jobs read the same way; the full reading, with the step conclusions
and the job timings, is in `lanes-at-head.md`.

| Run id | Job | Step | Command | Commit qualified or tested |
| --- | --- | --- | --- | --- |
| 34275597729 | Candidate source evidence | Qualify the complete candidate graph as candidate-controlled | `qualify complete-candidate` | e96160af (the head) |
| 34275597729 | Candidate source evidence | Run complete candidate-source regression | `scripts/run_tests.py` | e96160af (the head) |
| 34275597949 | Qualify and replay (candidate) | Qualify the exact candidate without publication credentials | — | **step skipped**: `if: inputs.mode == 'release-record'` |
| 34275597949 | Qualify and replay (release-record) | Qualify the exact candidate without publication credentials | `qualify complete-candidate`, then `unittest discover` | the commit bound by the selected record |

After, per pull request:

- qualifications of the head commit: **1** (was 2); suite runs of the head
  commit: **1** (was 2).
- qualifications in total: 2 (was 3); suite runs in total: 2 (was 3).

`REQ-CIP-008`'s measure is met: the head commit is qualified once and tested
once. The remaining pair belongs to the release-record leg, which qualifies
the commit a release record binds and which `ADR-CIP-001` keeps inside the
definition the release executes. The candidate leg still replays the bound
recipe twice, and it finished in 28 s instead of 106 s.

The line numbers of the counted commands after the change:
`candidate-evidence.yml` 71 (`qualify complete-candidate`) and 87
(`scripts/run_tests.py`); `release-qualification.yml` 135 and 139, both inside
the step guarded at line 127. Nothing else in the repository-owned workflows
invokes either command — `candidate-evidence.yml` 200 is
`qualify candidate-package`, `predecessor-evaluator-assessment.yml` 146 is
`qualify released-root` and `publish-pypi.yml` 445 is `qualify public-install`,
three different roles that `REQ-CIP-008`'s measure does not count.
