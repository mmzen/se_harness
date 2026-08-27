# WO-TST-003 implementation evidence

artifact: WO-TST-003
checkpoint: handoff
formal_snapshot_sha256: 524392ca95b413eb4d03be3bf05c7e516200ae127a7cbae8ef19e062d640129a

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout. Hosted: the publication rehearsal of the pull
  request that carries this change runs the definition in `candidate` mode
  with the marker set.

## What was built

- `.github/workflows/release-qualification.yml`: `SE_HARNESS_TEST_SCALE:
  full` in the `qualify` job's `env` (`REQ-TST-002`, `TST-SCL` 2). The
  suite step stays the canonical serial `python -m unittest discover -s
  tests -p 'test_*.py'`; no other line changes.
- `tests/test_ci_pipeline.py`: the definition sets the marker and keeps the
  serial command.
- Notes: `docs/notes/developing-se-harness.md` ("Ordinary development
  checks": who sets the marker), `docs/notes/ci-pipeline.md` ("After
  WO-TST-003").

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-TST-003 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 945 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| PyYAML parse of `release-qualification.yml` | workstation | `jobs.qualify.env.SE_HARNESS_TEST_SCALE == "full"` |
| `harnessctl check . --artifact WO-TST-003 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `524392ca95b413eb4d03be3bf05c7e516200ae127a7cbae8ef19e062d640129a` |
| `python -m unittest tests.test_ci_pipeline` | candidate | OK |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate | `Ran 969 tests in 62.351s (114 classes, 8 workers)` — `OK (skipped=24)`; the 1,000-artifact size ran |
| Hosted | `publication-rehearsal.yml`, `Qualify and replay (candidate)` on the pull request | not observed locally; the run's suite step reports `Ran 9xx tests` with the 1,000-artifact size executed (no scale skip in its output) |

## Deviations from the specification, recorded for the completion decision

None.

## Complete changed-path set

```
.github/workflows/release-qualification.yml
docs/engineering/test-suite/evidence/WO-TST-003/WO-TST-003-verification.md
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
tests/test_ci_pipeline.py
```

## Not done

- The hosted reading (needs the pull request); the completion transition;
  `VREC-TST-003`.
