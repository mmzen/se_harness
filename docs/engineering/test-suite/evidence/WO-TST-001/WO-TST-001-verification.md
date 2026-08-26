# WO-TST-001 implementation evidence

artifact: WO-TST-001
checkpoint: handoff
formal_snapshot_sha256: f43a8584d557422f564089558e0d03e553514be3beb2c02712bc7b56c3743323

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout; the serial `python -m unittest discover -s tests
  -p "test_*.py"` is the oracle for the runner's verdict (`VER-TST-001`).
- Workstation: Windows 11, CPython 3.14, twelve CPUs. Hosted: the
  `candidate-source` job of the pull request that carries this change.

## What was built

- **`scripts/run_tests.py` (REQ-TST-001, TST-RUN 1–6).** Standard library
  only. Discovery through a fresh `unittest.TestLoader` (the shared loader
  remembers its first top-level directory) with the repository root put
  first on `sys.path` (a script in `scripts/` otherwise resolves
  `se_harness` to another checkout's editable install); the unit of
  scheduling is the test class, ordered by the previous run's timings
  (`target/test-timings.json`, schema `se-harness-test-timings-v1`, derived
  output under the ignored `target/`), then by test count; one
  `concurrent.futures.ProcessPoolExecutor` worker per class, each running
  `unittest.TextTestRunner` in-process with the repository root as cwd and
  `SE_HARNESS_TEST_SCALE` set from `--scale`; results aggregated into
  `unittest`'s report form with every failure and error traceback; exit 1
  on any failure, error or unexpected success; a class that cannot be
  imported or a worker that dies is an error, never a drop; `--workers 1`
  runs the same classes in this process. Stale cached test modules are
  dropped before each discovery so a scratch suite never shadows another.
- **The scale marker (REQ-TST-002, TST-SCL).** `scale_sizes()` in
  `tests/test_workflow_execution.py`: sizes 100 and 500 always, 1,000 with
  `SE_HARNESS_TEST_SCALE=full`; the 1,000 size is reported skipped through
  `subTest` otherwise. `candidate-evidence.yml`'s suite step is
  `python scripts/run_tests.py --workers 4 --scale full --timings ""`.
- **Documentation (TST-DOC).** `AGENTS.md` owner region: the Test line
  names the runner as the fast route and keeps the serial command as
  canonical (owner region measured under its 6,000-byte bound by
  `tests/test_instruction_architecture.py`); `docs/notes/developing-se-harness.md`
  "Ordinary development checks"; `docs/notes/ci-pipeline.md` "The test
  suite" with the after figures. `.gitignore` already ignores `target/`.
- **Tests.** `tests/test_run_tests.py` (seven): on a scratch suite with a
  failing test, an erroring test, a skipped test and a module that fails to
  import, the serial and the three-worker run report the same pass, fail,
  error and skip sets and the same `unittest`-form summary; timings are
  written and order the next run longest-first; the scale marker reaches
  the workers; a runner crash on a class is reported as an error;
  `--workers 0` is refused; the scale helper's sizes by marker. The
  pinned suite-step assertion in `tests/test_standard_repository_lifecycle.py`
  moves to the new command (scope amendment `ce24b68`).

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-TST-001 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 942 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-TST-001 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | first probe refused `tests/test_standard_repository_lifecycle.py` as out of scope; after the owner's scope amendment (`ce24b68`) and before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `f43a8584d557422f564089558e0d03e553514be3beb2c02712bc7b56c3743323` |
| `python -m unittest tests.test_run_tests tests.test_standard_repository_lifecycle…` | candidate | OK |
| `python scripts/run_tests.py --workers 8` (reduced scale) | candidate | `Ran 965 tests in 79.925s (113 classes, 8 workers)` — `OK (skipped=24)` |
| `python scripts/run_tests.py --workers 4 --scale full` (the hosted lane's form) | candidate | `Ran 965 tests in 113.721s (113 classes, 4 workers)` — `OK (skipped=24)` |
| `python -m unittest discover -s tests -p "test_*.py"` (canonical serial, reduced scale) | candidate | `Ran 965 tests in 334.630s` — `OK (skipped=24)` |
| `python scripts/run_tests.py --workers 1 --timings ""` (the runner's serial form) | candidate | `Ran 965 tests in 331.619s (113 classes, 1 worker)` — `OK (skipped=24)`: the same 965 tests, the same 24 skips, the same verdict as the canonical run on the same tree |
| Hosted | `candidate-evidence.yml`, `candidate-source` suite step | not observed locally; the pull request's step duration is the reading (`VER-TST-001` scenario 3); before the change the step took about 6–7 minutes |

## Measured before and after (workstation)

| Run | Before | After |
| --- | ---: | ---: |
| serial, canonical | 367 s (958 tests) | 335 s (965 tests, the 1,000-artifact size skipped) |
| 4 workers | 125 s (module-level experiment) | 114 s at full scale |
| 8 workers | 122 s (module-level experiment) | 80 s at reduced scale |

## Deviations from the specification, recorded for the completion decision

1. **The release qualification does not set the marker.** `TST-SCL` 2
   names it, but `.github/workflows/release-qualification.yml` is not in
   this work order's scope; its serial suite therefore runs the reduced
   sizes until a later change sets `SE_HARNESS_TEST_SCALE=full` there. The
   hosted candidate lane runs the full size on every pull request.
2. **The runner uses `ProcessPoolExecutor`, not `multiprocessing.Pool`.**
   Same standard library, one reason: pool workers are daemonic and cannot
   spawn children, and the runner's own tests run the runner.
3. **Scope amendment.** `tests/test_standard_repository_lifecycle.py` added
   by the owner's decision during implementation (`ce24b68`).
4. **The count differs from the serial run by design where a module fails
   to import.** `unittest` counts a failed import as one run test; the
   runner reports it the same way, as the equality test asserts.

## Complete changed-path set

```
.github/workflows/candidate-evidence.yml
AGENTS.md
docs/engineering/test-suite/evidence/WO-TST-001/WO-TST-001-verification.md
docs/notes/ci-pipeline.md
docs/notes/developing-se-harness.md
scripts/run_tests.py
tests/test_run_tests.py
tests/test_standard_repository_lifecycle.py
tests/test_workflow_execution.py
```

## Not done

- The hosted reading (needs the pull request); the completion transition;
  `VREC-TST-001`; the fixture cache (`WO-TST-002`).
