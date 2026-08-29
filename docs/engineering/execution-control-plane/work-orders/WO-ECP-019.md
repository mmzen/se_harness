+++
id = "WO-ECP-019"
type = "work_order"
title = "Fold next into the check projection and retire accept-candidate"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change removes a public CLI command, changes the digest of every projection result and edits a managed template; all are trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_result.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_compliance.py",
  "tests/test_release_qualification.py",
  "tests/test_standard_repository_lifecycle.py",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/release-qualification-roles.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-025.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-014.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-016.md",
]

[relations]
implements = ["REQ-ECP-025"]
specifications = ["SPEC-ECP-014", "SPEC-ECP-001"]
architecture = ["ARCH-ECP-001", "ADR-ECP-007"]
verification = ["VER-ECP-016"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T18:39:39Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-ECP-019', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the check parser and projection context, the next alias and its notice, the accept-candidate removal and guard, the correctives, the four test modules, the template WORKFLOW.md, the three notes, the SPEC-ECP-001 amendment record, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file, WORKFLOW.json, any skill, contract file or profile, qualify, the candidate-evidence workflow, any verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T18:40:20Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve and start WO-ECP-019'. Start preflight PASS with no diagnostics over the approval commit 7148b57 carrying unmoved main 970a0ae, run with the governing exact public 0.11.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Fold next into the check projection and retire accept-candidate

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make the checkpoint-less `check` projection the execution context
(`ECP-CTX-001` to `ECP-CTX-003`), keep `next` as a byte-identical alias
with a deprecation notice for one release (`ECP-CTX-004`), point every
corrective at `check` (`ECP-CTX-005`), remove the `accept-candidate`
subcommand behind a guard naming `qualify candidate-package`
(`ECP-CTX-006`), and make the template, the notes and `SPEC-ECP-001`'s
amendment record say so (`ECP-CTX-007`, `ECP-CTX-008`). Audit items P2 and
P3 of 2026-08-29.

## Why now

The `focus` window closed with `WO-ECP-017`; `next` is the last second
name for the projection, and opening its window now lets the release after
0.11.0 carry the notice. `accept-candidate`'s one-cycle window
(`REQ-REB-022`) closed three releases ago.

## In scope

- `se_harness/cli.py`: the `check` parser (`--artifact` optional without a
  checkpoint), the `next` alias and its notice, the `accept-candidate`
  removal and guard.
- `se_harness/workflow.py`: the context computed in the projection;
  `next_step` deleted. `se_harness/workflow_compliance.py`: the correctives.
  `se_harness/workflow_result.py`: the renderer, if the `Context` section
  depends on the operation kind.
- `tests/test_workflow_execution.py`, `tests/test_workflow_compliance.py`,
  `tests/test_release_qualification.py`,
  `tests/test_standard_repository_lifecycle.py`.
- `templates/repository/standard/docs/engineering/WORKFLOW.md` (two
  sentences); `docs/notes/harnessctl-reference.md`, `harnessctl-check.md`,
  `release-qualification-roles.md`.
- `SPEC-ECP-001` amendment record; the packet; this domain's index.

## Out of scope

The removal of the `next` alias (a later work order, after the window);
`WORKFLOW.json`, any skill, contract file or profile; `qualify`, the
`candidate_acceptance` module and the candidate-evidence workflow; any
root hash-locked file; any historical record; the release carrying this
change.

## Authorized decision envelope

The wording of the two guards' messages, the notice and the notes; test
names; whether the renderer needs a change or the context alone drives the
`Context` section.

## Constraints

- `check` with an explicit `--artifact` and a checkpoint is unchanged in
  arguments and bytes.
- No hash-locked root file moves; the root `WORKFLOW.md` stays at its
  0.11.0 bytes.
- No retained rule text in `SPEC-ECP-001` is edited.

## Expected change surface

Four product modules, four test modules, one template, three notes, one
amendment record, the packet and the index.

## Required verification

Execute `VER-ECP-016` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-019/`.

## Stop and escalate conditions

Any need to change `WORKFLOW.json`, a skill contract or a profile; any
hash-locked file in the change set; any existing candidate-evidence
workflow assertion that can only pass by editing the workflow.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
