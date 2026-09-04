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

The template body was six headings until `WO-TCM-005` (SPEC-TCM-003):
Rationale, Behavior, Assumptions and dependencies, Acceptance examples, Open
decisions. It is now four: `In plain words`, `Why`, `Behavior` (a table of
trigger, response, on failure) and `Examples` (one normal, one failure).
The acceptance cases live in the verification contract; the method lives in
the specification; pending decisions are `DEC-` artifacts, so the `Open
decisions` section is gone. Six more draft-time advisories guard the
budgets: `W-AUT-003` at 30 words for the statement, `W-AUT-005` body over
250 words, `W-AUT-006` Why over five sentences or 120 words, `W-AUT-007` a
sentence over 25 words, `W-AUT-008` more than three code identifiers,
`W-AUT-009` a missing or long In plain words, `W-AUT-010` a WHEN whose
event is the act of evaluating. Approved requirements are not rewritten.

## Intents

`WO-TCM-007` (SPEC-TCM-004) gave the intent the same treatment. The template
has four sections, `In plain words`, `Problem`, `Success measures` (a table
of measure, today, when reached, observed) and `Not this`, and a front-matter
`outcome`: one sentence naming who can do or observe what after delivery,
which the Explorer shows under the title. Actors belong to the capability,
principles to a specification or an ADR, risks and open questions to their
own artifacts. Draft-time advisories guard it: `W-AUT-011` a missing, long
or solution-naming outcome, `W-AUT-012` Problem over five sentences or 120
words, `W-AUT-013` a success measure observed by a CI run, test, validator,
verification or implementation review (an acceptance check, which belongs
in the verification contract), `W-AUT-014` a measures table with no row,
`W-AUT-015` a repository path or source line range cited in the body; the
shared `W-AUT-005`, `W-AUT-007`, `W-AUT-008` and `W-AUT-009` fire on intent
drafts with the intent budgets (200 words, 25 words, two identifiers). An
`outcome` that is present but empty is `E-AUT-002`. Approved intents are not
rewritten; the Explorer's G0 intent-quality condition reads `satisfied` only
for an intent that carries an outcome and at least one measure row.

## Approval predicates and the migration

Two predicates, `QGP-G1-AUTHORING` and `QGP-G2-AUTHORING`, fail a definition's
approval when the file still carries a template placeholder (`<…>` outside
code) or when a legacy `Open decisions` section says anything but `None`
or a list of `DEC-` identifiers. They
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
