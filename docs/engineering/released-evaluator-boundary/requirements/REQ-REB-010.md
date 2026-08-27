+++
id = "REQ-REB-010"
type = "requirement"
title = "Retain rejected predecessor-bootstrap history without active authority"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-27"
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

## Retirement amendment of 2026-08-27

Retired on 2026-08-27 by `REQ-REB-029` under `WO-REB-029`, on the repository owner's direction, which decided this requirement is superseded. The rejected predecessor-bootstrap tuple is no longer validated. The consumer-installed validator no longer resolves a bootstrap contract for a rejected release record, no longer requires exactly one exact rejected contract behind it, and no longer compares the retained tuple against the current root; the rejected `REL-SEH-008` and `RLS-SEH-009` pair therefore stays on disk as inert data instead of as a checked historical tuple. What this requirement protected against is unaffected: no rejected contract can grant bootstrap authority, because no contract grants bootstrap authority at all, and nothing can reuse a tuple that no rule reads. Everything below is retained unchanged as history and is no longer an obligation.

`REQ-REB-011` is not retired and is not narrowed. Its rule stands in full: a rejected record remains valid but inert and does not claim a version against a second ready or released successor. Only the condition that narrowed one of its checks to records marked `se-harness-predecessor-bootstrap-v1` is removed, because that schema name no longer has a reader, and `VER-REB-013` requires a negative case proving the general rule still holds. The retained evidence bindings of `RLS-SEH-009` and `RLS-SEH-012` still verify from the files they bind.

The declared `superseded` status is not applied. `docs/engineering/WORKFLOW.json` admits no `approved` to `superseded` transition for a definition, and this artifact carries its own `draft` to `approved` event, which `WFL-005` requires to stay append-only. Setting the status therefore either contradicts that event (`E014`, measured on 2026-08-27) or deletes it. The retirement is recorded here instead, the instrument `WO-REB-028` already used for `REQ-REB-012`, `REQ-REB-015`, `SPEC-REB-003`, `SPEC-REB-005` and `SPEC-REB-007`. Whether the status is applied through a new transition or the definition family gains one is a separate owner decision; the retirement itself does not wait on it.

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
