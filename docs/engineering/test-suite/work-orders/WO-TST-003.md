+++
id = "WO-TST-003"
type = "work_order"
title = "Run the scale tests at full size in the release qualification"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The release qualification's suite step is what a release executes; the marker decides which assertions it runs."
decided_by = "engineering-owner"
[relations]
implements = ["REQ-TST-002"]
specifications = ["SPEC-TST-001"]
architecture = ["ARCH-TST-001", "ADR-TST-001"]
verification = ["VER-TST-001"]
[execution_scope]
paths = [
  ".github/workflows/release-qualification.yml",
  "tests/test_ci_pipeline.py",
  "docs/notes/developing-se-harness.md",
  "docs/notes/ci-pipeline.md",
  "docs/engineering/test-suite/evidence/",
]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T20:10:10Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: you can start WO-TST-003 (approval and start)."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T20:10:13Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: start."
+++

# Work Order: Run the scale tests at full size in the release qualification

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

The follow-up recorded in `WO-TST-001`'s deviation 1. `TST-SCL` 2 has the
release qualification set `SE_HARNESS_TEST_SCALE=full`; its workflow was
outside `WO-TST-001`'s scope, so its serial suite runs the reduced sizes.
Set the marker on the definition's suite step so a release qualification
runs the 1,000-artifact size.

## In scope

- `.github/workflows/release-qualification.yml`: `SE_HARNESS_TEST_SCALE:
  full` in the job's `env`, and the suite step unchanged otherwise (the
  serial `unittest discover` stays the release's form).
- `tests/test_ci_pipeline.py`: the definition sets the marker.
- Notes: one sentence each in `developing-se-harness.md` ("Ordinary
  development checks") and `ci-pipeline.md`.

## Out of scope

Running the release qualification through the parallel runner; any test
assertion.

## Authorized decision envelope

None needed.

## Constraints

No secret, no permission, no other step changes.

## Expected change surface

One workflow `env` line, one test, two note sentences, evidence.

## Required verification

`VER-TST-001` row 2; repository-required checks; the pull request's
rehearsal (`candidate` mode of the definition) green with the marker set;
handoff check.

## Evidence to record

Under `docs/engineering/test-suite/evidence/WO-TST-003/`: the rehearsal
run identifier showing the 1,000-artifact size ran.

## Stop and escalate conditions

Stop if the rehearsal's suite step fails at the full size.

## Completion report format

The `harnessctl check . --artifact WO-TST-003 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
