+++
id = "WO-HUP-022"
type = "work_order"
title = "Align the CI evaluator pin and catalog-link test with the adopted 0.19.0 root"
status = "rejected"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-27"
updated = "2026-09-27"

rejected_at = "2026-09-27T20:34:59Z"
rejected_by = "engineering-owner"
rejection_reason = "The requesting human in this conversation approved rejection and WO-HUP-023. Reject this unusable work authorization because released 0.19.0 cannot start its named-human approval; preserve the original event and failed evidence."
[assurance]
commit_bound_verification = "required"
rationale = "CI evaluator selection and the documentation check are trusted adoption state; the human approved required commit-bound verification in this conversation."
decided_by = "Requesting human in this conversation (repository owner)"

[execution_scope]
paths = [
  ".github/workflows/engineering-harness.yml",
  "tests/test_progressive_documentation.py",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-022.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-022/",
]

[relations]
implements = ["REQ-IAR-024"]
specifications = ["SPEC-IAR-014"]
verification = ["VER-HUP-021"]
architecture = ["ARCH-IAR-011", "ADR-IAR-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-27T20:30:08Z"
decided_by = "Requesting human in this conversation (repository owner)"
reason = "User: Approve WO-HUP-022 and required assurance. Authorize the reviewed two-line correction and required commit-bound verification."
scope_paths = [".github/workflows/engineering-harness.yml", "tests/test_progressive_documentation.py", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-022.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-022/"]

[[lifecycle_events]]
from = "approved"
to = "rejected"
decided_at = "2026-09-27T20:34:59Z"
decided_by = "engineering-owner"
reason = "The requesting human in this conversation approved rejection and WO-HUP-023. Reject this unusable work authorization because released 0.19.0 cannot start its named-human approval; preserve the original event and failed evidence."
+++

# Align the remaining 0.19.0 adoption checks

## Objective

Make CI use the adopted released evaluator and make the documentation test
follow the released artifact catalog. Full-suite evidence under WO-HUP-021
identified both stale references. This work supplements that adoption; it
changes no accepted requirement, verification contract or earlier approval.

## In scope

- Change only `SE_HARNESS_VERSION: "0.18.0"` to `"0.19.0"` in the editable
  Engineering Harness workflow. Keep all jobs, permissions and checks unchanged.
- Replace the test's old TRACEABILITY catalog URL with
  `../engineering/harness/ARTIFACTS.md#artifact-types`.
- Retain correction evidence and include this work in the adoption's shared
  VREC-HUP-021, prepared under WO-HUP-021's authorized record paths.

## Out of scope

Other workflow or test changes, weakened assertions, managed-file edits,
new product behavior, changes to earlier formal records, push, PR, merge and
publication. Any additional failed check needs its own bounded assessment.

## Authorized decision envelope

After human approval, the executor may start, apply the two reviewed lines,
check, commit locally, retain evidence, record completion and participate in
the existing adoption verification preparation under DR-015. Approval confirms
the proposed required commit-bound assurance classification. No verification
acceptance or external-action authority is implied.

## Constraints

Use released 0.19.0 for lifecycle operations. Preserve the original failing
full-suite result. Keep WO-HUP-021's original approved scope unchanged.

## Expected change surface

The two implementation lines are shown in
`../evidence/WO-HUP-022/correction.proposed.diff`. No installer or policy code
change is needed; the CI workflow is an editable supplied file.

## Required verification

The two affected test modules and the full source suite at full scale must
pass. Derive evaluator 0.19.0/candidate 0.20.0, run released integrity and
review checks, and assess the combined change scope against the original
adoption base. Keep platform skips and hosted checks pending before integration.
Reuse VER-HUP-021's ADOPT02, ADOPT05 and ADOPT06 acceptance criteria.

## Evidence to record

Exact proposed and applied diff, original failure references, corrected checks,
complete Git change inventory with assignment to each work order, handoff,
completion and shared candidate identity. The inventory must account for all
paths; selecting one work order must not hide an unassigned change.

## Stop and escalate conditions

Stop for changed scope, an unexpected workflow change, another failure needing
unapproved paths, or a failed required gate. Preserve actual lifecycle state.

## Completion report format

Report the two corrected references, actual checks, retained limitations and
the evaluator's next step. Human acceptance of the shared VREC remains separate.
