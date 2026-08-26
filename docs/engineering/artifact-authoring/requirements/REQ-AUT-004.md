+++
id = "REQ-AUT-004"
type = "requirement"
title = "Carry optional priority, source, and measure attributes on a requirement"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a requirement declares priority, source, or measure, THE SYSTEM SHALL validate priority as one of must, should, could, source as a non-empty string or artifact ID, and measure as a non-empty string, and SHALL leave a requirement without them valid."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-AUT-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T18:44:01Z"
decided_by = "requirements-steward"
+++

# Requirement: Carry optional priority, source, and measure attributes on a requirement

## Rationale

29148's attribute set includes priority, source, and a measurable criterion;
reviewers reach for them first and auditors map to them. The harness has
none, so performance and size obligations live in prose and no view can
order requirements by priority.

## Preconditions and trigger

Validation of any `requirement` artifact.

## Required response

- `priority` in `must`, `should`, `could` (structure error otherwise).
- `source`: free text (a stakeholder, a standard clause, an incident) or an
  artifact ID; when it is an artifact ID it must resolve.
- `measure`: free text stating a value and unit, encouraged for quality
  requirements; the policy explains when.
- All three optional; the template shows them filled.

## Failure and boundary behavior

An invalid value is a structure error; absence is not a diagnostic.

## Constraints

No relation is added; `source` naming an artifact is not a traceability
edge.

## Acceptance examples

### Example: normal behavior

**Given** `priority = "must"`, `source = "docs/rca/2026-08-20-0.5.0-release-governance-deadlock.md"`

**When** validated

**Then** no diagnostic.

### Example: failure behavior

**Given** `priority = "high"`

**When** validated

**Then** a structure error names the permitted values.

## Open decisions

None.
