+++
id = "WO-TST-001"
type = "work_order"
title = "The parallel runner and the scale marker"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The runner becomes the command every work order's evidence cites; its verdict must equal the serial run's on the exact commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "scripts/run_tests.py",
  "tests/test_workflow_execution.py",
  "tests/test_run_tests.py",
  "tests/test_standard_repository_lifecycle.py",
  "AGENTS.md",
  ".gitignore",
  ".github/workflows/candidate-evidence.yml",
  "docs/notes/developing-se-harness.md",
  "docs/notes/ci-pipeline.md",
  "docs/engineering/test-suite/evidence/",
]

[relations]
implements = ["REQ-TST-001", "REQ-TST-002"]
specifications = ["SPEC-TST-001"]
architecture = ["ARCH-TST-001", "ADR-TST-001"]
verification = ["VER-TST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T19:18:16Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: you can start WO-TST-001."
+++

# Work Order: The parallel runner and the scale marker

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

`scripts/run_tests.py` per `TST-RUN`; the scale marker per `TST-SCL`; the
`AGENTS.md` Test line and the `candidate-evidence.yml` suite step using
the runner with the marker set; notes with the before/after measurements.

## In scope

`TST-RUN` 1–6, `TST-SCL` 1–2, `TST-DOC` 1–3. Tests for the runner in
`tests/test_run_tests.py` (verdict equality on a small scratch suite, an
injected failure, an import error, timings written).

## Scope amendment, 2026-08-26

Owner decision 2026-08-26, taken interactively during implementation: add
`tests/test_standard_repository_lifecycle.py` to the execution scope. That
test pins the suite step of `candidate-evidence.yml` to the serial
`unittest discover` command, which this work order replaces with the
runner; the assertion moves to the new command. One assertion, no other
change to the file.

## Out of scope

The fixture cache (`WO-TST-002`); the release qualification definition,
which keeps the serial suite; any test assertion; the managed region of
`AGENTS.md`.

## Authorized decision envelope

The default worker count; whether the hosted lane uses four or more workers;
the timings file's location under `target/`.

## Constraints

No third-party dependency. `AGENTS.md`'s owner region stays within its
declared byte bound and required facts. The serial command stays listed
as canonical.

## Expected change surface

One script, one test file, one test edited, `AGENTS.md` owner region,
`.gitignore`, one workflow step, two notes, evidence.

## Required verification

`VER-TST-001` rows 1–2 and scenarios 1–3; repository-required checks; the
full suite serial and parallel on the candidate commit; handoff check.

## Evidence to record

Under `docs/engineering/test-suite/evidence/WO-TST-001/`: both verdicts
and wall times, the hosted step durations before and after.

## Stop and escalate conditions

Stop if the parallel verdict differs from the serial one on the same
commit, or if the `AGENTS.md` owner region would exceed its bound.

## Completion report format

The `harnessctl check . --artifact WO-TST-001 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
