# WO-REB-026 implementation evidence

artifact: WO-REB-026
checkpoint: handoff
formal_snapshot_sha256: 1d5a033c9d80e8cc6a37f7feeb984ad7db80c98b26634827606cc0d504e58d4e

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, branch `fix/reb-026-pages-view-for-ordinary-records`
  off `main` at `28487f0112b2f67c5f5471f1028840ec30cca6e5`, the merge of pull
  request #186.

## What was built

Five lines in the exclusion branch of *Validate with the released evaluator*
in `.github/workflows/pages-publication.yml`, after the excluded observation
is written: read the governance commit from `$RUNNER_TEMP/governance`, add a
detached worktree of that commit from the trusted `main` checkout at
`$RUNNER_TEMP/predecessor-view/governance`, assert the worktree's `HEAD`
equals the commit and that it is clean, and say so. For an ordinary record
the view is the complete governance snapshot — nothing is omitted — so
*Generate the target-local canonical Explorer* and every later step run
unchanged. The `declared` branch is untouched.

## Why

The last mile for `RLS-SEH-015` (run `33020380987`) succeeded through the
resolve job, the release-record qualification, the `v0.7.0` tag and GitHub
Release, and the PyPI promotion, then failed in the Pages build's
generation step (job `98349453978`): the step reads the view directory that
only `qualify predecessor-view --view-output` creates, and `WO-REB-025`'s
exclusion branch does not create it.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-REB-026 --phase start` | released 0.6.0 | `PASS` (recorded in the start transition) |
| `harnessctl preflight . --work-order WO-REB-026 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 960 artifacts, 0 errors, 53 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean; the workflow carries zero CR bytes |
| PyYAML `safe_load` | workstation | parses; jobs `build, deploy`; `predecessor-view-qualification.json` once and `mkdir "$RUNNER_TEMP/predecessor-view"` once, unchanged |
| The patched `run` block extracted from the YAML and executed with `bash` against a detached worktree of governance commit `088b08b` (the `qualify` invocation stubbed), then the unchanged generation step run against the result | workstation | exclusion branch taken for `RLS-SEH-015`; view worktree at `088b08befbce5874289fd5877510000048f24226`, clean; source worktree unchanged (0 dirty); `Harness Explorer generation: PASS — 957 artifacts, 3689 relations, 0 errors, 67 warnings`, manifest `c32e93cb…` |
| `python -m unittest tests.test_ci_pipeline tests.test_release_orchestration tests.test_dashboard_publication` | candidate | OK |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | `Ran 995 tests in 94.551s (117 classes, 8 workers)` — `OK (skipped=24)` |
| `harnessctl check . --artifact WO-REB-026 --checkpoint handoff --changed-path … --changes-complete --json` | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; formal snapshot above |
| Hosted | the pull request's lanes | pending the pull request; the decisive reading is the dispatch of `publish-dashboard-pages.yml` for `RLS-SEH-015` after merge |

## Deviations from the specification, recorded for the completion decision

1. **No new test**, for the reason `WO-REB-024` and `WO-REB-025` recorded.
   The proof is the local execution of the extracted branch through the
   unchanged generation step.

## Complete changed-path set

```
.github/workflows/pages-publication.yml
docs/engineering/released-evaluator-boundary/README.md
docs/engineering/released-evaluator-boundary/evidence/WO-REB-026-verification.md
docs/engineering/released-evaluator-boundary/work-orders/WO-REB-026.md
```

## Not done

- The hosted reading (needs the pull request); the completion transition;
  the verification record; the Pages dispatch.
