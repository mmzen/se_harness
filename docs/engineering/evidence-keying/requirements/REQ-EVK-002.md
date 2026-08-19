+++
id = "REQ-EVK-002"
type = "requirement"
title = "Keep evidence attribution consistent across harness surfaces"
status = "approved"
owners = ["quality-owner", "engineering-owner"]
created = "2026-08-19"
updated = "2026-08-19"
statement = "WHEN evidence attribution is used by capture-verification, formal validation, inspection, or Harness Explorer, THE SYSTEM SHALL apply one deterministic contract and produce equivalent work-order associations for equivalent paths."
verification_method = "automated-test-and-review"

[relations]
derives_from = ["CAP-EVK-001"]
+++

# Requirement: Keep evidence attribution consistent across harness surfaces

## Rationale

Record preparation, repository validation, and derived review views cannot safely disagree about whether the same retained path is keyed. A record that one command prepares must not fail or appear incomplete solely because another surface implements a different path-position assumption.

## Preconditions and trigger

One of the four named harness surfaces assesses the same normalized path and work-order ID under the same repository state.

## Required response

- Aggregate `capture-verification` accepts a selected work order only when at least one supplied safe path contains its exact key.
- Formal validation applies the same rule to authored aggregate verification records.
- Inspection and Explorer use the same work-order association map for missing-evidence findings and readiness evidence.
- Equivalent paths produce equivalent key sets regardless of discovery or input order.

## Failure and boundary behavior

Unkeyed aggregate evidence remains blocking during capture and formal validation. An implemented work order without keyed evidence retains the existing derived warning. No surface may silently select a different component from the same path.

## Constraints

- Do not turn inspection or Explorer into formal authority.
- Do not change VREC lifecycle or evidence-content adequacy decisions.
- Do not use a health score as a substitute for exact findings.

## Acceptance examples

### Example: equivalent positive assessment

**Given** an aggregate VREC names `evidence/WO-ABC-001/check.md`,

**When** capture, validation, inspection, and Explorer assess the path,

**Then** all four associate it with `WO-ABC-001`.

### Example: equivalent negative assessment

**Given** a retained path contains no supported work-order key,

**When** each surface assesses it,

**Then** none associates it with a work order.

## Open decisions

None when approved.
