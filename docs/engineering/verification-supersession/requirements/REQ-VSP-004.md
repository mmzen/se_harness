+++
id = "REQ-VSP-004"
type = "requirement"
title = "Preserve provenance and human authority"
status = "implemented"
owners = ["repository-owner", "quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a ready verification record is superseded, THE SYSTEM SHALL preserve its captured candidate identity and evidence metadata and SHALL require an explicit retained human decision."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-VSP-001"]
+++

# Requirement: Preserve provenance and human authority

## Rationale

Supersession changes governance interpretation, not historical facts about the captured candidate.

## Preconditions and trigger

An accountable owner reviews the old record, the successor, both scopes, and retained evidence.

## Required response

Limit the historical-record edit to status, updated date, `superseded_by`, and a human-decision note. Preserve `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, evidence paths, and original verification relations byte-for-byte. Retain a separate governance work order and evidence.

## Failure and boundary behavior

Block the transition when immutable fields differ, evidence is missing, the decision is not attributable, or automation would be the asserted decision maker.

## Constraints

Implementation may enable and validate supersession but cannot supersede a concrete record. Each transition requires later explicit authority and a separate governance commit.

## Acceptance examples

The eventual `VREC-AGR-001` governance diff changes only permitted lifecycle fields and narrative while retaining candidate `3f3ba521...`.

## Open decisions

None when approved.
