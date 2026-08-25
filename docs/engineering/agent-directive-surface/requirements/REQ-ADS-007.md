+++
id = "REQ-ADS-007"
type = "requirement"
title = "Keep the agent reading surface bounded and free of retired files"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a phase-appropriate preflight runs or a coding agent reads the owner region of this repository, THE SYSTEM SHALL emit a reading manifest closed to the managed router, the operating card, the selected work order with its governing chain, and the owner-region file; the operating card SHALL carry only the stop conditions and the managed trap list; and the owner region SHALL name no retired scaffold file, pointing instead to a repository-owned note for the release sequences."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-ADS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T11:40:02Z"
decided_by = "requirements-steward"
+++

# Requirement: Keep the agent reading surface bounded and free of retired files

## Rationale

`WO-ADS-001` delivered a bounded read only in part. The operating card restates
the state table and restitution headings that `WORKFLOW.md` already explains,
which the router's own routing principle discourages; the preflight manifest
still lists every routed policy because `tests/test_repository_context_retirement.py`
binds its prefix; and `docs/engineering/REPOSITORY_CONTEXT.md` remains in this
repository although the candidate harness withdrew the scaffold under
`WO-DST-021`, because `REQ-IAR-020` rules 3-4 oblige the owner region to name
that path and `SPEC-IAR-012` rule 12 bounds the region to 6,000 bytes, which the
release sequences do not fit.

This requirement finishes the intent of `REQ-ADS-003` and supersedes the
pointer obligation of `REQ-IAR-020`, following the `REQ-DST-065` /
`REQ-DST-008` precedent: the superseding transition is implementation work
under the governing work order.

## Preconditions and trigger

`harnessctl preflight --phase start|review`; rendering of the router and card
by the installer; a read of this repository's `AGENTS.md` owner region.

## Required response

- The reading manifest is the closed set: `ENGINEERING_HARNESS.md`,
  `docs/engineering/OPERATING_CARD.md`, the selected work order, every artifact
  it selects through `implements`, `specifications`, `architecture`, and
  `verification`, and `AGENTS.md`. Routed policies are not listed.
- The operating card carries the stop conditions and the managed trap list and
  nothing else; it stays a managed file bounded to 1,024 bytes.
- The owner region carries the operational entry point of `REQ-IAR-020` rules
  1-2 and 5-12 unchanged, names `docs/notes/developing-se-harness.md#release-sequences`
  as the home of the release-build, release-binding, and last-mile sequences,
  and names no file the harness has withdrawn.
- `docs/engineering/REPOSITORY_CONTEXT.md` is removed from this repository;
  its sequences live in the note; `REQ-IAR-020` becomes `superseded`.

## Failure and boundary behavior

A manifest that lists a routed policy, a card above the bound or carrying a
state table, or an owner region naming the retired path fails the
corresponding conformance test. Historical records that name the path remain
unchanged; the permitted-mentions inventory shrinks to them.

## Constraints

No lifecycle, decision-right, gate, or traceability rule changes. The 6,000-byte
owner-region bound of `SPEC-IAR-012` stays.

## Acceptance examples

### Example: normal behavior

**Given** a standard installation with one approved work order

**When** `preflight --phase start` runs

**Then** the manifest is the closed set above, the card is under 1,024 bytes
and contains `## Stop when` and `## Traps` only, and this repository's owner
region names the note, not the retired file.

### Example: failure behavior

**Given** a card regenerated with a state table

**When** the conformance test runs

**Then** it fails naming the extra section.

## Open decisions

None.
