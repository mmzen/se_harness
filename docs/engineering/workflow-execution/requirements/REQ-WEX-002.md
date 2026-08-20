+++
id = "REQ-WEX-002"
type = "requirement"
title = "Enforce lifecycle mutation preconditions atomically"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN a formal lifecycle mutation or provenance-record preparation is requested, THE SYSTEM SHALL validate the selected artifact type, source state, allowed target state, governing prerequisites, required actor inputs, immutable fields, and permitted mutation set before writing, and fail without partial writes when any condition is unmet."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Enforce lifecycle mutation preconditions atomically

## Rationale

Prose-only transition rules allow agents to apply the same requested transition differently. Validation after a write is insufficient when the operation can leave partial or misleading governance facts.

## Preconditions and trigger

## Required response

## Failure and boundary behavior

## Constraints

## Acceptance examples

### Example: normal behavior

**Given** an approved work order whose implementation is not complete

**When** verification-record capture is requested for that work order

**Then** the request fails, identifies the required implementation state, and writes no verification record or other file.

### Example: failure behavior

## Open decisions

The specification must enumerate the transition table, idempotence policy, and atomic-write boundary before this requirement is approved for implementation.
The operator selects an existing governed object or supplies a valid new record identity, requests one explicit preparation or transition, and supplies every actor input required for that action.
- Calculate one allowed mutation plan from the selected object type and current state.
- Validate every type-specific precondition and protected field before creating, replacing, or updating any file.
- Require verification-record capture to reference only work orders whose implementation is complete.
- Require normal release preparation to reference eligible verified assurance records and their exact covered work.
- Return the proposed or completed mutation set in deterministic form.
- Reject skipped, reversed, repeated, ambiguous, or type-incompatible transitions unless an explicit contract permits idempotence.
- Reject a verification-record capture when any referenced work order has not reached `implemented` or an eligible later provenance-backed work-order state.
- Reject release preparation when selected assurance is merely `ready`, rejected, or superseded.
- On any error, preserve every pre-operation file byte and report the failed precondition.
- Command availability does not imply authority to request the action.
- New lifecycle writes follow the active contract even when historical records remain readable under compatibility rules.
**Given** an implemented work order, complete verification coverage, retained evidence, and every other capture prerequisite

**When** a properly authorized operator requests preparation

**Then** exactly one ready verification record is written and no related formal artifact is mutated.
