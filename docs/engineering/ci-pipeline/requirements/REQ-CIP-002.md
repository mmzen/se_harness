+++
id = "REQ-CIP-002"
type = "requirement"
title = "Build the candidate wheel once per workflow and hand it to every consumer"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN the candidate-evidence workflow runs, THE SYSTEM SHALL build the candidate wheel in one job and provide it to every consuming job as a downloaded artifact whose digest the consumer verifies."
verification_method = "automated-workflow-inspection-and-run-observation"
[relations]
derives_from = ["CAP-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "requirements-steward"
+++

# Requirement: Build the candidate wheel once per workflow and hand it to every consumer

## Rationale

`candidate-evidence.yml` builds the same commit's wheel in
`candidate-package`, once per platform in `governance-migration`, and twice
inside `build_integration_package.py build` — five builds. Two further jobs,
`governance-migration-reconcile` and `integration-package-retain`, exist only
to compare digests produced elsewhere or to re-upload verified bytes under a
retention name.

## Preconditions and trigger

A `candidate-evidence` run on any event.

## Required response

- `candidate-source` builds the wheel from `git archive` of the commit with
  the pinned build tools and uploads it with its `SHA256SUMS`.
- `candidate-package`, `governance-migration` and the integration-package
  build download it, verify the digest, and do not rebuild.
- The migration rehearsal runs once per platform; each platform job outputs
  its `semantic_sha256`, and the cross-platform comparison is a job output
  check, not a job.
- `integration-package-retain` merges into the verify step: the retention
  upload happens once, from the job that verified.
- Job count: seven to four (`candidate-source`, `candidate-package`,
  `governance-migration` matrix, `integration-package` matrix).

## Failure and boundary behavior

A digest mismatch on download fails the consuming job with the two digests
in the message. A rebuild inside any consumer is a stop condition for
`WO-CIP-001`.

## Constraints

The wheel bytes are inert candidate evidence, not a promotable
distribution; the artifact retention stays at the present values.

## Acceptance examples

**Given** a `candidate-evidence` run
**When** its logs are searched for `pip wheel` and `python -m build`
**Then** exactly one wheel build appears, in `candidate-source`.

**Given** the two platform migration results differ
**When** the output comparison runs
**Then** the workflow fails naming both digests, with no separate job.

## Open decisions

None.
