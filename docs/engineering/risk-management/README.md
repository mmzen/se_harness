# Risk management Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this
> directory or index.

This domain makes a threat to governed work a governed artifact. A risk
(`RISK-`) records one cause, one effect, the stage it threatens, and its size on
a five-by-five scale. Recording it raises it. A raised risk does not stop
anything by itself: it names a pending decision (`DEC-`) whose `blocks` set
equals the artifacts it threatens, and the decision family's existing stop holds
those artifacts still. Disposing that decision answers the threat and moves the
risk in the same act. Only `mitigated` claims that the threat was reduced, and it
is refused unless a `verified` record covers the mitigating work order and a
residual is written down.

## Relationship to the decision domain

The decision family already supplies the stop, the accountable disposal, the
scoped deferral and the verbatim record. This domain adds what a decision has
nowhere to put: the measurement and the mitigation trace. It adds no gate
predicate, no configuration key, and no right to dispose a risk. It adds one
right, `DR-RISK-CLOSE`, for closure alone. `decision-management/` states that the
risk artifact is managed separately and afterward; this is that domain.

## Relationship to the retired pull request #156

Pull request #156 designed a self-contained risk family with its own gate
predicate, its own disposal right and its own command, before the decision family
existed. It cannot be resumed: three of its verification records are `ready` and
stale under a governor that has upgraded from 0.6.0 to 0.16.0, and a stale `ready`
record can neither be superseded nor rejected. It also edits template scripts that
`WO-DST-024` deleted and adds configuration keys that `WO-DST-025` removed. Its
statements survive here as `source` on the requirements; its identifiers do not.
`RSK-001` to `RSK-007` stay with the retired branch, so this packet begins at 010
and the retained release evidence naming `WO-RSK-001` stays unambiguous.
`ADR-RSK-010` records the three designs considered and why this one was chosen.

## Draft definition packet

`INT-RSK-010` -> `CAP-RSK-010` -> `REQ-RSK-010..016` -> `SPEC-RSK-010`,
`ARCH-RSK-010`, `ADR-RSK-010`, `VER-RSK-010` -> `WO-RSK-010`, `WO-RSK-011`.

- `INT-RSK-010`: make a threat a measured fact with a recorded answer.
- `CAP-RSK-010`: record a threat, size it, and answer it before the stage moves.
- `REQ-RSK-010`: a risk carries one cause, one effect and a measured size.
- `REQ-RSK-011`: every recorded risk is raised; there is no threshold.
- `REQ-RSK-012`: a raised risk stops the threatened stage through a decision.
- `REQ-RSK-013`: the answer is given once, on the decision, and copied over.
- `REQ-RSK-014`: `mitigated` needs verified coverage and a residual.
- `REQ-RSK-015`: recording a risk never widens a work order's scope.
- `REQ-RSK-016`: a release states the risks the released work carries.
- `SPEC-RSK-010`: the risk contract, thirty-six rules in the area `RSK-MGT`.
- `ARCH-RSK-010` and `ADR-RSK-010`: the boundary between the two families and
  the decision to borrow the stop rather than build a second one.
- `VER-RSK-010`: the evidence contract for all seven requirements.
- `WO-RSK-010`: the artifact, the raise, the pairing and the scope admission.
- `WO-RSK-011`: closure under verified coverage and the release register,
  stacked on `WO-RSK-010`.

The authoring policy already carries a `risk` checklist naming
`harnessctl raise-risk` and the five-by-five scale. It shipped with the 0.7.1
root on the assumption that #156 would land; this packet makes it true.

## Status

Drafted on 2026-09-07 after the owner selected the presented option "the risk
measures, the decision decides" from a proposal comparing it against a third
decision kind and against re-issuing #156. Nothing is approved: a definition
leaves `draft` only by an explicit decision under `DR-DEFINITION-DECIDE`, and
approval of a definition authorizes no work.
