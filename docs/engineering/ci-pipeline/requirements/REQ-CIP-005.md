+++
id = "REQ-CIP-005"
type = "requirement"
title = "Run only the qualification leg a record's schema needs and one Pages job"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-26"
updated = "2026-08-26"
statement = "WHEN the publication workflow has resolved a release record, THE SYSTEM SHALL run exactly the qualification leg for that record's distribution schema and deploy the Pages payload through one job definition shared with the standalone dashboard workflow."
verification_method = "automated-workflow-inspection-and-run-observation"
[relations]
derives_from = ["CAP-CIP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T15:17:28Z"
decided_by = "requirements-steward"
+++

# Requirement: Run only the qualification leg a record's schema needs and one Pages job

## Rationale

`publish-pypi.yml`'s `qualify` matrix has a schema-1 leg on Windows and a
schema-2 leg on Linux, every step gated on the resolved schema; one leg
always starts a runner, does a full-history checkout, downloads the plan
and executes nothing. `publish-dashboard-pages.yml` is a hand-maintained
copy of the release's `pages_build` and `pages_deploy` jobs.

## Preconditions and trigger

A `publish-pypi` or `publish-dashboard-pages` dispatch.

## Required response

- The matrix leg is selected from `resolve`'s `distribution_schema`
  output; the other leg does not start.
- The schema-1 leg is removed once no ready record can use schema 1, as
  `docs/notes/developing-se-harness.md` already states; the retained
  released schema-1 records are unaffected because they are never
  re-published.
- The Pages build and deploy become one `workflow_call` job used by both
  `publish-pypi.yml` and `publish-dashboard-pages.yml`.

## Failure and boundary behavior

An unknown schema fails `resolve`, as today.

## Constraints

The `github-pages` environment and the identity proof of the released
evaluator stay in the shared job.

## Acceptance examples

**Given** a schema-2 record dispatched
**When** the run is inspected
**Then** one qualification job ran and no job is recorded as skipped after
checkout.

## Open decisions

None.
