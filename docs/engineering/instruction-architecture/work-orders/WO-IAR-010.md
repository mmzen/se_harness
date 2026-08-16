+++
id = "WO-IAR-010"
type = "work_order"
title = "Correct temporal reassessment finding semantics"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
implements = ["REQ-IAR-018"]
specifications = ["SPEC-IAR-010"]
architecture = ["ARCH-IAR-010", "ADR-IAR-010"]
verification = ["VER-IAR-010"]
+++

# Work Order: Correct temporal reassessment finding semantics

## Lifecycle and authorization

The repository owner instructed creation of a separate branch and implementation of the reviewed Phase 1 correction on 2026-08-16. That instruction approves `REQ-IAR-018`, `SPEC-IAR-010`, `ARCH-IAR-010`, `ADR-IAR-010`, `VER-IAR-010`, and this bounded work order. The bounded implementation and retained evidence are complete, so the work order is now `implemented`. Evidence is retained at `docs/engineering/instruction-architecture/evidence/WO-IAR-010-verification.md`. This state records completed work, not independent verification, and does not authorize a commit, verification transition, push, pull request, release, publication, or deployment.

## Objective

Make the existing `W-HEX-003` observation represent a meaningful reassessment boundary by considering artifact role, lifecycle, declared relation type, and relation authority before comparing dates.

## In scope

- Add the exact fail-closed predicate from `SPEC-IAR-010` to the shared Harness Explorer finding producer.
- Preserve the existing rule ID and inspection suggestion while adding relation-specific evidence and bumping the rules version.
- Add controlled positive and negative tests across types, lifecycles, authorities, relations, and dates.
- Synchronize root and canonical generator sources, package data, and managed integrity metadata through the supported process.
- Add only concise documentation needed to keep the inspection rule description accurate.
- Retain work-order-keyed evidence and stop at an uncommitted candidate.

## Out of scope

Fixing the three architecture maintenance observations; superseding verification records; disposing draft release or operating contracts; adding provenance findings; changing validator rules; changing the suggestion catalog; adding configuration; dashboard UI redesign; governor reconciliation; version changes; commit, push, pull request, release, publication, or deployment.

## Authorized decision envelope

Implementation may choose immutable data structures, helper names, exact internal iteration, and focused fixture organization. It may not broaden the relation table, add a fallback heuristic, change another finding, reinterpret provenance, move trigger logic into inspection, or mutate artifacts automatically.

## Expected change surface

- Root and canonical `scripts/generate_harness_dashboard.py`.
- Focused dashboard/inspection, parity, integrity, package, and documentation tests as required.
- Concise rule documentation if current text would become inaccurate.
- `.engineering-harness.lock`, this domain index, and `WO-IAR-010` evidence.

## Implementation plan

1. Validate the approved packet and pass start preflight.
2. Capture the pre-change rule breakdown and add failing focused tests.
3. Implement the typed predicate in the shared producer and mirror the canonical source.
4. Synchronize managed integrity metadata through the supported managed transaction.
5. Run `VER-IAR-010`, retain exact evidence, mark implementation artifacts complete, and stop for candidate-commit authority.

## Stop and escalate conditions

Stop if the correction requires a new provenance rule, a validator behavior change, repository-configurable policy, a public schema break, historical artifact edits, root governor reconciliation, or authority beyond this work order.
