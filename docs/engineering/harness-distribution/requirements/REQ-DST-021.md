+++
id = "REQ-DST-021"
type = "requirement"
title = "Provide layered conceptual and operational notes"
status = "approved"
owners = ["product-owner", "documentation-owner", "quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"
statement = "WHEN a human reader consults docs/notes, THE SYSTEM SHALL provide SE-Harness-specific overview, conceptual data-model, and operational-phasing guides that reflect the current implementation at their declared expertise levels."
verification_method = "automated-inspection-and-manual-review"

[relations]
derives_from = ["CAP-DST-001"]
+++

# Requirement: Provide layered conceptual and operational notes

## Rationale

The existing notes include useful explanations but contain Mokiterions-specific material, the legacy 0.2.1 architecture relation, and duplicated policy. A progressive documentation path needs concise SE Harness material that remains subordinate to managed policy.

## Required response

- Provide a 4/10 Tier-0 overview covering purpose, main concepts, workflow fit, guarantees, and human or repository-owned control.
- Provide a 6/10 simplified UML-style model covering intent, requirements, specifications, architecture decisions, work orders, evidence, commits, validation, verification records, release contracts, and release decisions.
- Provide a 6/10 operational phasing guide showing when artifacts, implementation, checks, evidence, commits, accountable transitions, and release actions occur.
- Use diagrams and concrete paths where they materially improve comprehension.
- Identify non-authoritative notes explicitly and link authoritative policy instead of copying it wholesale.

## Failure and boundary behavior

No note may describe Mokiterions as the current repository, treat legacy `ARCH.constrains` as the current authoring model, make the validator override policy, or collapse automated checks into accountable verification.

## Constraints

The notes explain current behavior without becoming formal artifacts or installed managed policy. Historical formal artifacts remain unchanged even when they retain compatibility-era relations.

## Acceptance examples

A 4/10 reader can explain why the harness exists, and a 6/10 reader can identify the major entities, relation directions, phase boundaries, and human decisions without reading Python source.

## Open decisions

None when approved.
