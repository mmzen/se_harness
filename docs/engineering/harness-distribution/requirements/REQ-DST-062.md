+++
id = "REQ-DST-062"
type = "requirement"
title = "Provide durable demonstrator topology headroom"
status = "approved"
owners = ["product-owner", "technical-owner", "quality-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the SE Harness repository acceptance suite evaluates its compact Explorer topology, THE SYSTEM SHALL use a 2,097,152-byte UTF-8 acceptance target while continuing to report the exact observed size."
verification_method = "automated-performance-budget-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Provide durable demonstrator topology headroom

## Rationale

The 524,288-byte repository target was selected when the formal graph was materially smaller. Merged HUP and verification history now produce a valid 539-artifact, 1,944-relation topology of 525,689 bytes. The one-resource progressive design remains sound, but the current-repository acceptance test fails after ordinary governed growth.

A fourfold target provides meaningful headroom for the 0.5.1 recovery and continued governed evolution without returning artifact or evidence bodies to the topology resource.

## Preconditions and trigger

The deterministic progressive dashboard bundle has been generated for the SE Harness repository or an equivalent acceptance fixture, and the current-repository topology acceptance assertion is evaluated.

## Required response

- Compare the compact topology resource against exactly 2,097,152 UTF-8 bytes before compression.
- Report the actual topology bytes, configured target, resource role totals, and `topology_target_exceeded` observation.
- Keep target excess observational for general consumer generation while requiring the SE Harness repository acceptance fixture to remain at or below the target.
- Preserve deterministic serialization so identical accepted inputs and Git history produce identical bytes.

## Failure and boundary behavior

The SE Harness acceptance test fails when its topology exceeds 2,097,152 bytes. Consumer generation continues to report larger valid topology rather than misclassifying the formal graph as invalid. Exceeding this target does not weaken manifest size/digest verification or authorize silent truncation.

## Constraints

- The value is a repository acceptance target, not a universal consumer repository maximum and not an assurance score.
- Measurements remain uncompressed UTF-8 bytes.
- No topology field, relation, finding, readiness input, or provenance observation may be dropped to meet the target.
- A future need beyond 2 MiB requires explicit reassessment of topology sharding rather than another implicit increase.

## Acceptance examples

### Example: current merged repository

**Given** merged `main` produces a 525,689-byte compact topology,

**When** the updated acceptance suite evaluates it,

**Then** it passes against 2,097,152 bytes and reports both values.

### Example: future target excess

**Given** a future SE Harness topology exceeds 2,097,152 bytes,

**When** repository acceptance runs,

**Then** it fails explicitly without truncating data or invalidating the formal graph.

## Open decisions

The proposed target is exactly 2 MiB. Approval accepts that target; implementation may not choose a different value.
