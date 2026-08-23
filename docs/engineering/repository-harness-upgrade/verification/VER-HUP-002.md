+++
id = "VER-HUP-002"
type = "verification"
title = "Verify the independent standard-root upgrade to 0.6.0"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
verifies = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
+++

# Verification Contract: Verify the independent standard-root upgrade to 0.6.0

## Independence

Run governing identity, plan, apply, integrity, and post-apply checks with the immutable public 0.6.0 environment outside the checkout. Candidate-source and candidate-package lanes may test their own behavior but cannot supply root-governor authority.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-HUP-004 | released-evaluator identity and public archive reconciliation | isolated identity output plus RLS-SEH-012 digest | exact 0.6.0 payload/archive and every runtime origin outside checkout |
| REQ-HUP-005 | authorization, plan/apply/replay, lock and evidence comparison | `WO-HUP-002-evaluator-upgrade.json` plus managed inventories | exact approved writes, schema-3 identity, atomic success, and no-op replay |
| REQ-HUP-006 | owner/product/history diff audit and three-role checks | pre/post hashes, Git diff, tests, hosted results when available | owner context preserved; no product/release/external mutation or cross-role import |

## Acceptance scenarios

- Exact public 0.6.0 plans and applies only the approved standard-root update.
- Exact public 0.5.0 start preflight reproduces only the declared `A-E009` and two `A-E010` predecessor diagnostics, while released 0.6.0 validates the complete graph with zero errors before apply.
- The mandatory no-network recovery rehearsal rejects candidate contamination and stale identity, stops conflicting chains for accountable disposition, rolls back an injected interruption exactly, restores every standard control, and records every external action as false.
- Wrong prior lock, version, payload, archive, origin, entry point, or work-order packet stops before mutation.
- Modified managed predecessor or plan expansion fails without partial overwrite.
- Existing `REPOSITORY_CONTEXT.md` bytes survive while the schema-3 lock omits the path.
- Post-apply doctor and complete-graph validation pass under released 0.6.0.
- A repeated upgrade is a no-op and does not rewrite keyed evidence.
- Candidate source/package checks remain separately labeled and non-governing.

## Property and invariant tests

- Every managed file hash matches the schema-3 lock.
- The lock evaluator object equals version 0.6.0, payload SHA-256 `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`, archive name `se_harness-0.6.0-py3-none-any.whl`, and archive SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- `docs/engineering/REPOSITORY_CONTEXT.md` has the same pre/post SHA-256 and no lock entry.
- Changed paths equal the approved HUP-002 definitions, exact managed transaction, keyed evidence, and later implementation evidence only.
- No changed path appears under `se_harness/`, `templates/repository/standard/`, package metadata, repository release tools, release records, publisher, Pages publisher, or unrelated engineering domains.

## Static and architecture checks

- Target 0.6.0 validation has zero structure, governance, or policy errors or warnings.
- `doctor` passes with exact schema-3 evaluator identity and managed integrity.
- Managed workflow syntax, permissions, exact version installation, work-order selection, and candidate isolation remain valid.
- Architecture traceability and the accepted decision assessment are complete before work-order approval.

## Security and privacy checks

- Record public hashes and normalized non-secret origins.
- Scan retained evidence for tokens, usernames, private disposable paths, and environment leakage.
- Confirm no new credential, permission, publisher, protected environment, remote, or external action.

## Performance and resilience checks

Run the complete unit suite, including scale and deterministic dashboard cases. Exercise the no-network recovery rehearsal, repeat planning, no-op replay, prior-lock mismatch, target-identity mismatch, evidence collision, customized predecessor, and interrupted transaction rollback through existing tests or retained released acceptance evidence.

## Manual assessments

- Accountable owners review the exact 18-change plan and resulting diff.
- Assurance owner reviews identity, atomicity, owner preservation, and role separation before any VREC transition.
- Repository owner confirms product, release, publication, and external state remain untouched.

## Evidence retention

Retain the canonical transaction JSON and `WO-HUP-002-verification.md` with baseline and target identities, wheel/payload hashes, normalized origins, plan/apply/replay output, pre/post hashes, lock/evidence identities, graph planes, test counts, deviations, residual risks, and every unperformed lifecycle or external action.

## Residual uncertainty

Hosted runner behavior, package-index availability, and administrator-managed repository protection remain external. Local verification proves the observed candidate, not indefinite service availability or a later merge.
