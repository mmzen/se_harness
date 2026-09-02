+++
id = "WO-ECP-025"
type = "work_order"
title = "Delete the three CLI tombstone guards"
status = "draft"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[assurance]
commit_bound_verification = "required"
rationale = "The change touches the CLI entry point every invocation passes through and closes approved rules by amendment; the release after it ships the result to every consumer."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "tests/test_workflow_execution.py",
  "tests/test_release_qualification.py",
  "tests/test_cli_shape.py",
  "docs/notes/harnessctl-check.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/release-qualification-roles.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-024.md",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-030.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-013.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-014.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-019.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-013.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-016.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-021.md",
]

[relations]
implements = ["REQ-ECP-030"]
specifications = ["SPEC-ECP-019"]
verification = ["VER-ECP-021"]
+++

# Work Order: Delete the three CLI tombstone guards

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

## Objective

Close issue #310 (assessment item #285c): delete the `focus`, `next` and
`accept-candidate` pre-parse guards from `main()` in `se_harness/cli.py`
(`ECP-TMB-001`, `ECP-TMB-002`), delete their refusal tests and keep the
absence assertions with a source-reading test (`ECP-TMB-003`), make the
three notes state the plain refusal (`ECP-TMB-004`), and close the rules
that described the guards by dated amendment record (`ECP-TMB-005`). The
`--authorized-by` guard is included only if the approving owner says so
(`ECP-TMB-006`); the approval reason records the choice.

## In scope

- `se_harness/cli.py`: the three guard blocks and their comments out of
  `main()`; nothing else in the module moves.
- `tests/test_workflow_execution.py`, `tests/test_release_qualification.py`:
  the three refusal tests replaced by one absence test that reads `--help`
  and `main()`'s source; `tests/test_cli_shape.py` only if
  `--authorized-by` is included.
- The three notes; the amendment records on `REQ-ECP-024`, `SPEC-ECP-013`,
  `SPEC-ECP-014`, `VER-ECP-013`, `VER-ECP-016` (and `SPEC-ECP-016` if
  included); the domain index; this work order's evidence packet.

## Out of scope

- Any other one-release acceptance the specifications name (the
  whole-tree digest and `--changed-path` forms of `SPEC-ECP-001`, the
  substring-matched evidence of `SPEC-ECP-002`, the `--decision` form of
  `SPEC-ECP-004`): each is a separate observation for its own work order.
- Any registered command, option, result schema, contract JSON, managed
  template, release or publication.

## Authorized decision envelope

The shape of the absence test; the wording of the amendment records and
the note sentences.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- The suite, `validate`, `doctor` and the handoff check over the
  Git-derived change set pass before completion.

## Expected change surface

About thirty lines out of `cli.py`, three tests replaced by one, three
note sentences, six or seven short amendment records, this packet.

## Required verification

Execute `VER-ECP-021` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-025/`.

## Stop and escalate conditions

A suite failure beyond the baseline that the change explains; any need to
touch a registered command; any managed path in the change set.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
