+++
id = "ADR-RSK-010"
type = "adr"
title = "Borrow the decision family's stop and disposal for risks"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
decides = ["ARCH-RSK-010"]
+++

# ADR: Borrow the decision family's stop and disposal for risks

## Status

Proposed.

## Context

Pull request #156 introduced a risk artifact in April of this repository's
governance history and was never merged. It designed the family as fully
self-contained: its own relation `threatens`, its own gate predicate
`undisposed_risks_threatening_scope` wired into seven gates, its own decision
right `DR-RISK-DISPOSE` held by the threatened stage's owner, and its own
disposal command. Its branch cannot be resumed: three of its verification
records are `ready` and stale under a governor that has upgraded from 0.6.0 to
0.16.0, and a stale `ready` record can be neither superseded nor rejected. It
also edits template scripts that `WO-DST-024` deleted and adds configuration
keys that `WO-DST-025` has just removed.

Since #156 was written the decision family (`DEC-`) has been delivered and
verified. It supplies, in production, everything #156 built for stopping and
answering: `blocks` and `concerns` relations, `QGP-DECISION-OPEN` in all eight
gate groups, a scoped deferral with a revisit trigger, a disposition writable
only by `harnessctl decide`, and `DR-DECISION-DISPOSE` resolved from the owner of
the blocked artifact. What it has nowhere to put is a measurement, and it makes
no claim about work that reduced a threat.

The managed authoring policy already carries a `risk` checklist naming a
`harnessctl raise-risk` command and the five-by-five scale. It shipped with the
0.7.1 root, on the assumption that #156 would land. The type it describes does
not exist.

## Decision drivers

- One stopping rule. An owner should not have to learn two mechanisms that hold
  a stage still, and a reviewer should not have to look in two places to find
  what is blocking.
- One answer, recorded once. Two records of one answer drift.
- The measurement is the risk family's own contribution and belongs nowhere else.
- "Mitigated" is a claim about checked work and must rest on the same proof every
  other completion claim rests on.
- Reversibility. A family that no gate reads can be withdrawn later.
- The configuration surface was reduced to five keys today; no new key may appear
  without a reader.

## Considered options

### Option A: the risk measures, the decision decides (chosen)

A sixth family carrying only the measurement, the threatened artifacts, the
mitigation trace and a copy of the answer. A raised risk must name a pending
decision whose `blocks` set equals its `threatens` set; the existing predicate
does the stopping; `decide` does the answering and moves the risk in the same
act. Closure adds one narrow decision right.

Consequences: no gate predicate, no disposal right, no configuration key; two
files per material threat; the risk depends on the decision family, which must
therefore stay.

### Option B: a third decision kind

No new family. `kind = "risk"` on the decision artifact with a measurement
block and options fixed to accept, avoid, mitigate and stop.

Consequences: the smallest surface of the three, and no new directory. It
amends a specification that a `verified` record covers, so it needs a repair
work order and an amendment record. Because `decided` is terminal, a threat
under active mitigation must sit in `deferred` with the mitigation work order as
its revisit trigger, which reads as an unanswered decision rather than as work in
progress. A release register is not available from the decision family and would
be added separately. Rejected: the state model does not fit the thing being
modelled, and amending a verified contract to make it fit is the wrong price.

### Option C: re-issue the self-contained design of #156

Keep the original family, its predicate, its right and its command, repairing
only the mechanical breakages.

Consequences: highest fidelity to the retired design and the largest surface.
The repository would carry two mechanisms that stop a stage, two disposal
commands and two rights, evaluated on every transition. Rejected: it duplicates
delivered, verified machinery and re-opens a boundary the decision family already
settled.

## Decision

Option A. The risk family carries the measurement and the mitigation trace. It
adds no gate predicate; a raised risk stops its threatened artifacts only through
a paired decision, and the answer is given once, by disposing that decision. The
one authority the family adds is `DR-RISK-CLOSE`, held by the assurance owner, for
the single edge `mitigating -> mitigated`, which is refused unless a `verified` or
`released` record covers every mitigating work order and a residual is recorded.

The identifiers of the retired branch, `RSK-001` to `RSK-007` in every type, are
not reused. This packet begins at 010 so that the retained release evidence
naming `WO-RSK-001` and `WO-RSK-002` stays unambiguous.

## Consequences

Positive. One stopping rule and one disposing command for questions and threats
alike. The answer exists once, verbatim, with its role and time. The gate
contract does not change, so the family is reversible. The authoring policy's
existing `risk` checklist becomes true.

Negative. A material threat costs two files, and the pairing rule between them is
a graph error a raiser can trip. The risk family cannot be used in a repository
that has disabled decisions, because there is no such configuration and none is
added. A reader who expects a risk to block on its own must learn that the
decision beside it does.

Operational. Recording a threat mid-execution is admitted by the scope check for
one added file only, so an implementer never has to widen a work order to report
one. Nothing in an existing repository changes until the release that carries the
family is adopted.

Security. Every risk field is untrusted text, rendered as text. The raise carries
no authority beyond stopping a stage until an owner answers; the answer and the
closure are both checked against a role.

Migration. No existing artifact is rewritten. Prose threats in evidence packets
stay as history. Pull request #156 is closed with a reason and its branch is
retained; nothing on `main` refers to its artifacts except retained release
evidence, which keeps its wording.

## Validation

- The quality-gates contract, both copies, gains no predicate identifier.
- The decision-rights catalog gains exactly one row, and it is a closure right.
- A test asserts that a raised risk whose paired decision blocks a different set
  is a graph error.
- A test asserts that disposing one decision moves both the decision and the
  risk, in one act.
- A test asserts that closure is refused while the mitigating work order lacks a
  `verified` or `released` record.
- The installed configuration still declares five keys.
