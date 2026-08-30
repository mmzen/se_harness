+++
id = "WO-ECP-022"
type = "work_order"
title = "Normalise the harnessctl command shape"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the public CLI of every subcommand, the exit codes scripts rely on and the codes records cite; later decisions depend on the exact candidate behaviour."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/provenance.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "tests/test_harnessctl.py",
  "tests/test_workflow_execution.py",
  "tests/test_release_qualification.py",
  "tests/test_artifact_authoring.py",
  "tests/test_artifact_renumbering.py",
  "tests/test_recovery_rehearsal.py",
  "tests/test_evaluator_identity.py",
  "tests/test_revision_provenance.py",
  "tests/test_progressive_documentation.py",
  "tests/test_cli_shape.py",
  "tests/test_instruction_architecture.py",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-027.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-018.md",
]

[relations]
implements = ["REQ-ECP-027"]
specifications = ["SPEC-ECP-016"]
verification = ["VER-ECP-018"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-30T16:56:30Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-30 with the words 'Approve and start WO-ECP-021', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: cli.py and provenance.py (the workflow modules only for a leading-code strip), the nine test modules including the new tests/test_cli_shape.py, the two notes, this domain's index and the evidence packet. It authorizes no change to the schema-2 result, any gate, procedure, contract file, skill or hash-locked root file, preflight's --work-order, rehearse-recovery's shape, any verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-30T16:56:37Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-30, 'Approve and start WO-ECP-021'. Start preflight PASS with no diagnostics over the approval commit 4e3a584 carrying unmoved main 7cac025, run with the governing exact public 0.11.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-30T18:55:27Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-30 with the words 'Mark WO-ECP-021 implemented'. The evidence packet at docs/engineering/execution-control-plane/evidence/WO-ECP-022/ records: ECP-CLI-001 to ECP-CLI-009 implemented (the pinned target classification, prepare-release --owner with the --authorized-by guard, --json on every subcommand with the command-result object and every existing JSON shape unchanged, the 0/1/2 exit rule with failed results on standard output, one code per line, the four cause classes raised in the provenance module with a mutation-guard refusal as an exit-2 environment refusal, thirteen CLI-shape tests, the reference's rules section); the in-scope suites 471 OK plus the amended module 30 OK; the full Windows suite at its baseline; validate 1177 artifacts, 0 errors, doctor 0 FAIL, distributions PASS under the 0.11.0 root; the handoff check completed at its fixed point 516e2e4f over main 7cac025 and the thirteen pull-request lanes green at the packet head 8f1cdfd. The scope amendment of 2026-08-30 (tests/test_instruction_architecture.py, three assertions from standard error to standard output) is recorded on this work order and accepted with this decision; the requirement's two stated exclusions (preflight --work-order, rehearse-recovery's shape) stand. This decision authorizes no verification record, no release and no publication."
+++

# Work Order: Normalise the harnessctl command shape

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make every subcommand follow one shape: the target classification pinned
(`ECP-CLI-001`), `--owner` on `prepare-release` (`ECP-CLI-002`), `--json`
on every command with one command-result object (`ECP-CLI-003`), the
`0`/`1`/`2` exit rule with failed results on stdout (`ECP-CLI-004`,
`ECP-CLI-005`), one code per line (`ECP-CLI-006`), one cause per code for
the two record commands (`ECP-CLI-007`), CLI-level tests for the five
uncovered commands (`ECP-CLI-008`) and the reference's rules section
(`ECP-CLI-009`). Issue #282, functional assessment of 2026-08-30.

## Why now

Head of the assessment's critical path: `#280b` (the self-binding
handoff) rewrites the same modules and must follow, and `#281b` (the
generated code index) must not index `WEX301` before it is split.

## In scope

- `se_harness/cli.py`: the `--json` renderings and the command-result
  helper; the `--authorized-by` guard and `--owner`; the exit-code and
  stdout rule in `_capture_verification` and `_prepare_release`; the code
  split in `_project` and the two record handlers.
- `se_harness/provenance.py`: refusal classes carrying their code.
- `se_harness/workflow.py`, `se_harness/workflow_compliance.py`: only if
  `failed_result` or the remediation result must strip a leading code.
- Tests named in the scope; `tests/test_cli_shape.py` is new and holds
  the parser-classification, exit-code, stdout, one-code and five-command
  tests.
- The two notes; this domain's index; the packet.

## Out of scope

`preflight --work-order` and `rehearse-recovery`'s shape (stated in the
requirement); any change to the schema-2 result, a gate, a procedure, a
contract file, a skill or a hash-locked root file; the release carrying
this change.

## Authorized decision envelope

The exact member names inside each command result within `ECP-CLI-003`'s
list; test names; the wording of the reference section.

## Constraints

- Every existing `--json` shape is byte-for-byte unchanged for the same
  input.
- No hash-locked root file moves.

## Expected change surface

Two to four product modules, nine test modules (one new), two notes, the
packet and the index.

## Required verification

Execute `VER-ECP-018` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-022/`.

## Stop and escalate conditions

Any need to change a schema-2 field, a skill core, a contract file or a
hash-locked file; any existing JSON consumer test that can only pass by
changing the consumer.

## Scope amendment

2026-08-30, after start, on the engineering owner's decision 'Amend
WO-ECP-021 scope with tests/test_instruction_architecture.py': that
module is added to the execution scope. Three of its tests assert the
refused `upgrade --apply` message on standard error; `ECP-CLI-005` moves
every failed result to standard output, so the three assertions read
standard output. The amendment adds no other work and no product path; the
evidence packet is bound after this edit.

## Identifier renumbering

2026-08-30, after completion, on the engineering owner's decision
'Renumber the command-shape chain to WO-ECP-022': a parallel session
drafted a different chain for issue #280c and, both sessions having read
the same free identifier space, took the same four identifiers
(`REQ-ECP-026`, `SPEC-ECP-015`, `VER-ECP-017`, `WO-ECP-021`); that chain
merged to `main` first with a verified record and is immutable. This chain
is therefore renumbered to `REQ-ECP-027`, `SPEC-ECP-016`, `VER-ECP-018`
and `WO-ECP-022`, files, evidence directory, index rows and citations
included. The owner's quoted decision phrases in the lifecycle events
above keep their original words: they name the identifier as it was when
each decision was taken. `renumber-artifacts` refused the whole plan at
inventory (`REN043` on the unrelated `VREC-WEX-001`), so the renumbering
is by hand; that refusal is a finding of this packet. No content beyond
the identifiers changes.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
