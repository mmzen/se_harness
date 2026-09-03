+++
id = "ADR-DCM-001"
type = "adr"
title = "Model pending decisions as a blocking artifact with a verbatim disposition"
status = "draft"
owners = ["technical-owner", "product-owner", "repository-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[relations]
decides = ["ARCH-DCM-001"]
+++

# ADR: Model pending decisions as a blocking artifact with a verbatim disposition

## Status

Proposed.

## Context

A pending decision in this repository is prose: a section in one artifact
checked once at approval, or a paragraph and a reason field when the
decision appears during execution. The instruction-chain assessment of
2026-09-02 recorded two costs: decisions made during execution have no home
and are found only by readers who know where to look, and the owner's
selection channel is written nowhere. The owner asked for decisions to be
real artifacts, blocking while unresolved, with an explicit exception
mechanism.

## Decision drivers

- Fail closed (`HRN-008`): an unresolved decision must stop the work it
  concerns without a silent bypass.
- Attribution (`HRN-005`): an answer is a decision by the role that holds
  the right, recorded verbatim.
- Reach: one decision often concerns several artifacts.
- Ceremony: the mechanism must be cheap enough that agents use it instead
  of asking open questions.
- Separation: the ADR remains the record of settled architectural
  decisions; the risk artifact is decided separately.

## Considered options

1. **Keep the prose section, add checks.** Extend `QGP-G1-AUTHORING` to
   check `## Open decisions` at more checkpoints. Rejected: prose cannot
   name options, a decider or other artifacts, and cannot be disposed by a
   transition.
2. **Record decisions only as lifecycle events on the concerned artifact.**
   Rejected: an event has no `open` state, cannot block, and cannot span
   artifacts; the question and the options would still live in prose.
3. **A `[pending_decision]` table on the concerned artifact.** Rejected: a
   decision concerning several artifacts would be duplicated and could
   drift; a deviation belongs to a specification the work order does not
   own.
4. **One decision artifact type, in two kinds, with a gate and a
   disposition command.** Selected.
5. **Fold decisions into the risk artifact.** Rejected by the owner: the
   risk artifact is managed separately and afterward.

## Decision

Adopt option 4 as `SPEC-DCM-001` and `ARCH-DCM-001` define it:

- `DEC-` artifacts with `kind = "question"` or `"deviation"`, options with
  ids and labels, a recommendation, `concerns` and `blocks` relations.
- A gate, `QGP-DECISION-OPEN`, evaluated at every transition of a
  definition, a work order, a verification record or a release record,
  refusing while a decision that blocks the artifact is `open` or
  `deferred` outside its scope.
- A disposition written only by `harnessctl decide` under
  `DR-DECISION-DISPOSE`, recording the option id and label, the role, the
  time and the reason verbatim; `deferred` needs scope and revisit;
  `accept` needs revisit.
- Standing deviations projected by the validator onto the specification,
  the work order and the records; revisit warnings on the specification.
- An authoring threshold so that small questions stay in reason fields.

## Consequences

Positive: decisions become visible, attributed, blocking and measurable;
the selection channel becomes a rule; deviations stop hiding in prose; the
Explorer's in-flight tile gains real data.

Negative: one more artifact type, lifecycle family, gate, command and
decision right to maintain; a new failure mode for agents (a blocked
transition they must trace to a decision), mitigated by the refusal naming
the decision and the command; a threshold that must be stated clearly or
the type is either avoided or overused.

Operational: root managed copies change at the next release adoption;
consumer repositories receive the type through the ordinary upgrade; no
existing artifact is rewritten.

Security: decision text is untrusted and rendered as text; a disposition is
trusted only because the tool wrote it under a checked right.

Migration: none for existing artifacts; existing prose deviations stay as
history.

## Validation

`VER-DCM-001` verifies the gate on fixtures, the decision-right and
time-bound refusals, the verbatim disposition, the projection of accepted
deviations onto records and the Explorer, the diagnostics, the templates
and the upgrade path.
