+++
id = "WO-KIS-008"
type = "work_order"
title = "Apply generic KISS guidance to authoring and review"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Subsequent authoring and review will rely on the distributed policy and reading route."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/harness-simplification/README.md",
  "docs/engineering/harness-simplification/capabilities/CAP-KIS-002.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-008/",
  "docs/engineering/harness-simplification/intent/INT-KIS-002.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-008.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-002.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-008.evaluator-evidence.json",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-008.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-002.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-008.md",
  "docs/notes/design-simplicity.md",
  "plugins/verity-plane/common/skills/change/SKILL.md",
  "plugins/verity-plane/common/skills/change/references/artifacts.md",
  "plugins/verity-plane/common/skills/change/references/work-orders.md",
  "plugins/verity-plane/common/skills/evidence/references/records.md",
  "se_harness/preflight.py",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md",
  "templates/repository/standard/docs/engineering/templates/ADR.template.md",
  "templates/repository/standard/docs/engineering/templates/ARCHITECTURE.template.md",
  "templates/repository/standard/docs/engineering/templates/CAPABILITY.template.md",
  "templates/repository/standard/docs/engineering/templates/INTENT.template.md",
  "templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md",
  "templates/repository/standard/docs/engineering/templates/SPECIFICATION.template.md",
  "templates/repository/standard/docs/engineering/templates/VERIFICATION.template.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "tests/test_artifact_authoring_policy.py",
  "tests/test_artifact_catalog.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_instruction_architecture.py"
]

[relations]
implements = ["REQ-KIS-008"]
specifications = ["SPEC-KIS-002"]
verification = ["VER-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T19:44:45Z"
decided_by = "engineering-owner"
reason = "The owner accepted the generic simplicity rule and exact policy/template/instruction/skill routing, then said \"OK, go for this modification then\" on 2026-09-14. Record engineering-owner approval of WO-KIS-008 for that bounded proposal. No completion, verification, release, merge or live adoption decision is inferred."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T19:45:59Z"
decided_by = "engineering-owner"
reason = "The owner explicitly instructed implementation of the accepted generic authoring and review modification: \"OK, go for this modification then\". Start this approved bounded work on that instruction; completion and assurance remain separate."
+++

# Apply generic KISS guidance to authoring and review

## Objective and scope

Implement SPEC-KIS-002 in the shared candidate policy, its existing template and CLI
routes, general instructions and common plugin skills. Update only the declared files
needed for that behavior and its focused verification. Keep the implementation small.

## Decision envelope

The owner accepted the general wording and exact integration proposal, then instructed
implementation. Record definition approval and start separately through the released
evaluator. Execution delegation continues within this approved scope, subject to the
installed 0.17.0 rule requiring the class at the PR base and successful live required CI.
Choose concise wording, relevant template links and ordinary behavioral tests. Reuse
existing components; a new gate, score, receipt or review actor is outside this work order.

## Exclusions

Do not implement the remaining plugin backlog, change lifecycle or decision rights,
rewrite historical records, release, merge, or upgrade root/live installed policies.
Significant new architecture or any other behavioral change requires revised scope.

## Verification and evidence

Meet VER-KIS-002 and repository-required checks. Candidate wheels, if needed, are
explicitly non-promotable and built outside the checkout. Retain concise results in
this work order's evidence directory and use existing raw-output storage. Reserved
VREC paths permit later preparation only when its actual prerequisites are met.

## Stop and handoff

Stop for a failed required gate, unresolved material contract conflict or necessary
out-of-scope change. Report changes, checks and actual lifecycle state with the released
schema-2 handoff and one next action. A passing implementation does not invent an owner
completion, assurance, release, merge or adoption decision.
