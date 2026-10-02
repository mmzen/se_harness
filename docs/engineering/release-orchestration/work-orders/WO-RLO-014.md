+++
id = "WO-RLO-014"
type = "work_order"
title = "Implement complete-release authority and package preparation"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"

[assurance]
commit_bound_verification = "required"
rationale = "Required verification confirmed by mmzen: release and publication decisions depend on this changed authority, preparation, workflow or activation evidence; assess the exact implemented commit."
decided_by = "mmzen"

[execution_scope]
paths = [
  "se_harness/workflow_contract.json",
  "se_harness/workflow_procedures.py",
  "se_harness/workflow_result.py",
  "se_harness/instruction_discovery.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/harness/AUTHORITY.md",
  "templates/repository/standard/docs/engineering/harness/RELEASE.md",
  "templates/repository/standard/docs/engineering/harness/DELIVER_RESULT.md",
  "templates/repository/standard/docs/engineering/harness/RESULTS.md",
  "templates/repository/standard/docs/engineering/templates/RELEASE_CONTRACT.template.md",
  "plugins/verity-plane/common/skills/change/references/authority.md",
  "plugins/verity-plane/common/skills/evidence/",
  "repository_tools/plugin_distribution.py",
  "scripts/build_plugin_marketplace.py",
  "tests/test_workflow_procedures.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_documentation_contract.py",
  "tests/test_workflow_restitution.py",
  "tests/test_instruction_discovery.py",
  "tests/test_instruction_architecture.py",
  "tests/test_cli_shape.py",
  "tests/plugin_integration/package_assembly/",
  "tests/plugin_integration/evidence-skill/portable/fixtures/external/",
  "tests/plugin_integration/evidence-skill/portable/fixtures/unauthorized-release/",
  "docs/engineering/release-orchestration/intent/INT-RLO-002.md",
  "docs/engineering/release-orchestration/capabilities/CAP-RLO-005.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-021.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-022.md",
  "docs/engineering/release-orchestration/requirements/REQ-RLO-023.md",
  "docs/engineering/release-orchestration/specifications/SPEC-RLO-007.md",
  "docs/engineering/release-orchestration/architecture/ARCH-RLO-006.md",
  "docs/engineering/release-orchestration/architecture/adr/ADR-RLO-006.md",
  "docs/engineering/release-orchestration/verification/VER-RLO-011.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-014.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-015.md",
  "docs/engineering/release-orchestration/work-orders/WO-RLO-016.md",
  "docs/engineering/release-orchestration/evidence/WO-RLO-014/",
  "docs/engineering/release-orchestration/verification-records/",
  "docs/engineering/release-orchestration/risks/RISK-RLO-001.md",
]

[relations]
implements = ["REQ-RLO-021", "REQ-RLO-022"]
specifications = ["SPEC-RLO-007"]
verification = ["VER-RLO-011"]
architecture = ["ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-02T20:17:28Z"
decided_by = "mmzen"
reason = "Human repository owner mmzen answered \"Approve package, verification and review PR\" to the exact package review for WO-RLO-014/015/016 and their governing definitions, with required commit-bound verification under VER-RLO-011. This authorizes bounded implementation, local checks and commits, completion and verification preparation, ordinary review-branch push and draft PR from work/complete-release-approval to mmzen/se_harness:main, and its later verification-decision update. Human verification acceptance, merge, actual releases and the exact live configuration change remain separate. The selected released evaluator 0.21.0 governs this work. Reviewed draft SHA-256 00268034c4244d941e2e1dbace590515952d8fb28e0d2ea1a3b93401c435bc29; approved transition input SHA-256 82e820327d4e58620ee3a8e10af619e34ed6fcd66f25228b0e6e5a92a1e152b1. Only the confirmed WO assurance fields were added before this transition."
scope_paths = ["se_harness/workflow_contract.json", "se_harness/workflow_procedures.py", "se_harness/workflow_result.py", "se_harness/instruction_discovery.json", "templates/repository/standard/docs/engineering/WORKFLOW.json", "templates/repository/standard/docs/engineering/harness/AUTHORITY.md", "templates/repository/standard/docs/engineering/harness/RELEASE.md", "templates/repository/standard/docs/engineering/harness/DELIVER_RESULT.md", "templates/repository/standard/docs/engineering/harness/RESULTS.md", "templates/repository/standard/docs/engineering/templates/RELEASE_CONTRACT.template.md", "plugins/verity-plane/common/skills/change/references/authority.md", "plugins/verity-plane/common/skills/evidence/", "repository_tools/plugin_distribution.py", "scripts/build_plugin_marketplace.py", "tests/test_workflow_procedures.py", "tests/test_workflow_execution.py", "tests/test_workflow_documentation_contract.py", "tests/test_workflow_restitution.py", "tests/test_instruction_discovery.py", "tests/test_instruction_architecture.py", "tests/test_cli_shape.py", "tests/plugin_integration/package_assembly/", "tests/plugin_integration/evidence-skill/portable/fixtures/external/", "tests/plugin_integration/evidence-skill/portable/fixtures/unauthorized-release/", "docs/engineering/release-orchestration/intent/INT-RLO-002.md", "docs/engineering/release-orchestration/capabilities/CAP-RLO-005.md", "docs/engineering/release-orchestration/requirements/REQ-RLO-021.md", "docs/engineering/release-orchestration/requirements/REQ-RLO-022.md", "docs/engineering/release-orchestration/requirements/REQ-RLO-023.md", "docs/engineering/release-orchestration/specifications/SPEC-RLO-007.md", "docs/engineering/release-orchestration/architecture/ARCH-RLO-006.md", "docs/engineering/release-orchestration/architecture/adr/ADR-RLO-006.md", "docs/engineering/release-orchestration/verification/VER-RLO-011.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-014.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-015.md", "docs/engineering/release-orchestration/work-orders/WO-RLO-016.md", "docs/engineering/release-orchestration/evidence/WO-RLO-014/", "docs/engineering/release-orchestration/verification-records/", "docs/engineering/release-orchestration/risks/RISK-RLO-001.md"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-02T20:19:17Z"
decided_by = "Codex agent"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed. Start approved implementation after passing start preflight; mmzen approved package, required verification and bounded review PR."
+++

# Implement complete-release authority and package preparation

## Objective

One reviewed release response covers its listed external actions, and exact plugin payloads can be qualified before evaluator publication.

## In scope

Implement RLO-ONE-001 through RLO-ONE-003 and the portable boundaries of RLO-ONE-007. Update the machine procedure and its readable instructions together. Add candidate staging to the existing plugin builder and separate immutable payload identity from later governance receipts. Keep legacy released-input behavior and refusal coverage.

## Constraints and dependencies

Start only after the governing drafts, architecture decision, verification contract and this work order have been approved. WO-RLO-015 consumes these interfaces; any change outside the reviewed contract needs review.

Use SPEC-RLO-007 and ARCH-RLO-006/ADR-RLO-006. Preserve historical formal records,
published bytes and unrelated repository content. Every listed path is a ceiling,
not a request to modify files without need. Approved definition files are included
only for transport of this reviewed package and evaluator-applied transitions;
their accepted meaning must not be rewritten.

## Out of scope

No production release, package publication, marketplace or marker mutation,
live provider-setting change, credential refresh, repository adoption or force
push. No new formal artifact type or general orchestration service. No rewriting
accepted older definitions or treating draft instructions as current authority.

## Authorized decision envelope

When this exact work order is approved, the agent may implement the listed scope,
perform checks, make local commits, record completion and prepare commit-bound
verification under the selected released evaluator. This draft proposes required
assurance; its human classification is not yet recorded. Human verification and
any external action require actual matching authority.

The proposed review-delivery grant covers ordinary branch updates and a draft PR
from work/complete-release-approval to main in mmzen/se_harness, then the final
verification-decision update. It excludes merge and publication. This grant is
part of the package to review; no push is authorized merely by this draft.

## Proposed assurance classification

Required commit-bound verification. Later release and publication decisions rely
on this changed authority, preparation, workflow or activation evidence. The human
must confirm this classification with the package approval; only then will the
`[assurance]` fields name that human. No decision-maker is fabricated in this draft.

## Required verification

Run VER-RLO-011 ONE01 through ONE04 and the product part of ONE08, focused workflow/discovery/package tests, the ordinary full suite and required scope/handoff checks.

## Evidence to record

Store the review, commands, outputs, identities and results in
`docs/engineering/release-orchestration/evidence/WO-RLO-014/`. Generated VREC files and their evaluator JSON belong
only under `docs/engineering/release-orchestration/verification-records/` for this work. Reserve those destinations
in scope so preparation does not need a later paperwork-only scope correction.

## Stop and escalate conditions

Stop the affected operation on mismatched scope, changed reviewed definitions,
failed required checks, unavailable required inputs or a missing provider control.
Inspect uncertain writes before retrying. Report changed scope before editing it.
Do not solve an implementation gap by weakening required verification.

## Completion report format

State implemented behavior, exact candidate, checks and limitations; link retained
evidence and the prepared verification record; report the evaluator's current next
action. Distinguish local readiness from live delivery or configuration completion.
