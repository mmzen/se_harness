+++
id = "WO-ECP-015"
type = "work_order"
title = "Fold focus into check: the checkpoint-less projection, one name in every contract"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the public CLI, the workflow contract every consumer installs and a shipped skill; each is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_result.py",
  "se_harness/workflow_contract.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/.agents/skills/harness-orient/",
  "templates/repository/standard/.claude/skills/harness-orient/",
  "tests/",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/harness-overview.md",
  "README.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-022.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-011.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-011.md",
  "docs/engineering/execution-control-plane/architecture/adr/ADR-ECP-007.md",
  "docs/engineering/execution-control-plane/architecture/ARCH-ECP-001.md",
]

[relations]
implements = ["REQ-ECP-022"]
specifications = ["SPEC-ECP-011"]
architecture = ["ARCH-ECP-001", "ADR-ECP-007"]
verification = ["VER-ECP-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T11:07:05Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-ECP-015', as a decision distinct from the approval of its definitions and of ADR-ECP-007 seconds earlier, and after the ARCH-ECP-001 amendment that addresses REQ-ECP-022. Authorizes start preflight and then only the declared scope: the checkpoint-less check projection, the byte-identical focus alias, the contract steps and WFL-003, the harness-orient skill, tests, the notes and README, this domain's index and the evidence packet. It authorizes no change to a hash-locked root file of this repository, no verification record, no release and no publication. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T11:07:12Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve and start WO-ECP-015'. Start preflight PASS with no diagnostics over the approval commit 3222e4e carrying unmoved main 5e5e9d6, run with the governing exact public 0.10.0 evaluator outside the checkout, on this Windows checkout. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Fold focus into check: the checkpoint-less projection, one name in every contract

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make `harnessctl check` without `--checkpoint` return the projection
`focus` returns today (`ECP-ONE-001` to `ECP-ONE-003`); keep `focus` for
one release as a byte-identical alias with a deprecation notice
(`ECP-ONE-004`, `ECP-ONE-005`); rename the five procedure steps' argv and
`WFL-003` to `check` (`ECP-ONE-006`); point the shipped `harness-orient`
skill at `check` (`ECP-ONE-007`); update the notes and the README
(`ECP-ONE-008`); record the amendments on `SPEC-ECP-001` and
`ARCH-ECP-001`.

## Why now

The owner's challenge of 2026-08-29 has a measured answer — `focus` is
`check` with no checkpoint — and the repository just adopted 0.10.0, so
the change rides the next ordinary release (candidate 0.11.0) and reaches
this repository's own procedures through the following root adoption.

## In scope

- `se_harness/cli.py`: `check --checkpoint` becomes optional; the
  checkpoint-specific options are refused without one; `focus` dispatches
  to the same projection and prints the notice on standard error.
- `se_harness/workflow.py` / `workflow_compliance.py`: the projection is
  one function serving both entry points; `operation.kind` per
  `ECP-ONE-002`.
- `workflow_contract.json` and the template `WORKFLOW.json` (byte-identical):
  the five steps' argv; `WORKFLOW.md`: `WFL-003`, the procedure table, the
  lifecycle-decision steps, and the `next`-or-`focus` sentence.
- `harness-orient`: `orient.py` invokes `check`; `SKILL.md`,
  `skill-contract.json` and the Claude adapter follow where they name the
  command or pin the script.
- Tests: the identity cases per state, the refusals, the alias fixture, the
  contract and skill assertions; every existing assertion kept.
- `docs/notes/harnessctl-reference.md`, `harnessctl-check.md`,
  `harness-overview.md`, `README.md` command block.
- The `## Amendment record` on `SPEC-ECP-001` (`ECP-NXT-004`) and on
  `ARCH-ECP-001` (addresses `REQ-ECP-022`, conforms to `SPEC-ECP-011`); the
  domain index; the evidence packet.

## Out of scope

Removing the alias (a later work order after one release); `harnessctl
next`; any gate, predicate, lifecycle state or decision right; any
hash-locked root file of this repository (its installed contracts follow
at the next root adoption); the release that carries this change.

## Authorized decision envelope

The exact wording of the notice and of the amendment records; whether the
alias is implemented as an argparse alias or a thin handler; the placement
of the new tests; the README sentence.

## Constraints

- `focus`'s stdout and `--json` bytes do not change during the alias window.
- No step identifier or gate binding changes in `WORKFLOW.json`.
- `se_harness/workflow_contract.json` stays byte-identical to the template.
- Hash-locked root files do not move.

## Expected change surface

Four product modules, the contract in two copies, one managed policy
document, the orient skill files, tests, three notes, the README, the two
amendment records, the packet and the evidence.

## Required verification

Execute `VER-ECP-011` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-015/`.

## Stop and escalate conditions

An existing `focus` byte that would have to change inside the alias
window; a consumer-visible refusal that `focus` did not raise; a step
identifier or gate binding that would have to move; any need to touch a
hash-locked file.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
