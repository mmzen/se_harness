+++
id = "SPEC-TCM-007"
type = "specification"
title = "Authoring advisories refuse approval of a definition draft"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-09-06"
updated = "2026-09-06"
contract = "A conforming gate refuses to approve a definition draft that still draws an authoring advisory, names each advisory, and changes nothing else about validation or approved artifacts."

[relations]
specifies = ["REQ-TCM-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T14:54:35Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 with the instruction 'i approve' after reviewing PR #366 (REQ-TCM-017, SPEC-TCM-007, VER-TCM-007, WO-TCM-011), which executes DEC-TCM-004 and the regime recorded for the requirement, intent and capability families: advisory for one release, then blocking at approval."
+++

# Specification: Authoring advisories refuse approval of a definition draft

## In plain words

The approval gate already asks whether a decision about the draft is still
open. It now also asks whether the draft still draws a writing advisory,
and refuses when it does.

## Scope

The `authoring_ready` evaluator behind `QGP-G1-AUTHORING` and
`QGP-G2-AUTHORING`, the validator's advisory functions it reads, and the
authoring guide. The budgets and codes of `SPEC-TCM-003`, `SPEC-TCM-004`,
`SPEC-TCM-005` and `SPEC-TCM-006` are read, not changed. Every rule of this
specification carries a normative keyword and a name a test can cite.

## Terms

- **Authoring advisory.** A validator message of the `W-AUT` family, raised
  on a draft and never on an approved artifact.
- **Definition kinds.** Intent, capability, requirement and specification,
  the four types with an advisory family.
- **Authoring predicate.** `QGP-G1-AUTHORING` for intents, capabilities and
  requirements, `QGP-G2-AUTHORING` for specifications, both evaluated by
  `authoring_ready` at the approval transition.

## Rules

**TCM-RFB-001.** The validator MUST expose `authoring_advisories(artifact)`,
returning the `W-AUT` diagnostics its four per-type functions raise for one
artifact.

**TCM-RFB-002.** `authoring_advisories` MUST evaluate the artifact as a
draft regardless of its recorded status, so the gate reads what the author
would have seen.

**TCM-RFB-003.** `authoring_ready` MUST keep its placeholder and legacy
`Open decisions` checks and evaluate them before the advisory check.

**TCM-RFB-004.** For a draft of a definition kind, `authoring_ready` MUST
fail when `authoring_advisories` returns one or more diagnostics.

**TCM-RFB-005.** The failure message MUST list every advisory as code and
message, in the validator's order, and end with "fix the draft and run the
transition again".

**TCM-RFB-006.** For an artifact of any other type, `authoring_ready` MUST
pass the advisory check without reading the validator.

**TCM-RFB-007.** `authoring_ready` MUST read the advisories through the
validator module the evaluator already loads for preflight, never through
a second copy of the budgets.

**TCM-RFB-008.** No budget constant, advisory code or message of
`SPEC-TCM-003` to `SPEC-TCM-006` MAY change under this specification.

**TCM-RFB-009.** `validate` MUST keep reporting advisories apart from
errors and warnings and MUST keep passing with advisories present.

**TCM-RFB-010.** `check --checkpoint transition` and an unapplied
`transition` MUST show the failing predicate with the same message before
any file is written.

**TCM-RFB-011.** The definition checklists of `ARTIFACT_AUTHORING.md` MUST
state that a draft drawing an advisory is not approved until it is fixed.

**TCM-RFB-012.** The evaluator MUST NOT read advisories for a target other
than `approved`, so implementation, supersession and rejection are
unchanged.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| A draft requirement with a 31-word statement is approved | the transition is refused; the message names `W-AUT-003` with the measured value | `QGP-G1-AUTHORING: fail` |
| A draft specification with two rules over 30 words is approved | the transition is refused; the message names `W-AUT-021` twice | `QGP-G2-AUTHORING: fail` |
| A draft verification contract is approved | the placeholder check runs; no advisory is read | `QGP-G1-AUTHORING: pass` |
| The validator module cannot be loaded | the predicate is not assessable and the transition does not proceed | `QGP-G1-AUTHORING: not_assessable` |
| An approved artifact is moved to implemented | no authoring predicate is bound to that target; nothing is read | none |

## Examples

**Given** `REQ-TCM-014` as it was approved, **when** the product owner
approves it under this gate, **then** the approval completes (TCM-RFB-004
with zero advisories).

**Given** `REQ-HUP-031` as it was drafted, whose statement exceeds 30 words
and whose body cites more than three code identifiers, **when** the product
owner approves it, **then** the gate refuses and names `W-AUT-003`,
`W-AUT-005`, `W-AUT-007`, `W-AUT-008` and `W-AUT-010` (TCM-RFB-004,
TCM-RFB-005).

**Given** a draft architecture, **when** it is approved, **then** only the
placeholder check runs (TCM-RFB-006).

**Given** a repository whose drafts draw twelve advisories, **when**
`validate` runs, **then** it passes and lists them apart (TCM-RFB-009).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-TCM-017` | TCM-RFB-001, TCM-RFB-002, TCM-RFB-003, TCM-RFB-004, TCM-RFB-005, TCM-RFB-006, TCM-RFB-007, TCM-RFB-008, TCM-RFB-009, TCM-RFB-010, TCM-RFB-011, TCM-RFB-012 |

## Not decided here

- Whether an owner may waive the refusal for one draft. No waiver is
  specified: the draft is fixed, or the family's budget is amended.
- Whether the budgets themselves move; the reading of 2026-09-06 is the
  work order's input, and a change is an amendment of the family's
  specification.
- The exact wording of the refusal beyond the code, the message and the
  closing sentence.
