+++
id = "ARCH-RSK-010"
type = "architecture"
title = "The risk carries the measurement; the decision carries the act"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
addresses = ["REQ-RSK-012", "REQ-RSK-013", "REQ-RSK-014"]
conforms_to = ["SPEC-RSK-010"]

[decision_assessment]
outcome = "adr_required"
triggers = [
  "cross-cutting-policy",
  "responsibility-or-dependency-direction",
  "difficult-to-reverse",
  "material-alternatives",
]
rationale = "The risk artifact adds a family that can stop any stage of any domain, which is cross-cutting policy. Whether it stops stages itself or borrows the decision family's stop fixes the dependency direction between two artifact families and is very hard to reverse once records bind it. Three materially different designs were on the table, and the retired PR #156 chose a different one."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T20:49:30Z"
decided_by = "technical-owner"
reason = "Approved by the accountable owner on 2026-09-07, by selecting the presented option in the ratified decision channel. The one-way dependency from the risk to the decision leaves SPEC-DCM-001 unamended."
+++

# Architecture: The risk carries the measurement; the decision carries the act

## Context and scope

The risk family must stop a threatened stage until an accountable role answers.
The decision family already does exactly that: an artifact in `open` blocks
every transition of the artifacts in its `blocks` relation, through
`QGP-DECISION-OPEN` in all eight gate groups, and its disposition is written only
by `harnessctl decide` under `DR-DECISION-DISPOSE`. This architecture fixes the
boundary between the two families so that the stopping and answering machinery
exists once.

`addresses` names the three requirements that fix that boundary: the stop
(`REQ-RSK-012`), the single answering act (`REQ-RSK-013`), and closure under
verified coverage (`REQ-RSK-014`). The measurement rules, the raise, the scope
admission and the release register are routine and are specified without
architectural significance.

## Components and responsibilities

| Component | Responsibility | Must not |
| --- | --- | --- |
| The risk artifact | Hold the measurement of one threat, its threatened artifacts, and a copy of the answer | Block a transition; hold a decision right; be edited to record an answer |
| The decision artifact | Hold the question, the options, the decider, the blocked artifacts and the verbatim answer | Hold likelihood, impact or a score |
| `raise-risk` | Compute the score, write the risk, and optionally write the paired decision | Dispose anything |
| `decide` | Dispose the decision and, in the same act, move the risk the decision concerns | Move a risk that no disposed decision concerns |
| `transition` | Apply closure, `mitigating -> mitigated`, under `DR-RISK-CLOSE` | Apply any other risk edge |
| `prepare-release` | Derive the release register from the graph | Accept a hand-written register |

## Dependency direction

The risk family depends on the decision family and never the reverse. The
decision code needs no knowledge of a risk beyond the generic `concerns`
relation it already permits to any type; only the risk code reads decisions.
`SPEC-DCM-001` is therefore not amended by this work.

## Data and control flow

Recording a threat writes a risk in `raised` and a decision in `open` that
blocks the threatened artifacts. Any transition of a threatened artifact fails
the existing decision predicate, which names the decision, its options and the
deciding role. Disposing the decision writes the decision's `[disposition]`,
then the paired risk transition and the risk's copied disposition, in one act
under one lock. Closure is a separate later act, gated on verified coverage.
Release preparation reads the graph and writes the derived register.

## Trust boundaries

Every field of a risk is untrusted repository text and is rendered as text, never
as markup or a command. The raiser needs no decision right and can therefore be
any actor, human or agent; this is deliberate, and the only authority the raise
carries is the ability to stop a stage until an owner answers. The answer crosses
into authority and is checked against `DR-DECISION-DISPOSE`; closure is checked
against `DR-RISK-CLOSE`.

## Required patterns

- One measurement, one place: likelihood, impact and score exist only on the
  risk.
- One answer, one act: the risk's state and its recorded answer are written by
  the same command that disposes the decision.
- Borrowed stop: the blocking predicate is the decision family's, unchanged.
- Derived registers: the release list and the Explorer rows are computed from
  the graph, never authored.

## Prohibited patterns

- A gate predicate that reads risks.
- A decision right that disposes a risk.
- A risk field that duplicates a decision field, including the question, the
  options, the recommendation and the deciding role.
- A configuration key that governs which risks are raised.
- A risk state written by any command other than `raise-risk`, `decide` and
  `transition`.

## Quality attributes

Learnability: an owner learns one stopping rule and one disposing command for
both questions and threats. Auditability: the answer exists once, verbatim, with
its role and time. Reversibility: because no gate reads risks, withdrawing the
family later removes files and two commands without touching the gate contract.

## Conformance checks

- No new predicate identifier appears in either copy of the quality-gates
  contract (RSK-MGT-014).
- The decision-rights catalog gains exactly one row (RSK-MGT-032).
- The risk schema declares no question, option, recommendation or decider field
  (RSK-MGT-002).
- A raised risk whose paired decision blocks a different set is a graph error
  (RSK-MGT-013).

## Related ADRs

`ADR-RSK-010` records the decision to borrow the decision family's stop and
disposal rather than give the risk family its own, and the two rejected
alternatives.
