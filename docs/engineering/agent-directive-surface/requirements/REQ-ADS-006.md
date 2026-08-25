+++
id = "REQ-ADS-006"
type = "requirement"
title = "The managed router states the scope of its own obligations"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN the managed router is rendered, THE SYSTEM SHALL state that `HRN-003`, the lifecycle-restitution rules, and the stop conditions bind an actor executing or reporting a lifecycle stage, and that reading, analysis, and answering questions are unconstrained provided no state changes and no finding is presented as a formal result."
verification_method = "manual-review"
[relations]
derives_from = ["CAP-ADS-001"]
+++

# Requirement: The managed router states the scope of its own obligations

## Rationale

`HRN-003` requires selecting one artifact before acting; the owner fragment
forbids appending repository-wide findings. Taken literally, a repository
review requested by the owner violates both. Nothing states whether the rules
bind a lifecycle stage only or every interaction, so an agent must guess, and
both safe guesses (refuse; ignore) are wrong.

## Preconditions and trigger

Rendering of `ENGINEERING_HARNESS.md` by the installer from its template.

## Required response

One paragraph under a `Scope of these obligations` heading, before the global
invariants, with the wording in `SPEC-ADS-001` rule `ADS-SCP-001`.

## Failure and boundary behavior

The paragraph adds no authority and waives none. It does not permit a state
change, a decision claim, or a finding presented as a formal result outside a
stage.

## Constraints

Managed template change only; the root copy in this repository follows on the
next governor upgrade.

## Acceptance examples

### Example: normal behavior

**Given** an owner asks an agent to assess the repository

**When** the agent reads the router

**Then** it finds the scope paragraph and answers without selecting a work
order and without claiming a formal result.

### Example: failure behavior

**Given** the same request

**When** the agent attempts a transition as part of the answer

**Then** the stop conditions apply unchanged.

## Open decisions

None.
