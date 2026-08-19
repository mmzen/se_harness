+++
id = "REQ-RLO-009"
type = "requirement"
title = "Keep portable release preparation format-neutral"
status = "approved"
owners = ["product-owner", "release-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN any repository prepares a release record through portable SE Harness, THE SYSTEM SHALL bind only format-neutral governance identities and expose no se_harness-package, build-format, checksum-layout, publication-channel, or deployment semantics."
verification_method = "automated-package-template-and-cli-boundary-test"

[relations]
derives_from = ["CAP-RLO-002"]
+++

# Requirement: Keep portable release preparation format-neutral

## Rationale

The optional distribution support introduced for RLO-001 hard-codes the `se_harness` wheel, sdist, and `SHA256SUMS` contract in the packaged CLI, managed validator, and consumer release template. That contradicts the already-approved repository-specific scope.

## Preconditions and trigger

A coding agent or repository owner invokes portable `harnessctl prepare-release`, installs or upgrades the standard harness, or validates a consumer artifact graph.

## Required response

Prepare and validate only the RLS core: release contract, eligible VRECs, exact released-work coverage, version, candidate commit, Git object format, optional tag, accountable owner, and lifecycle state. The packaged CLI, Python modules, managed validator, and standard consumer templates must contain no Python-distribution or SE Harness publication policy.

## Failure and boundary behavior

Reject invalid core governance fields or relations exactly as before. Repository-owned metadata may not create core assurance merely because it is present; portable validation must neither interpret it as package provenance nor require a SE Harness-specific format.

## Constraints

Preserve one standard installation, Python 3.11+ standard-library behavior, managed upgrade safety, and the existing authority boundary of `prepare-release`.

## Acceptance examples

### Example: normal behavior

**Given** a Java, Rust, or Python consumer repository with eligible verified work

**When** its agent runs `harnessctl prepare-release`

**Then** the ready RLS is created without any wheel, sdist, PyPI, Pages, or `SHA256SUMS` concept.

### Example: failure behavior

A candidate with mismatched VREC commits remains rejected even though no distribution-format validation runs.

## Open decisions

None.
