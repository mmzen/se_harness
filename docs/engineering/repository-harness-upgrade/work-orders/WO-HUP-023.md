+++
id = "WO-HUP-023"
type = "work_order"
title = "Recover approval encoding and finish the two-line 0.19.0 adoption correction"
status = "in_progress"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

[assurance]
commit_bound_verification = "required"
rationale = "Later decisions depend on CI evaluator selection and the documentation check; the requesting human confirmed required commit-bound verification for this work order."

decided_by = "Requesting human in this conversation (repository owner)"

[execution_scope]
paths = [
  ".github/workflows/engineering-harness.yml",
  "tests/test_progressive_documentation.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-022.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-022/",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-023.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-023/",
]

[relations]
implements = ["REQ-IAR-024"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-HUP-021"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T20:34:59Z"
decided_by = "engineering-owner"
reason = "Decision by the requesting human in this conversation, acting as repository and engineering owner: Approve rejection and WO-HUP-023. Approve the reviewed two-line correction, recovery scope and required commit-bound assurance. engineering-owner is the released evaluator legacy encoding for this human decision."
scope_paths = [".github/workflows/engineering-harness.yml", "tests/test_progressive_documentation.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-022.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-022/", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-023.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-023/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-27T20:35:49Z"
decided_by = "Codex executor under approved WO-HUP-023"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Start the approved correction under the recorded human approval and DR-015."
+++

# Recover approval encoding and finish the adoption correction

## Objective

Apply the two implementation lines already reviewed for WO-HUP-022 through
an executable work order. Preserve the actual approval and failed start of
WO-HUP-022. Do not rewrite its lifecycle history.

## Reason for a new work order

The human approved WO-HUP-022 and required assurance. The agent applied that
decision with `decided_by = "Requesting human in this conversation (repository owner)"`.
Released 0.19.0 accepted the approval, but its start gate searches for the
literal `engineering-owner` value. Start therefore failed with
`QGP-G3-SCOPE` / `WEX-ECP-022`. No implementation was performed under WO-HUP-022.

The released lifecycle has no approval-correction or reapproval operation.
The proposed recovery is an explicit human rejection of the unusable
WO-HUP-022, followed by approval of this work order. The approval command
must use `engineering-owner` as the legacy encoding. Its reason must identify
the requesting human in this conversation and quote the actual decision.
The label alone supplies no authority. This is a new work authorization,
not an amendment to an accepted definition or a fabricated revision link.

## In scope

- Change only `SE_HARNESS_VERSION: "0.18.0"` to `"0.19.0"` in the editable
  Engineering Harness workflow. Preserve all jobs, permissions and checks.
- Replace the documentation test's old catalog URL with
  `../engineering/harness/ARTIFACTS.md#artifact-types`.
- Apply only the human-authorized rejection of WO-HUP-022 through the released
  transition command. Preserve its earlier approval event and failed evidence.
- Retain the correction and recovery evidence. Prepare the shared
  VREC-HUP-021 under WO-HUP-021's authorized record paths, covering WO-HUP-021
  and WO-HUP-023. Do not present rejected WO-HUP-022 as implemented work.

## Out of scope

Other workflow or test changes, evaluator code or policy changes, weakened
checks, manual lifecycle-history edits, changes to accepted definitions,
push, PR, merge and publication. Correcting the released identity-handling
defect itself requires separate governed work.

## Authorized decision envelope

The review requests two exact human decisions: reject WO-HUP-022 because its
approval cannot establish the evaluator's execution grant, and approve
WO-HUP-023 with required commit-bound verification. No decision is inferred
from this draft or from approval of a different ID.

After approval, the executor may start, apply the two reviewed implementation
lines, check, commit locally, retain evidence, record completion and prepare
verification under DR-015. Human verification and external actions remain
separate decisions.

## Constraints

Use released 0.19.0 for lifecycle operations. Preserve the original failed
full suite and start-preview result. Keep WO-HUP-021's approved scope and
WO-HUP-022's original approval history unchanged. Append a rejection only
through the released evaluator after the human authorizes it.

## Expected change surface

The implementation remains the exact two-line diff at
`../evidence/WO-HUP-022/correction.proposed.diff`. The additional paths record
the recovery, its actual decisions and evidence; they authorize no other
changes to the workflow, tests or prior work-order content.

## Required verification

The two affected test modules and the full source suite at full scale must
pass. Derive evaluator 0.19.0/candidate 0.20.0, run released integrity and
review checks, and assess the combined change scope against the original
adoption base. Preserve platform skips. Hosted checks remain required before
integration. Use VER-HUP-021's ADOPT02, ADOPT05 and ADOPT06 criteria.

## Evidence to record

Retain the reviewed two-line diff, human decisions, failed approval/start
sequence, supported recovery transitions, corrected checks, complete Git
change inventory assigned to each executing work order, handoff, completion
and shared candidate identity. Report the instruction/evaluator mismatch as
a known released limitation; do not claim it was fixed by this work.

## Stop and escalate conditions

Stop for changed scope, another failed gate, unexpected workflow changes or
additional implementation paths. A repeated identity mismatch stops execution;
it does not authorize changing the evaluator or editing lifecycle history.

## Completion report format

Report the two corrected references, recovery effects, actual checks, retained
limitations and evaluator-selected next step. Keep human acceptance of the
shared VREC separate.
