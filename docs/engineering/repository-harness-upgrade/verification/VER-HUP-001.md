+++
id = "VER-HUP-001"
type = "verification"
title = "Verify the independent standard-root upgrade to 0.5.0"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"

[relations]
verifies = ["REQ-HUP-001", "REQ-HUP-002", "REQ-HUP-003"]
+++

# Verification Contract: Verify the independent standard-root upgrade to 0.5.0

## Independence

Run governance checks with the immutable public 0.5.0 environment outside the checkout. Candidate-source and candidate-package lanes may test their own behavior but cannot supply root validation, preflight, or assurance authority.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-HUP-001 | released-evaluator identity and distribution hash | external environment inventory | exact 0.5.0, exact wheel digest, all runtime origins outside checkout |
| REQ-HUP-002 | plan/apply replay, lock and changed-surface comparison | managed upgrade evidence | only approved safe managed updates and transactional integrity |
| REQ-HUP-003 | local/hosted three-role checks and rollback review | CI URLs, identity manifests, base/candidate diff | no cross-role import, all gates pass, prior root recoverable |

## Acceptance scenarios

- Exact external public 0.5.0 plans and applies the reviewed standard-root update.
- Wrong version, digest, origin, or entry point stops before mutation.
- Modified managed predecessor fails without overwrite.
- Hosted Engineering Harness installs public 0.5.0 and passes review preflight for `WO-HUP-001`.
- Candidate source/package checks remain separately labeled evidence.

## Property and invariant tests

- Every managed file hash matches the resulting schema-2 lock.
- No changed path appears under `se_harness/`, product templates, package metadata, release domains, publisher, Pages recovery, or issue content.
- All declared evaluator version fields equal 0.5.0 after apply.
- Re-running upgrade reports no further safe change.

## Static and architecture checks

- Formal graph validation has zero structure, governance, or policy errors/warnings.
- Workflow YAML preserves permissions, exact package installation, work-order selection, and candidate isolation.
- Architecture selection and no-significant-decision assessment are complete before approval.

## Security and privacy checks

- Record public hashes and normalized non-secret origins.
- Scan retained evidence for tokens and private disposable paths.
- Confirm no new secret, permission, external publisher, or environment change.

## Performance and resilience checks

No production performance change applies. Exercise repeat planning, safe no-op replay, lock mismatch, and interrupted/failed apply recovery where supported.

## Manual assessments

- Accountable owner reviews the exact three-file plan and resulting diff.
- Assurance owner reviews origin separation and retained evidence before any VREC transition.
- Repository owner confirms product/release scope remains untouched.

## Evidence retention

Retain evidence at `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-001-verification.md`, including evaluator identity, wheel digest, pre/post hashes, plan/apply output, graph planes, test counts, workflow results, changed-surface proof, deviations, residual risks, and unperformed actions.

## Residual uncertainty

Future package-index or GitHub behavior and administrator-managed branch protection remain external. Verification proves the candidate and observed hosted runs, not indefinite service availability.
