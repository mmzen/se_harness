+++
id = "ADR-IAR-006"
type = "adr"
title = "Put the authoritative artifact catalog in traceability policy"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
decides = ["ARCH-IAR-006"]
+++

# ADR: Put the authoritative artifact catalog in traceability policy

## Status

Accepted on 2026-08-15 through the repository owner's instruction `ok go for implementation`.

## Context

SE Harness exposes twelve canonical formal artifact types, but their meaning and applicability are distributed across managed policies, human notes, templates, and executable checks. Adding guidance in every location would improve local discoverability while making future inconsistency more likely. The instruction architecture therefore needs one normative owner with thin routes and explanations elsewhere.

## Decision drivers

- Give humans and coding agents one answer for artifact purpose and applicability.
- Preserve the single managed router and focused-policy design.
- Keep lifecycle procedure, decision rights, type locations, and progressive explanation in their existing owners.
- Make drift from the executable type registry detectable.
- Avoid generating ceremonial artifacts or hiding conditionality.
- Preserve safe installation, upgrades, packaging, and historical records.

## Considered options

1. **Create a new managed `ARTIFACT_MODEL.md`.** Clear naming, but adds another policy module and routing destination with substantial overlap with traceability.
2. **Make `docs/engineering/templates/README.md` authoritative.** Convenient during authoring, but conflates policy with scaffolding mechanics and makes template text a decision source.
3. **Make the human overview or UML note authoritative.** Accessible, but violates the existing boundary that notes are non-authoritative progressive explanations.
4. **Put the catalog in `TRACEABILITY.md` and cross-reference it.** Extends the existing owner of artifact relations and coverage while keeping one router and focused supporting documents.
5. **Encode the catalog only in Python and generate documentation.** Strong structural consistency, but turns implementation into product authority and makes semantic review of generated policy indirect.

## Decision

Choose option 4. `TRACEABILITY.md` owns the normative artifact-applicability catalog. `ENGINEERING_HARNESS.md` routes agents to it; notes and templates cross-reference it and retain their current explanatory or authoring responsibilities.

Keep the catalog human-authored and accountably reviewed. Add a deterministic structural test that compares catalog membership with the canonical artifact registry, but do not treat the registry or test as semantic authority.

As part of the same consistency boundary, correct the validator so a work order may omit `architecture` when no active architecture addresses its requirements. Continue to fail omitted applicable architecture and missing required ADR coverage.

## Consequences

- `TRACEABILITY.md` becomes slightly longer but remains focused on artifact meaning, coverage, and relations.
- Humans gain a progressive route from overview to normative detail without a duplicated full catalog.
- Coding agents receive one explicit managed destination.
- Registry changes require an accompanying catalog change and test update.
- Templates can remain concise and type-specific.
- Work orders for routine changes no longer need nominal architecture solely to satisfy schema.
- Validator, preflight, policy, templates, tests, package data, and lock must change consistently.
- Semantic catalog quality still requires accountable review; structural tests cannot assess prose correctness.

## Rejected implications

This decision does not make every artifact mandatory for every change, create a new artifact type, infer significance, authorize automated artifact generation, move lifecycle procedure out of `WORKFLOW.md`, or turn notes and templates into formal authority.

## Validation

Execute `VER-IAR-006`, including catalog/registry parity, routing and cross-reference review, all work-order architecture applicability cases, managed upgrade and package parity, security-shaped inputs, dual-runtime checks, and the full regression suite.
