+++
id = "WO-TCM-010"
type = "work_order"
title = "Correct the first example of SPEC-TCM-006 by record"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[assurance]
commit_bound_verification = "not_required"
rationale = "One example sentence of an approved specification is corrected by record, with an amendment record naming the finding; no rule, constant, template, code or test changes, and the candidate validator already proves the behaviour the corrected example describes (VER-TCM-006, VREC-TCM-009 verified)."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/technical-communication/specifications/SPEC-TCM-006.md",
  "docs/engineering/technical-communication/README.md",
  "docs/engineering/technical-communication/work-orders/WO-TCM-010.md",
  "docs/engineering/technical-communication/evidence/WO-TCM-010/",
]

[relations]
implements = ["REQ-TCM-014"]
specifications = ["SPEC-TCM-006"]
verification = ["VER-TCM-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T13:47:44Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable repository owner on 2026-09-06 with the instruction 'I approve WO-TCM-010' after reviewing PR #364: one example sentence of SPEC-TCM-006 corrected by record with an amendment record, commit-bound verification not required. WO-TCM-010 carries no delegation class; its start and completion are the engineering owner's explicit acts on the same instruction."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-06T13:47:51Z"
decided_by = "engineering-owner"
reason = "Started by the accountable engineering owner on 2026-09-06 on the owner's instruction 'I approve WO-TCM-010' (PR #364), which the pull request stated would be followed by the start, the amendment and the completion on the same branch. Start preflight PASS under exact 0.15.0."
+++

# Work Order: Correct the first example of SPEC-TCM-006 by record

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `not_required`:
the change is one example sentence and an amendment record.

## Objective

`WO-TCM-009`'s evidence packet (disclosure 1) found that the first example
of `SPEC-TCM-006`, "a draft written as this specification is draws no
advisory", is false: read as a draft by the candidate validator, the
specification's rules `TCM-RFS-003`, `-010`, `-012`, `-014` and `-018` run
to 31 to 39 words and draw `W-AUT-021`, and a 40-word sentence in `Scope`
draws `W-AUT-007`. Replace the example with one that is true of the shape
the specification prescribes, and record in an amendment record that the
five rules stand as written because `TCM-RFS-023` forbids a shape rewrite
of an approved specification.

## In scope

- The first `Examples` entry of `SPEC-TCM-006`, rewritten to describe a
  draft in the prescribed shape within every budget, so that the example
  is a true statement the tests of `VER-TCM-006` already prove.
- An `## Amendment record` section on `SPEC-TCM-006` naming this work
  order, the finding, and the five rules left as written.
- This domain's index.

## Out of scope

Any change to a rule's text, identifier or the coverage table; any change
to the template, the validator, the generator or the Explorer; a record.

## Authorized decision envelope

The wording of the corrected example and of the amendment record.

## Constraints

- The rules section is unchanged byte for byte.
- The corrected example names only behaviour the candidate tests prove.

## Expected change surface

`SPEC-TCM-006.md` (one example and a new amendment record) and this
domain's index.

## Required verification

The released-evaluator `validate` and `preflight`; the handoff check over
the Git-derived change set; a read of the corrected example against
`test_a_reader_first_draft_within_every_budget_raises_no_advisory`.

## Evidence to record

`docs/engineering/technical-communication/evidence/WO-TCM-010/`: the
handoff packet the gate requires at the handoff checkpoint. Scope amended
on 2026-09-06 by the repository owner, who selected "Amend the scope" when
the executor reported that the draft had omitted the evidence directory;
commit-bound verification remains not required.

## Stop and escalate conditions

Any need to change a rule; any advisory or error raised by the released
evaluator on the amended specification.

## Completion report format

The changed-path ledger and the handoff `check` restitution; the
completion decision is the engineering owner's.
