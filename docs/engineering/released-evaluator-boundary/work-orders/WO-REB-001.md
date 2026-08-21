+++
id = "WO-REB-001"
type = "work_order"
title = "Align publication with the standard released evaluator"
status = "implemented"
owners = ["engineering-owner", "release-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "Publication and future release decisions will rely on the correctness of the changed lock contract, workflow inputs, and evaluator resolution behavior."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-002", "REQ-REB-004"]
specifications = ["SPEC-REB-001"]
architecture = ["ARCH-REB-001", "ADR-REB-001"]
verification = ["VER-REB-001"]
+++

# Work Order: Align publication with the standard released evaluator

## Lifecycle

This work order is implemented with retained evidence in `evidence/WO-REB-001-implementation.md`. It is not commit-bound verified or released and does not authorize publication, release, or work assigned to `WO-REB-002` or `WO-REB-003`.

## Objective

Remove the active publication split-brain identified by issue #81 by making every publication entry point resolve and verify the standard released evaluator described by the repository lock. Retire active `governor` roles, flags, fields, and descriptor dependencies without adding another repository-specific self-hosting profile.

## In scope

- Implement the schema-3 standard-lock evaluator identity and bounded schema-2 migration behavior defined by `SPEC-REB-001`.
- Provide one reusable publication resolver for the locked evaluator identity, payload, optional source archive, interpreter, and entry point.
- Change the PyPI and dashboard publication workflows to use the supported `released-evaluator` role and evaluator archive input.
- Change the dashboard publication helper to consume the standard lock rather than `.self-hosting/governor.toml`.
- Extend active-surface invariant checks so executable workflows, scripts, templates, and current operational documentation cannot reintroduce retired self-hosting roles or inputs.
- Add focused success and fail-closed tests for lock parsing, evaluator resolution, workflow arguments, and retired-surface detection.

## Out of scope

- Enforcing the evaluator guard inside every mutating command or changing release-readiness evidence; that belongs to `WO-REB-002`.
- Evaluator upgrade separation, draft-chain conflict handling, or incident recovery rehearsal; that belongs to `WO-REB-003`.
- Publishing a package, dashboard, release, tag, or repository change to an external service.
- Changing product behavior unrelated to evaluator identity or publication entry points.

## Authorized decision envelope

The implementation agent may choose internal function boundaries, diagnostic identifiers, and test-fixture names. It may not weaken exact identity matching, allow fallback to candidate source, introduce a second lock or special self-hosting profile, reinterpret historical records as active configuration, or change lifecycle status without accountable approval.

## Constraints

- Preserve exactly one standard installation and upgrade model.
- Candidate source, candidate packages, and the checkout interpreter remain ineligible to evaluate or mutate the installed root.
- Resolver failure must be explicit and fail closed before publication-side effects.
- Historical incident and release records may retain legacy terminology when clearly historical.
- Schema-2 compatibility is read-only until the separately governed migration is applied.
- Retire unsupported `governor` inputs only through the accepted standard contract.

## Expected change surface

- Standard lock schema, parser, templates, managed-integrity metadata, and migration support.
- Runtime identity and publication evaluator resolution components.
- PyPI and dashboard publication workflows and repository publication helpers.
- Active-surface invariant checks, tests, and current operator documentation.

## Required verification

- Validate schema-3 parsing, payload identity, optional archive identity, and schema-2 read-only behavior with positive and negative fixtures.
- Prove both publication workflows invoke the supported `released-evaluator` role and evaluator archive argument.
- Prove the dashboard helper resolves only from the standard lock and fails closed on missing, malformed, or mismatched identity.
- Prove active executable surfaces contain no retired self-hosting role, flag, field, or descriptor dependency.
- Run independent engineering-artifact validation and relevant focused tests from an isolated released evaluator.
- Capture eligible commit-bound verification covering `WO-REB-001`.

## Evidence to record

- Exact commands, exit codes, and focused test results.
- Evaluator version, payload digest, archive digest when applicable, interpreter, entry point, and checkout-isolation diagnostics.
- Changed workflow invocations, resolver diagnostics, and active-surface scan results with historical exclusions.
- The eligible commit-bound verification record covering `WO-REB-001`.

## Stop and escalate conditions

- The standard lock cannot express all identity needed by a publication entry point without a second descriptor.
- A publication path requires candidate source, an editable install, or the checkout interpreter.
- Migration would overwrite an unrecognized lock or cannot be made deterministic and reviewable.
- Retired terminology carries current behavior not covered by this work order.
- Required verification needs external publication credentials or side effects.

## Completion report format

Report completed scope, changed components, evaluator identity, validation results, retained evidence, remaining risks, lifecycle state, and the single recommended next accountable action.
