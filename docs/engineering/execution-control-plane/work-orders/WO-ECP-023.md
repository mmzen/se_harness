+++
id = "WO-ECP-023"
type = "work_order"
title = "The Git-derived handoff check self-binds in one run"
status = "approved"
owners = ["engineering-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the core checkpoint every governed change passes through and the digest CI compares; that is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow_compliance.py",
  "se_harness/cli.py",
  "tests/test_workflow_compliance.py",
  "docs/notes/harnessctl-check.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-028.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-017.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-019.md",
]

[relations]
implements = ["REQ-ECP-028"]
specifications = ["SPEC-ECP-017"]
verification = ["VER-ECP-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T07:44:38Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-31 by selecting the presented option 'Approve and start WO-ECP-023', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the compliance module's rebind helper and change-set union, the check handler's writes and refusal codes, the compliance test module, the two notes, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file, no verification record, no release and no publication. Start preflight has not been run."
+++

# Work Order: The Git-derived handoff check self-binds in one run

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make `check --checkpoint handoff --from-git BASE` self-binding
(`ECP-SBH-001` to `ECP-SBH-006`): the run rebinds an existing packet header
to the current formal snapshot before evaluating, and evaluates the change
set united with the retained result path, so one run is the declared,
digest-stable result. Issue #280, part b — the last open part of the
assessment's top-impact finding.

## Why now

The handoff digest is only stable after two runs, because the first run's
retained `handoff.json` joins the second run's change set; and after every
merge from the base branch the packet must be re-bound by hand or
`QGP-G4I-EVIDENCE` reads `not_assessable`. Issue #280 measures the cost on
WO-ECP-020: two of fifteen commits existed only for these mechanics. Parts
a and c are merged (PRs #293, #294); this part must be in the 0.12.0
candidate for the release (#284) to retire the trap for every consumer.

## In scope

- `se_harness/workflow_compliance.py`: the rebind helper reusing the
  packet parser, renderer and line-ending guard; the self-binding step and
  the change-set union in `check_workflow`; the rebind entry in the
  result's writes.
- `se_harness/cli.py`: the retained-result write appended beside the
  rebind entry instead of replacing the writes list; the `WEX-ECP-0*`
  refusal codes of `check` preserved on the blocked result rather than
  relabelled `WEX210`.
- `tests/test_workflow_compliance.py`: cases for `ECP-SBH-001` to
  `ECP-SBH-006`, and the existing Git-derived expectations extended with
  the retained result path.
- `docs/notes/harnessctl-check.md` and `docs/notes/harnessctl-reference.md`:
  the self-binding behaviour replacing the two-run and manual-rebind
  descriptions.
- This domain's index and the evidence packet.

## Out of scope

The `evidence` command and packet creation; the `scope` checkpoint and the
declared change-set forms; the managed workflow template and the
hash-locked root files (the root evaluator keeps the two-run behaviour
until the next root adoption); the release that carries this change; every
other module the CLI normalisation (#282) rewrote.

## Authorized decision envelope

The name and placement of the rebind helper; whether the change-set union
is applied inside `git_change_set`'s caller or beside it; the exact wording
of messages, comments and the two notes; the names and placement of the
test cases.

## Constraints

- No contract file, result schema, selector rule or gate definition
  changes.
- `result_sha256` remains the digest of the canonical restitution block;
  nothing status-dependent enters that block from this work.
- The retained-result rules (`ECP-PRB-002`, `ECP-SCP-004`) and the
  `evidence` command's refusal codes are unchanged.
- Existing tests keep passing unmodified except where they pin the two-run
  change set.

## Expected change surface

Two product modules, one test module, two notes, the domain index, the
three definition artifacts of this packet, and the evidence packet.

## Required verification

Execute `VER-ECP-019` in full; repository-required checks; the handoff
check over the Git-derived change set, run under the governing 0.11.0 root
evaluator, whose released two-run behaviour on this repository is recorded
as expected.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-023/`.

## Stop and escalate conditions

Any need to touch a contract file, the result schema or a hash-locked
file; a digest instability the change-set union does not close (a third
state the fixed point does not reach); a test that pins the two-run
behaviour for a reason other than the mechanics this work order removes.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
