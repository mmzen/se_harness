+++
id = "WO-ECP-025"
type = "work_order"
title = "Delete the four CLI tombstone guards, by the delegated route"
status = "in_progress"
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

[delegation]
class = "execution"

[relations]
implements = ["REQ-ECP-030"]
specifications = ["SPEC-ECP-019"]
verification = ["VER-ECP-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T14:38:23Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-02 by selecting the presented options 'Include the --authorized-by guard too' and 'Delegated route (the delegation class)', as a decision distinct from the approval of its definitions in the same transaction. This approval is the delegating act under DR-007 and DR-015: the work order carries [delegation] class = 'execution', so DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE may be applied by the delegated-executor role while the required validate check is success for the exact candidate head, read from the base of the pull request through the gate WO-ECP-024 configured. It authorizes only the declared scope: the four guard blocks out of main(), the tests, the three notes, the seven amendment records, the domain index and the evidence packet. It authorizes no registered command change, no managed path, no verification decision, no release and no publication; the merges remain the owner's decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-02T14:47:47Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 68af51fa014b64e89cc22fe19081de2c5200f696 (check-run 100294830645, source github-checks)."
+++

# Work Order: Delete the four CLI tombstone guards, by the delegated route

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006`; the gate configuration is the owner-content
`.engineering-harness.delegation.toml` of `WO-ECP-024`). The class is read
at the base of the pull request, so the approved packet merges to `main`
first and the execution follows on a second branch. The approval below, the
verification of the record it prepares, and every merge stay human
decisions. Commit-bound verification is `required`.

## Objective

Close issue #310 (assessment item #285c): delete the `focus`, `next` and
`accept-candidate` pre-parse guards from `main()` in `se_harness/cli.py`
(`ECP-TMB-001`, `ECP-TMB-002`), delete their refusal tests and keep the
absence assertions with a source-reading test (`ECP-TMB-003`), make the
three notes state the plain refusal (`ECP-TMB-004`), and close the rules
that described the guards by dated amendment record (`ECP-TMB-005`), and retire the
fourth guard of the same kind, `prepare-release --authorized-by`, the same
way (`ECP-TMB-006`), on the owner's decision of 2026-09-02.

## In scope

- `se_harness/cli.py`: the three guard blocks and their comments out of
  `main()`; nothing else in the module moves.
- `tests/test_workflow_execution.py`, `tests/test_release_qualification.py`:
  the three refusal tests replaced by one absence test that reads `--help`
  and `main()`'s source; `tests/test_cli_shape.py`'s `--authorized-by`
  refusal assertion becomes an unrecognized-argument assertion.
- The three notes; the amendment records on `REQ-ECP-024`, `SPEC-ECP-013`,
  `SPEC-ECP-014`, `SPEC-ECP-016`, `VER-ECP-013`, `VER-ECP-016`; the domain
  index; this work order's evidence packet with the delegated lifecycle
  events quoted back.

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

About forty lines out of `cli.py`, three tests replaced by one and one
assertion reworded, three note sentences, seven short amendment records,
this packet.

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
