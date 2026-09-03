+++
id = "INT-DCM-001"
type = "intent"
title = "Make every pending decision a governed, blocking artifact"
status = "draft"
owners = ["product-owner", "repository-owner"]
created = "2026-09-03"
updated = "2026-09-03"

[relations]
+++

# Intent: Make every pending decision a governed, blocking artifact

## Problem

Governed work stops on decisions: which option a requirement should take,
whether an implementation may depart from a rule of a specification, what a
work order does when its scope proves wrong. Today each such decision is
prose. It sits in the `## Open decisions` section of one artifact, or in a
paragraph of a specification, or in the `reason` field of a lifecycle
event. It has no identifier, no owner, no state, and no relation to the
other artifacts it concerns. The tool checks it once, at approval, and only
asks that the section reads `None`.

Two consequences were measured on 2026-09-01 and 2026-09-02
(`docs/notes/assessment-instruction-chain-2026-09-02.md`). A decision that
appears during execution, such as the Lineage prefetch deviation under
`WO-DST-023`, has no home and ends up as text in a specification the reader
must know to open. And the way the accountable owner decides, by selecting
one presented option, is recorded in every reason field but written in no
rule, so a fresh agent would invent another wording and the record would
drift.

## Desired outcomes

- A pending decision is one artifact with an identifier, a question, a
  closed set of options, a recommendation, and the role that must answer.
- While it is open, the artifacts it blocks cannot change state. No field
  and no priority opens that gate; only the accountable role's answer, or an
  explicit, scoped, time-bounded deferral.
- The answer is recorded verbatim as the decision's disposition and as a
  lifecycle event. The decided artifact is kept, like a rejected one.
- An implementation that cannot meet a rule of a specification raises a
  decision of kind deviation. Its acceptance stays visible on the
  specification, the work order, and every record that covers the work,
  until a later decision amends or supersedes the rule.
- The Explorer shows what needs a decision today, and the time from raising
  a decision to disposing it becomes a measurable figure.

## Actors and stakeholders

- The repository owner and the role owners decide; they bear the cost of an
  undecided question and the risk of an unrecorded answer.
- Coding agents raise decisions when they meet an ambiguity above a stated
  threshold, and stop instead of asking an open question.
- Reviewers and auditors read the disposition and the standing deviations
  on the records they review.
- Consumer repositories receive the type through the ordinary managed
  upgrade.

## Success measures

| Measure | Baseline | Target | Observation window |
|---|---:|---:|---|
| Decisions recorded as artifacts rather than prose | 0 | every decision above the threshold | first release after adoption |
| Transitions applied while a blocking decision was open | not measurable | 0 | every generated bundle |
| Accepted deviations without a revisit trigger | not measurable | 0 | every validation run |
| Raise-to-dispose time | not measurable | reported per decision in the Explorer | every generated bundle |

## Non-goals

- Replacing the ADR: a settled architectural decision keeps its own artifact.
- Managing risks: the risk artifact is a separate initiative and is decided
  separately.
- Recording every small question: below the threshold the agent asks and
  the answer stays in the reason field, as today.
- Changing how a host presents options to a human; the artifact records the
  selection, the host is free.

## Principles and immutable constraints

- Fail closed: an open decision blocks, and no numeric field unblocks it
  (`HRN-008`).
- A disposition is an explicit, attributed decision (`HRN-005`); only the
  role with the decision right may make it.
- The chosen option is recorded verbatim, never paraphrased.
- The decider of a deviation is the owner of the rule departed from, not
  the owner of the work order.
- Nothing is deleted: decided and withdrawn decisions stay in history.

## Risks and assumptions

Facts: the validator and the workflow contract already gate every
transition by artifact family and status; adding a family and a predicate
follows the existing pattern. Assumption: the threshold in
`ARTIFACT_AUTHORING.md` keeps the count of decision artifacts small enough
that agents use rather than avoid them. Open decision: none at this level;
the specification decides the exact gate placement.
