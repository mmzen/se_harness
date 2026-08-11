+++
id = "REQ-WLC-001"
type = "requirement"
title = "Define distinct work-order lifecycle meanings"
status = "implemented"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a work order changes lifecycle state, THE SYSTEM SHALL distinguish authorization as approved, execution completion as implemented, commit-bound assurance as verified, and release inclusion as released."
verification_method = "inspection"

[relations]
derives_from = ["CAP-WLC-001"]
+++

# Requirement: Define distinct work-order lifecycle meanings

## Acceptance criteria

- The workflow and work-order template define the lifecycle sequence.
- `approved` does not claim completion.
- `implemented` records completed work and retained evidence without claiming VREC coverage.
- `verified` and `released` are used only with corresponding commit-bound provenance when the repository requires it.
