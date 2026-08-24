+++
id = "REQ-VSP-008"
type = "requirement"
title = "Preserve preparation provenance during verification supersession"
status = "approved"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN a verification record produced by the supported preparation path is explicitly superseded, THE SYSTEM SHALL preserve its preparation provenance and complete the declared transition without fabricating a verification decision."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-VSP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:35:25Z"
decided_by = "repository-owner"
+++

# Requirement: Preserve preparation provenance during verification supersession

## Rationale

`capture-verification` in 0.6.0 correctly records candidate capture with `prepared_at` and `prepared_by`, and omits `verified_at` because no assurance decision has occurred. The validator nevertheless requires `verified_at` after `ready -> superseded`, even though supersession is an alternative to verification. The supported writer, transition command, and validator therefore disagree and can strand a valid ready record.

## Preconditions and trigger

A current-format VREC is `ready`, retains `prepared_at` and `prepared_by`, and has one eligible verified or released successor covering all of its work. An assurance owner explicitly selects that successor through the supported lifecycle command.

## Required response

The transition must add only the supersession decision fields, successor relation, lifecycle event, status, and update date. It must preserve the preparation fields and must not add `verified_at` or `verified_by`. The proposed final graph must validate and the record must leave the active assurance queue.

## Failure and boundary behavior

Reject missing or malformed preparation provenance, fabricated verification fields on a current prepared record, an ineligible successor, incomplete work coverage, a cycle, or an active release reference. Failure must leave repository files unchanged and identify the violated invariant.

## Constraints

- Legacy records without `prepared_at` that use historical `verified_at` as their capture timestamp remain valid without rewriting history.
- Rejection remains a distinct assurance decision and is not a substitute for supersession.
- The change must not supersede, reject, verify, or otherwise mutate any concrete repository VREC.
- Root managed files remain governed by the installed released evaluator and are not upgraded by this work.

## Acceptance examples

### Example: current prepared record

**Given** a ready VREC created by `capture-verification` and a coverage-preserving verified successor

**When** the assurance owner applies `ready -> superseded`

**Then** the command succeeds, retains `prepared_at` and `prepared_by`, adds the supersession decision, and leaves verification decision fields absent.

### Example: legacy capture record

**Given** a historical superseded VREC without `prepared_at` whose `verified_at` field recorded candidate capture under an older schema

**When** the current validator reads the record

**Then** the record remains valid and no migration or reinterpretation is written.

### Example: fabricated verification

**Given** a current prepared VREC that moved directly from ready to superseded

**When** it also claims a `verified_at` or `verified_by` decision

**Then** validation fails because supersession did not verify the candidate.

## Open decisions

None when approved.
