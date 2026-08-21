+++
id = "REQ-WEX-008"
type = "requirement"
title = "Evaluate workflow compliance at governed checkpoints"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN a selected workflow operation reaches its start, pre-action, transition, or final-handoff checkpoint, THE SYSTEM SHALL resolve the applicable workflow rule, evaluate each required quality-gate predicate as pass, fail, or not_assessable with exact evidence, and prevent a governed action or completion claim unless every required gate reports pass."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Evaluate workflow compliance at governed checkpoints

## Rationale

Gate identifiers in a workflow contract do not enforce compliance by
themselves. Provider-specific interpretation remains possible when an agent is
asked to decide whether a gate passed or when several command-specific checks
do not expose one common result.

## Preconditions and trigger

The operator has selected a workflow artifact and action for which the active
machine-readable workflow can resolve one ordered rule. A checkpoint occurs
before bounded implementation begins, before a governed lifecycle or external
action, and before the iteration claims completion or emits its final handoff.

## Required response

- Resolve exactly one applicable workflow rule using the active ordered
  workflow contract.
- Enumerate every gate named by that rule and every predicate defined for each
  gate.
- Report each predicate as `pass`, `fail`, or `not_assessable` with its rule ID,
  evidence source, and exact reason.
- Treat missing, unreadable, stale, or externally unavailable required evidence
  as `not_assessable`, never as `pass`.
- Permit the governed action only when every required predicate reports
  `pass`.
- Re-evaluate final-state and completion predicates before emitting a successful
  final handoff.
- Return the same structured compliance result to human and machine consumers.

## Failure and boundary behavior

- An unresolved or ambiguous workflow rule fails the checkpoint.
- A `fail` or `not_assessable` required predicate prevents the governed action
  or completion claim and leaves lifecycle state unchanged.
- Failure output identifies the exact predicate and one safe retry or one
  accountable escalation; it MUST NOT return only an aggregate failure label.
- The compliance result MUST NOT authenticate an actor, infer a decision right,
  approve an artifact, accept risk, or perform an external action.

## Constraints

- Compliance is evaluated at deterministic boundaries rather than continuously
  after every file edit.
- Exact gate results remain authoritative; an aggregate score or dashboard
  status MUST NOT replace them.
- Gate definitions have one normative machine-readable owner. Command-specific
  checks MAY implement predicates but MUST NOT silently redefine them.
- Scope and restitution filtering follow `REQ-WEX-007`; an unrelated finding
  does not become a compliance failure for the selected action unless it is an
  applicable repository-integrity blocker.
- Gate evaluation is derived evidence and does not exercise the decision right
  associated with the selected workflow rule.

## Acceptance examples

### Example: normal behavior

**Given** an approved work order selected for implementation, a valid governing
chain, a passing start preflight, and explicit engineering-owner authority

**When** the start checkpoint is evaluated

**Then** every `QG-G3-WORK-AUTHORIZATION` predicate reports `pass` with its
evidence, the applicable workflow rule is identified, and implementation may
begin without changing lifecycle state merely because the check passed.

### Example: failure behavior

**Given** an in-progress work order whose required retained evidence cannot be
read

**When** the completion checkpoint is evaluated

**Then** the evidence predicate reports `not_assessable`, the work order remains
`in_progress`, and the result identifies the missing evidence and one exact
retry action.

## Open decisions

The specification must define the executable gate registry, checkpoint-to-rule
mapping, evidence freshness rules, public check interface, and composition of
existing preflight and transition checks before this requirement is approved
for implementation.
