+++
id = "WO-IAR-002"
type = "work_order"
title = "Separate managed router invariants from workflow procedure"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
implements = ["REQ-IAR-010"]
specifications = ["SPEC-IAR-002"]
architecture = ["ARCH-IAR-002", "ADR-IAR-002"]
verification = ["VER-IAR-002"]
+++

# Work Order: Separate managed router invariants from workflow procedure

## Lifecycle

The repository owner approved this work order before execution. It progressed through `in_progress` and reached `implemented` only after the bounded change and retained evidence were complete. Commit, verification capture, assurance transition, release, push, and pull-request actions still require their applicable separate authority.

## Objective

Remove duplicated verification and release procedure from the managed router while preserving its non-waivable provenance, authority, and external-action boundaries and keeping complete ordered procedure directly reachable in focused policy.

## Authorization

The repository owner approved the `IAR-002` requirement, specification, architecture, ADR, verification contract, and this bounded work order on 2026-08-12 with the instruction `ok for implementation`. This decision authorizes implementation and retained evidence only; it does not authorize commit, push, pull-request creation, verification capture or transition, release, tagging, publication, or deployment.

## In scope

- Refine the canonical `ENGINEERING_HARNESS.md` commit-bound verification and release section according to `SPEC-IAR-002`.
- Propagate that managed change to the self-hosted repository and integrity lock through the supported upgrade mechanism.
- Add or adjust focused instruction-content, installation, upgrade, parity, and regression tests.
- Update the instruction-architecture acceptance scenario and retain work-order-keyed verification evidence.
- Make only documentation adjustments required to keep public descriptions accurate and non-duplicative.

## Out of scope

Changing `capture-verification` or `prepare-release` behavior; changing lifecycle eligibility, aggregate coverage, traceability semantics, decision rights, quality gates, policy-module procedure, artifact schema, ownership modes, installation profiles, historical formal artifacts, verification or release status, tags, package builds, publication, or deployment.

## Authorized decision envelope

Implementation may refine concise wording, assertion structure, and test placement while preserving every semantic obligation and conformance check. It may not remove a required invariant, create a second procedural owner, weaken managed-file conflict behavior, or hand-edit a managed digest.

## Constraints

- Preserve `ADR-IAR-001` and implement `ADR-IAR-002` as one compatible refinement.
- Keep Python 3.11+ standard-library runtime behavior and one standard installation.
- Treat target content, paths, lock metadata, and artifact text as untrusted input.
- Preserve unrelated user content and historical governance facts.

## Expected change surface

Canonical router template; self-hosted managed router and lock; focused instruction/installer tests; instruction-architecture acceptance scenario; bounded explanatory documentation if mechanically required; and `WO-IAR-002` evidence.

## Implementation plan

1. Approve `REQ-IAR-010`, `SPEC-IAR-002`, `ARCH-IAR-002`, `ADR-IAR-002`, `VER-IAR-002`, and this work order through an accountable decision.
2. Add focused tests that express the required router invariants, responsibility boundary, fresh-install result, safe upgrade, conflict preservation, and parity behavior.
3. Replace the duplicated canonical router procedure with the concise invariant-and-route contract defined by the specification.
4. Apply the supported self-upgrade so the operational router and schema-2 lock are reconciled transactionally.
5. Run `VER-IAR-002`, inspect the bounded diff, and retain exact `WO-IAR-002` evidence.
6. Mark the work order implemented and stop for separately authorized candidate commit and verification capture.

## Required verification

Execute every check in `VER-IAR-002`, including focused semantic assertions, fresh installation, every relevant safe/conflicting upgrade state, managed parity, `doctor`, formal validation, phase-appropriate preflight, CLI help, deterministic dashboard generation, and the full unit suite on Python 3.11 and the local supported runtime.

## Evidence to record

Exact commands and exit codes; Python versions; focused and full test counts; install/upgrade fixtures; changed-file inventory; canonical/root/lock parity; graph and integrity diagnostics; deterministic dashboard snapshots; manual responsibility inspection; deviations; and residual risks.

## Stop and escalate conditions

Stop if implementation would alter workflow semantics, overwrite customized content, require a manual lock digest, remove a decision or provenance constraint, change an external interface, touch historical record facts, fail a required check, or require an action outside this bounded implementation authority.

## Completion report format

Report scope delivered, changed components, verification commands and results, evidence path, deviations and residual risks, final work-order status, and explicitly unperformed governance or external actions.

## Implementation result

The canonical router now retains stable exact-commit, later-governance-commit, accountable-decision, and no-external-action invariants while routing ordered procedure to the four focused managed policies. The supported self-upgrade reconciled the operational router and schema-2 lock. Focused tests prove fresh-install content, prior-router migration, idempotence, and fail-closed preservation of customized content. Complete verification is retained in `docs/engineering/instruction-architecture/evidence/WO-IAR-002-verification.md`.
