+++
id = "ADR-IAR-002"
type = "adr"
title = "Keep invariant summaries in the router and procedure in focused policy"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
decides = ["ARCH-IAR-002"]
+++

# ADR: Keep invariant summaries in the router and procedure in focused policy

## Status

Accepted on 2026-08-12 through the repository owner's instruction `ok for implementation`.

## Context

The router's commit-bound verification and release paragraph currently repeats part of the ordered procedure already maintained in `WORKFLOW.md`. The router must remain useful and safe when first read, but duplication creates drift risk and blurs the modular-policy boundary established by `ADR-IAR-001`.

## Decision drivers

- Preserve immediate visibility of non-waivable provenance and authority constraints.
- Give ordered lifecycle procedure one focused, reviewable owner.
- Minimize synchronization obligations between fully managed files.
- Preserve the one-router architecture and direct discoverability of policy modules.
- Avoid changing runtime behavior or historical governance facts.

## Considered options

1. **Retain both procedural descriptions.** Simple initially, but preserves drift and ambiguity.
2. **Remove the router section entirely.** Eliminates duplication, but hides critical commit and authority invariants from the central contract.
3. **Move all workflow policy into the router.** Creates a policy monolith and contradicts the established modular architecture.
4. **Keep stable invariants in the router and ordered procedure in focused modules.** Preserves safety context while establishing a clear responsibility boundary.

## Decision

Choose option 4. The managed router will state the exact-candidate, later-governance-commit, accountable-authority, and no-external-action invariants and route actors to the applicable policies. `WORKFLOW.md` will remain the owner of ordered verification and release procedure. `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and `TRACEABILITY.md` retain their existing specialized responsibilities.

## Consequences

- The primary contract becomes shorter and less likely to drift from workflow procedure.
- Reviewers must assess semantic coverage across the router and its direct policy destinations rather than treating either file in isolation.
- Managed template content and lock metadata change, so safe installation, upgrade, self-hosting parity, and regression evidence are required.
- The architecture does not prevent conceptual overlap where different policies legitimately describe authority, gates, or provenance from their own perspective; it prevents duplicated ordered procedure.

## Validation

Validate required invariant phrases and direct policy routes, absence of the duplicated command-order paragraph, preservation of the detailed workflow, safe managed upgrade behavior, canonical/root/lock parity, and the complete verification contract `VER-IAR-002`.
