+++
id = "REQ-DST-030"
type = "requirement"
title = "Preserve Explorer semantic fidelity"
status = "implemented"
owners = ["product-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"
statement = "WHEN a reader explores harness state, THE SYSTEM SHALL preserve the current artifact, relation, finding, coverage, readiness, provenance, supersession, evidence, and experiment semantics while answering all five Harness Explorer questions."
verification_method = "automated-test-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Preserve Explorer semantic fidelity

## Rationale

A visually stronger interface is valuable only when it retains the distinctions that make SE Harness assessable. A compact aggregate score, renamed relation, flattened finding, or inferred approval would make the dashboard easier to scan but less truthful.

## Required response

The interface must continue to answer:

1. Why does this artifact or work exist?
2. Is the active definition covered by specifications and independent verification contracts?
3. What declared direct and transitive relationships require reassessment after a change?
4. What is inconsistent or not assessable, and why?
5. What do controlled experiment observations say about whether the harness helps?

It must render every current artifact type and preserve declared relation direction, type, authority, target existence, and derived-path explanation. It must retain structured finding fields, exact readiness gate conditions, `not_assessable` as distinct from pass or fail, observed-versus-authoritative revision labels, VREC supersession history, evidence paths, and controlled experiment results.

Definition coverage must not be labeled or calculated as commit-bound verification. Lifecycle state is authority, not confidence, and the interface must not replace explicit gates with an aggregate health score.

## Failure and boundary behavior

Unknown future artifact types and relation types must remain visible with neutral styling. Missing evidence is not satisfied evidence. Derived relations and observations must remain visibly non-authoritative.

## Acceptance examples

### Example: not-assessable gate

**Given** a work order lacks information required to evaluate one readiness condition

**When** the readiness view renders

**Then** it shows the exact condition as `not_assessable`, not passed or failed.

### Example: superseded verification

**Given** a ready VREC was explicitly superseded by an eligible verified successor

**When** its lineage is inspected

**Then** both records, commits, coverage, authority, and old-to-successor relationship remain understandable.
