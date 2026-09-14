+++
id = "WO-KIS-009"
type = "work_order"
title = "Make delegated execution the single route"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-09-14"
updated = "2026-09-14"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Subsequent execution and preparation rely on changed authority and workflow behavior."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/harness-simplification/README.md",
  "docs/engineering/harness-simplification/architecture/ARCH-KIS-002.md",
  "docs/engineering/harness-simplification/architecture/adr/ADR-KIS-002.md",
  "docs/engineering/harness-simplification/capabilities/CAP-KIS-003.md",
  "docs/engineering/harness-simplification/evidence/VREC-KIS-009-evaluator.json",
  "docs/engineering/harness-simplification/evidence/WO-KIS-009/",
  "docs/engineering/harness-simplification/intent/INT-KIS-003.md",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-009.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-003.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-009.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-003.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-009.md",
  "docs/notes/agentic-execution-roadmap.md",
  "docs/notes/delegation-class.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/harness-operational-phasing.md",
  "docs/notes/harnessctl-reference.md",
  "plugins/verity-plane/common/skills/change/",
  "plugins/verity-plane/common/skills/evidence/",
  "se_harness/cli.py",
  "se_harness/engine/validate_engineering_artifacts.py",
  "se_harness/engine/validation_decisions.py",
  "se_harness/gate_source.py",
  "se_harness/provenance.py",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow.py",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_edges.py",
  "se_harness/workflow_predicates.py",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_result.py",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/OPERATING_CARD.md",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "tests/artifact_support.py",
  "tests/fixture_support.py",
  "tests/plugin_integration/change_skill/",
  "tests/plugin_integration/evidence-skill/README.md",
  "tests/test_agentic_execution.py",
  "tests/test_artifact_authoring_policy.py",
  "tests/test_artifact_catalog.py",
  "tests/test_cli_shape.py",
  "tests/test_codes_and_contract_tables.py",
  "tests/test_delegation_class.py",
  "tests/test_instruction_architecture.py",
  "tests/test_managed_template_texts.py",
  "tests/test_one_validation.py",
  "tests/test_operating_contract_readiness.py",
  "tests/test_preflight.py",
  "tests/test_revision_provenance.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_work_order_assurance.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_procedures.py",
  "tests/test_workflow_restitution.py",
  "tests/workflow_support.py"
]

[relations]
implements = ["REQ-KIS-009"]
specifications = ["SPEC-KIS-003"]
verification = ["VER-KIS-003"]
architecture = ["ARCH-KIS-002", "ADR-KIS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-14T20:38:27Z"
decided_by = "engineering-owner"
reason = "The owner requested the delegated route as the only route, reviewed the complete proposal and accepted it with \"yes: go\" on 2026-09-14. Record engineering-owner approval of WO-KIS-009 for that bounded scope, including its retained acceptance boundaries and prospective adoption. No completion, verification, merge, release or live adoption result is inferred."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-14T20:39:42Z"
decided_by = "engineering-owner"
reason = "The owner accepted the single execution route proposal and explicitly instructed implementation with \"yes: go\". Start the approved selected work; the current released governor continues to apply."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-14T21:24:26Z"
decided_by = "engineering-owner"
reason = "The owner explicitly said \"i approve completion + prepare verification record + I verify verification record\" after the WO-KIS-009 implementation report and PR #476. Record the engineering-owner completion decision for reviewed candidate 5c52d7ca21de0850608f3f6f19572bb92c40a230. The final local suite passed 1067 tests with 15 skips; all hosted checks passed or were intentionally skipped. This transition marks WO-KIS-009 implemented. Preparation and the separately supplied assurance decision will be applied in order to the resulting VREC; no merge, release or adoption is authorized."
+++

# Make delegated execution the single route

## Objective and scope

Implement the accepted one-route proposal through SPEC-KIS-003 and ARCH-KIS-002. Change
only the named runtime/contract, candidate policy/templates, common skills, current notes
and tests needed for that behavior. Remove obsolete route checks and instructions with it.

## Authorized decision envelope

The owner accepted the retained proposal and said "yes: go". Record the matching definition
approvals and implementation start through the currently released evaluator. Routine design,
helpers, test fixtures, local commits and the established push/PR route are authorized
within this work. Candidate test wheels outside the checkout are non-promotable evidence.
This WO carries the old execution class only because the current 0.17.0 governor requires
it; it is not the proposed future template. Its base-branch/CI delegation prerequisites
continue to govern actual completion and VREC preparation until normal adoption.

## Out of scope

No root managed-policy edits, release, merge, publication, live adoption, rewritten old
approvals/VRECs/RLS, new operation modes, automatic work selection or forced subagents.
Keep reserved owner decisions and meaningful gates. Do not fix unrelated plugin backlog.

## Required verification and evidence

Meet VER-KIS-003 and required repository checks. Retain concise commands, outcomes, relevant
failures, candidate and CI/raw-output locations under this WO evidence directory. Review
simplicity through the shared authoring policy. VREC destinations permit later preparation
when authorized and ready; they do not assert a prepared or verified result.

## Stop and completion report

Stop the affected action on failed retained gates, changed approved scope or missing actual
authority. Report implemented behavior, deleted route complexity, checks and limitations
using the released schema-2 handoff. Do not invent completion, assurance or delivery facts.
