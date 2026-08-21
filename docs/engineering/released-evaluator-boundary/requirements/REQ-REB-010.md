+++
id = "REQ-REB-010"
type = "requirement"
title = "Retain rejected predecessor-bootstrap history without active authority"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN a predecessor-bootstrap release record and its exact release contract are explicitly rejected, THE SYSTEM SHALL continue validating their immutable historical tuple and evidence without treating the rejected contract as active bootstrap authority or permitting its reuse."
verification_method = "automated-lifecycle-provenance-and-negative-authority-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T17:46:21Z"
decided_by = "requirements-steward"
+++

# Requirement: Retain rejected predecessor-bootstrap history without active authority

## Rationale

The current validator requires every record carrying `preparation_schema = "se-harness-predecessor-bootstrap-v1"` to satisfy an `approved` release contract, regardless of whether the record is `ready` or `rejected`. The authorized disposition of `RLS-SEH-009` and `REL-SEH-008` therefore fails atomically: once the old contract is rejected, the rejected record becomes invalid; if the old contract remains approved, a successor bootstrap contract cannot be approved because cardinality is limited to one.

Rejected history must remain internally verifiable without retaining operational authority. Otherwise a failed one-shot bootstrap permanently blocks any corrected successor.

## Preconditions and trigger

- One exact predecessor-prepared RLS contains a complete canonical evidence binding and satisfies the contract that declared its ID and version.
- The accountable release owner explicitly rejects both the RLS and that release contract with retained reasons.
- A later successor contract may need to become the repository's sole approved bootstrap contract.

## Required response

- Validate a rejected predecessor-bootstrap RLS against its exact rejected contract, immutable tuple, candidate, relations, evidence, and lifecycle facts.
- Exclude rejected contracts from active bootstrap cardinality and all binder, preparation, publication, credential, and release authority.
- Continue requiring an approved exact contract for every `ready` predecessor-bootstrap RLS.
- Reject mixed states, mismatched IDs/versions, changed evidence, more than one approved bootstrap contract, or any attempt to reuse a rejected contract.

## Failure and boundary behavior

A ready RLS with a rejected contract, a rejected RLS with an approved or unrelated contract, changed historical tuple, or use of a rejected contract for binding/publication fails closed. Historical acceptance never transitions, prepares, publishes, or authorizes anything.

## Constraints

- Preserve the original RLS and contract bytes except their separately authorized lifecycle metadata.
- Preserve one-shot terminality and exact active-contract cardinality.
- Do not create a generic historical or schema-2 allowlist.
- Keep the released 0.5.0 root unchanged.

## Acceptance examples

### Example: normal behavior

**Given** `RLS-SEH-009` and `REL-SEH-008` are both explicitly rejected with their original bootstrap tuple unchanged

**When** candidate validation runs after `REL-SEH-009` becomes the sole approved bootstrap contract

**Then** the old rejected pair remains valid history and only the new approved contract can authorize a ready bootstrap record.

### Example: failure behavior

**Given** a rejected contract is selected by a ready RLS or publication resolver

**When** the operation evaluates authority

**Then** it fails before mutation or credentials.

## Decision state

The terminal-history rule is approved for bounded local implementation under `WO-REB-005`. Applying it to `RLS-SEH-009`, `REL-SEH-008`, or any successor contract remains deferred until the C3 validator exists and the accountable lifecycle action is separately authorized.
