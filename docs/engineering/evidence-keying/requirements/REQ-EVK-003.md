+++
id = "REQ-EVK-003"
type = "requirement"
title = "Preserve provenance, safety, and installation compatibility"
status = "approved"
owners = ["security-owner", "quality-owner", "engineering-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN the expanded evidence-attribution convention is installed or used, THE SYSTEM SHALL preserve existing flat filename behavior, historical evidence and record paths, filesystem safety controls, repository customizations, and the single standard installation."
verification_method = "automated-test-and-security-review"

[relations]
derives_from = ["CAP-EVK-001"]
+++

# Requirement: Preserve provenance, safety, and installation compatibility

## Rationale

The correction exists to avoid renaming commit-bound evidence. It must not introduce a different provenance break, weaken path handling, or use a new installation profile to hide incompatible behavior.

## Preconditions and trigger

The behavior is exercised in source, a packaged installation, or an upgrade of an existing uncustomized standard installation.

## Required response

- Continue recognizing every previously valid flat work-order-prefixed filename.
- Leave historical evidence, VRECs, RLS records, candidate commits, and released facts unchanged.
- Preserve normalized-relative-path, repository-containment, regular-file, symlink/junction, and safe-destination checks.
- Deliver managed script changes through the existing plan-first, customization-preserving upgrade mechanism.
- Retain one standard consumer installation and Python 3.11+ standard-library runtime behavior.

## Failure and boundary behavior

Customized managed content remains blocked for manual review. Unsafe or ambiguous filesystem paths fail before attribution can qualify them. No automatic migration moves repository-owned evidence.

## Constraints

- No new runtime dependency or external service.
- No automatic lifecycle transition, commit, tag, release, publication, or governor promotion.
- No historical evidence-body or record-metadata rewrite.

## Acceptance examples

### Example: flat compatibility

**Given** `evidence/WO-ABC-001-verification.md` is currently recognized,

**When** the correction is installed,

**Then** the path remains keyed to `WO-ABC-001` with no repository rewrite.

### Example: customized upgrade

**Given** a consumer customized a managed validator,

**When** upgrade is planned,

**Then** the customization is reported and no partial overwrite occurs.

## Open decisions

None when approved.
