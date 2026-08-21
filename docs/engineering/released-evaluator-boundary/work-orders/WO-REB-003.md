+++
id = "WO-REB-003"
type = "work_order"
title = "Harden evaluator upgrades and bounded recovery"
status = "implemented"
owners = ["engineering-owner", "repository-owner", "quality-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "Operators and future governance decisions will rely on the changed upgrade policy, conflict diagnostics, and executable recovery controls."
decided_by = "engineering-owner"

[relations]
implements = ["REQ-REB-005", "REQ-REB-006", "REQ-REB-007"]
specifications = ["SPEC-REB-002"]
architecture = ["ARCH-REB-001", "ADR-REB-001"]
verification = ["VER-REB-001"]
+++

# Work Order: Harden evaluator upgrades and bounded recovery

## Lifecycle

Bounded implementation is complete with retained evidence at `docs/engineering/released-evaluator-boundary/evidence/WO-REB-003-verification.md`. This implemented state records source, tests, and disposable rehearsal only. It does not authorize an actual evaluator upgrade, incident action, external publication, release, deployment, commit-bound verification, or lifecycle disposition of conflicting chains.

## Objective

Keep evaluator upgrades distinct from product releases, expose incompatible draft and ready chains without silently creating authority, and provide a bounded recovery procedure that can be rehearsed safely before another publication incident.

## In scope

- Define and enforce the evaluator-upgrade transaction: separate approval, exact candidate evaluator identity, reproducible installation, isolated verification, atomic lock update, and rollback evidence.
- Ensure a product release command cannot silently upgrade the evaluator or change the standard lock.
- Add read-only inspection and validation diagnostics for multiple draft or ready chains, including their requirement, specification, architecture, work-order, verification, release, and evaluator identities.
- Require ambiguous or incompatible chains to stop for accountable disposition rather than selecting a winner or fabricating lifecycle authority.
- Add an operator runbook for publication-deadlock recovery with prerequisites, bounded commands, success criteria, rollback points, and escalation triggers.
- Add a disposable-root rehearsal covering candidate contamination, stale or mismatched evaluator identity, conflicting chains, interrupted migration, and safe rollback without real credentials or publication.
- Normalize current operator terminology to `evaluator` while preserving clearly marked historical terminology.

## Out of scope

- Performing an actual evaluator upgrade in the installed root.
- Resolving or deleting existing draft or ready chains without accountable direction.
- Publishing a product, dashboard, package, release, or tag.
- Replacing the standard lifecycle with an emergency or repository-specific governance profile.
- Incident response outside the evaluator-boundary failure modes defined by `SPEC-REB-002`.

## Authorized decision envelope

The implementation agent may choose read-only presentation details, diagnostic identifiers, runbook organization, and disposable-fixture construction. It may not infer approval, automatically transition or discard artifacts, couple a product version to an evaluator version, use candidate source to escape a deadlock, or add an ungoverned override path.

## Constraints

- Evaluator upgrade and product release remain separate governed transactions even when they occur near each other.
- Inspection may reveal conflicts but must not mutate lifecycle state or choose an authoritative chain.
- Recovery commands must be bounded, auditable, idempotent where feasible, and stop before external side effects.
- Rehearsal uses disposable roots and synthetic identities; real credentials and production publication targets are forbidden.
- Historical records remain immutable and may retain legacy words when their historical meaning is explicit.
- Any lock transition preserves a recoverable previous identity and evidence.

## Expected change surface

- Evaluator upgrade policy, commands or guarded migration components, and lock-transition evidence.
- Read-only inspection, validation, and dashboard diagnostics for chain conflicts.
- Operator runbook, rehearsal fixtures, current terminology, and focused tests.
- Repository documentation describing accountable disposition and rollback boundaries.

## Required verification

- Prove product release paths cannot modify evaluator identity or the standard lock.
- Prove evaluator upgrades require separate approved scope, verify exact identity in isolation, update atomically, and retain rollback evidence.
- Exercise compatible and incompatible multi-chain fixtures; assert deterministic diagnostics and no inferred lifecycle authority.
- Run the complete recovery rehearsal in a disposable root, including interrupted migration and rollback, with no network publication or credentials.
- Scan current executable and operator surfaces for retired terminology, excluding clearly identified historical records.
- Run independent artifact validation and relevant focused and regression suites from the exact external released evaluator.
- Capture eligible commit-bound verification covering `WO-REB-003`.

## Evidence to record

- Evaluator-upgrade transaction and rollback results, including before/after lock identities.
- Conflict fixtures, diagnostics, and proof that inspection made no lifecycle mutation.
- Executed recovery transcript, root digests, rollback outcome, and absence of external side effects.
- Terminology scan, historical exclusions, evaluator isolation proof, and the eligible commit-bound verification record covering `WO-REB-003`.

## Stop and escalate conditions

- An evaluator upgrade cannot be atomic or preserve rollback evidence.
- Conflict handling would require selecting, approving, superseding, or deleting an artifact chain.
- Recovery needs candidate authority, an exact-identity bypass, real credentials, or external publication.
- A product release path mutates evaluator identity in a way that cannot be separated within this scope.
- The rehearsal exposes an unbounded failure mode outside the accepted specification.

## Completion report format

Report the upgrade boundary, conflict behavior, runbook and rehearsal results, exact tests, evaluator identity, rollback proof, operational risks, lifecycle state, and the single recommended next accountable action.
