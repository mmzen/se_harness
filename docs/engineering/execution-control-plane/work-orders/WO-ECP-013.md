+++
id = "WO-ECP-013"
type = "work_order"
title = "A scope checkpoint so the pull-request gate is green in every lifecycle state"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the checkpoint set of the evaluator, a shipped gate binding, and the managed workflow every consumer runs on every pull request; each is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow_contract.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_procedures.py",
  "se_harness/cli.py",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow_contract.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/.github/workflows/engineering-harness.yml",
  "templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-020.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-009.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-003.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-009.md",
  "docs/engineering/execution-control-plane/architecture/adr/ADR-ECP-006.md",
  "docs/engineering/execution-control-plane/architecture/ARCH-ECP-001.md",
]

[relations]
implements = ["REQ-ECP-020"]
specifications = ["SPEC-ECP-009"]
architecture = ["ARCH-ECP-001", "ADR-ECP-006"]
verification = ["VER-ECP-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T08:27:36Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'i approve the artifact packet and you can start WO-ECP-013', as a decision distinct from the approval of its definitions and of ADR-ECP-006 seconds earlier, and after the ARCH-ECP-001 amendment that addresses REQ-ECP-020. Authorizes start preflight and then only the declared scope: the scope checkpoint in the evaluator and its contracts, the managed workflow step, the managed policy documents, tests, the two notes, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file of this repository, no verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T08:28:01Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'you can start WO-ECP-013'. Start preflight PASS with no diagnostics over the approval commit e2f11b5 carrying unmoved main 1d19d17, run with the governing exact public 0.9.0 evaluator outside the checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
+++

# Work Order: A scope checkpoint so the pull-request gate is green in every lifecycle state

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Add the `scope` checkpoint to `harnessctl check` (`ECP-SCP-001` to
`ECP-SCP-005`), bind it in the quality-gates contract to the three scope
predicates of `QG-G4-IMPLEMENTATION-EVIDENCE` in every work-order state, and
make the managed workflow run it on every pull request, running the handoff
check and the digest comparison only while the work order is `in_progress`
(`ECP-SCP-006` to `ECP-SCP-009`); document the five checkpoints
(`ECP-SCP-010`); record the amendment on `SPEC-ECP-003`. Issue #255.

## Why now

Since the root moved to 0.9.0, every pull request of this repository is red
from its completion transition to its merge, and packet-only pull requests
are not scope-checked at all. Both were accepted as owner-disclosed reds on
#253 and #257; each further work order repeats it until this one ships and
a root adopts it.

## In scope

- `se_harness/workflow_contract.py`: `CHECKPOINTS` gains `scope`.
- `se_harness/workflow_compliance.py`: `check_workflow` accepts `scope`
  for a work order in any state, evaluates `QG-G4-IMPLEMENTATION-EVIDENCE`
  at it regardless of the selected rule, refuses a record with `WEX210`;
  `select_current_step` treats `scope` as `handoff` for step selection;
  `harnessctl evidence` keeps its four checkpoints.
- `se_harness/cli.py`: `check --checkpoint` choices gain `scope`; the
  retention of `handoff.json` stays bound to `handoff`.
- `QUALITY_GATES.json` (packaged and template, byte-identical): the gate
  declares `scope`; the three scope predicates declare `scope`; the other
  five declare the gate's previous three checkpoints. `QUALITY_GATES.md`
  and `WORKFLOW.md` name the five checkpoints; `WORKFLOW.json` is touched
  only if a test requires the checkpoint list there.
- The managed workflow step per `ECP-SCP-006` to `ECP-SCP-009`, and the
  pull-request template seed if its wording names the handoff check.
- Tests: per-state scope checks, the refused record, no `handoff.json` at
  scope, the step text, contract byte equality; every existing handoff test
  unchanged.
- `docs/notes/harnessctl-reference.md` and `docs/notes/harnessctl-check.md`
  updated for five checkpoints, the check note's tables carrying `scope`.
- The `## Amendment record` on `SPEC-ECP-003` for `ECP-GTE-001`,
  `ECP-GTE-002` and `ECP-GTE-004`; the domain index; the evidence packet.

## Out of scope

The formal snapshot's line-ending dependence (issue #256); the digest
preimage (`ECP-DIG-*`); any lifecycle state, decision right, rule or
procedure of `WORKFLOW.json`; any hash-locked root file of this repository
(its managed lane keeps the old step until the next root adoption); the
release that carries this change.

## Authorized decision envelope

Whether `select_current_step` gains a `scope` branch or aliases `handoff`;
the exact wording of the amendment record and of the step's log line; the
names and placement of the test cases; whether the pull-request template
seed needs a wording change.

## Constraints

- No predicate identifier or evaluator changes; `REQ-ECP-006` stays
  literally true.
- `se_harness/quality_gates_contract.json` and `workflow_contract.json`
  stay byte-identical to their template copies.
- Hash-locked root files of this repository do not move.
- The handoff checkpoint's behaviour and its retained result are unchanged.

## Expected change surface

Four product modules, two contract JSON files in two copies, two managed
policy documents, the managed workflow and possibly the seed, the tests,
two notes, the domain index, the amendment record and the packet.

## Required verification

Execute `VER-ECP-009` in full; repository-required checks; the pull
request's lanes with the old managed step's red at completion recorded as
expected; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-013/`.

## Stop and escalate conditions

A contract validator that rejects a fifth checkpoint name in a way the
schema cannot express; a test that pins the four-checkpoint set for a reason
other than enumeration; any need to touch a hash-locked file; a consumer
rehearsal in which the new step fails on an in-scope diff.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
