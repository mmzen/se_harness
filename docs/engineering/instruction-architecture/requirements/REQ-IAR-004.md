+++
id = "REQ-IAR-004"
type = "requirement"
title = "Make focused policy directly discoverable"
status = "implemented"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN an actor reaches the managed harness contract, THE SYSTEM SHALL expose each focused policy module directly and identify the decision point at which it applies."
verification_method = "inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Make focused policy directly discoverable

## Acceptance criteria

- `ENGINEERING_HARNESS.md` directly indexes `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md`.
- Each index entry states when the module must be consulted.
- `docs/engineering/README.md` indexes repository-specific artifact domains but does not duplicate the managed workflow or command contract.
- Shared policy remains in focused modules instead of being merged into one large instruction file.
- A maintained policy module is never reachable only through an owner-editable secondary document.
