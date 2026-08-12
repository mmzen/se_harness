+++
id = "REQ-IAR-012"
type = "requirement"
title = "Require explicit architecture-decision applicability"
status = "implemented"
owners = ["requirements-steward", "technical-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN architecture is defined or selected for implementation, THE SYSTEM SHALL require an explicit accountable assessment of significant decision applicability and SHALL require ADR coverage for every architecture assessed as containing a significant decision."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Require explicit architecture-decision applicability

## Rationale

The current preflight rejects a work order with no selected ADR, but it does not require an architecture author to assess significance, does not explain when an ADR is necessary, and does not verify ADR coverage independently for every selected architecture. This leaves authoring to agent judgment while encouraging ceremonial ADRs for routine work.

## Required response

- Every architecture artifact records exactly one structured decision assessment: `adr_required` or `no_significant_decision`.
- `adr_required` is selected when the architecture introduces or materially changes at least one significant-decision trigger and is covered by at least one active ADR whose `decides` relation targets that architecture.
- `no_significant_decision` requires a non-empty rationale and accountable technical assessor and permits no ADR only when every trigger is false.
- Every selected architecture is evaluated separately. An ADR may decide one architecture or a coherent decision spanning several architectures and requirements; no one-ADR-per-requirement rule is imposed.
- Artifact validation, preflight, required CI, and Harness Explorer report missing, contradictory, or uncovered assessments consistently.
- Existing completed architecture artifacts in `implemented`, `verified`, or `released` state without the new assessment remain compatible during a defined migration window but produce a visible advisory and require an already-active deciding ADR. Architecture in `draft`, `approved`, or `in_progress` state must comply.

## Significant-decision triggers

The controlled trigger vocabulary covers:

- `system-boundary`
- `responsibility-or-dependency-direction`
- `public-interface-or-protocol`
- `data-ownership-or-persistence`
- `security-privacy-or-trust-boundary`
- `deployment-or-operating-model`
- `concurrency-consistency-reliability-or-failure-strategy`
- `technology-framework-vendor-or-external-service`
- `material-performance-scalability-or-cost-tradeoff`
- `cross-cutting-policy`
- `difficult-to-reverse`
- `material-alternatives`

Initial software design normally activates one or more triggers, but the rule remains evidence-based rather than being hard-coded to project age.

## Failure and boundary behavior

- Missing assessment blocks approval of new or ongoing architecture and blocks work-order start/review readiness, except for the bounded completed-state legacy rule.
- `adr_required` without an active deciding ADR blocks readiness.
- `no_significant_decision` with a non-empty trigger, empty rationale, or missing accountable assessor blocks readiness.
- An ADR selected by a work order but not deciding any selected architecture remains invalid.
- Automation reports contradictions but does not decide whether free-form prose is architecturally significant or approve a no-ADR rationale.

## Constraints

- Preserve typed artifact identity and relation authority.
- Do not require one ADR per requirement, specification, work order, or architecture when no significant decision exists.
- Do not allow an absent ADR or blank assessment to mean not applicable.
- Do not auto-generate or auto-approve ADRs from source code or natural-language inference.
- Do not materially rewrite a completed legacy architecture to exploit the migration exception; introduce a new draft architecture and assessment for a new decision.

## Acceptance examples

### Example: first system design

**Given** an architecture selects component boundaries, dependency direction, and persistence ownership

**When** decision applicability is assessed

**Then** the corresponding triggers require an ADR and preflight fails until an active deciding ADR is selected.

### Example: routine implementation

**Given** a change applies an existing approved architecture without changing boundaries, interfaces, trust, persistence, technology, or material trade-offs

**When** the technical owner records `no_significant_decision` with rationale and no triggers

**Then** the work order may proceed without creating a ceremonial ADR.

### Example: one coherent decision spans requirements

**Given** several requirements share one persistence and consistency choice

**When** one ADR records that coherent trade-off and decides the applicable architecture

**Then** no duplicate ADR per requirement is required.
