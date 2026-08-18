+++
id = "REQ-RLO-005"
type = "requirement"
title = "Promote exact GitHub assets through protected PyPI identity"
status = "approved"
owners = ["release-owner", "security-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN the exact final GitHub Release exists and the protected PyPI deployment is approved, THE SYSTEM SHALL publish only its verified wheel and sdist through the configured top-level Trusted Publisher without checkout, rebuild, stored credentials, or duplicate suppression."
verification_method = "automated-policy-preflight-and-authorized-deployment-review"

[relations]
derives_from = ["CAP-RLO-001"]
+++

# Requirement: Promote exact GitHub assets through protected PyPI identity

## Rationale

PyPI files are immutable and its OIDC publisher is bound to a top-level workflow filename. Convenience must not expand the credential boundary or create a second build path.

## Preconditions and trigger

The GitHub Release is final and exact. The `pypi` environment permits `main`, the configured PyPI publisher matches the trusted workflow filename and environment, and an accountable reviewer approves the deployment.

## Required response

Download the three GitHub assets, independently compare both distribution hashes and the exact checksum manifest, copy only wheel and sdist into the publisher directory, and invoke the full-SHA-pinned PyPA action with metadata verification and attestations. On a replay after complete publication, verify both PyPI files and hashes and report completion without invoking a duplicate upload.

## Failure and boundary behavior

Missing approval, publisher drift, partial PyPI state, unexpected filename, metadata failure, attestation failure, or any hash mismatch stops and preserves external state. Never use `skip-existing`, a token fallback, deletion, replacement, or a newly built file.

## Constraints

The OIDC job remains in the PyPI-trusted top-level workflow, checks out no code, runs no candidate program, and has only `contents: read` plus `id-token: write`.

## Acceptance examples

An unpublished exact version is promoted after environment approval. A fully matching version is observed as already complete on replay. One existing file or a wrong hash is a blocking partial publication.

## Open decisions

None.
