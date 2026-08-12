+++
id = "REQ-IAR-013"
type = "requirement"
title = "Distinguish architecture drivers from specification conformance"
status = "implemented"
owners = ["requirements-steward", "technical-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN architecture traceability is authored or evaluated, THE SYSTEM SHALL distinguish the requirements that drive architecture from the specifications to which architecture conforms and SHALL evaluate their typed direct and transitive relationships deterministically."
verification_method = "automated-test-and-inspection"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Distinguish architecture drivers from specification conformance

## Rationale

The current `architecture.constrains` relation is semantically and structurally ambiguous. The canonical template targets a specification, most existing architecture artifacts target requirements, the traceability policy depicts direct requirement coverage, and validation accepts either artifact type. As a result, the graph cannot reliably explain whether an edge records an architectural driver, a detailed contract, or merely historical convention.

Architecture practice needs both forms of traceability. Architecturally significant requirements explain why the architecture has its structure; specifications state the detailed behavior and interfaces the architecture must respect. Replacing requirement traceability with specification traceability would lose the direct rationale, while retaining one polymorphic relation prevents deterministic validation.

## Required response

- Architecture declares architecturally significant requirement drivers through `addresses`.
- Architecture declares applicable detailed behavioral or interface contracts through `conforms_to`.
- `addresses` targets requirements only; `conforms_to` targets specifications only.
- Every addressed requirement is included in the requirements specified by at least one conforming specification, creating a coherent traceability triangle.
- A conforming specification may cover routine requirements that are not architecturally significant; architecture is not linked artificially to every requirement.
- Work-order preflight evaluates specification coverage for all selected requirements and architecture applicability only where declared by the typed graph.
- The graph and Explorer distinguish direct authoritative relations from deterministic transitive projections.
- Existing `constrains` relations remain readable during a bounded compatibility window, with explicit classification and warnings, and are never rewritten automatically.

## Traceability invariant

```text
SPEC --specifies--> REQ
ARCH --addresses--> REQ
ARCH --conforms_to--> SPEC
ADR  --decides----> ARCH
```

For an architecture `A`, every requirement in `A.addresses` must belong to the union of `specifies` targets of the specifications in `A.conforms_to`. The inverse is not required: a specification can define non-architecturally-significant behavior.

## Failure and boundary behavior

- Missing typed relations on a new or ongoing architecture block activation and work-order readiness.
- A wrong target type, unknown target, empty relation, or incoherent triangle is an error.
- A selected architecture unrelated to every selected work-order specification is not applicable and blocks readiness.
- If an active architecture directly addresses a work-order requirement, the work order must select that architecture and any ADR required by its decision assessment.
- Automation does not infer architectural significance from prose, a diff, a specification, or a legacy edge.
- Ambiguous legacy relations that mix requirement and specification targets fail closed.

## Constraints

- Preserve direct requirement rationale rather than replacing it with transitive-only traceability.
- Do not require architecture coverage for every functional or routine requirement.
- Do not interpret architecture alone as satisfying a requirement; implementation and verification remain separate.
- Preserve formal artifact identity, declared relation authority, decision-assessment rules, and work-order scope.
- Preserve historical completed artifacts and captured provenance.

## Acceptance examples

### Example: architecturally significant requirement

**Given** a persistence requirement drives data ownership and consistency boundaries

**When** an architecture addresses that requirement and conforms to its detailed specification

**Then** the graph exposes both the direct driver and the exact governing contract.

### Example: routine behavior

**Given** a specification covers a routine validation rule that does not influence structure

**When** architecture conforms to the specification

**Then** the routine requirement need not be added to `addresses` merely to produce nominal coverage.

### Example: legacy ambiguity

**Given** a historical completed architecture contains `constrains` targets of more than one artifact type

**When** the graph is validated

**Then** automation reports the ambiguity and does not choose a meaning or rewrite the artifact.

## Open decisions

There are no unresolved product decisions in this draft. Diagnostic numbers, internal helper boundaries, and Explorer presentation are delegated to implementation if the semantic and migration contracts remain unchanged.
