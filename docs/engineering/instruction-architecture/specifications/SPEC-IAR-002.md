+++
id = "SPEC-IAR-002"
type = "specification"
title = "Invariant router and procedural policy responsibility"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
specifies = ["REQ-IAR-010"]
+++

# Specification: Invariant router and procedural policy responsibility

## Scope

Refine the commit-bound verification and release guidance in the canonical managed router, propagate it through the supported installation and self-hosting paths, and verify that ordered procedure has one focused owner. This is an instruction-responsibility change, not a lifecycle or command-behavior change.

## Actors and external systems

- Engineering agents and human actors following the installed harness.
- Repository owners adopting or upgrading the managed router.
- The installer and managed-file lock that distribute and protect the router.

## Inputs

- The canonical `ENGINEERING_HARNESS.md` template.
- The installed `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md` policy modules.
- Existing managed-file state and lock metadata during installation or upgrade.

## Outputs

- A concise commit-bound verification and release section in the canonical and self-hosted router.
- Updated self-hosted managed integrity produced through the supported upgrade path.
- Tests and retained evidence demonstrating semantic preservation and safe distribution.

## State model

No product or governance lifecycle state changes. Existing managed-file modes, conflict states, and transactional upgrade behavior remain unchanged.

## Behavioral rules

1. `ENGINEERING_HARNESS.md` remains the single managed contract and router.
2. Its commit-bound verification and release section must state that verification and release follow the focused policies, that records identify the exact candidate commit and therefore reside in later governance commits, and that harness commands do not exercise accountable decision rights or perform external lifecycle actions.
3. The recommended concise wording is:

   > Verification and release follow `docs/engineering/WORKFLOW.md`, subject to `QUALITY_GATES.md`, `TRACEABILITY.md`, and `DECISION_RIGHTS.md`. VRECs and release records must identify the exact candidate commit they govern and therefore reside in later governance commits. Harness commands may prepare records, but never exercise accountable decision rights or commit, push, tag, release, publish, or deploy.

4. The router must not restate the ordered `capture-verification` and `prepare-release` procedure, aggregate CLI arguments, or record-transition sequence maintained in `WORKFLOW.md`.
5. `WORKFLOW.md` retains the ordered lifecycle procedure; `TRACEABILITY.md` retains binding and coverage semantics; `DECISION_RIGHTS.md` retains accountable ownership; and `QUALITY_GATES.md` retains the gate model.
6. Implementation must update the canonical template first and reconcile the self-hosted copy and lock through the supported installer/upgrade mechanism rather than by hand-editing a digest.
7. Fresh installation and a safe upgrade of unchanged managed content must produce the new router. Customized, damaged, or ambiguous managed content must retain existing fail-closed preservation behavior.
8. No implementation may change the CLI behavior, artifact schema, status-transition rules, policy-module bodies, or historical formal records merely to satisfy this specification.

## Error and recovery behavior

Existing installer conflict diagnostics and no-partial-write behavior apply. If template/root/lock parity cannot be established through the supported mechanism, implementation stops rather than weakening integrity or editing lock data manually.

## Data and interface contracts

No command-line, JSON, artifact metadata, or public Python interface changes. The managed router remains UTF-8 text protected by the installed schema-2 lock representation.

## Security and privacy properties

The refinement must retain all explicit authority and side-effect prohibitions. Target content and lock metadata remain untrusted. No new external service or data handling is introduced.

## Performance and capacity

Not applicable beyond preserving deterministic installation, upgrade, doctor, and preflight behavior.

## Observability

Existing `doctor`, preflight, formal validation, and deterministic dashboard results provide structural evidence. Focused tests must identify responsibility drift with a clear assertion rather than relying only on a complete-file snapshot.

## Compatibility and migration

This is a normal managed-template upgrade. Unchanged prior content may be upgraded transactionally; customized content must be preserved and reported under the existing contract. No installation profile, ownership-mode migration, or artifact migration is introduced.

## Examples and counterexamples

- **Conforming:** the router states exact-commit, later-governance-commit, decision-right, and no-external-action invariants and points to focused policy.
- **Nonconforming:** the router repeats the exact sequence and arguments for `capture-verification` and `prepare-release`.
- **Nonconforming:** procedural text is removed along with the provenance or authority boundary.
- **Nonconforming:** `WORKFLOW.md` is removed or made reachable only through an owner-controlled index.

## Explicitly unspecified decisions

Test helper organization and minor prose refinements are delegated to implementation, provided the required semantics and direct routing remain mechanically inspectable.
