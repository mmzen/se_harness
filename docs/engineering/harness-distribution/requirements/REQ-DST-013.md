+++
id = "REQ-DST-013"
type = "requirement"
title = "Keep public release and baseline guidance truthful"
status = "implemented"
owners = ["product-owner", "quality-owner", "release-owner", "documentation-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN the public README describes package versions, release provenance, or independent CI assurance, THE SYSTEM SHALL keep version examples synchronized with project metadata and SHALL distinguish current configuration from immutable release history and future promotion decisions."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Keep public release and baseline guidance truthful

## Rationale

Version-specific examples are useful but become misleading when they drift. The current README also names baseline version 0.2.0 in conceptual CI documentation even though baseline promotion is a separately governed configuration choice after each publication.

## Required response

- Keep any exact installation example synchronized with the version declared by the package.
- Link immutable GitHub releases and the production PyPI project without treating either as release authorization.
- Explain that protected OIDC publication promotes already verified GitHub assets without rebuilding them.
- Refer conceptually to the exact configured released CI baseline instead of embedding a baseline version that can drift from the workflow.
- Identify `.github/workflows/engineering-harness.yml` and retained release evidence as the authoritative observations for the current pin and historical proof.

## Failure and boundary behavior

README wording must not advance the actual baseline pin, rewrite historical release facts, claim that candidate tests are independent assurance, or imply that a successful package installation verifies a repository's product artifacts.

## Constraints

Changing the CI workflow pin, version, release records, tags, GitHub releases, PyPI files, attestations, or historical evidence is outside this requirement's documentation implementation.

## Acceptance examples

After a version change, a deterministic test fails until the public exact-version installation example is updated. Baseline wording remains accurate even when the configured pin advances under a later work order.

## Open decisions

None when approved.
