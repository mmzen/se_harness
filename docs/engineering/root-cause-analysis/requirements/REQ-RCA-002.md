+++
id = "REQ-RCA-002"
type = "requirement"
title = "Retain exact recovery evidence and provenance"
status = "draft"
owners = ["product-owner", "quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the RCA states a material release, recovery, integrity, or verification fact, THE REPOSITORY SHALL identify inspectable evidence and SHALL distinguish technical observation from lifecycle authority."
verification_method = "evidence-reconciliation-and-manual-review"

[relations]
derives_from = ["CAP-RCA-001"]
+++

# Requirement: Retain exact recovery evidence and provenance

## Rationale

The incident itself was caused partly by confusing syntactic output and technical evidence with authority. The retrospective must not repeat that mistake, and its key claims must be independently checkable.

## Preconditions and trigger

- The RCA states a candidate, tag, commit, release, workflow result, public package, checksum, attestation, evaluator identity, conversion, or publisher-restoration fact.
- Public or immutable repository evidence exists for the claim.

## Required response

- Cite immutable commit IDs for the alpha candidate, root conversion, final candidate, emergency publisher, and publisher restoration.
- Link the relevant GitHub Actions runs, final GitHub release, and PyPI project release.
- Record the final wheel and source-distribution SHA-256 values.
- State explicitly that passing checks, public installation, and supply-chain observations reduced emergency risk but did not retroactively create normal lifecycle authorization.
- Label material inference as analysis rather than presenting it as an external observation.

## Failure and boundary behavior

- A broken, mutable-only, ambiguous, or contradictory evidence reference blocks the affected claim.
- If a material fact cannot be reconciled, the RCA must state the uncertainty rather than infer success.
- Evidence must not be described as an approval, verification transition, or release decision unless the applicable formal artifact records that decision.

## Constraints

- Prefer immutable commit IDs, immutable tag targets, exact workflow run IDs, and distribution digests.
- Public URLs may supplement but not replace immutable identity where one exists.
- Do not copy secrets, tokens, environment approvals, or excessive log output into the repository.

## Acceptance examples

### Example: normal behavior

**Given** the RCA says the normal publisher was restored

**When** a reviewer follows its evidence

**Then** commit `43c05f4235fbcf21d154ff4350cd6a87549f0bea` and both post-restoration workflow runs demonstrate the claimed technical state.

### Example: failure behavior

**Given** a public package installation passed

**When** the RCA describes that observation as normal release authorization

**Then** the evidence statement violates the requirement and blocks approval.

## Open decisions

None. Reviewers may require additional evidence if an enumerated claim cannot be independently reconciled.
