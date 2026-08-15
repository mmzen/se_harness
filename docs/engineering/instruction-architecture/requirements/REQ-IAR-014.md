+++
id = "REQ-IAR-014"
type = "requirement"
title = "Provide one authoritative artifact applicability catalog"
status = "implemented"
owners = ["requirements-steward", "repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN a human or coding agent selects, authors, or reviews SE Harness engineering material, THE SYSTEM SHALL provide one authoritative and complete artifact-applicability catalog that defines every standard formal artifact's objective, applicability, omission and reuse rules, accountable owner, and primary traceability relations and SHALL keep executable validation consistent with that catalog."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Provide one authoritative artifact applicability catalog

## Problem

Artifact meaning is currently distributed across the human overview, UML note, workflow, traceability policy, quality gates, type-specific templates, and validator. A reader can find the canonical type names and locations, but cannot consult one authoritative source to determine why each type exists, when its coverage is required, when a new instance is unnecessary, and when omission is valid.

This fragmentation creates two recurring risks. Humans can mistake a reusable upstream artifact for a one-file-per-change quota, while coding agents can infer applicability from templates or validator behavior instead of accountable policy. The known work-order architecture tension demonstrates the second risk: policy says routine requirements must not receive fabricated architecture coverage, while the current validator still requires a non-empty work-order `architecture` relation.

## Required outcome

- One managed authoritative catalog covers every canonical standard formal artifact type registered by the implementation.
- Each entry states the artifact's objective, applicability trigger, valid omission or reuse rule, accountable owner, and primary incoming or outgoing traceability relations.
- The catalog distinguishes required graph coverage from mandatory creation of a new file. Existing active artifacts may be reused when they genuinely cover the new scope.
- Conditional artifacts are explicit. Architecture follows significant requirement drivers; ADRs follow the architecture decision assessment; verification and release records follow candidate and decision phases; release and operating artifacts follow their applicable lifecycle boundary.
- Formal artifacts are distinguished from retained evidence, acceptance scenarios, commits, dashboards, tickets, and other non-authoritative observations.
- The managed router sends agents directly to the catalog for artifact purpose and applicability. Human notes explain progressively and cross-reference the authoritative catalog instead of copying it wholesale.
- Templates remain authoring aids and cannot silently redefine applicability.
- Executable validation and preflight agree with the catalog, including valid work orders whose selected requirements have no applicable architecture.
- A deterministic test fails when the canonical artifact-type registry and catalog coverage diverge.

## Applicability principle

“Required” means that the active graph or lifecycle phase needs valid coverage. It does not mean that every work order creates a fresh instance of every artifact type. Authors must prefer truthful reuse over duplication and truthful omission over ceremonial artifacts.

## Failure behavior

- An unlisted canonical type, duplicate catalog entry, unsupported catalog type, missing applicability statement, or registry/catalog mismatch fails candidate verification.
- If documentation and executable behavior disagree, the change stops rather than describing the executable behavior as authoritative policy.
- Omission of applicable architecture or a required deciding ADR remains an error.
- Absence of architecture for routine requirements with no active `addresses` relation is valid and must not require a placeholder or fabricated architecture.
- Automation does not infer product meaning, architectural significance, accountable ownership, verification, or release authority from prose or file presence.

## Constraints

- Preserve the single managed router and focused-policy architecture.
- Preserve the twelve canonical standard artifact types, their stable IDs, and their existing lifecycle and provenance semantics.
- Do not introduce a one-artifact-per-requirement, per-work-order, or per-release quota.
- Do not make non-authoritative notes or templates the normative source.
- Preserve Python 3.11+ standard-library runtime behavior and deterministic diagnostics.
- Preserve historical artifacts and commit-bound verification or release facts.

## Acceptance examples

### Reusing existing definition

**Given** an approved intent, capability, specification, and verification contract still cover a new bounded requirement change

**When** a work order selects the relevant active artifacts

**Then** the catalog does not require duplicate upstream files merely because a new work order exists.

### Routine change without architecture

**Given** selected requirements have complete specification and verification coverage and no active architecture addresses them

**When** a work order omits the `architecture` relation

**Then** validation and preflight accept the omission rather than requiring nominal architecture.

### Significant decision

**Given** applicable architecture has `decision_assessment.outcome = "adr_required"`

**When** a work order selects that architecture

**Then** it also selects at least one active ADR that decides the architecture.

### Release boundary

**Given** implementation is complete but no release is being prepared

**When** the candidate is verified

**Then** no release record is required until an accountable release decision is proposed.

## Open decisions

There are no unresolved product decisions in this draft. Exact table layout, test helper structure, and diagnostic identifiers may be selected during implementation if they preserve the approved authority and applicability contract.
