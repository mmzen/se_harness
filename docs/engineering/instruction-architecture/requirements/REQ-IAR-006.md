+++
id = "REQ-IAR-006"
type = "requirement"
title = "Provide deterministic read-only work-order preflight"
status = "implemented"
owners = ["requirements-steward", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"
statement = "WHEN a work order is selected for implementation, THE SYSTEM SHALL provide a deterministic read-only preflight that validates readiness and enumerates the complete governing inputs without inferring authority."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Provide deterministic read-only work-order preflight

## Acceptance criteria

- `harnessctl preflight . --work-order WO-...` checks installation integrity, repository-context completeness, formal graph validity, work-order existence and an implementation-authorized `approved` or `in_progress` status, and the complete linked intent-to-verification chain.
- `--phase review` additionally accepts `implemented`, `verified`, or `released` so pull-request CI can assess completed work without falsifying lifecycle status.
- Success output lists ordered paths for the managed contract, required policy modules, repository context, selected work order, and every linked governing artifact, followed by required validation and repository commands.
- Failure output reports stable diagnostic codes and every independently detectable blocker in deterministic order.
- `--json` returns the same facts in a versioned machine-readable schema.
- Preflight writes no repository file, changes no lifecycle status, and does not claim that a human or agent read the listed material.
- Paths and work-order IDs are handled as untrusted input and cannot escape the repository root or enter a shell command.
