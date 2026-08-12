+++
id = "SPEC-IAR-003"
type = "specification"
title = "Review routing and visualization procedure ownership"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
specifies = ["REQ-IAR-011"]
+++

# Specification: Review routing and visualization procedure ownership

## Scope

Move exact review-preflight and dashboard procedure from the managed router into the focused workflow while retaining a concise review evidence boundary in the router. This is a managed-instruction allocation change only.

## Behavioral rules

1. Replace the router's review paragraph with:

   > Review readiness and visualization follow `docs/engineering/WORKFLOW.md`, subject to `QUALITY_GATES.md`. Preflight and Harness Explorer outputs are derived, read-only evidence; neither approves work nor verifies a candidate.

2. Replace workflow step 6 with:

   > Retain evidence keyed to every release-bearing work-order ID, run `harnessctl preflight . --work-order WO-... --phase review`, generate Harness Explorer with `harnessctl dashboard .`, and inspect the candidate's consistency and anomaly findings.

3. The router must not contain the exact review-preflight or dashboard invocation after the change.
4. `WORKFLOW.md` must retain both exact commands in the correct pre-candidate-commit phase.
5. The canonical router and workflow templates must change first; operational copies and schema-2 lock entries must be reconciled through the supported upgrade path.
6. Exact prior managed content upgrades transactionally; customized or ambiguous content is preserved and blocks all writes.
7. No CLI behavior, output schema, artifact lifecycle, quality gate, traceability rule, ownership mode, or historical record changes.

## Error and recovery behavior

Existing installer conflict reporting and no-partial-write behavior apply independently and transactionally across both managed files. Failure to establish canonical/root/lock parity is a stop condition.

## Observability

Focused tests assert content responsibility, exact-prior upgrade behavior, idempotence, and preservation on conflict. Existing doctor, preflight, validation, and dashboard commands provide structural evidence.

## Compatibility and migration

This is a normal schema-2 managed-content upgrade affecting two fully managed files. It introduces no installation profile, file, command, or ownership-mode migration.

## Explicitly unspecified decisions

Minor prose and test-helper organization may vary only if all required meanings and exact command ownership remain mechanically inspectable.
