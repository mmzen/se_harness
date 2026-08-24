+++
id = "ARCH-VSP-002"
type = "architecture"
title = "State-aware verification provenance boundary"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
addresses = ["REQ-VSP-008"]
conforms_to = ["SPEC-VSP-002"]

[decision_assessment]
outcome = "adr_required"
triggers = ["data-ownership-or-persistence", "cross-cutting-policy"]
rationale = "The correction assigns durable meanings to preparation, verification, and supersession fields across writer, transition, validation, installed templates, and immutable legacy history; choosing that compatibility model is a cross-cutting provenance decision."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:35:25Z"
decided_by = "technical-owner"
+++

# Architecture: State-aware verification provenance boundary

## Context and scope

The current writer and transition mutator already model preparation and supersession as separate events, but the packaged validator still applies the older `verified_at` capture requirement to every superseded record. The architecture establishes one state-aware provenance boundary that supports current records without rewriting legacy history.

## Components and responsibilities

- `capture-verification` owns current preparation fields and continues to omit assurance-decision fields.
- The lifecycle transition mutator owns status-specific decision fields and never converts one decision type into another.
- The packaged managed validator classifies the record generation from preparation-field presence and enforces the corresponding lifecycle shape.
- Direct validation, transition final-graph validation, preflight, dashboard, and installed repositories consume the same packaged validator implementation.
- Verification tests exercise both current end-to-end commands and legacy immutable fixtures.
- Managed templates and repository-owned reference documentation explain the field meanings without changing decision authority.

## Dependency direction

The preparation writer and transition mutator produce authored metadata. The packaged validator reads that metadata and never feeds inferred state back into it. Workflow planning depends on successful validation of the proposed final graph. Inspection and presentation consume the validated graph and grant no authority.

## Data and control flow

Clean candidate -> preparation fields -> ready VREC -> explicit assurance supersession decision -> transition-only fields and event -> candidate validator -> historical inspection projection. Legacy VRECs enter only at the validator boundary and are never passed through a migration writer.

## Trust boundaries

Artifact bytes, lifecycle events, timestamps, actor names, relations, evidence paths, and successor records are untrusted. The explicit assurance decision remains the only authority input. Compatibility classification uses field presence only to select validation semantics; it does not grant authority.

## Required patterns

- Separate preparation facts from assurance decisions for current records.
- Validate each terminal shape by both lifecycle state and provenance generation.
- Preserve legacy `verified_at` capture metadata without renaming or rewriting it.
- Validate proposed transition output with the same packaged validator used by direct validation.
- Keep the released root copy immutable during candidate development.
- Retain atomic no-write behavior on every failed plan or apply.

## Prohibited patterns

- Fabricating `verified_at` or `verified_by` to make supersession pass.
- Treating supersession as verification or rejection.
- Globally making verification fields optional for verified current records.
- Editing concrete historical VRECs as part of the behavior fix.
- Maintaining separate status rules in transition and direct-validation paths.
- Overwriting the installed root validator outside a governed release upgrade.

## Quality attributes

Historical truth, lifecycle correctness, backward compatibility, deterministic validation, least authority, and atomic failure take priority over uniform field presence.

## Conformance checks

Conformance requires a current capture-to-supersession end-to-end pass, direct validator matrices for current and legacy shapes, unchanged rejection and verified transitions, installed-template parity, full regression, formal graph validation, released-root health, and exact diff review.

## Related ADRs

`ADR-VSP-002` selects state-aware dual-generation validation rather than fabricated verification or historical migration.
