+++
id = "SPEC-IAR-005"
type = "specification"
title = "Typed architecture traceability and migration contract"
status = "implemented"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
specifies = ["REQ-IAR-013"]
+++

# Specification: Typed architecture traceability and migration contract

## Scope

Replace the polymorphic architecture `constrains` convention for new work with two typed relations, enforce their semantic triangle through validation and preflight, expose direct and transitive traceability in Harness Explorer, and retain bounded compatibility for completed historical architecture.

## Metadata contract

A compliant new architecture declares:

```toml
[relations]
addresses = ["REQ-ORD-004", "REQ-ORD-007"]
conforms_to = ["SPEC-ORD-002"]
```

- `addresses` is a duplicate-free, non-empty list of requirement IDs. It identifies only requirements that materially drive architecture.
- `conforms_to` is a duplicate-free, non-empty list of specification IDs. It identifies detailed contracts relevant to the architecture.
- Neither relation is a claim that architecture or documentation alone satisfies delivered behavior.
- The relation name is interpreted in the source artifact's type context; the existing verification-record `conforms_to` relation retains its current verification-contract meaning.

## Coherence rules

1. Every `addresses` target exists and has type `requirement`.
2. Every `conforms_to` target exists and has type `specification`.
3. Every active addressed requirement is included in the `specifies` relation of at least one conforming active specification.
4. A conforming specification may specify additional requirements that the architecture does not address.
5. `addresses` does not replace requirement coverage by specification or verification.
6. `conforms_to` does not replace the direct record of an architecturally significant requirement driver.
7. ADR coverage remains `ADR.decides -> ARCH` and is governed independently by the architecture's `decision_assessment`.

## Work-order and preflight rules

1. Existing G1 behavior remains: every selected active requirement needs selected active specification and verification coverage.
2. Preflight no longer treats the union of a polymorphic `constrains` relation as architecture coverage for every implemented requirement.
3. Every selected typed architecture must share at least one `conforms_to` specification with the work order's selected specifications.
4. If an active architecture's `addresses` relation intersects the work order's implemented requirements, that architecture is applicable and must be selected.
5. A routine requirement with no active `addresses` edge does not acquire an artificial architecture-coverage obligation.
6. Every selected architecture still undergoes decision-assessment and conditional ADR coverage checks.
7. A selected ADR must decide at least one selected architecture, as under the existing contract.
8. Text and JSON preflight output distinguish missing architecture selection, wrong relation types, incoherent triangles, specification irrelevance, and ADR coverage.

## Validation contract

- Central relation validation knows the allowed target types for `architecture.addresses`, `architecture.conforms_to`, and compatibility `architecture.constrains`.
- New or ongoing architecture in `draft`, `approved`, or `in_progress` must declare both typed relations. A dual declaration containing legacy `constrains` is accepted during bootstrap only when its targets are consistent with the corresponding typed relation and produces a deprecation advisory.
- Active architecture relation coherence is evaluated deterministically from formal metadata only.
- Unknown relations remain subject to the repository's existing extensibility policy; no unrelated relation namespace is closed by this change.
- Diagnostic ordering, text, and JSON serialization remain deterministic and treat artifact values as untrusted data.

## Direct and transitive graph projection

Explorer records declared edges with `authority = "declared"` and may derive:

```text
ARCH --conforms_to--> SPEC --specifies--> REQ
```

as a non-authoritative `conforms_transitively_to_requirement` projection. Direct `ARCH.addresses -> REQ` remains distinguishable. Explorer reports:

- addressed requirements;
- conforming specifications;
- transitively specified requirements;
- addressed requirements missing from the transitive set;
- legacy relation class and migration state;
- work-order architecture applicability anomalies.

Derived edges aid explanation and impact analysis but do not become formal relations or authority.

## Migration and compatibility

- Fresh installations and upgraded canonical templates use only `addresses` and `conforms_to`.
- Installation and upgrade never edit repository-owned formal architecture artifacts.
- A completed architecture in `implemented`, `verified`, or `released` with only `constrains` enters the compatibility classifier:
  - all requirement targets: `legacy_requirement_trace`;
  - all specification targets: `legacy_specification_trace`;
  - mixed or non-architecture targets: `legacy_ambiguous`, which is an error.
- Compatibility classification may support old preflight behavior and derived Explorer views, but it never asserts which requirements were architecturally significant.
- A new or ongoing architecture cannot use legacy-only `constrains`.
- A dual-declared bootstrap artifact is valid only when each legacy target appears in its matching typed relation; it receives a visible deprecation advisory.
- Historical completed artifacts are migrated only through separately authorized governance work. New architectural choices require new typed architecture rather than semantic rewriting of completed records.
- Removal of compatibility behavior requires a later governed release supported by migration evidence.

## Managed content

Update the architecture template, traceability and quality-gate policy, preflight reading model, validator, Explorer generator/view, candidate checks, acceptance tests, and schema-2 lock through the supported transactional upgrade. Keep the managed router focused on routing and authority invariants.

## Security and authority boundaries

Relation names, arrays, IDs, paths, and artifact content are untrusted. They are parsed without execution or shell interpolation. Automation validates declared type and graph consistency but cannot determine whether a requirement is architecturally significant, approve a migration, rewrite historical artifacts, or grant work authority.

## Explicitly unspecified decisions

Stable diagnostic numbers, internal registry structure, visual styling, and the duration label of the compatibility window are delegated to implementation. They must not change the typed semantics, applicability rules, or no-rewrite boundary.
