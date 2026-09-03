+++
id = "REQ-DCM-002"
type = "requirement"
title = "The accountable role disposes a decision with a verbatim option"
status = "draft"
owners = ["product-owner", "repository-owner", "quality-owner"]
created = "2026-09-03"
updated = "2026-09-03"
statement = "WHEN the role holding the decision right selects one option of an open or deferred decision, THE SYSTEM SHALL record the option identifier, its label, the role, the time and the verbatim reason as the decision's disposition and as its lifecycle event."
verification_method = ["test"]
priority = "must"
source = "docs/notes/decision-artifact-proposal-2026-09-03.md; the ratified but unwritten selection channel noted in docs/notes/assessment-instruction-chain-2026-09-02.md"
measure = "every disposition carries the option identifier, label, role, timestamp and reason; a disposition by a role without the right is refused"

[relations]
derives_from = ["CAP-DCM-001"]
+++

# Requirement: The accountable role disposes a decision with a verbatim option

## Rationale

The owner already decides by selecting a presented option, and the agent
records "by selecting the presented option '…'" in the reason field. That
convention is ratified and written nowhere. Making the selection the
disposition of an artifact gives it a rule, a shape and a decision right:
the option is recorded by identifier and by label, so a paraphrase cannot
replace the answer, and the role is checked, so a work order cannot answer
a question that belongs to the owner of a specification.

## Behavior

- Trigger: `harnessctl decide` (or the equivalent transition) is applied to
  a decision in status `open` or `deferred`, with one option identifier,
  one accountable role and a reason.
- Response: the decision's `disposition` table records the option
  identifier, the option label copied from the artifact, the role, the
  UTC time and the reason verbatim; a lifecycle event records the same
  transition; the status becomes `decided`, or `deferred` when the option
  is a deferral with scope and revisit.
- On failure: an option identifier that the decision does not declare, a
  role without the decision right for the blocked artifact (or, for a
  deviation, for the departed specification), a deferral without scope or
  revisit, or an acceptance without revisit is refused with no change.

## Assumptions and dependencies

- `DECISION_RIGHTS.md` defines `DR-DECISION-DISPOSE`: the right belongs to
  the owner of the artifact the decision blocks; for a deviation, to the
  owner of the specification in `against`.
- The disposition is written by the tool, never by hand; a hand-written
  disposition is a graph error.

## Acceptance examples

### Example: a selection is recorded verbatim

**Given** `DEC-X-001` is `open` with options `a`, `b`, `c` and the product
owner holds the right,

**When** the product owner applies `decide DEC-X-001 --option b`,

**Then** the disposition reads option `b` with its label, `product-owner`,
the time and the reason, the status is `decided`, and the blocked
transitions are admitted.

### Example: the wrong role is refused

**Given** the same decision,

**When** the engineering owner applies the same command,

**Then** the command is refused, the status stays `open`, and the result
names the role that holds the right.

## Open decisions

None.
