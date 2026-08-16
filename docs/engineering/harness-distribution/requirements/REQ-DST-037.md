+++
id = "REQ-DST-037"
type = "requirement"
title = "Keep observed Explorer revisions legible"
status = "approved"
owners = ["product-owner", "quality-owner", "security-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN Harness Explorer presents repository provenance in its bounded navigation area, THE SYSTEM SHALL show a legible presentation-only abbreviation of a valid full Git revision while preserving the complete canonical value, its accessibility, and its exclusive use for identity and assurance decisions."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep observed Explorer revisions legible

## Rationale

The Explorer sidebar currently prints the complete observed repository revision in a narrow footer. A SHA-1 or SHA-256 value can cross the navigation boundary and obscure nearby content. A short visible prefix improves legibility, but it must never weaken provenance or imply that a prefix is an authoritative commit identity.

The footer reports an observed snapshot revision. Commit-bound VREC and release authority continue to depend on complete exact revisions in canonical records and data.

## Required response

- In the sidebar, display a valid full 40- or 64-character hexadecimal Git revision as its first 12 characters followed by an ellipsis.
- Label or describe the value as an observed revision rather than an exact commit ID.
- Preserve the complete revision unchanged in canonical snapshot data, the existing Snapshot Information view, and programmatically associated accessible text for the abbreviated display.
- Use the complete value for every comparison, lookup, relation, link, manifest, VREC/RLS record, digest, and provenance decision. The visible prefix is presentation only and does not establish uniqueness or equality.
- Do not abbreviate non-hash values such as `unavailable`; present them safely without inventing provenance.
- Prevent repository, branch, revision, and other untrusted sidebar text from crossing the navigation boundary at supported desktop and narrow widths.
- Preserve the existing non-authoritative snapshot wording and safe text-only rendering.

## Acceptance examples

### SHA-1 snapshot

**Given** the canonical observed revision is a 40-character hexadecimal SHA-1 value

**When** the sidebar renders

**Then** it shows the first 12 characters plus an ellipsis, the full value remains available through Snapshot Information and accessible text, and canonical data is unchanged.

### SHA-256 snapshot

**Given** the canonical observed revision is a 64-character hexadecimal SHA-256 value

**When** the sidebar renders

**Then** the same presentation-only 12-character abbreviation rule applies without changing the underlying value.

### Missing or unusual provenance

**Given** the observed revision is `unavailable` or is not a valid full hexadecimal Git object ID

**When** the sidebar renders

**Then** the value is not abbreviated, is rendered as inert text, and remains contained within the sidebar.

### Prefix collision

**Given** two complete revisions share the same first 12 characters

**When** Explorer processes their snapshots

**Then** no identity or assurance behavior treats them as equal because all such behavior uses the complete canonical revisions.

## Out of scope

This requirement does not change Git object-format support, snapshot generation, provenance capture, canonical data, VREC/RLS commit binding, artifact identity, repository validation, or lifecycle authority.
