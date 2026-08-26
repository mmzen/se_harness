+++
id = "REQ-TST-001"
type = "requirement"
title = "Run test classes across worker processes with one aggregated verdict"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN the suite is run through the repository-owned runner, THE SYSTEM SHALL distribute discovered test classes across the requested number of worker processes, longest known first, and SHALL return one aggregated report whose pass, fail, error and skip sets equal the serial run's on the same commit."
verification_method = "automated-test-and-timed-comparison"
[relations]
derives_from = ["CAP-TST-001"]
+++

# Requirement: Run test classes across worker processes with one aggregated verdict

## Rationale

Measured 2026-08-26: serial 367 seconds; module-level scheduling 125
seconds at four workers and 122 at eight, because `test_workflow_execution`
(84 seconds, 83 tests) is the critical path; class-level scheduling has a
computed floor of about 91, 61 and 47 seconds at four, six and eight
workers. All 52 modules pass in isolation, so the tests are already
parallel-safe.

## Preconditions and trigger

`python scripts/run_tests.py [--workers N] [--timings PATH]` from the
repository root.

## Required response

- Discover with `unittest`'s loader; the unit of scheduling is the test
  class; order classes by the last recorded timing when a timings file is
  present, else by test count.
- One `unittest` process per class batch; standard library only.
- Aggregate results: counts, every failure and error with its traceback,
  skips; exit 1 on any failure or error; print the same one-line summary
  form `unittest` prints.
- Record per-class timings to the timings file for the next run.

## Failure and boundary behavior

A worker that dies is reported as an error for every class it held. A
class that cannot be imported is reported as an error, not dropped.
`--workers 1` is the serial reference and must produce the same verdict.

## Constraints

No third-party dependency. `python -m unittest discover -s tests -p
"test_*.py"` remains valid and canonical.

## Acceptance examples

**Given** the repository at one commit
**When** the runner runs with `--workers 1` and with `--workers 4`
**Then** both report the same pass, fail, error and skip sets, and the
four-worker wall time is under half the serial one on a four-core host.

## Open decisions

None.
