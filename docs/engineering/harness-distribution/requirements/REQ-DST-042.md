+++
id = "REQ-DST-042"
type = "requirement"
title = "Present complete artifact identity and metadata"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a reader focuses an artifact in Explorer Lineage, THE SYSTEM SHALL present its exact identity and applicable canonical metadata without substituting presentation terminology for repository facts."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Present complete artifact identity and metadata

## Rationale

The current detail panel shows a title, a combined type/state line, owners, a definition-coverage badge, and the repository path. It omits the artifact ID from the title and omits dates and useful type-specific metadata, making the selected formal record harder to identify and compare with its repository source.

## Preconditions and trigger

This requirement applies whenever a resolved formal artifact is selected from the Lineage board, visit history, relation detail, Readiness, or another Explorer route.

## Required response

- Render the heading as `<exact artifact ID> - <exact artifact title>`.
- Present exact type, lifecycle state, owners, creation date, update date, and repository-relative source path.
- Present applicable type-specific canonical metadata, including requirement verification method and commit/release fields where those fields exist.
- Keep relations in the Relations tab and evidence documents in the Evidence tab rather than duplicating large structures in Overview.
- Use explicit absent or not-applicable wording only when a field is meaningful for that artifact type; omit irrelevant fields.

## Failure and boundary behavior

Missing optional metadata must not prevent the remaining artifact detail from rendering. A missing or malformed required field remains visible as an explicit unavailable value and does not cause the browser to invent a replacement.

## Constraints

- Repository metadata remains authoritative; the panel is read-only presentation.
- Preserve exact IDs, dates, commits, hashes, versions, tags, paths, and lifecycle values.
- Do not expose raw front matter as an unbounded metadata dump or duplicate relation authority.
- Do not infer approval, assurance, coverage, release, or correctness from field presence.

## Acceptance examples

### Example: work-order identity

**Given** `WO-IAR-010` has title `Correct temporal reassessment finding semantics`,

**When** it is focused,

**Then** the heading is `WO-IAR-010 - Correct temporal reassessment finding semantics` and its owners, type, state, dates, and repository path are visible.

### Example: absent optional date

**Given** a forward-compatible artifact lacks an optional update date,

**When** it is focused,

**Then** the panel identifies the date as unavailable without hiding the artifact or manufacturing a date.

## Open decisions

None when approved.
