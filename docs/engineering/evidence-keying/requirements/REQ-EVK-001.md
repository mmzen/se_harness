+++
id = "REQ-EVK-001"
type = "requirement"
title = "Recognize exact work-order keys in evidence paths"
status = "approved"
owners = ["product-owner", "quality-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN a normalized retained-evidence path is assessed for a work-order key, THE SYSTEM SHALL recognize the exact case-sensitive work-order ID at the existing filename boundary or in a path component at or below a literal evidence directory."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-EVK-001"]
+++

# Requirement: Recognize exact work-order keys in evidence paths

## Rationale

“Keyed to a work order” describes attribution, not a mandatory flat filesystem layout. Supporting the established filename convention and a directory named for the work order preserves clear attribution without forcing unsafe historical renames.

## Preconditions and trigger

The input is a normalized repository-relative retained-evidence path. Filesystem safety and existence are assessed separately by the applicable command or validator.

## Required response

- Preserve the existing case-sensitive filename prefix convention and its `-`, `.`, or end-of-component boundary.
- When a literal lowercase `evidence` component exists, assess every later component, including the filename, using the same exact boundary.
- Return every unique exact work-order key in deterministic order.
- Treat repeated occurrences of the same key as one association.

## Failure and boundary behavior

Embedded IDs, wrong case, missing boundaries, and identifiers occurring only in ancestors before `evidence` do not create directory-based attribution. An unkeyed path remains unkeyed and receives the existing phase-appropriate failure or finding.

## Constraints

- Do not infer IDs from artifact relations, branch names, commits, or file content.
- Do not alter path normalization, containment, existence, symlink, or regular-file rules.
- Do not require historical files or records to be renamed.

## Acceptance examples

### Example: directory-per-work-order evidence

**Given** `docs/engineering/example/evidence/WO-ABC-001/check.md` is a normalized retained-evidence path,

**When** the path is assessed,

**Then** it is keyed to `WO-ABC-001`.

### Example: misleading ancestor

**Given** `docs/engineering/WO-ABC-001/evidence/check.md` has no keyed filename or descendant component,

**When** the path is assessed,

**Then** it is not keyed to `WO-ABC-001`.

## Open decisions

None when approved.
