+++
id = "REQ-REB-019"
type = "requirement"
title = "Keep rejected verification and release records as non-authoritative history"
status = "approved"
owners = ["requirements-steward", "quality-owner", "release-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN a verification record or release record is rejected, THE SYSTEM SHALL retain it as immutable visible terminal history with attributed rejection metadata, SHALL grant it no assurance or release authority, SHALL not let it reserve an active release version, and SHALL require remediation to use a distinct record."
verification_method = "automated-rejected-history-and-succession-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "requirements-steward"
+++

# Requirement: Keep rejected verification and release records as non-authoritative history

## Rationale

Rejected records are evidence of a real decision and must not be deleted or rewritten. They are also final failed proposals and must not behave like active candidates. The 0.6.0 release exposed both sides of this rule: the failed `RLS-SEH-009` had to remain visible, while a corrected `RLS-SEH-012` for the same version had to become possible without reopening the rejected record.

Candidate 0.6 already accepts properly formed rejected VREC and RLS records and excludes rejected RLS records from active-version uniqueness. This requirement preserves that behavior and binds it to the authoritative registry so later changes cannot reintroduce the contradiction.

The approved compatibility amendment also preserves existing non-authoritative
`ready` and `superseded` definition/work-order fixtures as visible terminal
input. Those rows do not change the rejected-record rules, reserve a version,
or authorize a new transition.

## Required response

- Admit `rejected` for verification and release records only with canonical `rejected_at`, `rejected_by`, `rejection_reason`, and matching final lifecycle-event metadata.
- Mark rejected VREC and RLS states terminal, visible, non-authoritative, and non-version-reserving in the lifecycle registry.
- Reject any transition out of a rejected record, removal or mutation of its captured identity, or use of it as eligible assurance or release coverage.
- Permit a distinct correctly governed RLS to reuse the same version when every other version-reserving record is absent.
- Continue to reject two or more ready/released records that reserve the same version.
- Keep a predecessor incompatibility factual: use an explicit bounded adapter when authorized, rather than weakening successor semantics or patching the locked predecessor root.

## Boundary behavior

This requirement does not define the production compatibility-view service tracked by issue #104, replace raw release commands tracked by issue #109, upgrade the root evaluator, or rewrite `RLS-SEH-009`, `RLS-SEH-012`, their release contracts, VRECs, candidates, evidence, tags, or distributions.

A rejected record may remain linked and rendered as history. Visibility does not make it authoritative. Passing successor validation does not mean predecessor validation passed, and an adapter-assisted predecessor claim must stay explicitly labeled as a compatibility-view claim.

## Acceptance examples

### Corrected succession

**Given** one rejected RLS for version `1.2.0` with complete rejection metadata

**When** a distinct ready RLS for version `1.2.0` is validated and prepared

**Then** the rejected RLS remains byte-identical history and the new ready RLS is the sole version-reserving proposal.

### Conflicting active proposals

**Given** two ready/released RLS records for the same version

**When** the graph or release-preparation command validates version uniqueness

**Then** it fails both records using the registry's version-reservation semantics.

### Invalid reuse

**Given** a rejected VREC or RLS selected as assurance or release authority

**When** a transition, release preparation, or gate evaluation runs

**Then** it fails without changing the rejected record or any related artifact.
