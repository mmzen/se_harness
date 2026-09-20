+++
id = "WO-KIS-010"
type = "work_order"
title = "Keep evidence outcomes truthful"
status = "approved"
owners = ["engineering-owner"]
created = "2026-09-19"
updated = "2026-09-20"

[assurance]
commit_bound_verification = "required"
rationale = "Later engineering and assurance decisions rely on the changed checks, policy or agent guidance; classification takes effect on actual WO approval."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/harness-simplification/evidence/WO-KIS-010/",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-010.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-004.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md",
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
  "tests/test_workflow_restitution.py",
  "tests/workflow_support.py",
]

[relations]
implements = ["REQ-KIS-010"]
specifications = ["SPEC-KIS-004"]
verification = ["VER-KIS-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "engineering-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: ff54233ced59d8c3e0d68bc060d42545b0b569ac8f7b6d6c12ecf2b1b8296ff0. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
scope_paths = ["docs/engineering/harness-simplification/evidence/WO-KIS-010/", "docs/engineering/harness-simplification/requirements/REQ-KIS-010.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-004.md", "docs/engineering/harness-simplification/verification-records/VREC-KIS-010.md", "docs/engineering/harness-simplification/verification/VER-KIS-004.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-010.md", "docs/notes/harnessctl-check.md", "docs/notes/harnessctl-reference.md", "se_harness/cli.py", "se_harness/engine/validation_evidence.py", "se_harness/evaluator_evidence.py", "se_harness/provenance.py", "se_harness/quality_gates_contract.json", "se_harness/workflow_compliance.py", "se_harness/workflow_contract.json", "se_harness/workflow_evidence_packet.py", "se_harness/workflow_predicates.py", "se_harness/workflow_result.py", "templates/repository/standard/docs/engineering/QUALITY_GATES.json", "templates/repository/standard/docs/engineering/QUALITY_GATES.md", "templates/repository/standard/docs/engineering/WORKFLOW.json", "templates/repository/standard/docs/engineering/WORKFLOW.md", "tests/test_revision_provenance.py", "tests/test_workflow_compliance.py", "tests/test_workflow_restitution.py", "tests/workflow_support.py"]
+++

# Keep evidence outcomes truthful

## Objective and scope

Implement SPEC-KIS-004 for REQ-KIS-010; meet VER-KIS-004. The work addresses assessment findings
F3, F9. Fix only the specified behavior, its affected existing tests and
its candidate-policy/plugin explanations. The exact admitted paths are above.

## Decision envelope

This draft proposes the listed work; it records no approval or execution grant.
After actual WO approval, the executor may make local implementation choices,
edit the named paths, run checks, retain evidence, record qualifying completion
and prepare required verification through the installed single procedure.
The assurance classification above is proposed for the engineering owner's
approval; no owner decision has been fabricated by writing it.

## Limits and dependencies

Implement first. WO-KIS-011 consumes this evidence meaning; coordinate shared compliance code before that work starts.

Keep changes inside these paths and the behavioral contract. Unlisted files
need a scoped amendment. Do not broaden behavior while keeping only the same
file list. Read current main and applicable definitions before execution; this
packet was drafted on assessed commit f05c478a, while refreshed origin/main
was 2b87e044. Reconcile relevant upstream changes without overwriting them.

No root locked-policy replacement, historical approval/VREC/RLS edits, product
release, live project upgrade, credential change, push, PR creation, merge,
publication or deployment is authorized by this draft. A later explicit
external-action instruction must name its exact candidate and destination.
No promotable distributions are built under this work. Required ephemeral
package tests after approval remain clearly non-promotable.

## Required verification and evidence

Meet VER-KIS-004. Run focused affected checks and the repository-required
regression, package, CLI, graph, doctor and phase-appropriate preflight checks
at the applicable implementation boundaries. Use the selected released
evaluator for governing operations; candidate runs establish proposed behavior
only. Use the existing supported Windows/Linux CI routes rather than adding
a qualification pipeline.

Keep one concise evidence summary under evidence/WO-KIS-010/ with the
candidate, command and checker identity, observed results, relevant failures,
raw-output references and remaining limitations. Future verification records
are prepared with the existing capture command after the candidate exists;
the admitted destination is not evidence of preparation or approval.

## Stop and handoff

Stop the affected action on missing actual authority, changed approved scope,
invalid selected inputs, failed required gates or uncertain writes. Preserve
completed valid work. Read back state before retrying an uncertain mutation.
At handoff use the released schema-2 result and state actual changes, checks,
limitations, unchanged decisions and its one typed next step. Draft approval,
implementation completion, assurance and delivery remain separate facts.
