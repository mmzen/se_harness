+++
id = "REQ-AEX-002"
type = "requirement"
title = "Constrain autonomous mutation with an explicit autonomy envelope"
status = "approved"
owners = ["product-owner", "requirements-steward", "engineering-owner"]
created = "2026-08-24"
updated = "2026-08-24"
statement = "WHEN autonomous execution can modify repository content or lifecycle state, THE SYSTEM SHALL require and validate an explicit autonomy envelope bound to the selected work order, current repository state, permitted operations, path scope, execution profiles, evidence obligations, retry limits, and accountable-decision-required stops; and SHALL reject stale, ambiguous, self-expanded, or out-of-scope execution before any write."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-AEX-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T09:03:54Z"
decided_by = "requirements-steward"
+++

# Requirement: Constrain autonomous mutation with an explicit autonomy envelope

## Rationale

An approved work order bounds implementation scope, but long-running agent
execution also needs an executable answer to which routine operations may
continue without another human interaction. Prompts and runtime permission
modes are not reliable or authoritative representations of that boundary.

## Preconditions and trigger

An agent, skill, or orchestrator requests a repository write, lifecycle
preparation, lifecycle transition, retained evidence write, or other governed
mutation without a new action-time human interaction.

## Required response

- Resolve exactly one eligible selected work order and its governing chain.
- Validate the envelope's immutable identity and current-state binding.
- Validate permitted operation classes and exact path or component scope.
- Validate allowed execution profiles, writer count, evidence obligations,
  bounded retries, and stop-before decision classes.
- Apply existing mutation guard, installed integrity, released-evaluator
  identity, safe-path, stale-input, proposed-final-graph, and rollback checks.
- Refuse any operation not expressly admitted by both the work order and the
  envelope.
- Record which envelope admitted each governed autonomous operation.

## Failure and boundary behavior

- Missing, duplicated, expired, stale, malformed, case-ambiguous, or conflicting
  envelopes fail closed.
- A child agent, skill, adapter, model, or runtime override cannot enlarge the
  envelope inherited from the parent workflow.
- A retry may repeat only an already-permitted operation within its declared
  bound; it cannot change scope, decision class, or external target.
- An `accountable-decision-required` decision or
  `action-time-authorization-required` action always stops before its effect.
- Failure leaves no partial mutation or misleading success receipt.

## Constraints

- Read-only inspection may operate without a mutation envelope but still obeys
  repository and runtime permissions.
- An envelope may narrow an approved work order but cannot broaden it.
- The exact representation must be deterministic and treat every field as
  untrusted input.
- Envelope approval does not authorize commit, push, merge, tag, publication,
  deployment, operation, or credential use unless managed policy defines and an
  accountable owner explicitly names that exact action.

## Acceptance examples

### Example: permitted implementation continues

**Given** an approved work order and a valid envelope permitting implementation,
tests, and evidence inside `se_harness/` and `tests/`

**When** the implementation worker requests an admitted source edit

**Then** the harness validates the current work order, envelope, evaluator, and
path before the write and records the envelope identity in the receipt.

### Example: child worker attempts expansion

**Given** a child worker whose assigned scope is read-only test analysis

**When** it requests a managed-policy edit or adds a new allowed path to its
local task description

**Then** the request fails before writing and the parent workflow receives an
out-of-scope diagnostic.

## Open decisions

Before approval, accountable owners must decide which existing decision rights
are pre-delegatable and whether an envelope is embedded in a work order,
recorded as a separate formal artifact relation, or represented as a validated
non-authoritative execution object derived from an explicit decision.
