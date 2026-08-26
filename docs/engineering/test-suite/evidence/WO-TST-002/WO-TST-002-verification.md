# WO-TST-002 implementation evidence

artifact: WO-TST-002
checkpoint: handoff
formal_snapshot_sha256: 96ab4177eda7d00f175abfc1c2867fe5a5ad186984da3d896acbb2c938ca7708

Retained by the implementation actor on 2026-08-26. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout; the canonical serial `python -m unittest
  discover -s tests -p "test_*.py"` on the same tree is the oracle.
- Workstation: Windows 11, CPython 3.14, twelve CPUs.

## What was built

- **`tests/fixture_support.py` (REQ-TST-003, TST-FIX 1).**
  `standard_repository(destination, project_name)`: one real
  `harnessctl init` per project name per test process into a session
  temporary directory (registered with `atexit`; re-initialised if the
  directory has gone), then `shutil.copytree` into the fixture's own
  directory, which must be absent or empty. `initialisations()` exposes the
  order of real inits for the cache test. Byte-identical to a direct
  `init`: 62 files including the lock (`tests/test_fixture_support.py`).
- **Fixtures converted (eleven files).** `test_adr_applicability`,
  `test_architecture_traceability`, `test_artifact_authoring`,
  `test_artifact_authoring_policy`, `test_artifact_renumbering`,
  `test_instruction_architecture` (three sites, including
  `installed_target`), `test_repository_context_retirement`,
  `test_revision_provenance` (two sites), `test_workflow_compliance`,
  `test_workflow_execution`, `test_workflow_documentation_contract`. Each
  replaced an `init`-plus-assert pair with one `standard_repository` call;
  no assertion changed. Fixtures that test `init` itself
  (`test_harnessctl`, `test_mutation_guard`, `test_hash_bound_integrity`'s
  subprocess init, `test_release_build`'s venv init, the `plan_install`
  call sites in `test_standard_repository_lifecycle` and
  `test_legacy_release_evidence`) are unchanged (TST-FIX 2).
- **Tests.** `tests/test_fixture_support.py` (three): copies are
  byte-identical to a direct `init` and two copies cost one `init`; a
  non-empty destination is refused without change; a removed cache
  directory is re-initialised.
- **Documentation.** `docs/notes/ci-pipeline.md`, "After WO-TST-002".

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-TST-002 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 943 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-TST-002 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `96ab4177eda7d00f175abfc1c2867fe5a5ad186984da3d896acbb2c938ca7708` |
| `python -m unittest` over the eleven converted modules and `test_fixture_support` | candidate | OK, 4 skips |
| `python scripts/run_tests.py --workers 8` | candidate | `Ran 968 tests in 55.997s (114 classes, 8 workers)` — `OK (skipped=24)` (was 80 s before the cache) |
| `python scripts/run_tests.py --workers 4 --scale full` | candidate | `Ran 968 tests in 86.234s (114 classes, 4 workers)` — `OK (skipped=24)` (was 114 s) |
| `python -m unittest discover -s tests -p "test_*.py"` (canonical serial) | candidate | `Ran 968 tests in 329.674s` — `OK (skipped=24)`: the same verdict as the runner; was 335 s before the cache |

## Deviations from the specification, recorded for the completion decision

1. **Eleven fixtures converted, not "about twenty-five".** The work order's
   estimate counted `init` call sites; the sites that test `init` itself,
   run it in a subprocess or a venv, or drive `plan_install` directly are
   excluded by `TST-FIX` 2, and the remaining ones are the eleven above.
   They cover the modules that carried most of the fixed cost
   (`test_workflow_execution` alone runs 83 tests on the helper).
2. **A first version of the helper named cache directories by cache size**
   and collided after a re-initialisation; fixed to a monotonic counter
   before commit, caught by the helper's own tests.
3. **The serial saving is 5 s, not the ~100 s `REQ-TST-003`'s rationale
   predicted.** Canonical serial: 335 s before the cache, 330 s after;
   parallel: 80 → 56 s at eight workers, 114 → 86 s at four. The estimate
   came from a profile in which `init`'s durable writes dominated; that
   profile inflated `fsync` (the fsync-neutralised suite had already shown
   only 34 s at stake), and most of a fixture's fixed cost is elsewhere
   (validation and the graph work each test does). The cache is
   byte-identical and cheap, and it removes disk contention between
   workers, which is where its measured benefit lies.

## Complete changed-path set

```
docs/engineering/test-suite/evidence/WO-TST-002/WO-TST-002-verification.md
docs/notes/ci-pipeline.md
tests/fixture_support.py
tests/test_adr_applicability.py
tests/test_architecture_traceability.py
tests/test_artifact_authoring.py
tests/test_artifact_authoring_policy.py
tests/test_artifact_renumbering.py
tests/test_fixture_support.py
tests/test_instruction_architecture.py
tests/test_repository_context_retirement.py
tests/test_revision_provenance.py
tests/test_workflow_compliance.py
tests/test_workflow_documentation_contract.py
tests/test_workflow_execution.py
```

## Deviation acceptances

Recorded on 2026-08-26 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-TST-002` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 - eleven fixtures converted, not about twenty-five | Accept: the estimate counted call sites; the excluded sites test `init` itself. |
| 2 - cache-directory naming collision fixed before commit | Accept: caught by the helper's own tests. |
| 3 - the serial saving is 5 s, not about 100 s | Accept: keep the cache for its parallel benefit; the rationale's estimate was wrong and the evidence says so. |

## Not done

- The completion transition; `VREC-TST-002`. The hosted reading comes from
  the pull request's `candidate-source` suite step.
