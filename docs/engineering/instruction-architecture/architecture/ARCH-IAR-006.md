+++
id = "ARCH-IAR-006"
type = "architecture"
title = "Single-source artifact applicability policy"
status = "implemented"
owners = ["technical-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
addresses = ["REQ-IAR-014"]
conforms_to = ["SPEC-IAR-006"]

[decision_assessment]
outcome = "adr_required"
triggers = ["public-interface-or-protocol", "cross-cutting-policy", "difficult-to-reverse", "material-alternatives"]
rationale = "Artifact applicability is a public, cross-cutting governance contract consumed by humans, coding agents, templates, validation, preflight, and upgrades. Choosing its authoritative owner and consistency boundary has material alternatives and affects every future artifact packet."
assessed_by = "technical-owner"
+++

# Architecture: Single-source artifact applicability policy

## Context

The current instruction architecture correctly separates the router, focused policy, human notes, templates, and executable checks, but artifact definitions and applicability are spread across those layers. The architecture needs one normative owner while preserving progressive explanation and type-specific authoring help.

## Components and responsibilities

- **Managed router:** directs coding agents to the focused owner for artifact purpose, applicability, and relations; it does not copy the catalog.
- **Traceability policy:** owns the complete normative catalog and the distinction between graph coverage, reuse, and new artifact creation.
- **Workflow and decision-rights policies:** retain lifecycle procedure and accountable roles; the catalog references rather than duplicates them.
- **Human notes:** provide progressive explanation and diagrams, then link to the authoritative catalog.
- **Template index and type templates:** provide paths, fields, and authoring prompts without redefining applicability.
- **Artifact registry:** remains the executable canonical type set.
- **Validator and preflight:** enforce catalog-compatible structural rules, especially conditional architecture selection.
- **Consistency tests:** compare registry membership, catalog entries, managed copies, package data, and routing expectations.

## Dependency direction

```text
ENGINEERING_HARNESS.md --------routes-------> TRACEABILITY.md catalog
       human notes --------cross-reference--->       |
       templates ----------authoring aid------>       |
                                                       v
artifact_layout_registry.py ----type set----> consistency tests
                                                       |
                                                       v
                                        validator + preflight behavior
```

The catalog owns policy meaning. Registry and executable checks prove supported structure; they do not become product authority.

## Required patterns

- One catalog entry per canonical standard artifact type.
- Direct routing from the managed agent contract.
- Progressive human explanation by cross-reference.
- Explicit applicability, omission, and reuse language.
- Conditional work-order architecture relation derived from typed `addresses` edges.
- Machine checks for membership and managed-distribution parity.
- Historical artifact preservation and transactional managed-file upgrades.

## Prohibited patterns

- A second authoritative catalog in notes, templates, source code, or README.
- Treating template presence or validator implementation as policy authority.
- Requiring one new artifact of every type per work order.
- Fabricating architecture or ADRs to satisfy schema cardinality.
- Allowing a work order to omit active applicable architecture.
- Generating normative prose from source without accountable review.
- Rewriting historical formal artifacts during upgrade.

## Control flow

1. An operator or agent reaches the managed router.
2. The router sends artifact-purpose and applicability questions to the traceability catalog.
3. The author determines whether existing active artifacts cover the scope or new definitions are needed.
4. The work order selects complete requirement, specification, verification, and conditionally applicable architecture/ADR coverage.
5. Validator and preflight evaluate the declared graph against the same structural boundary.
6. CI tests registry/catalog completeness and managed/package parity.
7. Accountable humans retain semantic approval and lifecycle authority.

## Trust and authority boundaries

Repository Markdown, TOML, relation values, paths, and type names are untrusted inputs. Structural automation can prove that a type is cataloged and a declared relation is coherent; it cannot prove that a definition is meaningful, that reuse is honest, or that an omitted architecture decision is insignificant.

## Quality attributes

Discoverability, single-source authority, progressive readability, deterministic enforcement, low ceremonial overhead, safe upgrades, historical stability, and consistent Python 3.11+ behavior.

## Conformance checks

Exercise exact type-set coverage, duplicate/missing/unknown catalog entries, agent routing, relative human cross-references, template wording, routine work without architecture, applicable architecture omission, irrelevant selection, ADR applicability, root/template/package parity, customized upgrade protection, deterministic diagnostics, and full regression.

## Related ADR

`ADR-IAR-006` decides the authoritative owner and consistency strategy for this architecture.
