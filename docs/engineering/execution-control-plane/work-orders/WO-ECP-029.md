+++
id = "WO-ECP-029"
type = "work_order"
title = "Wave 1, group B: remove the adopt alias after its one release"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[assurance]
commit_bound_verification = "required"
rationale = "The change removes a registered command name from the public CLI and closes approved rules by amendment; the release after it ships the result to every consumer."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/cli.py",
  "tests/test_cli_shape.py",
  "tests/test_harnessctl.py",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-031.md",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-033.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-020.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-022.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-022.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-024.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-029.md",
]

[relations]
implements = ["REQ-ECP-033"]
specifications = ["SPEC-ECP-022"]
verification = ["VER-ECP-024"]
+++

# Work Order: Wave 1, group B: remove the adopt alias after its one release

## Lifecycle

Draft. Approval is the engineering owner's decision; it approves no
definition. Commit-bound verification is `required`. No `architecture`
relation, as `WO-ECP-025` to `WO-ECP-027`.

## Objective

Execute rules `ECP-DEL-015` to `ECP-DEL-019` of `SPEC-ECP-022`: the alias
window `WO-ECP-026` opened on 2026-09-06 closes. The 0.16.0 verifier, now
this repository's root, runs `init` in its `adopt` scenario, so the released
verifier no longer calls the name, and `REQ-ECP-030`'s one-release rule is
met.

## In scope

- `se_harness/cli.py`: the `adopt` parser block out; `init` is the one
  installation command.
- `tests/test_cli_shape.py`: `adopt` out of the repository-command set;
  `tests/test_harnessctl.py`: the alias test out.
- `docs/notes/harnessctl-reference.md`: the `adopt` row and synopsis line
  out.
- Amendment records closing the alias window on `SPEC-ECP-020`,
  `REQ-ECP-031`, `VER-ECP-022` and `SPEC-ECP-016`.
- The domain index; this work order's evidence packet and its record.

## Out of scope

- `candidate_acceptance.SCENARIO_IDS`: the scenario id `adopt` stays so the
  acceptance contract digest does not move.
- Anything of groups A and C.

## Authorized decision envelope

The wording of the amendment records.

## Constraints

- No managed path moves.
- The suite, `validate`, `doctor` and the handoff check pass before
  completion.

## Expected change surface

Ten lines out of `cli.py`, one set literal, one test, two reference lines,
four amendment records, this packet.

## Required verification

Execute `VER-ECP-024` for group B; repository-required checks; the pull
request's lanes; the handoff check; a verification record bound to the
candidate commit.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-029/`.

## Stop and escalate conditions

The candidate-package lane failing on `adopt`: the released verifier still
calls the name, stop.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
