+++
id = "REQ-RLO-001"
type = "requirement"
title = "Resolve one released record as the sole release identity"
status = "approved"
owners = ["release-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN last-mile publication is dispatched from main, THE SYSTEM SHALL accept one released RLS identifier and derive every version, tag, candidate, verification, distribution, and governance identity without duplicate operator-supplied release parameters."
verification_method = "automated-resolution-and-failure-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Resolve one released record as the sole release identity

## Rationale

Re-entering a tag, commit, version, hashes, and governance commit at different stages can create a valid-looking transaction assembled from inconsistent facts. The released RLS must be the single governed selector.

## Preconditions and trigger

An accountable operator manually dispatches the repository-specific workflow from `main` with one syntactically valid `RLS-*` ID. The record must already be `released` in the trusted main history.

## Required response

Resolve exactly one record and derive its version, tag, candidate commit, object format, included VREC set, release contract, released work, structured distribution identity, and the immutable main-history governance commit that first contains the released record. Confirm the VREC and tag candidate identities agree.

## Failure and boundary behavior

Fail before candidate checkout, build, tag creation, asset upload, OIDC, or Pages permissions when the workflow is not running from `main`, the ID is absent or ambiguous, the record is not released, its governance commit is not in main history, or any declared identity disagrees. Do not infer the newest record or accept corrective override inputs.

## Constraints

Workflow dispatch is operational initiation, not a lifecycle transition. A coding agent may submit the dispatch after explicit human authorization but may not manufacture that authorization.

## Acceptance examples

**Given** released `RLS-SEH-008` in `main`, **when** the operator dispatches with only that ID, **then** all downstream identities come from the resolved record. **Given** a ready RLS or a released RLS found only on another branch, **then** resolution stops without external mutation.

## Open decisions

None.
