+++
id = "WO-ECP-021"
type = "work_order"
title = "Normalise the harnessctl command shape"
status = "draft"
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
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
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

Execute `VER-ECP-017` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-021/`.

## Stop and escalate conditions

Any need to change a schema-2 field, a skill core, a contract file or a
hash-locked file; any existing JSON consumer test that can only pass by
changing the consumer.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
