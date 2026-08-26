+++
id = "SPEC-TST-001"
type = "specification"
title = "The parallel runner, the scale marker, and the fixture cache"
status = "approved"
owners = ["technical-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
specifies = ["REQ-TST-001", "REQ-TST-002", "REQ-TST-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "technical-owner"
+++

# Specification: The parallel runner, the scale marker, and the fixture cache

## Scope

Binds `WO-TST-001` and `WO-TST-002`. Rule identifiers `TST-xxx-nnn`.

## Runner (TST-RUN)

1. `scripts/run_tests.py` (repository-owned): `--workers N` (default
   `min(8, os.cpu_count())`), `--timings PATH` (default
   `target/test-timings.json`, derived output), `--pattern`, `--start-dir`,
   `--scale full|reduced` (sets the marker for the workers).
2. Discovery through `unittest.defaultTestLoader.discover`; scheduling
   unit: `TestCase` subclass; order: last recorded timing descending, then
   test count descending.
3. Workers: `multiprocessing` processes each running one class through a
   `unittest.TextTestRunner` in-process, with the repository root as cwd,
   returning a serialisable result (counts, skip reasons, failure and error
   tracebacks as text, elapsed seconds).
4. Aggregation: one report in `unittest`'s form (`Ran N tests in Xs`,
   `OK`/`FAILED (failures=a, errors=b)`, `skipped=c`), every failure and
   error printed with its traceback; exit 1 on any failure or error; a dead
   worker's classes are errors.
5. Timings written to the timings file after every run; the file is
   derived output, ignored by Git.
6. `--workers 1` must equal `python -m unittest discover -s tests -p
   "test_*.py"` in its pass, fail, error and skip sets.

## Marker (TST-SCL)

1. `SE_HARNESS_TEST_SCALE=full` enables the 1,000-artifact size in the two
   scale tests; otherwise that size is reported skipped through `subTest`.
2. `candidate-evidence.yml`'s suite step and the release qualification set
   it; the local default does not.

## Cache (TST-FIX)

1. `tests/fixture_support.py` (or the existing support module):
   `standard_repository(destination)` copies from a session cache created
   by one `init`; a test proves byte equality with a direct `init`.
2. Fixtures that assert on `init` itself are unchanged.

## Documentation (TST-DOC)

1. `AGENTS.md` owner region: the Test line names the runner as the fast
   route and keeps `unittest discover` as canonical.
2. `docs/notes/developing-se-harness.md`, "Ordinary development checks";
   `docs/notes/ci-pipeline.md`, "The test suite" (measurements before and
   after); `.gitignore` for the timings file if not already covered by
   `target/`.

## Failure behaviour

A run whose parallel verdict differs from the serial verdict on the same
commit is a defect of the runner, never of the suite.
