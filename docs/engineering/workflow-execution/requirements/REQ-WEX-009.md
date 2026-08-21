+++
id = "REQ-WEX-009"
type = "requirement"
title = "Emit a concise canonical iteration restitution"
status = "approved"
owners = ["requirements-steward", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"
statement = "WHEN a bounded workflow iteration completes, blocks, or reaches a stop condition, THE SYSTEM SHALL emit one concise canonical restitution that states the outcome, work done, expected work not done, current lifecycle state, exact decision required, exactly one next step, and an exact command or suggested response, with alternatives only when the workflow contract declares them."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-WEX-001"]
+++

# Requirement: Emit a concise canonical iteration restitution

## Rationale

`REQ-WEX-005` establishes one semantic handoff, but its current fields do not
distinguish expected work that remains incomplete and do not fully constrain
provider-added prose. Operators need the same terse, decision-ready closure
after every iteration regardless of the agent host.

## Preconditions and trigger

One selected-scope workflow iteration has completed an operation, reached a
governed stop condition, or failed without partial writes. The final scope and
compliance checkpoint has produced a result or an exact reason why it cannot be
assessed.

## Required response

Emit these fields in this order:

1. `Outcome`: `completed` or `blocked`.
2. `Done`: only observable effects that occurred during the iteration.
3. `Not done`: only authorized or expected effects that remain incomplete, or
   `None`.
4. `Blocked by`: the exact failed predicate, only when outcome is `blocked`.
5. `Current lifecycle state`: actual artifact IDs and final states.
6. `Decision required`: `None` or the exact accountable role, artifact, and
   decision.
7. `Next`: exactly one action legal in the final reported state.
8. `Command or response`: one exact command or one precise suggested human
   response.
9. `Alternatives`: only alternatives declared by the selected workflow rule.

The machine-readable form and human renderer must carry the same fields and
meaning. A supported agent adapter must return the canonical human restitution
without adding findings, decisions, or next actions.

## Failure and boundary behavior

- `Done` MUST NOT claim an effect that did not occur.
- `Not done` MUST NOT become a general backlog, repository-health report, or
  list of unrelated work.
- A blocked restitution names the exact failed or non-assessable predicate and
  reports unchanged or final formal state.
- Missing authority is a decision requirement, not an invitation for the agent
  to choose an actor or decision.
- Failure still returns one safe retry or one accountable escalation as `Next`.

## Constraints

- Wording must be simple, direct, and free of introductory or concluding prose
  outside the canonical fields.
- Each entry states one fact or action and uses actual artifact IDs when known.
- Information MUST NOT be duplicated across fields.
- `Next` is singular. Legal branches appear only under `Alternatives` and do not
  weaken the primary recommendation.
- Unrelated findings and actions are excluded according to `REQ-WEX-007`.
- Compliance claims are derived only from the result required by `REQ-WEX-008`.
- The restitution is derived evidence; it cannot approve or execute its own
  recommendation.

## Acceptance examples

### Example: normal behavior

**Given** an implementation iteration that changed two authorized files, passed
its configured checks, retained evidence, and still requires engineering-owner
completion authority

**When** the iteration closes

**Then** restitution reports the two completed effects, `Not done: transition
WO-... to implemented`, the current `in_progress` state, the exact engineering
owner decision, and one transition-preview command as `Next`, without unrelated
repository findings or additional prose.

### Example: failure behavior

**Given** a requested completion whose required test predicate fails

**When** the iteration reaches its stop condition

**Then** restitution reports only work that actually completed, identifies the
failed predicate under `Blocked by`, keeps the work order `in_progress`, states
that no decision is currently actionable, and recommends one exact test retry
or remediation action.

## Open decisions

The specification must define the versioned receipt schema, scalar and list
cardinality, empty-value rendering, maximum verbosity rules, adapter
conformance boundary, and compatibility path from `REQ-WEX-005` before this
requirement is approved for implementation.
