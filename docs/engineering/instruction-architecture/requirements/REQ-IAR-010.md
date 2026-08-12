+++
id = "REQ-IAR-010"
type = "requirement"
title = "Separate router invariants from procedural workflow"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN the managed harness contract presents verification and release guidance, THE SYSTEM SHALL retain non-waivable provenance and authority invariants while routing ordered lifecycle procedure to the focused policy modules without duplicating that procedure."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Separate router invariants from procedural workflow

## Rationale

`ENGINEERING_HARNESS.md` is the single managed contract and router, while `WORKFLOW.md` owns the ordered lifecycle. Repeating the verification and release sequence in both files increases reading cost, creates a synchronization obligation, and can introduce subtle ambiguity without strengthening enforcement.

## Preconditions and trigger

The standard harness is installed or upgraded and an actor reaches the commit-bound verification and release section of the managed router.

## Required response

- The router preserves the non-waivable facts that verification and release records bind an exact candidate commit, must reside in later governance commits, and cannot be prepared as an exercise of accountable authority.
- The router directly sends actors to `WORKFLOW.md`, `QUALITY_GATES.md`, `TRACEABILITY.md`, and `DECISION_RIGHTS.md` for their respective procedure, gate, provenance, and authority responsibilities.
- `WORKFLOW.md` remains the focused owner of the ordered candidate, verification-capture, assurance-transition, release-preparation, release-transition, tagging, and publication sequence.
- The router does not repeat command ordering, aggregate argument instructions, or lifecycle-transition procedure already maintained in `WORKFLOW.md`.
- Fresh installations, safe upgrades, and the self-hosted repository expose the same managed wording and ownership boundary.

## Failure and boundary behavior

- A customized or ambiguous managed router is preserved and reported through the existing fail-closed upgrade contract; it is not overwritten to enforce this refinement.
- Removing procedural duplication must not remove a provenance invariant, weaken a decision right, change a lifecycle rule, or authorize an external action.
- Instructions remain guidance. Managed integrity, preflight, validation, CI, and accountable review remain the enforcement and decision boundaries.

## Constraints

- Preserve the one-router, focused-policy architecture established by `ADR-IAR-001`.
- Do not merge focused policies into `ENGINEERING_HARNESS.md` or make the owner-controlled engineering README authoritative.
- Do not change the behavior of `capture-verification`, `prepare-release`, verification transitions, release transitions, tagging, publication, or deployment.

## Acceptance examples

### Example: an agent needs the release sequence

**Given** the agent has read `ENGINEERING_HARNESS.md`

**When** the agent reaches commit-bound verification and release guidance

**Then** the router states the binding and authority invariants and directs the agent to the focused policies for the exact sequence.

### Example: a managed router was customized

**Given** a target repository's managed router differs from its recorded managed content

**When** the harness upgrade is planned

**Then** the existing conflict behavior preserves the file and makes no partial write.

## Open decisions

The exact concise wording may be refined during implementation if it preserves every required invariant and responsibility boundary above.
