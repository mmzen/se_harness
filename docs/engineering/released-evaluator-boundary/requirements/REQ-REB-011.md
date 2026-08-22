+++
id = "REQ-REB-011"
type = "requirement"
title = "Permit an active successor for an unreleased rejected version"
status = "approved"
owners = ["requirements-steward", "repository-owner", "release-owner"]
created = "2026-08-22"
updated = "2026-08-22"
statement = "WHEN one or more release attempts for an unpublished version are terminally rejected, THE SYSTEM SHALL retain those records without letting them claim the version against at most one ready or released successor."
verification_method = "automated-release-version-lifecycle-matrix"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T22:17:21Z"
decided_by = "requirements-steward"
+++

# Requirement: Permit an active successor for an unreleased rejected version

## Rationale

`RLS-SEH-009` is an immutable rejected attempt for version `0.6.0`. The current candidate understands its rejected lifecycle and exact rejected bootstrap contract, but the generic version-uniqueness rule still counts it as an active claim. That makes the approved successor `RLS-SEH-010` structurally impossible even though no `v0.6.0` tag or public release exists.

Rejected records are audit history, not active promotion claims. Version uniqueness must continue preventing competing ready or released records while allowing an accountable correction to retain every failed attempt.

## Preconditions and trigger

- Each historical record is validly `rejected`, with complete rejection metadata and lifecycle evidence.
- Any predecessor-bootstrap history still satisfies its exact rejected declaring contract and retains immutable evaluator evidence.
- The version has no released record, immutable release tag, or external publication.
- A distinct approved release contract names the successor record.

## Required response

- Exclude valid rejected release records from the active version-claim cardinality.
- Permit at most one `ready` or `released` release record for a version.
- Preserve all rejected record identities, versions, commits, relations, evidence, and lifecycle facts.
- Apply the same rule in candidate validation and future ordinary `prepare-release` behavior.
- Keep each predecessor-bootstrap record subject to its exact status-matched contract and evidence checks.

## Failure and boundary behavior

Two ready records, a ready and released record, or two released records for one version fail. A malformed rejection, mixed bootstrap RLS/contract status, missing evidence, changed history, existing released record, tag, or publication also fails. Automation never converts a rejection into permission to overwrite or move an immutable external release.

## Constraints

- Do not rename, renumber, delete, repoint, or change `RLS-SEH-009`.
- Do not weaken candidate, commit, work-set, VREC, contract, evaluator, or evidence identity checks.
- The exception is lifecycle-based, not an ID allowlist.
- It applies only before one active record becomes released; publication immutability remains unchanged.

## Acceptance examples

### Example: normal behavior

**Given** rejected `RLS-SEH-009` and a distinct correctly bound ready successor for unpublished `0.6.0`

**When** candidate validation evaluates release-version cardinality

**Then** it validates one active claim while retaining the rejected attempt as history.

### Example: failure behavior

**Given** two ready records for version `0.6.0`

**When** validation or preparation evaluates the version

**Then** it fails before release mutation, tag creation, credentials, or publication.

## Open decisions

No product decision remains open. Helper names and diagnostic wording are delegated; active cardinality and historical preservation are not.
