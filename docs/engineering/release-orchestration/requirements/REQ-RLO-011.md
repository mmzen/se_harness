+++
id = "REQ-RLO-011"
type = "requirement"
title = "Preserve deterministic one-input publication after decoupling"
status = "approved"
owners = ["release-owner", "security-owner", "quality-owner"]
created = "2026-08-18"
updated = "2026-08-18"
statement = "WHEN a released se_harness RLS drives the publication workflow, THE SYSTEM SHALL validate its repository-owned distribution provenance from trusted main and preserve the existing one-input, deterministic-build, credential-separation, immutable-state, replay, and observation guarantees."
verification_method = "automated-workflow-policy-state-and-failure-test"

[relations]
derives_from = ["CAP-RLO-002"]
+++

# Requirement: Preserve deterministic one-input publication after decoupling

## Rationale

Correcting the product boundary must not regress the last-mile automation or move untrusted candidate code into a publication boundary.

## Preconditions and trigger

One released RLS containing the repository-owned distribution block is committed to trusted `main` and selected through the existing workflow input.

## Required response

Resolve and validate the distribution with trusted repository-owned code, reconstruct the candidate twice without credentials, and retain the current GitHub, PyPI, Pages, public-install, replay, and stage-result behavior. Privileged jobs must consume only independently checked inert identities and bytes.

## Failure and boundary behavior

Missing or malformed repository distribution provenance must block before candidate execution or external mutation. Exact external state remains replay-complete; partial or mismatched immutable state remains blocking and non-destructive.

## Constraints

Keep the top-level `publish-pypi.yml` identity, protected environments, one `release_record` input, main-only resolution, action pins, permission separation, and the prohibition on automatic formal transitions.

## Acceptance examples

### Example: normal behavior

**Given** a released RLS with exact repository-owned distribution provenance

**When** the release owner dispatches the existing workflow with only its ID

**Then** the same deterministic and trust-separated release transaction completes or safely replays.

### Example: failure behavior

A released RLS without the repository distribution block remains valid graph history but is refused as publication input before any credential is available.

## Open decisions

None.
