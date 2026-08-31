+++
id = "WO-ECP-021"
type = "work_order"
title = "The managed lane reads the live pull-request body"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the managed workflow every consumer runs on every pull request; that is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "tests/test_ci_pipeline.py",
  "tests/test_instruction_architecture.py",
  "AGENTS.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-026.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-015.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-017.md",
]

[relations]
implements = ["REQ-ECP-026"]
specifications = ["SPEC-ECP-015"]
verification = ["VER-ECP-017"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T17:07:52Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-30 by selecting the presented option 'Approve and start WO-ECP-021', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the template workflow's permission, fetch-and-reduce step and selector event path, the two test modules, the AGENTS.md trap note, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file, no verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-30T17:08:26Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-30, taken by selecting the presented option 'Approve and start WO-ECP-021'. Start checkpoint Completed with every gate pass over the approval commit e4bf728 on branch wo/ecp-live-pr-body carrying unmoved main 7cac025, run with the governing exact public 0.11.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-30T18:09:03Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-30 under DR-WO-COMPLETE, by selecting the presented option 'Mark WO-ECP-021 implemented', on the handoff check reading Completed over the Git-derived change set at its fixed point 531a113c, no scope amendment. The evidence packet at docs/engineering/execution-control-plane/evidence/WO-ECP-021/ records: the template lane's live-body read (ECP-LPB-001 to -006) with the stored event payload gone from the template, the template assertions and the selector cases over the reduced shape, the AGENTS.md trap restated for both lanes, the domain index rows; the affected suites 55 and 81 OK, the full Windows suite at its baseline (1155 tests, one known test_artifact_authoring error), validate 0 errors, doctor 0 FAIL, release distributions PASS, all under the 0.11.0 root outside the checkout. The hash-locked root lane is unchanged and keeps the stored-payload behaviour until the next root adoption. No deviations. This decision authorizes no verification record, no release and no publication."
+++

# Work Order: The managed lane reads the live pull-request body

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make the standard template's managed pull-request lane select the
`Harness-Work-Order` and `Harness-Restitution` declarations from the pull
request's current body, fetched from the hosting API during the run, instead
of from the stored event payload (`ECP-LPB-001` to `ECP-LPB-006`), so that a
corrected body is honoured by a re-run without a new push. Issue #280,
part c.

## Why now

A body corrected after the trigger leaves the managed check red until a
no-op push refreshes the stored payload; PR #277 needed exactly that push,
and `AGENTS.md` carries the behaviour as a trap. The assessment of
2026-08-30 ranks the fix in Wave 1: it must be in the template before the
0.12.0 release for any root to ever adopt it, and it touches no module the
CLI normalisation (#282) rewrites.

## In scope

- `templates/repository/standard/.github/workflows/engineering-harness.yml`:
  the `pull-requests: read` permission; the guarded fetch-and-reduce step
  writing `$RUNNER_TEMP/live-event.json`; both `select-work-order`
  invocations reading that file; the header comment naming the live read.
- `tests/test_ci_pipeline.py`: assertions for `ECP-LPB-001` to
  `ECP-LPB-004` and `ECP-LPB-006` over the template bytes.
- `tests/test_instruction_architecture.py`: selector cases over
  test-written files in the live event file's shape (`ECP-LPB-005`).
- `AGENTS.md` (owner region): the stored-payload trap restated as the
  root-lane behaviour until the next root adoption, beside the template
  lane's re-run recovery.
- This domain's index and the evidence packet.

## Out of scope

The hash-locked root copy of the workflow (this repository's own lane keeps
the stored-payload behaviour until the next root adoption); the selector
module `se_harness/github_ci.py`; the self-binding handoff (#280b) and the
CLI normalisation (#282); every other workflow file; the release that
carries this change.

## Authorized decision envelope

The exact wording of the step name, its log line and the header comment;
whether the fetch uses one combined step or a fetch line and a reduce line
inside it; the names and placement of the test cases; the exact wording of
the `AGENTS.md` trap note.

## Constraints

- No selector rule, evaluator module, contract file or result schema
  changes.
- Hash-locked root files of this repository do not move.
- The scope and handoff checks keep every input they have today; nothing
  a pull-request body carries becomes an input of `check`.
- Existing workflow tests keep passing unmodified except where a pinned
  string names the stored payload.

## Expected change surface

The template workflow, two test modules, the owner region of `AGENTS.md`,
the domain index, the three definition artifacts of this packet, and the
evidence packet.

## Required verification

Execute `VER-ECP-017` in full; repository-required checks; the handoff
check over the Git-derived change set; the pull request's lanes, with the
root lane's stored-payload behaviour still in force on this repository
recorded as expected.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-021/`.

## Stop and escalate conditions

Any need to touch a hash-locked file or the selector module; a hosting-API
behaviour that makes the live fetch unavailable to the workflow token on
fork pull requests; a test that pins the stored event payload for a reason
other than the selection this work order moves.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
