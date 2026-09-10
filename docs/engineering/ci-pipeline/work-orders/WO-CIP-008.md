+++
id = "WO-CIP-008"
type = "work_order"
title = "Issue #433, pipeline: amend two approved definitions for the renamed rehearsal job"
status = "implemented"
owners = ["engineering-owner", "technical-owner", "quality-owner"]
created = "2026-09-10"
updated = "2026-09-10"

[assurance]
commit_bound_verification = "required"
rationale = "The change amends an approved architecture and an approved requirement that later pipeline work orders, verifications and releases read as the definition of the lanes; the traceability they carry is trusted engineering state."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/ci-pipeline/architecture/ARCH-CIP-001.md",
  "docs/engineering/ci-pipeline/requirements/REQ-CIP-002.md",
  "docs/engineering/ci-pipeline/README.md",
  "docs/engineering/ci-pipeline/evidence/",
  "docs/engineering/ci-pipeline/verification-records/",
  "tests/test_ci_pipeline.py",
  "docs/engineering/ci-pipeline/requirements/REQ-CIP-010.md",
  "docs/engineering/ci-pipeline/specifications/SPEC-CIP-004.md",
  "docs/engineering/ci-pipeline/verification/VER-CIP-004.md",
  "docs/engineering/ci-pipeline/work-orders/WO-CIP-008.md",
]

[delegation]
class = "execution"

[relations]
implements = ["REQ-CIP-010"]
specifications = ["SPEC-CIP-004"]
verification = ["VER-CIP-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T10:19:05Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-10 by selecting the presented option 'Approve both packets (Recommended)', as a decision distinct from the approval of its definitions in the same transaction. This approval is the delegating act under DR-007 and DR-015: the work order carries [delegation] class = 'execution', so DR-WO-START, DR-WO-COMPLETE and DR-VREC-PREPARE may be applied by the delegated-executor role while the required validate check is success for the exact candidate head, read from the base of the pull request. It authorizes only the declared scope: the prose and amendment records of ARCH-CIP-001 and REQ-CIP-002 with their updated dates, the definitions test in tests/test_ci_pipeline.py, the domain index and the evidence packet. It authorizes no change to any workflow, script, module, managed template or hash-locked root file, no move of an identifier, statement, relation, lifecycle event or decision assessment, no verification decision, no release and no publication; the merges remain the owner's decisions."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-10T11:07:21Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 82e9b323154548faee0ad3b7b51b030c94996354 (check-run 102835980976, source github-checks)."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-10T12:36:12Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-COMPLETE under [delegation] class 'execution': required check 'validate' success at 1602fcb4f029682959c1c94adee8dbdd8bc7b9f4 (check-run 102867604140, source github-checks). Completion decided by the delegated-executor role on 2026-09-10 under the execution delegation class WO-CIP-008 carries, delegated by the engineering owner in the approval of 2026-09-10 and read at the base of pull request #439, main at 7457a401. Rules CIP-AMD-001 to CIP-AMD-005 of SPEC-CIP-004 are met and mapped to evidence in docs/engineering/ci-pipeline/evidence/WO-CIP-008/WO-CIP-008-handoff.md and readings.md: ARCH-CIP-001 and REQ-CIP-002 name the rehearsal job upgrade-rehearsal, each carries a dated amendment record, only updated changed in their front matter, and DefinitionNamesTests pins that the old name survives in the artifact bodies only inside those records. The retained handoff check from origin/main completed, nine predicates passing, eight changed paths in scope. Released 0.17.0: validate 1,480 artifacts, 0 errors, 46 W013; doctor 99 PASS; preflight PASS. Local suite 1,127 tests at the Windows baseline; the hosted lanes at 1602fcb4 are the record, 17 of 17 success. Disclosed: the acceptance grep also returns three front-matter lines of REQ-CIP-009 and REQ-CIP-010 naming the retired name as retired, so the test reads bodies and pins those two, and CIP-AMD-004's wording is left to the owner's reading; commit 70b12f67 carried a test syntax error repaired at 51720719; the lane at 70b12f67 read WEX201 on a foreign path until origin/main was merged at 1602fcb4. No workflow, script or managed path changed. Completion approves nothing: record preparation is this role's separate decision; verification and the merge remain the human owners."
+++

# Work Order: Issue #433, pipeline: amend two approved definitions for the renamed rehearsal job

## Lifecycle

This work order carries `[delegation] class = "execution"`: approving it is
the act of delegating `DR-WO-START`, `DR-WO-COMPLETE` and `DR-VREC-PREPARE`
to the `delegated-executor` role, each unlocked only while the required
`validate` check is `success` for the exact candidate head (`REQ-ECP-011`,
`SPEC-ECP-006`; the gate configuration is the owner-content
`.engineering-harness.delegation.toml`). The class is read at the base of
the pull request, so the approved packet merges to `main` first and the
execution follows on a second branch. The approval below, the verification
of the record it prepares, and every merge stay human decisions.
Commit-bound verification is `required`.

## Objective

Execute rules `CIP-AMD-001` to `CIP-AMD-005` of `SPEC-CIP-004`: `ARCH-CIP-001`
and `REQ-CIP-002` name the rehearsal job `upgrade-rehearsal`, each carries an
amendment record dating the rename under `WO-CIP-007` and, for the
requirement, the reconcile job's removal under `WO-CIP-001`; a test pins that
the old name survives only inside those records.

## In scope

- `ARCH-CIP-001`: the Components line and the amendment record
  (`CIP-AMD-001`).
- `REQ-CIP-002`: the Rationale, Required response and job-count prose and
  the amendment record (`CIP-AMD-002`).
- `updated` on both, and nothing else in their front matter (`CIP-AMD-003`).
- `tests/test_ci_pipeline.py`: the definitions test (`CIP-AMD-004`).
- The domain index and the evidence packet (`CIP-AMD-005`).

## Out of scope

- Every workflow, script and module: the workflows were repaired by
  `WO-CIP-007`.
- Every managed template and hash-locked root file.
- Historical evidence packets and verification records under the domain that
  name the old job; they state what was true when written.
- Any other approved definition of the domain.

## Authorized decision envelope

The wording of the corrected prose and of the two amendment records; whether
the rationale of `REQ-CIP-002` is reworded or left to the amendment, provided
the old name occurs only in the record; where the test lives in the module.
The implementer may not move an identifier, statement, relation, lifecycle
event or decision assessment, or touch a workflow.

## Constraints

- No managed path moves; `doctor` reads the managed set unchanged.
- The suite, `validate`, `doctor` and the handoff check over the Git-derived
  change set pass before completion; the pull request's own lanes are the run
  observation `VER-CIP-004` names.
- Each amendment record follows the shape of `SPEC-CIP-001`'s: a bold opening
  sentence naming the change, the date and the work order, then the amended
  reading.

## Expected change surface

About six lines of prose and one amendment record in each definition; one
test of about twenty lines; one index bullet; this packet.

## Required verification

Execute `VER-CIP-004` in full; repository-required checks; the pull request's
lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/ci-pipeline/evidence/WO-CIP-008/`: the grep before and
after, the front-matter diff, the `validate` and `doctor` readings, the lane
results at the head and the handoff packet.

## Stop and escalate conditions

An amendment that would need more than prose; the released evaluator
reporting either definition after the change; a suite failure beyond the
baseline; any workflow, script or managed path in the change set.

## Completion report format

The evidence packet, the changed-path ledger and the handoff `check`
restitution: the grep before and after, the front-matter diff and the lane
results each labelled. The completion decision is the `delegated-executor`'s
under the class this work order carries, while the required `validate` check
is `success` for the head; the owner refuses it by rejecting the pull
request.
