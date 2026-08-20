+++
id = "REQ-HUP-001"
type = "requirement"
title = "Prove the exact released 0.5.0 evaluator"
status = "approved"
owners = ["repository-owner", "security-owner"]
created = "2026-08-20"
updated = "2026-08-20"
statement = "WHEN the repository evaluates or applies the root governor upgrade, THE SYSTEM SHALL use an isolated public se-harness 0.5.0 installation outside the checkout and prove its version, distribution root, entry point, and immutable wheel digest before relying on it."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-001"]
+++

# Requirement: Prove the exact released 0.5.0 evaluator

## Rationale

The 0.5.0 incident was caused by mixing the developing product with its evaluator. Public availability alone is not enough; the runtime actually performing governance must be role-correct and independently installed.

## Preconditions and trigger

- The public version is exactly `0.5.0`.
- The wheel SHA-256 is `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- The operator requests read-only planning or a separately approved apply operation.

## Required response

- Resolve both module and distribution metadata beneath the isolated public installation.
- Require the console entry point and Python executable to be outside the candidate checkout.
- Emit the released-evaluator role, expected version, expected root, checkout root, entry point, and wheel digest.
- Stop before artifact or managed-file mutation when any identity differs.

## Failure and boundary behavior

Missing distribution metadata, checkout imports, wrong version, wrong root, absent entry point, or digest mismatch fails closed. Candidate source or candidate package identity never substitutes for the released evaluator.

## Constraints

No network-acquired bytes may be trusted before hash and distribution identity checks. The target product repository is input data, not the evaluator runtime.

## Acceptance examples

### Example: isolated final evaluator

**Given** the exact public 0.5.0 wheel installed in an external environment

**When** released-evaluator identity is checked against the repository checkout

**Then** every runtime origin is external and the expected digest and version match.

### Example: checkout shadowing

**Given** `PYTHONPATH` or the working directory would import candidate `se_harness`

**When** identity is checked

**Then** the operation fails before planning or mutation.

## Open decisions

No product decision remains; accountable approval of the exact identity is still required before implementation.
