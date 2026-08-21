+++
id = "WO-REB-002"
type = "work_order"
title = "Enforce evaluator identity for mutation and release readiness"
status = "implemented"
owners = ["engineering-owner", "security-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "All later root mutations and release-readiness decisions will trust the new pre-write guard and evaluator-bound evidence."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-001", "REQ-REB-003"]
specifications = ["SPEC-REB-001"]
architecture = ["ARCH-REB-001", "ADR-REB-001"]
verification = ["VER-REB-001"]
+++

# Work Order: Enforce evaluator identity for mutation and release readiness

## Lifecycle

This work order is implemented with retained evidence in `docs/engineering/released-evaluator-boundary/evidence/WO-REB-002-implementation.md`. Commit-bound assurance remains pending. This state does not verify the candidate, authorize work assigned to `WO-REB-003`, or authorize external publication, release, or deployment.

## Objective

Make the locked released-evaluator identity a mandatory, fail-closed precondition of every installed-root mutation and bind that same identity into canonical verification and release-readiness evidence.

## In scope

- Implement one internal evaluator guard from the identity contract established by `WO-REB-001`.
- Invoke the guard inside all public installed-root mutators before their first write, including upgrade apply, non-dry-run domain scaffolding, artifact creation, renumber apply, verification capture, and release preparation.
- Make future mutators use the same guarded dispatch boundary by construction or by an enforceable invariant test.
- Return stable diagnostics for lock, payload, archive, environment, interpreter, and entry-point mismatches.
- Record evaluator role, version, payload digest, archive digest when required, interpreter, entry point, and isolation result in canonical verification evidence.
- Require release preparation and release-readiness validation to consume matching evaluator-bound evidence.
- Update templates, provenance validation, operator documentation, and focused tests for the new evidence contract.

## Out of scope

- Publication workflow and dashboard-helper migration; that belongs to `WO-REB-001`.
- Evaluator upgrade separation, conflict inspection, and recovery rehearsal; that belongs to `WO-REB-003`.
- Approving work orders, capturing a real release verification, preparing a real release, or publishing externally.
- Broad mutation-command redesign beyond the common guard boundary.

## Authorized decision envelope

The implementation agent may choose the internal guard API, diagnostic identifiers, and how common mutator dispatch is factored. It may not add bypass switches, defer the check until after a write, treat candidate identity as sufficient, infer evaluator identity from the checkout, or allow incomplete identity evidence to support release readiness.

## Constraints

- Begin only after the `WO-REB-001` identity contract is implemented and stable enough to consume.
- Every rejected mutation must leave the installed root byte-for-byte unchanged.
- Dry-run and read-only commands remain read-only; they may expose diagnostics without acquiring mutation authority.
- Exact version plus payload identity is mandatory, and archive identity is mandatory where the standard lock requires it.
- Evidence schema changes must remain deterministic, portable, and independently validated.
- Candidate-source tests are candidate evidence only; authoritative checks use the exact released evaluator outside the checkout.

## Expected change surface

- Shared CLI mutation dispatch and runtime-identity guard components.
- Upgrade, scaffold, artifact creation, renumber, verification-capture, and release-preparation command paths.
- Verification and release record schemas, templates, provenance validators, and diagnostics.
- Focused mutation-exclusion, evidence-binding, and regression tests.

## Required verification

- For every public mutator, inject missing lock, version mismatch, payload mismatch, archive mismatch, candidate interpreter, editable install, and checkout contamination where applicable; assert deterministic rejection and zero writes.
- Prove a matching released evaluator can execute each authorized mutation path in a disposable root.
- Prove canonical verification evidence records exact evaluator identity and release preparation rejects absent or mismatched identity.
- Prove new public mutators cannot bypass the common guard through an invariant or dispatch-coverage test.
- Run independent artifact validation and relevant focused and regression suites from the exact external released evaluator.
- Capture eligible commit-bound verification covering `WO-REB-002`.

## Evidence to record

- Exact mutation matrix, commands, exit codes, diagnostics, and before/after root digests for rejection cases.
- Successful disposable-root mutation results under the matching evaluator.
- Canonical evidence and release-readiness rejection examples.
- Evaluator identity and isolation proof plus the eligible commit-bound verification record covering `WO-REB-002`.

## Stop and escalate conditions

- Any public mutator cannot be placed behind the common guard before its first write.
- Exact payload or archive identity cannot be recovered or verified from the standard contract.
- The evidence change would invalidate historical records without an explicit compatibility rule.
- Release preparation needs identity not established by `WO-REB-001`.
- A test requires mutation of the real installed root or release credentials.

## Completion report format

Report the guarded command inventory, identity and evidence contracts, tests and zero-write proofs, evaluator identity, retained evidence, compatibility concerns, lifecycle state, and the single recommended next accountable action.
