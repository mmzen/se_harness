+++
id = "REQ-IAR-003"
type = "requirement"
title = "Declare file ownership and lifecycle explicitly"
status = "implemented"
owners = ["requirements-steward", "engineering-owner", "repository-owner"]
created = "2026-08-11"
updated = "2026-08-21"
statement = "WHEN instruction and policy files are installed, THE SYSTEM SHALL record an explicit ownership mode for every file so managed policy, managed fragments, and repository-owned seeds cannot be confused."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Declare file ownership and lifecycle explicitly

## Acceptance criteria

- `AGENTS.md` and `CLAUDE.md` are lock-tracked managed fragments inside owner-controlled files.
- `ENGINEERING_HARNESS.md`, `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md` are fully managed and lock-tracked.
- `docs/engineering/README.md` is installed as an owner-owned seed and tracked by presence rather than content digest after installation.
- `doctor` reports the mode and integrity result of every required installed file.
- The self-hosting repository follows the same declared modes as a target installation or records an explicit validated exception; absence from the lock is not accepted as an implicit mode.
