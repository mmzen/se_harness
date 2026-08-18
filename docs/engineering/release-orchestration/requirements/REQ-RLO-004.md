+++
id = "REQ-RLO-004"
type = "requirement"
title = "Materialize an immutable GitHub release"
status = "approved"
owners = ["release-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN exact candidate qualification succeeds, THE SYSTEM SHALL create or verify the declared immutable tag and publish one final GitHub Release containing exactly the verified wheel, normalized sdist, and checksum manifest."
verification_method = "automated-github-state-and-fixture-test"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Materialize an immutable GitHub release

## Rationale

GitHub Release is the retained promotion boundary consumed by PyPI and users. A moved tag, partial asset set, generated-latest selection, or upload-before-verification would sever provenance.

## Preconditions and trigger

The credential-free job has produced a hash-matching bundle and trusted resolution has confirmed the RLS is released on `main`.

## Required response

Create a deterministic annotated tag on the exact candidate if absent, or verify the peeled target if present. Stage a draft GitHub Release, upload exactly the three declared assets, verify names, counts, sizes, and digests through GitHub metadata and downloaded bytes, then publish the final non-prerelease release with deterministic lineage notes.

## Failure and boundary behavior

An existing mismatched tag, release, asset, or unexpected fourth asset is blocking. A matching existing tag or final release may be verified as completed. Do not move tags, replace final assets, infer a target branch, or delete mismatched public state automatically.

## Constraints

Only this job receives job-scoped GitHub release write permission. It executes trusted main-owned orchestration code and treats the transferred bundle as untrusted until every digest matches.

## Acceptance examples

An absent tag and release are created exactly once. A replay verifies the existing exact state. A tag pointing to another commit or a release containing a different wheel fails without mutation.

## Open decisions

None.
