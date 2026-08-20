+++
id = "REQ-HUP-002"
type = "requirement"
title = "Apply one safe standard-root upgrade transaction"
status = "approved"
owners = ["engineering-owner", "repository-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN an accountable owner authorizes the 0.5.0 root upgrade, THE SYSTEM SHALL update only managed standard-root files proven safe against the current lock, regenerate managed integrity transactionally, and preserve every repository-owned or ambiguous surface."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-001"]
+++

# Requirement: Apply one safe standard-root upgrade transaction

## Rationale

An evaluator selection is represented by the installed runtime, root configuration, managed contract, workflow, and integrity lock together. Hand-editing a subset would recreate a split identity.

## Preconditions and trigger

- `WO-HUP-001` is approved and start preflight passes under the current installed governor.
- Released 0.5.0 identity passes `REQ-HUP-001`.
- Read-only `harnessctl upgrade .` reports a bounded deterministic plan.

## Required response

- Apply through public 0.5.0 `harnessctl upgrade . --apply` only after exact plan review.
- Change only files the installer proves equal to their current managed lock or canonically safe predecessor.
- Render the root configuration, evaluator workflow, managed contract, and lock consistently for 0.5.0.
- Preserve repository-owned artifacts, repository context, candidate-evidence workflow, publisher, Pages recovery, package source, and tests.
- Leave a recoverable working tree and deterministic before/after inventory.

## Failure and boundary behavior

Customized, ambiguous, missing, concurrently changed, or lock-divergent managed content stops the transaction without partial replacement. Repository-owned content is never overwritten merely because it differs from a portable template.

## Constraints

The current dry-run identifies only `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, and `ENGINEERING_HARNESS.md` as version-divergent managed files. Any broader plan requires renewed accountable review.

## Acceptance examples

### Example: exact managed predecessor

**Given** the three proposed files match the current lock

**When** the approved public 0.5.0 upgrader applies the plan

**Then** all managed outputs and the resulting lock agree on 0.5.0 and no repository-owned surface changes.

### Example: concurrent customization

**Given** one proposed managed file changed after plan review

**When** apply is attempted

**Then** the transaction stops and reports the conflict without silently replacing the file.

## Open decisions

Approval must name whether the observed three-file plan is accepted; implementation may not broaden it.
