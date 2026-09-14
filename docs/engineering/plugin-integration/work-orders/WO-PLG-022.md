+++
id = "WO-PLG-022"
type = "work_order"
title = "Apply accepted KISS rules to the remaining plugin plan"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[assurance]
commit_bound_verification = "required"
rationale = "Future work will rely on the amended formal requirements and verification plans."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-022-evaluator.json",
  "docs/engineering/plugin-integration/evidence/WO-PLG-022/",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-015.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-016.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-024.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-027.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-009.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-014.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-016.md",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-022.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-009.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-014.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-016.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-022.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-009.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-014.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-016.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-022.md",
  "docs/notes/plugin-backlog-kiss-2026-09-14.md",
  "docs/notes/plugin-definition-delivery-2026-09-08.md"
]

[relations]
implements = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-PLG-035", "REQ-PLG-036", "REQ-PLG-037", "REQ-KIS-001", "REQ-KIS-002", "REQ-KIS-003", "REQ-KIS-004", "REQ-KIS-005", "REQ-KIS-006", "REQ-KIS-007", "REQ-KIS-008", "REQ-KIS-009"]
specifications = ["SPEC-PLG-021", "SPEC-KIS-001", "SPEC-KIS-002", "SPEC-KIS-003"]
verification = ["VER-PLG-022"]
architecture = ["ARCH-PLG-004", "ADR-PLG-004", "ARCH-KIS-001", "ADR-KIS-001", "ARCH-KIS-002", "ADR-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T21:40:10Z"
decided_by = "engineering-owner"
reason = "The owner explicitly requested making the remaining plugin work orders compliant with all accepted KISS work on 2026-09-14. Record the bounded planning-amendment approve decision only. Future plugin implementation, completion, assurance, release and adoption remain unperformed."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T21:41:04Z"
decided_by = "engineering-owner"
reason = "The owner explicitly requested making the remaining plugin work orders compliant with all accepted KISS work on 2026-09-14. Record the bounded planning-amendment start decision only. Future plugin implementation, completion, assurance, release and adoption remain unperformed."
+++

# Apply accepted KISS rules to the remaining plugin plan

## Objective and scope

Revise the remaining plugin definitions before implementation resumes. Consolidate
connection and maintenance into WO-PLG-009, installation guidance and useful host
checks into WO-PLG-016, and keep optional helpers deferred under WO-PLG-014.
Update the current index and prospective helper applicability. Do not implement runtime
changes, activate a future work order, publish a plugin or change a live repository.

## Authority and execution

The owner requested this bounded amendment after merging WO-KIS-009. This work applies
already accepted requirements, not a new product architecture. The request authorizes
preparation, editing, checks, local commits and the established push/PR delivery.
Released 0.17.0 still governs actual lifecycle transitions; the new single-route
policy is candidate source until released and adopted. This WO does not activate
branch-local delegation or manufacture completion, verification or adoption decisions.

The two future implementation packets stay draft. Their eventual approval authorizes
routine execution under the installed policy; this planning amendment starts neither.
Existing helper definition approvals retain their recorded history; the dated owner-
directed amendment narrows prospective scope without claiming helper implementation.

## Verification and evidence

Meet VER-PLG-022. Preserve historical VREC/RLS files and bound evidence bytes. Keep the
owner request, baseline, disposition of all five old packets and check results in one
evidence note. Stop only for a material contract conflict, failed required check or
necessary change outside this bounded scope. Report the actual remaining next action.
