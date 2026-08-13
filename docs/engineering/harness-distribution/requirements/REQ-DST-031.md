+++
id = "REQ-DST-031"
type = "requirement"
title = "Preserve deterministic verification provenance"
status = "implemented"
owners = ["quality-owner", "technical-owner"]
created = "2026-08-13"
updated = "2026-08-13"
statement = "WHEN Explorer output is generated repeatedly from unchanged repository state, THE SYSTEM SHALL preserve byte-deterministic dashboard-data.json output and its commit-bound artifact snapshot meaning."
verification_method = "automated-determinism-test"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Preserve deterministic verification provenance

## Rationale

`capture-verification` hashes the canonical `dashboard-data.json` output into `artifact_snapshot_sha256`. A generation timestamp or presentation-only state inside that snapshot would change the hash without a repository-state change and weaken reproducibility.

## Required response

The canonical snapshot must remain deterministic for identical repository content and Git state. Generation time, elapsed time, rendered-asset hashes, and other run observations belong only in `generation-summary.json` or other explicitly non-canonical output.

The HTML renderer may embed the canonical snapshot using safe deterministic escaping. UI-only calculations must not mutate the serialized snapshot or change the snapshot hash contract.

## Failure and boundary behavior

Generation must fail clearly rather than emit partially replaced templates, multiple snapshot sentinels, or an output set whose snapshot and summary disagree.

## Acceptance examples

### Example: repeated generation

**Given** repository content and observed Git state are unchanged

**When** Explorer is generated twice

**Then** both `dashboard-data.json` files and reported snapshot SHA-256 values are identical.
