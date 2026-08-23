+++
id = "REQ-REB-016"
type = "requirement"
title = "Declare a complete predecessor-to-successor governance migration contract"
status = "approved"
owners = ["requirements-steward", "repository-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN a successor changes governance behavior that the locked released predecessor cannot completely create or interpret, THE SYSTEM SHALL require one machine-readable migration contract that defines every evaluator role, artifact view, authority effect, compatibility boundary, failure condition, and post-publication adoption exit before that successor can qualify for release."
verification_method = "automated-contract-and-boundary-test"

[relations]
derives_from = ["CAP-REB-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "requirements-steward"
+++

# Requirement: Declare a complete predecessor-to-successor governance migration contract

## Rationale

Issue #101 and the 0.6.0 RCA show that individually correct release steps are not enough. Version 0.5.0 could govern the repository, while candidate 0.6.0 introduced schemas and lifecycle meanings that 0.5.0 could not fully create or parse. Because the handover was not defined as one contract before release work began, bootstrap preparation, rejected-history handling, successor preparation, hosted assessment, publication, rendering, and later root adoption were discovered and corrected separately.

The migration must therefore be an explicit product contract rather than a release-specific checklist. It must identify which evaluator makes each technical observation, which accountable human owns each decision, which repository view is evaluated, and which state changes are permitted. Candidate code may produce evidence, but it must never obtain predecessor or human authority from the migration contract.

## Preconditions and trigger

This requirement applies when a proposed successor changes at least one behavior used by release governance and the locked released predecessor cannot perform or parse the successor form unchanged. Relevant changes include formal artifact schemas, lifecycle states or meanings, evidence formats, release-record preparation, validation, rendering, publication gates, or root-upgrade inputs.

## Required response

- Classify the compatibility delta before release qualification as compatible or migration-required, with the exact affected operations.
- Use one versioned machine-readable contract for the full migration, not stage-specific prose or independent diagnostic allowlists.
- Define closed roles for the released predecessor, successor candidate, current complete-graph validator, accountable decision fixtures used only in rehearsal, publication/render planners, and post-publication upgrade simulator.
- Define the ordered stages: prepare, validate, reject, replace, assess, release-plan, publish-plan, render, and adopt.
- For every stage, declare the input repository view, evaluator role, required observations, permitted repository mutations, authority effect, failure result, and retained output.
- Bind an execution to exact predecessor distribution identity, exact successor candidate identity, exact source or fixture identity, and every adapter or compatibility-view identity.
- Keep product release and later root-evaluator adoption as separate state machines. The predecessor remains selected until a separately governed upgrade applies an already immutable public successor.
- Produce canonical, privacy-bounded output suitable for independent replay and commit-bound evidence.

## Failure and boundary behavior

Missing stages, undeclared evaluator/target combinations, candidate root mutation, an implicit lifecycle decision, an unbound compatibility view, accepted-error lists, mutable evaluator identity, or combined publication/adoption authority make the migration contract invalid. Qualification must stop before a release decision or privileged external action. Failure does not change the operational repository, lifecycle state, root evaluator, Git refs, publication state, or deployment state.

## Constraints

- The contract records technical roles and observations; it grants no product, engineering, assurance, release, publication, deployment, or adoption authority.
- Historical records remain immutable and visible.
- Compatibility views are read-only, exact, derived from declared evidence, and never represented as complete predecessor validation.
- The contract cannot select a candidate as the root evaluator merely because it contains the successor implementation.
- This requirement does not prescribe the lifecycle vocabulary source of truth tracked by #103, the shared compatibility-view implementation tracked by #104, or production role-specific commands tracked by #109.

## Acceptance examples

### Example: normal behavior

**Given** a released N-1 evaluator and a candidate N that introduces a release-record field N-1 cannot create

**When** candidate N enters release qualification

**Then** one validated migration contract names the predecessor preparation stage, successor complete-validation stage, any exact compatibility view, simulated rejection/replacement path, publication and rendering plans, and a separate post-publication adoption exit without granting candidate N root authority.

### Example: failure behavior

**Given** a migration script invokes candidate N as the root evaluator or skips predecessor-incompatible rejected history through an unbound omission

**When** the migration contract is validated

**Then** validation fails before qualification and reports the exact undeclared role, view, or stage.

## Open decisions

The technical and security owners must accept the contract schema, role model, and staged isolation design in `SPEC-REB-008`, `ARCH-REB-007`, and `ADR-REB-007` before this requirement can become approved.
