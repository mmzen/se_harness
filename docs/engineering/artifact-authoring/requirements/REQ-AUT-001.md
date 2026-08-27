+++
id = "REQ-AUT-001"
type = "requirement"
title = "Distribute one managed authoring policy consumed by the drafting skill and by create-artifact"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN the standard harness installs or upgrades, THE SYSTEM SHALL provide one managed, hash-locked authoring policy at docs/engineering/ARTIFACT_AUTHORING.md, routed from the managed router, listed by preflight, applied by the harness-draft-change skill without restatement, and summarised per artifact type by create-artifact when it creates a draft."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "requirements-steward"
+++

# Requirement: Distribute one managed authoring policy consumed by the drafting skill and by create-artifact

## Rationale

`ADR-TCM-001` placed communication rules in a managed policy rather than in
skills, because a skill governs only the moment it is invoked while a policy
governs every route. Authoring rules have the same shape. A dedicated
"write requirements" skill would duplicate `harness-draft-change` and add
reading surface that `WO-ADS-002` just removed.

## Preconditions and trigger

`init`, `adopt`, `upgrade`; `create-artifact`; explicit invocation of
`harness-draft-change`.

## Required response

- Canonical source `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`,
  installed as `docs/engineering/ARTIFACT_AUTHORING.md` in mode `managed`.
- One routing row in `ENGINEERING_HARNESS.md`: "Authoring rules for formal
  artifacts"; no consumer restates the policy body.
- Listed in preflight's `REQUIRED_PATHS` and `POLICY_PATHS`.
- `harness-draft-change` gains one sentence: apply the authoring policy for
  each selected type; contract version and vectors updated.
- `create-artifact` prints the type's checklist section from the installed
  policy after creating a draft; `--quiet` suppresses it.

## Failure and boundary behavior

A missing or customised policy fails `doctor` like any managed file. A
policy section absent for a type prints nothing.

## Constraints

No new skill, role, right, or gate is introduced by this requirement.

## Acceptance examples

### Example: normal behavior

**Given** a fresh installation

**When** `create-artifact --type requirement` runs

**Then** the draft is written and the requirement checklist is printed.

### Example: failure behavior

**Given** the installed policy is edited by hand

**When** `doctor` runs

**Then** it reports the managed-file mismatch.

## Open decisions

None.
