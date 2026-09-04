# Decision artifacts

Summary: a decision artifact (`DEC-`) records one pending question, or one
implementation deviation, as a formal artifact. While it is open, the
artifacts it blocks cannot change state. A named role answers it with
`harnessctl decide`; the answer is retained verbatim. This note describes the
model that `SPEC-DCM-001` fixes and that `WO-DCM-001` implemented.

## When a question becomes an artifact

Most questions are small. The actor asks, the owner answers, and the answer
goes into the `reason` of the next transition. A question becomes a decision
artifact when one of three things is true:

- it blocks a transition of another artifact;
- it concerns more than one artifact;
- it must survive the approval of the artifact that raised it.

A definition lists its pending decisions in its `## Open decisions` section as
`DEC-` identifiers, or reads `None`. Prose there is refused at approval
(`E-DCM-004`).

## Two kinds

A `question` is an ambiguity met while authoring or planning. It has at least
two options and one recommendation. Its deciding role is the owner of each
artifact it blocks; for a work order, the engineering owner also decides.

A `deviation` is raised during execution when an implementation cannot meet
one rule of one specification. It names the rule as `against = "SPEC-xxx#rule"`
and the fact as `observed`. Its options are drawn from a closed set and always
include `stop`:

| Option | Meaning |
| --- | --- |
| `amend` | Change the rule; the specification is amended by record. |
| `supersede` | Replace the specification. |
| `accept` | Keep the rule and the implementation; the deviation stands, time-bounded. |
| `stop` | Stop the work. |

The deciding role of a deviation is the owner of the specification it departs
from.

## The block

A decision names the artifacts it is about in `concerns`, and the ones that
cannot move in `blocks`. Every blocked artifact is also a concerned one.

Every quality gate carries one `QGP-<gate>-DECISION` predicate. It fails when
an `open` decision names the selected artifact in `blocks`, or when a
`deferred` decision names it without a scope admitting the requested
transition. The failure message names the decision, its question, its
options, the deciding role, and the `decide` command that clears it. Nothing
else changes: the blocked artifact keeps its state until the decision is
disposed and its own transition is requested again.

## Disposition

```text
harnessctl decide . --artifact DEC-PRD-001 --option keep --decision engineering-owner --reason "One record; the split buys nothing." --apply
```

`decide` writes a `[disposition]` table with the option, its label, the role,
the time, and the verbatim reason, then records one lifecycle event. It is the
only path: `transition` refuses a decision, and a hand-written disposition is
`E-DCM-003`.

| State | Meaning | Reached by |
| --- | --- | --- |
| `open` | Pending; blocks. | Creation. |
| `decided` | One option chosen. Terminal. | `decide --option`. |
| `deferred` | Pending, with a scope of admitted transitions and a revisit trigger. | `decide --defer --scope ... --revisit ...`. |
| `withdrawn` | The question no longer applies. Terminal. | `decide --withdraw`. |

A deferral admits exactly the transitions its `--scope` entries name, written
as `ARTIFACT-ID:FROM-TO`. Every other blocked transition still waits. A
deferred decision is later decided or withdrawn.

## Standing deviations

An accepted deviation does not disappear. It stands on the specification it
departs from, on the work orders it concerns, and on every verification or
release record covering that work. The validator projects this standing; the
verification record body lists it under `## Standing deviations`; the Explorer
shows it on each of those records. The standing ends when a later decided
deviation against the same rule chose `amend` or `supersede`.

Acceptance is time-bounded. `--revisit` names a release, a date, or an
artifact state. A revisit that names an already released version is
`W-DCM-001`; two acceptances against the same rule are `W-DCM-002`, because the
rule, not the implementations, is then probably wrong.

## Where decisions appear

- `harnessctl check --artifact DEC-...` projects the open decision to
  `WFL-DEC-OPEN` and names `DR-DECISION-DISPOSE` as the decision right.
- `harnessctl inspect` lists open and deferred decisions in the
  `decision_required` queue with the action `dispose-decision`.
- The Explorer's in-flight tile lists open and deferred decisions with their
  age and deciding role; a concerned artifact's record shows its decision
  trail; the summary metrics report `decisions_open`, `decisions_decided`, and
  raise-to-dispose times.

## Diagnostics

| Code | Meaning |
| --- | --- |
| `E-DCM-001` | A `blocks` target is missing, of a type that cannot be blocked, or not also in `concerns`. |
| `E-DCM-002` | A field required by the decision's kind is missing or malformed. |
| `E-DCM-003` | A disposition without a lifecycle event, an undeclared option, or a missing scope or revisit. |
| `E-DCM-004` | Prose in a definition's `## Open decisions` section. |
| `W-DCM-001` | An accepted deviation is past its revisit trigger. |
| `W-DCM-002` | Two or more accepted deviations stand against one rule. |

The design discussion that led to this model is retained in
[the proposal of 2026-09-03](decision-artifact-proposal-2026-09-03.md).
