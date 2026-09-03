# Decision management Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata,
> typed relations, lifecycle state, and accountable decisions—not this
> directory or index.

This domain makes a pending decision a governed artifact. A decision
(`DEC-`) has a question, a closed set of options, a recommendation and the
role that must answer. While it is `open`, the artifacts it blocks cannot
change state. The accountable role disposes it with one option, recorded
verbatim. A deviation, an implementation that cannot meet one rule of one
specification, is a decision of the second kind; its acceptance stays
visible on the specification, the work order and the records until the rule
changes. The proposal is `docs/notes/decision-artifact-proposal-2026-09-03.md`.

## Draft definition packet

`INT-DCM-001` -> `CAP-DCM-001` -> `REQ-DCM-001..003` -> `SPEC-DCM-001`,
`ARCH-DCM-001`, `ADR-DCM-001`, `VER-DCM-001` -> `WO-DCM-001`.

- `INT-DCM-001`: make every pending decision a governed, blocking artifact.
- `CAP-DCM-001`: raise, block on, and dispose governed decisions.
- `REQ-DCM-001`: an open decision blocks the transitions it names.
- `REQ-DCM-002`: the accountable role disposes a decision with a verbatim
  option.
- `REQ-DCM-003`: an accepted deviation stays visible until the rule changes.
- `SPEC-DCM-001`: the decision artifact contract (fields, kinds, relations,
  lifecycle, gate, command, decision right, diagnostics, projection).
- `ARCH-DCM-001` and `ADR-DCM-001`: the gating architecture and the decision
  to model pending decisions as a blocking artifact rather than prose, an
  event, or a field.
- `VER-DCM-001`: the evidence contract.
- `WO-DCM-001`: the bounded implementation in the candidate; the root adopts
  at the next release adoption.

The risk artifact is not part of this domain; the owner manages it
separately and afterward.

On 2026-09-03 the repository owner instructed the creation of this packet
after reviewing the proposal, then approved all ten artifacts the same day
with the instruction "i approve with execution delegation" (PR #329). The
approved packet is on `main`; `WO-DCM-001` carries the delegation class, so
the execution travels the delegated route from here: the delegated start
follows once the required `validate` check is green at the execution
branch's head, and completion and record preparation follow the same gate.
The verification decision on the record, merge, release and publication
stay human.

## Execution

`WO-DCM-001` started on 2026-09-03 under the delegated route on the branch
`wo/dcm-001-execution` (PR #330). The implementation is candidate source:
`se_harness/decisions.py` and the `decide` command, the `decision` lifecycle
family and the per-gate `QGP-*-DECISION` predicates in both contract copies,
the validator's decision rules and standing-deviation projection, the
`DECISION.template.md` template and layout registry entry, the Explorer's
in-flight tile, record panel and metrics, and `tests/test_decision_management.py`.
The reader's note is `docs/notes/decision-artifacts.md`; the command is in
`docs/notes/harnessctl-reference.md`. `SPEC-DCM-001` carries one amendment
record: the single predicate it names is implemented as one predicate per
gate. The root managed copies are unchanged until the next release adoption.
