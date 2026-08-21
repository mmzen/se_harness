+++
id = "REQ-REB-003"
type = "requirement"
title = "Bind released-evaluator identity into release readiness"
status = "approved"
owners = ["requirements-steward", "quality-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN release readiness is prepared, THE SYSTEM SHALL retain one canonical evaluator identity observation containing the exact version, distribution digest, bounded runtime origins, and checkout-exclusion proof and SHALL bind that observation to the ready release record."
verification_method = "automated-schema-provenance-and-boundary-test"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Bind released-evaluator identity into release readiness

## Rationale

The incident demonstrated that artifact syntax and configured version are not sufficient authority evidence. Accountable assurance and release owners need one durable observation identifying the actual runtime used for readiness checks.

## Preconditions and trigger

An authorized actor prepares a ready release record from eligible verified work and an exact clean candidate commit.

## Required response

- Produce deterministic identity evidence for the selected released evaluator.
- Include version, wheel filename and SHA-256, module origin, distribution origin, template origin, Python executable origin, entry-point origin, isolation state, and checkout-boundary result.
- Normalize host-specific prefixes while preserving machine-assessable relative origin and boundary facts.
- Bind the evidence path and SHA-256 in the ready release record or its formally validated provenance block.
- Revalidate the binding before authorized publication.

## Failure and boundary behavior

Missing fields, absolute host-data leakage, digest mismatch, failed runtime identity, candidate role, changed evidence bytes, or a record that does not bind the evidence fails preparation or validation. Evidence does not itself verify or release the candidate.

## Constraints

- The evidence must not contain credentials, environment dumps, or unrelated filesystem paths.
- A caller-supplied digest that was not independently checked against acquired bytes is not sufficient.
- Historical release records remain immutable and are not retrofitted.

## Acceptance examples

### Example: normal behavior

**Given** a clean candidate, eligible VREC coverage, and an externally installed released evaluator

**When** `prepare-release` produces a ready RLS

**Then** the RLS binds canonical identity evidence whose digest and normalized origins validate.

### Example: failure behavior

**Given** identity JSON produced by candidate source or modified after capture

**When** release readiness is validated

**Then** validation fails without transitioning or publishing the release.

## Open decisions

The approved normalized identity schema and release-record binding are defined by `SPEC-REB-001`.
