+++
id = "REQ-CIP-002"
type = "requirement"
title = "Build the candidate wheel once per workflow and hand it to every consumer"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-09-10"
statement = "WHEN the candidate-evidence workflow runs, THE SYSTEM SHALL build the candidate wheel in one job and provide it to every consuming job as a downloaded artifact whose digest the consumer verifies."
verification_method = ["inspection"]
verification_notes = "automated-workflow-inspection-and-run-observation"
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
`candidate-package`, once per platform in the upgrade rehearsal, and twice
inside `build_integration_package.py build` — five builds. Two further jobs,
the rehearsal's reconcile job and `integration-package-retain`, exist only
to compare digests produced elsewhere or to re-upload verified bytes under a
retention name.

## Preconditions and trigger

A `candidate-evidence` run on any event.

## Required response

- `candidate-source` builds the wheel from `git archive` of the commit with
  the pinned build tools and uploads it with its `SHA256SUMS`.
- `candidate-package`, `upgrade-rehearsal` and the integration-package
  build download it, verify the digest, and do not rebuild.
- The migration rehearsal runs once per platform; each platform job outputs
  its `semantic_sha256`, and the cross-platform comparison is a job output
  check, not a job.
- `integration-package-retain` merges into the verify step: the retention
  upload happens once, from the job that verified.
- Job count: seven to four (`candidate-source`, `candidate-package`,
  `upgrade-rehearsal` matrix, `integration-package` matrix).

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

## Amendment record

**The rehearsal job is `upgrade-rehearsal` and the reconcile job is gone,
amended 2026-09-10 under `WO-CIP-008` (`REQ-CIP-010`, `SPEC-CIP-004`
`CIP-AMD-002`).** When this requirement was approved on 2026-08-26 the
rehearsal job was `governance-migration` and `governance-migration-reconcile`
existed; the Rationale, the Required response and the job count named them.
`WO-CIP-001` removed the reconcile job (`VREC-CIP-001`). `WO-CIP-007`
(`SPEC-CIP-003` `CIP-ONE-012`, verified by `VREC-CIP-007`) renamed the
rehearsal job, its artifact, its `needs` entries and its outputs on
2026-09-08, with a scope that did not admit this file. The prose above now
uses the current name and describes the reconcile job without its retired
one; the statement, the relations and the lifecycle events are unchanged.
