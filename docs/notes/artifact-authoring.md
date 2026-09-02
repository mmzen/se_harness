# Artifact authoring

<!-- Target expertise: 5/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> Non-authoritative operator guidance. The installed harness, the exact released
> evaluator, the formal artifacts, and accountable decisions remain authoritative.

`docs/engineering/ARTIFACT_AUTHORING.md` is the managed policy that says how
each formal artifact type is written. It has one section per type with a
checklist (what a reviewer checks) and guidance (how to think about it).
Rules the tool can enforce are marked *mechanical* and live in the validator
or a gate; the rest are judgement rules.

## Where you meet it

- `harnessctl create-artifact` prints the checklist for the type it just
  created; `--quiet` suppresses it.
- The managed router lists it under "Authoring rules for formal artifacts".

## Requirements

The requirement template offers the five EARS shapes — always, event
(`WHEN`), state (`WHILE`), unwanted (`IF … THEN`), optional feature
(`WHERE`) — and asks for one obligation per requirement. The validator
signals, as maintenance warnings that never block:

- `W-AUT-001` — the statement opens with none of the five shapes;
- `W-AUT-002` — the statement carries more than one `SHALL`;
- `W-AUT-003` — the statement is longer than 300 characters;
- `W-AUT-004` — `verification_method` is still a free-text string.

`verification_method` may now be an array from `test`, `analysis`,
`inspection`, `demonstration`, with free text in `verification_notes`; the
one-time migration of existing strings and the approval predicates against
leftover placeholders and open decisions are `WO-AUT-002`. Three optional
attributes are validated when present: `priority` (`must`, `should`,
`could`), `source`, and `measure`.

The template body is six headings: Rationale, Behavior (trigger, response,
on failure), Assumptions and dependencies, Acceptance examples, Open
decisions. Executable scenarios go to `acceptance/<REQ-ID>.feature` and are
named by the verification contract.

## Approval predicates and the migration

Two predicates, `QGP-G1-AUTHORING` and `QGP-G2-AUTHORING`, fail a definition's
approval when the file still carries a template placeholder (`<…>` outside
code) or when its `Open decisions` section says anything but `None`. They
are evaluated by `harnessctl transition` when a definition leaves `draft`.

`scripts/migrate_verification_methods.py` maps free-text
`verification_method` strings to the closed vocabulary and keeps the original
in `verification_notes`. It is a dry run by default and prints a mapping
report; `--apply` writes. It has not been run on this repository: the
released 0.6.0 evaluator that governs it requires the string form. Running
it, and promoting the string form from `W-AUT-004` to an error, belong to the
transaction that adopts a released successor as this repository's evaluator.

## Why a policy and not a skill

`ADR-AUT-001`: rules in a skill apply only while the skill runs; rules in a
managed policy apply on every route, and rules in the validator apply
whether anyone read the policy or not. No per-type writing skill is planned.
