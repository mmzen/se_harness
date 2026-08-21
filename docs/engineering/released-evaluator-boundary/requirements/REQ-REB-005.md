+++
id = "REQ-REB-005"
type = "requirement"
title = "Separate evaluator upgrades from product releases"
status = "approved"
owners = ["requirements-steward", "repository-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN a repository selects a newer released evaluator, THE SYSTEM SHALL require a separately governed standard-root upgrade after immutable publication and SHALL NOT infer that upgrade authority from product implementation or release authorization."
verification_method = "policy-validation-and-human-review"

[relations]
derives_from = ["CAP-REB-001"]
+++

# Requirement: Separate evaluator upgrades from product releases

## Rationale

Coupling product release, evaluator adoption, root migration, and publication created the circular dependency described in the RCA. Separate work and evidence keep the old evaluator authoritative until the new published evaluator is deliberately adopted.

## Preconditions and trigger

A target evaluator version has been immutably published and maintainers propose changing the version or distribution identity recorded by the standard root.

## Required response

- Select a bounded evaluator-upgrade work order with explicit prior and target identities.
- Use the current evaluator for start preflight and an external exact target evaluator for the reviewed upgrade transaction.
- Retain plan, digest, origin, rollback, no-op replay, and post-upgrade validation evidence.
- Keep product implementation, release decision, external publication, and root adoption as separately authorized events.
- Model any unavoidable dependency and sequencing explicitly rather than relying on conversational intent.

## Failure and boundary behavior

An unpublished target, local candidate wheel, combined unbounded work order, missing old-root authority, or ambiguous sequencing stops upgrade application. Product release state remains unchanged.

## Constraints

- A separately published evaluator may be the product of an earlier release, but its later adoption is still separate governed work.
- This requirement does not mandate a particular branch naming convention or hosting workflow.

## Acceptance examples

### Example: normal behavior

**Given** version N+1 is publicly immutable and product release work is complete

**When** maintainers adopt N+1 for the root

**Then** a distinct approved upgrade work order governs plan, apply, and evidence.

### Example: failure behavior

**Given** one work order attempts to build version N+1 and make that same unpublished code the root evaluator

**When** readiness is assessed

**Then** the work is rejected as a circular authority sequence.

## Open decisions

No product decision remains open; the exact inspection heuristics for detecting mixed scope are specified by `SPEC-REB-002`.
