+++
id = "ARCH-IAR-005"
type = "architecture"
title = "Typed requirement-driver and specification-conformance graph"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
addresses = ["REQ-IAR-013"]
conforms_to = ["SPEC-IAR-005"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "The artifact relation vocabulary is a cross-cutting public metadata contract, and the choice between requirement-only, specification-only, and dual typed traceability materially changes validation, preflight, migration, and graph interpretation."
assessed_by = "technical-owner"
+++

# Architecture: Typed requirement-driver and specification-conformance graph

## Context and scope

The graph currently overloads `architecture.constrains`. This architecture separates the reason for a structural choice from the detailed contract it must respect, without claiming that all requirements are architecturally significant.

Before implementation, this artifact briefly carried a current-schema `constrains` bootstrap edge so the approved packet could pass the old preflight. Once the typed validator and preflight existed, implementation removed that bridge. The active artifact now demonstrates the authoritative `addresses` and `conforms_to` model; consistent dual declaration remains covered only as a bounded migration case.

## Components and responsibilities

- **Typed relation contract:** defines direct `addresses` and `conforms_to` semantics and target types.
- **Validator:** verifies type, cardinality, duplicates, existence, triangle coherence, and legacy classification.
- **Preflight:** composes work-order requirements, selected specifications, applicable architectures, decision assessments, and ADRs.
- **Harness Explorer:** preserves declared edges and adds visibly derived transitive projections and anomalies.
- **Managed policies and templates:** guide authors toward architecturally significant requirements rather than nominal all-requirement coverage.
- **Compatibility classifier:** reads historical `constrains` forms without mutating them or inventing significance.

## Dependency direction

Formal artifacts point toward the upstream authority or contract they depend on:

```text
ARCH --addresses--> REQ <--specifies-- SPEC
  |                                   ^
  +-------------conforms_to-----------+
  ^
  |
decides
  |
 ADR
```

The direct requirement edge answers “why did architecture need to change?” The specification edge answers “which exact behavior or interface must this structure respect?”

## Data and control flow

1. Parse artifacts and typed declared relations.
2. Classify architecture relation state as typed, consistent dual-declared, legacy requirement, legacy specification, or ambiguous.
3. Validate relation targets and the typed traceability triangle.
4. For a selected work order, resolve G1 requirement coverage independently.
5. Determine architecture applicability from explicit `addresses` intersections and specification relevance.
6. Apply the existing decision-assessment and ADR coverage model to every selected architecture.
7. Project declared and derived graph states into Explorer without modifying artifacts.

## Trust boundaries

The graph consumes untrusted repository text. Target type is established by the parsed artifact, never by an ID prefix alone. Derived transitive edges are observations, not authority. Automation cannot decide that a routine requirement is an architectural driver or silently convert a historical edge.

## Required patterns

- Direct, typed requirement-driver traceability.
- Direct, typed specification-conformance traceability.
- A coherent but non-symmetric triangle: every addressed requirement is specified through a conforming specification, but not every specified requirement must be addressed.
- Independent G1 definition/verification coverage and G2 architecture/decision coverage.
- Explicit compatibility classes with fail-closed ambiguity.
- One canonical relation implementation shared by validation, preflight, Explorer, templates, and tests.

## Prohibited patterns

- Specification-only traceability that erases the architectural rationale.
- Requirement-only traceability that omits the exact governing contract.
- Forcing architecture edges onto every routine requirement.
- Continuing a polymorphic relation without target-type semantics.
- Treating a transitive projection as a declared relation.
- Rewriting completed repository-owned artifacts during installation or upgrade.

## Quality attributes

Semantic clarity, deterministic validation, explainable impact analysis, low false coverage, backward compatibility, safe adoption, and consistent behavior across Python 3.11+ runtimes.

## Conformance checks

Exercise typed target matrices, triangle subsets, multi-specification and multi-requirement cardinality, routine requirements, work-order relevance, active architecture selection, dual-declared bootstrap behavior, all legacy classes, transactional upgrades, Explorer authority labels, injection-shaped inputs, and dual-runtime regression.

## Related ADRs

- `ADR-IAR-004`: Use explicit conditional ADR applicability.
- `ADR-IAR-005`: Use dual typed architecture traceability with bounded legacy compatibility.
