+++
id = "WO-ECP-020"
type = "work_order"
title = "Remove the next alias"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change removes a public CLI command; that is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "tests/test_workflow_execution.py",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-025.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-014.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-016.md",
]

[relations]
implements = ["REQ-ECP-025"]
specifications = ["SPEC-ECP-014"]
verification = ["VER-ECP-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T20:46:21Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-ECP-020', on the owner's decision 'we remove next now' of the same day. The definitions it implements are REQ-ECP-025, SPEC-ECP-014 and VER-ECP-016 as amended by the records drafted under this work order. Authorizes start preflight and then only the declared scope: the next parser, handler and notice removed behind a guard naming check, the alias test made a refusal test, the reference and check notes, the three amendment records, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file, WORKFLOW.json, any skill, contract file or profile, any verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T20:47:24Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve and start WO-ECP-020'. Start preflight PASS with no diagnostics over d936295, stacked on WO-ECP-019's completion commit ee1e6af, after the unrelated architecture relations were removed (W021, W017), run with the governing exact public 0.11.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Remove the next alias

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Close the alias window `WO-ECP-019` opened before it ships: delete the
`next` subcommand behind a pre-parse guard that names `harnessctl check`,
drop its reference row and the notes' mention of the window, and record
the owner's decision as amendment records on `REQ-ECP-025`, `SPEC-ECP-014`
(`ECP-CTX-004` becomes the refusal, `ECP-CTX-007` loses the alias row) and
`VER-ECP-016` (the alias row becomes a refusal row).

## Why now

The owner's decision of 2026-08-29, "we remove next now", on the finding
that the managed `WORKFLOW.md` and the evaluator always travel together,
so no root instruction ever names `next` against an evaluator that lacks
it; the alias would only have served consumer-owned content, and the
audit's goal was one name. Doing it before the release after 0.11.0 means
no release ever ships the notice.

## In scope

- `se_harness/cli.py`: the `next` parser, `_next` and the notice removed;
  the guard beside the `focus` and `accept-candidate` guards.
- `tests/test_workflow_execution.py`: the alias test becomes the refusal
  test; the word census asserts no `next` row.
- `docs/notes/harnessctl-reference.md`, `harnessctl-check.md`.
- The three amendment records; the packet; this domain's index.

## Out of scope

`workflow.py`, `workflow_compliance.py`, the template `WORKFLOW.md` (already
on `check`); any contract file, skill or profile; any hash-locked root
file; any historical record; the release carrying this change.

## Authorized decision envelope

The wording of the guard's message and of the notes; test names.

## Constraints

- `check`'s bytes are unchanged.
- No retained rule text is edited except as the amendment records state.

## Expected change surface

One product module, one test module, two notes, three amendment records,
the packet and the index.

## Required verification

Execute `VER-ECP-016` as amended; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-020/`.

## Stop and escalate conditions

Any hash-locked file in the change set; any need to touch `WORKFLOW.json`,
a skill contract or a profile.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
