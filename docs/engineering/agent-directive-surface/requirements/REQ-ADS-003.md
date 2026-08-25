+++
id = "REQ-ADS-003"
type = "requirement"
title = "The phase reading manifest and a generated operating card are the mandatory read"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a phase-appropriate preflight runs, THE SYSTEM SHALL emit the complete mandatory reading set for that phase, and the managed router SHALL name that manifest plus one contract-generated operating card of at most 3072 bytes as the reading an agent must complete before acting; other routed policies SHALL be reference material."
verification_method = "automated-test-and-manual-review"
[relations]
derives_from = ["CAP-ADS-001"]
+++

# Requirement: The phase reading manifest and a generated operating card are the mandatory read

## Rationale

"Read `ENGINEERING_HARNESS.md` before engineering work" fans out to six routed
documents and two JSON contracts, about 27k tokens, before the work-order
manifest. Most of it explains contracts the evaluator already enforces and
declares the JSON authoritative if they differ. Reading is unverifiable; an
agent either spends a fifth of its context or quotes rules it never read.
Preflight already emits a phase-specific manifest; the router should trust it.

## Preconditions and trigger

`harnessctl preflight --phase start|review` on a selected work order, and
rendering of the managed router by the installer.

## Required response

- The preflight reading manifest is complete for the phase: router, operating
  card, the selected work order and its governing chain, and any owner-region
  command file the phase names.
- The installer renders `docs/engineering/OPERATING_CARD.md` from
  `WORKFLOW.json` and `QUALITY_GATES.json`: state table, permitted transitions,
  the nine restitution headings in order, the stop conditions, and the
  managed trap list. It is a managed file, at most 3072 bytes, and regenerated
  on upgrade.
- The router's reading instruction names the manifest and the card, and labels
  `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, and
  `TRACEABILITY.md` as reference for humans and for the tool.

## Failure and boundary behavior

A card that exceeds 3072 bytes or drifts from its source contracts fails the
installer's own conformance test. The card carries no rule that is not in a
contract; it is derived content.

## Constraints

The card is a rendering, not a policy owner. `HRN-004` is unchanged: only
`harnessctl` computes legality.

## Acceptance examples

### Example: normal behavior

**Given** a standard installation

**When** `preflight --phase start` runs for an approved work order

**Then** the manifest lists the router, the card, and the governing chain, and
the card's byte size is at most 3072.

### Example: failure behavior

**Given** a `WORKFLOW.json` with one added transition

**When** the card is not regenerated

**Then** the conformance test fails naming the missing transition.

## Open decisions

None.
