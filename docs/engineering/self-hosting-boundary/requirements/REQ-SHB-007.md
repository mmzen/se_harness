+++
id = "REQ-SHB-007"
type = "requirement"
title = "Protect self-hosting controls from standard upgrade"
status = "approved"
owners = ["requirements-steward", "repository-owner", "technical-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN standard repository upgrade evaluates the se-harness implementation repository, THE SYSTEM SHALL preserve its declared repository-specific self-hosting controls when they match their current lock, report consumer-template divergence without overwriting, and fail transactionally on missing, ambiguous, or modified controls."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-SHB-001"]
+++

# Requirement: Protect self-hosting controls from standard upgrade

## Rationale

The implementation repository intentionally owns a self-hosting configuration and three-plane workflow that differ from the standard consumer template. The current `doctor` recognizes this boundary, but the standard upgrade planner treats both files as ordinary managed content and proposes replacing them when their existing bytes correctly match the root lock. Applying that plan would remove the declared self-hosting role and replace the independent three-plane workflow with the consumer workflow.

## Preconditions and trigger

- The target identifies the exact `se-harness` implementation repository through repository-specific configuration, project metadata, source layout, and governor descriptor.
- A normal `harnessctl upgrade` plan or apply evaluates managed repository content.
- The protected paths are exactly `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml`.

## Required response

- Classify consumer, valid self-hosting, and ambiguous self-hosting targets before planning any write.
- For a valid self-hosting target, compare each protected file with its current root lock entry rather than with the rendered consumer template.
- Report a lock-matching protected file explicitly as `protected` and preserve its bytes and lock evidence during normal upgrade.
- Report that the consumer template differs when applicable without treating the difference as candidate drift or permission to merge.
- Continue to plan safe updates for every other standard managed file under existing integrity rules.
- Preserve ordinary consumer workflow installation and upgrade behavior unchanged.

## Failure and boundary behavior

- A missing protected file, missing or malformed lock entry, content mismatch, incomplete self-hosting declaration, invalid governor descriptor, or target-identity ambiguity blocks the complete apply without partial writes.
- Normal upgrade never refreshes a protected digest merely because the current file differs from its prior lock.
- Changing protected content requires a separately selected work order and the explicit governor-control reconciliation defined by `REQ-SHB-009`; publication or package installation alone never authorizes it.
- The protected-path set cannot expand through configuration or repository content.

## Constraints

- Do not create a consumer installation profile.
- Preserve schema-2 canonical text integrity and schema-1 compatibility behavior.
- Keep `doctor`, preflight, upgrade, and `reconcile-governor` on one shared self-hosting classification policy.
- Automation may preserve, diagnose, or reconcile authorized content; it may not infer approval, verification, release, publication, or governor promotion.

## Acceptance examples

### Example: normal self-hosting upgrade

**Given** both protected files match their root lock and ordinary candidate-managed files need safe updates,

**When** normal upgrade is planned and applied,

**Then** the protected files remain byte-identical, their disposition is visible, and eligible ordinary files update transactionally.

### Example: modified protected workflow

**Given** the self-hosting workflow differs from its root lock,

**When** normal upgrade is planned or applied,

**Then** the workflow is classified as a blocking protected-control mismatch and no file is written.

## Open decisions

None. The exact internal enum and diagnostic-code names remain delegated to the implementation.
