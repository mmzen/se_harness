+++
id = "WO-KIS-014"
type = "work_order"
title = "Finish truthful evidence with the complete test scope"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-20"
updated = "2026-09-20"

[assurance]
commit_bound_verification = "required"
rationale = "Completion and later assurance depend on changed evidence assessment; approval is still required."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/harness-simplification/evidence/WO-KIS-010/",
  "docs/engineering/harness-simplification/evidence/WO-KIS-014/",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-010.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-014.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-004.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-014.md",
  "docs/notes/diagnostic-codes.md",
  "docs/notes/harnessctl-check.md",
  "docs/notes/harnessctl-reference.md",
  "se_harness/cli.py",
  "se_harness/engine/validation_evidence.py",
  "se_harness/evaluator_evidence.py",
  "se_harness/provenance.py",
  "se_harness/quality_gates_contract.json",
  "se_harness/workflow_compliance.py",
  "se_harness/workflow_contract.json",
  "se_harness/workflow_evidence_packet.py",
  "se_harness/workflow_predicates.py",
  "se_harness/workflow_result.py",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.json",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/WORKFLOW.json",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "tests/test_revision_provenance.py",
  "tests/test_workflow_compliance.py",
  "tests/test_workflow_execution.py",
  "tests/test_workflow_restitution.py",
 ]

[relations]
implements = ["REQ-KIS-010"]
specifications = ["SPEC-KIS-004"]
verification = ["VER-KIS-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T07:15:43Z"
decided_by = "engineering-owner"
reason = "On 2026-09-20 the owner explicitly answered \"Approve replacement scope and closure\" to approval of the prepared WO-KIS-014 and closure of WO-KIS-010 as replaced. Reviewed WO-KIS-014 full-byte SHA-256: 57cc3a020d9e54abd79a5fe78a5e096e30bf613402e7f87af1b2acae9e51fdf9. Preserve partial implementation and history. Existing onboarding failures remain unresolved. This decision grants no assurance acceptance or external delivery."
scope_paths = ["docs/engineering/harness-simplification/evidence/WO-KIS-010/", "docs/engineering/harness-simplification/evidence/WO-KIS-014/", "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md", "docs/engineering/harness-simplification/verification-records/VREC-KIS-010.md", "docs/engineering/harness-simplification/verification-records/VREC-KIS-014.md", "docs/engineering/harness-simplification/verification/VER-KIS-004.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-014.md", "docs/notes/diagnostic-codes.md", "docs/notes/harnessctl-check.md", "docs/notes/harnessctl-reference.md", "se_harness/cli.py", "se_harness/engine/validation_evidence.py", "se_harness/evaluator_evidence.py", "se_harness/provenance.py", "se_harness/quality_gates_contract.json", "se_harness/workflow_compliance.py", "se_harness/workflow_contract.json", "se_harness/workflow_evidence_packet.py", "se_harness/workflow_predicates.py", "se_harness/workflow_result.py", "templates/repository/standard/docs/engineering/QUALITY_GATES.json", "templates/repository/standard/docs/engineering/QUALITY_GATES.md", "templates/repository/standard/docs/engineering/WORKFLOW.json", "templates/repository/standard/docs/engineering/WORKFLOW.md", "tests/test_revision_provenance.py", "tests/test_workflow_compliance.py", "tests/test_workflow_execution.py", "tests/test_workflow_restitution.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-20T07:17:36Z"
decided_by = "delegated-executor"
reason = "Execution of DR-WO-START under recorded engineering-owner approval; relevant local gates passed. Codex continues the owner-approved replacement scope after the explicit approval and closure decision dated 2026-09-20."
+++

# Finish truthful evidence with the complete test scope

## Objective

Finish the existing REQ-KIS-010 / SPEC-KIS-004 / VER-KIS-004 repair. Retain and
review the local implementation already made under WO-KIS-010. The required
behavior is unchanged. This draft adds the two files omitted from that order:

- tests/test_workflow_execution.py: replace the attachment-only fixture with a
  recorded contract-authorized assessment. Keep completion and integrity tests.
- docs/notes/diagnostic-codes.md: regenerate the existing diagnostic index to
  reflect the changed messages. Do not introduce a new generator or code family.

Remove the unused guessed path tests/workflow_support.py from future authority.
Keep all other existing implementation paths so the complete candidate diff is
reviewable under one selected order. The new WO, evidence folder and VREC path
serve the existing lifecycle; their names grant no approval.

## Proposed owner decision

Approve this exact draft and reject WO-KIS-010 as replaced by a complete scope.
Preserve WO-KIS-010's history, evidence and partial implementation. Rejection
closes the old execution envelope; it is not a failed verification verdict.
The released checker supports these transitions. It has no supported in-place
scope amendment for an in-progress WO. Do not edit historical approval events.

After that actual decision, start this WO through the normal released procedure.
The earlier scheduling references to WO-KIS-010 in WO-KIS-011 and WO-KIS-013
mean this same evidence behavior; this continuation does not start those orders.

## Execution and limits

Approval covers local edits, tests, evidence, ordinary commits, qualifying
completion and required VREC preparation. Owner review follows DEC-KIS-001.
It grants no assurance acceptance, root-policy upgrade, push, PR, merge,
release, publication, deployment or live repository-setting change.

No historical VREC/RLS or old approval facts may be rewritten. No promotable
distribution is built. Use released 0.18.0 for governing actions and clearly
label candidate-source checks. Preserve the original assessment archives.

## Required checks and remaining blockers

Meet VER-KIS-004, including its normal and failure cases. Run the affected tests,
full repository suite, distribution-provenance check, CLI, graph, doctor and
review preflight. Preserve actual logs and checker/candidate identities.
Exercise the existing Windows/Linux routes before claiming both platforms.

The starting commit already has 12 failing onboarding assertions; this draft
does not authorize changing README.md or the onboarding tests. Those failures
remain visible and cannot be called a passing full suite. If they continue to
block required acceptance, obtain a separate bounded owner decision; do not
silently waive them or broaden this order. Linux has not yet been exercised.

## Stop and handoff

Stop affected work on changed scope, missing authority, failed required checks
or uncertain writes. Leave the order in progress until completion requirements
are met. Report actual changes, checks, limitations and the released schema-2
result's one accountable next step. Preparation is separate from acceptance.
