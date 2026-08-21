+++
id = "REQ-WEX-003"
type = "requirement"
title = "Keep execution, assurance, and release state independent"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN a verification record or release record changes lifecycle state, THE SYSTEM SHALL mutate only that selected record and its applicable decision metadata, preserve the lifecycle state of related work orders and provenance records, and derive assurance and release projections from the typed records rather than synchronizing related statuses."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Keep execution, assurance, and release state independent

## Rationale

Work-order execution, commit-bound assurance, and release authorization are distinct accountable facts. Implicitly synchronizing them makes identical human decisions produce agent-dependent mutations and obscures which actor authorized each state.

## Preconditions and trigger

## Required response

## Failure and boundary behavior

## Constraints

## Acceptance examples

### Example: normal behavior

**Given** an implemented work order referenced by a ready verification record

**When** the assurance owner explicitly verifies the VREC

**Then** only the VREC gains verified state and decision metadata, while the work order remains `implemented` and its assurance projection becomes verified through VREC coverage.

### Example: failure behavior

## Open decisions

The specification must define derived assurance and release projections without redefining the existing formal lifecycle meanings.
A selected VREC or RLS has passed the applicable transition preconditions and the accountable owner has made the explicit decision represented by the requested target state.
- Apply the requested state and applicable decision metadata only to the selected record.
- Preserve referenced work-order, VREC, RLS, requirement, specification, architecture, ADR, and verification-contract files byte-for-byte.
- Calculate work assurance from eligible direct VREC coverage and release inclusion from eligible RLS coverage.
- Report any separately available related-record transition as a distinct action requiring its own authority and request.
- Do not infer a work-order transition from VREC verification or RLS release.
- Do not infer a VREC transition from RLS preparation or release.
- Reject a mutation plan containing an undeclared related-artifact write.
- This requirement does not remove lifecycle values that remain valid under configured provenance.
- A separately requested, authorized, and legal transition of a related work order is not implicit synchronization.
**Given** a verified VREC included by a ready release record

**When** the release owner explicitly releases the RLS

**Then** the RLS alone changes lifecycle state and neither the VREC nor its work orders are rewritten.
