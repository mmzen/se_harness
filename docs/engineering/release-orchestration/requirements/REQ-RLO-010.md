+++
id = "REQ-RLO-010"
type = "requirement"
title = "Bind SE Harness distributions through repository-owned tooling"
status = "approved"
owners = ["release-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN the se_harness repository binds a Python distribution to a ready release record, THE SYSTEM SHALL use repository-owned tooling to validate and atomically retain the exact candidate, version, epoch, filenames, hashes, and canonical checksum identity."
verification_method = "automated-repository-binder-and-schema-test"

[relations]
derives_from = ["CAP-RLO-002"]
+++

# Requirement: Bind SE Harness distributions through repository-owned tooling

## Rationale

Removing package semantics from portable `harnessctl` must not weaken the exact provenance used by this repository's deterministic publication workflow.

## Preconditions and trigger

Generic `harnessctl prepare-release` has produced an uncommitted `ready` RLS for one candidate, and the repository release build has produced a structured bundle manifest for the same version and commit.

## Required response

A repository-owned binder must validate the existing complete `python-wheel-sdist` schema, safe version-derived basenames, candidate timestamp, lowercase hashes, canonical two-line `SHA256SUMS`, and source manifest identity before adding the repository-owned distribution table to the RLS.

## Failure and boundary behavior

Reject absent, partial, duplicate, unsafe, wrong-version, wrong-candidate, wrong-epoch, or hash-inconsistent input. Failure must leave the RLS byte-for-byte unchanged. The binder may operate only on a `ready` record and may not change its lifecycle or core governance fields.

## Constraints

The shared distribution implementation must live outside the packaged `se_harness*` namespace and outside the standard consumer template. It must remain deterministic, bounded, and standard-library-only.

## Acceptance examples

### Example: normal behavior

**Given** a ready RLS and an exact manifest for the same candidate and version

**When** the repository binder runs

**Then** it atomically retains the exact distribution block without changing the RLS status or relations.

### Example: failure behavior

A manifest naming another version or candidate is refused and the original ready RLS remains unchanged.

## Open decisions

None.
