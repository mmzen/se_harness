+++
id = "REQ-DST-050"
type = "requirement"
title = "Load Explorer views progressively"
status = "approved"
owners = ["product-owner", "technical-owner"]
created = "2026-08-17"
updated = "2026-08-17"
statement = "WHEN a reader enters an Explorer view, THE SYSTEM SHALL request and verify only the coarse view dataset needed for that view while preserving independently usable loading and failure states for other views."
verification_method = "automated-browser-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Load Explorer views progressively

## Rationale

Overview topology and Readiness have different data needs. Loading every route before the first useful render defeats progressive access and couples an unrelated failure to the complete dashboard.

## Preconditions and trigger

The shell has verified the manifest and loaded the repository summary. The reader remains on Overview or selects Overview, Lineage, or Readiness.

## Required response

- Load compact topology data only when Overview or Lineage needs repository relationships.
- Load readiness and provenance detail only when Readiness is entered.
- Deduplicate concurrent requests and cache only resources verified for the current manifest/revision.
- Keep navigation controls and already verified panels usable while another view loads.
- Preserve all canonical relation directions, resolution states, lifecycle values, assurance signals, and authority labels.

## Failure and boundary behavior

A failed view dataset produces a retryable error in that view. It does not invent zero counts, clear verified data in another view, transition an artifact, or mark the formal graph invalid.

## Constraints

- Page routing remains client-side and read-only.
- The accepted 3D graph library remains independently lazy and optional.
- View loading does not change the dashboard's authority boundary.

## Acceptance examples

### Example: Readiness is not opened

**Given** a reader opens Overview and inspects topology,

**When** the reader never enters Readiness,

**Then** the Readiness dataset is not requested.

### Example: topology failure

**Given** summary data is valid but topology data fails integrity verification,

**When** Overview renders,

**Then** repository metrics remain readable and the topology panel reports a retryable integrity failure.

## Open decisions

None when approved.
