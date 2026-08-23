+++
id = "REQ-HUP-004"
type = "requirement"
title = "Prove the exact released 0.6.0 evaluator"
status = "approved"
owners = ["repository-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN the repository plans, applies, or verifies the root-governor transition, THE SYSTEM SHALL use the isolated immutable public se-harness 0.6.0 wheel outside the checkout and prove its version, payload, archive, runtime origins, entry point, interpreter isolation, and checkout exclusion before relying on it."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Prove the exact released 0.6.0 evaluator

## Rationale

The product checkout cannot govern its own root adoption. A version string or importable module is insufficient; the exact installed public bytes and runtime boundary must agree with the released record.

## Preconditions and trigger

- The target is `se-harness==0.6.0`.
- The selected archive is `se_harness-0.6.0-py3-none-any.whl` with SHA-256 `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- The installed payload SHA-256 is `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- The operator requests read-only planning or a separately approved apply operation.

## Required response

- Resolve module, distribution, templates, interpreter, and console entry point beneath one isolated external evaluator root.
- Require isolated Python, disabled user site, absent `PYTHONPATH`, and complete checkout exclusion.
- Reconcile archive name and SHA-256 with `RLS-SEH-012` and reconcile the installed payload manifest and SHA-256.
- Stop before repository mutation when any identity, origin, digest, or environment property differs.

## Failure and boundary behavior

Missing distribution metadata, an editable or source install, wrong version, wrong digest, checkout import, foreign entry point, enabled user site, inherited `PYTHONPATH`, or non-isolated execution fails closed. Candidate source or candidate-package identity never substitutes for the released evaluator.

## Acceptance examples

### Example: isolated public evaluator

**Given** exact published wheel bytes installed outside the checkout

**When** released-evaluator identity is checked

**Then** all origins are external and the version, payload, archive, entry point, isolation, and checkout-exclusion claims match.

### Example: same-version checkout shadowing

**Given** the checkout could satisfy `import se_harness`

**When** the evaluator identity is checked

**Then** the operation stops even if the imported code also reports 0.6.0.

## Open decisions

No product decision remains. Apply remains bounded by approved `WO-HUP-002`, the immediate identity recheck, and exact plan equivalence.
