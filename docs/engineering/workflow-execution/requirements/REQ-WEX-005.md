+++
id = "REQ-WEX-005"
type = "requirement"
title = "Emit a canonical workflow handoff"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN selected workflow state is inspected or a permitted lifecycle action completes or fails, THE SYSTEM SHALL emit stable machine-readable and human-readable handoffs containing the completed action, current lifecycle state, scoped blockers, exactly one recommended next authorized step, required authority, exact command or suggested response, and only currently valid bounded alternatives."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Emit a canonical workflow handoff

## Rationale

The managed conversational fields establish useful handoff content, but provider-specific interpretation still changes structure, verbosity, and next-action selection. One canonical result lets each agent render the same lifecycle meaning without making its prose authoritative.

## Preconditions and trigger

## Required response

## Failure and boundary behavior

## Constraints

## Acceptance examples

### Example: normal behavior

**Given** a newly drafted definition packet with no accountable approval

**When** its selected state is inspected

**Then** the handoff recommends review and approval or revision as the single next step, identifies the accountable owners, and supplies a concrete suggested response.

### Example: failure behavior

## Open decisions

The specification must define the versioned schema, stable ordering, rendering contract, and reconciliation with `REQ-IAR-019` and `SPEC-IAR-011` before this requirement is approved for implementation.
The operator selects one workflow scope, or a selected-scope lifecycle operation reaches either a successful completion or a failure without partial writes.
- Emit the existing managed lifecycle handoff concepts as one versioned semantic result.
- Recommend exactly one bounded next step selected from actions legal in the final reported state.
- Identify the human role or separate authorization required before that step.
- Supply an exact non-destructive command when a command is currently applicable; otherwise supply a precise suggested human response.
- Emit alternatives only when multiple paths are legal and authorized at the same state, without weakening the primary recommendation.
- Keep human-readable and machine-readable forms semantically equivalent.
- On failure, report only completed effects, the unchanged or final formal state, the failed condition, and one safe remediation or escalation step.
- Do not recommend implementation, verification, release, or an external action when its prerequisites or authority are absent.
- Do not replace a bounded next step with a generic request for instructions.
- The handoff is derived evidence and cannot approve or execute its recommendation.
- Stable structure does not require identical natural-language decoration outside the canonical fields.
- This requirement operationalizes the existing conversational handoff obligation; downstream specifications must reconcile any earlier interface constraint that excluded CLI or machine-readable output.
**Given** a requested transition that fails a precondition

**When** the operation returns

**Then** both output forms report no partial lifecycle change and recommend one exact remediation or escalation action rather than advancing to the later lifecycle stage.
