+++
id = "REQ-WAC-001"
type = "requirement"
title = "Declare commit-bound verification applicability"
status = "implemented"
owners = ["quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"
statement = "WHEN a work order becomes actionable, SE Harness SHALL require an explicit accountable declaration of whether commit-bound verification is required and SHALL expose that declaration during preflight."
verification_method = "validator, preflight, template, and lifecycle tests"

[relations]
derives_from = ["CAP-WAC-001"]
+++

# Requirement: Declare commit-bound verification applicability

## Rationale

The existing `verification` relation identifies implementation evidence contracts; it does not say whether an additional commit-bound VREC is obligatory. Applicability must be stated rather than inferred from an artifact title or lifecycle state.

## Required response

- Represent exactly `required` or `not_required` in structured work-order metadata.
- Require non-empty rationale and accountable decision role fields.
- Reject a malformed declaration.
- Require a valid declaration before start preflight accepts an approved or in-progress work order.
- Display the decision, rationale, and accountable role in start and review preflight.

## Failure and boundary behavior

A selected work order without a valid declaration cannot begin new bounded execution. The tool reports the missing decision but never chooses a default or edits the artifact.

## Constraints

Do not reinterpret `relations.verification`, work-order status, filenames, dates, branches, commit messages, or prose as the applicability decision.

## Acceptance examples

An approved work order declaring `required` passes the new preflight boundary. The same work order with a missing value, unknown value, blank rationale, or blank deciding role fails deterministically.

## Open decisions

None. The accountable declaration model is selected by `ADR-WAC-001`.
