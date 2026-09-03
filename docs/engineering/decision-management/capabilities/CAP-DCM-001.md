+++
id = "CAP-DCM-001"
type = "capability"
title = "Raise, block on, and dispose governed decisions"
status = "draft"
owners = ["product-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[relations]
derives_from = ["INT-DCM-001"]
+++

# Capability: Raise, block on, and dispose governed decisions

## Actor and need

An actor working on governed artifacts, human or agent, meets a question
that the artifacts do not answer, or an implementation that cannot meet a
rule. The actor needs to record the question with its options where the
tool, the reviewer and the Explorer can see it, and needs the affected work
to wait until the accountable role answers.

## Capability statement

`An actor can raise a decision artifact that blocks the transitions of the
artifacts it names, and the accountable role can dispose or defer it with
a verbatim, attributed answer, under the managed lifecycle and gates.`

## Boundaries

- The capability covers pending decisions and implementation deviations. It
  does not cover risks, and it does not replace the ADR.
- The gate applies to the artifacts a decision `blocks`, at every
  checkpoint the workflow contract evaluates for them.
- A deferral is scoped and time-bounded. An acceptance of a deviation is
  time-bounded.
- Below the authoring threshold, a question is asked and answered in a
  reason field, as today.

## Outcomes

- Every decision above the threshold has an identifier, an owner, a state,
  options, and typed relations.
- No transition of a blocked artifact is applied while its decision is open.
- Every disposition names the option, the role, the time and the reason.
- Accepted deviations stay visible on the specification, the work order,
  and the records that cover the work.
- The Explorer lists open decisions by age and decider, and reports the
  raise-to-dispose time.

## Candidate requirements

- `REQ-DCM-001`: an open decision blocks the transitions it names.
- `REQ-DCM-002`: the accountable role disposes a decision with a verbatim,
  attributed option.
- `REQ-DCM-003`: an accepted deviation stays visible on the rule, the work,
  and the records until the rule changes.
