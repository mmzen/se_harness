+++
id = "WO-CIP-001"
type = "work_order"
title = "Run once per commit and build once per workflow"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The work changes the trigger policy of every candidate-evidence workflow and the artifact flow of candidate bytes; later assurance decisions read the runs it produces."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  ".github/workflows/candidate-evidence.yml",
  ".github/workflows/predecessor-evaluator-assessment.yml",
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  ".github/scripts/build_integration_package.py",
  "docs/notes/ci-pipeline.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/README.md",
  "docs/engineering/ci-pipeline/evidence/",
  "tests/",
]

[relations]
implements = ["REQ-CIP-001", "REQ-CIP-002"]
specifications = ["SPEC-CIP-001"]
architecture = ["ARCH-CIP-001", "ADR-CIP-001", "ADR-CIP-002"]
verification = ["VER-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "engineering-owner"
+++

# Work Order: Run once per commit and build once per workflow

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification and any release decision are separate accountable acts.

## Objective

P1 and P2: trigger filters and cancelling concurrency on the three
candidate-evidence workflows; one wheel build in `candidate-source` handed
down as a digest-verified artifact; the reconcile-only and retain-only jobs
folded into their producers; `candidate-evidence` at four jobs.

## In scope

`CIP-TRG` 1–3; `CIP-ART` 1–5; `build_integration_package.py build`
accepting a prebuilt wheel instead of building two; the `CIP-DOC` updates:
`ci-pipeline.md` "after" figures, `developing-se-harness.md` "Ordinary
development checks" and "Evaluator and candidate evidence", workflow
header comments.

## Out of scope

The rehearsal lane, the release workflow, the release contract, the
predecessor derivation. The root `engineering-harness.yml`, which follows
at the governor upgrade.

## Authorized decision envelope

Job names, artifact names, retention values unchanged. The engineering
owner may keep a fifth job if the integration verify cannot upload the
retention artifact from the matrix; the evidence says why.

## Constraints

No check removed; the integration-package jobs keep their pull-request-only
condition; the wheel artifact is not promotable and says so in its name.

## Expected change surface

Two repository-owned workflows, one template workflow, one script, notes,
tests that parse the workflows, evidence.

## Required verification

`VER-CIP-001` rows 1–2 and scenarios 1–2; repository-required checks; full
suite on both platforms; handoff check with the complete changed-path set.

## Evidence to record

Under `docs/engineering/ci-pipeline/evidence/WO-CIP-001/`: the runs list
for two pushes, the log search for builds, the job count before and after.

## Stop and escalate conditions

Stop if any consumer must rebuild, if a pull-request-only job stops
passing, or if the template change would require editing the root copy.

## Completion report format

The `harnessctl check . --artifact WO-CIP-001 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
