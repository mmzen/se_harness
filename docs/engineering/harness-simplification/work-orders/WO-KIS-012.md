+++
id = "WO-KIS-012"
type = "work_order"
title = "Match repository protection to the stated approval policy"
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
  ".github/CODEOWNERS",
  ".github/PULL_REQUEST_TEMPLATE.md",
  ".github/workflows/candidate-evidence.yml",
  ".github/workflows/engineering-harness.yml",
  ".github/workflows/pages-publication.yml",
  ".github/workflows/publish-dashboard-pages.yml",
  ".github/workflows/publish-pypi.yml",
  "docs/engineering/harness-simplification/decisions/DEC-KIS-001.md",
  "docs/engineering/harness-simplification/evidence/WO-KIS-012/",
  "docs/engineering/harness-simplification/requirements/REQ-KIS-012.md",
  "docs/engineering/harness-simplification/specifications/SPEC-KIS-006.md",
  "docs/engineering/harness-simplification/verification-records/VREC-KIS-012.md",
  "docs/engineering/harness-simplification/verification/VER-KIS-006.md",
  "docs/engineering/harness-simplification/work-orders/WO-KIS-012.md",
  "docs/notes/recovery-integration-controls.md",
  "plugins/verity-plane/common/skills/change/references/authority.md",
  "plugins/verity-plane/common/skills/evidence/references/external-actions.md",
  "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md",
  "templates/repository/standard/docs/engineering/QUALITY_GATES.md",
  "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md",
  "tests/test_instruction_architecture.py",
  "tests/test_workflow_documentation_contract.py",
]

[relations]
implements = ["REQ-KIS-012"]
specifications = ["SPEC-KIS-006"]
verification = ["VER-KIS-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-20T06:27:29Z"
decided_by = "engineering-owner"
reason = "On 2026-09-20 the owner approved the presented recovery artifact package with \"i approve\". Record approval of this reviewed artifact in the named owner role. Reviewed full-byte SHA-256: 50830d2ff2fac97bd8adb968f5906f180eca80e4e43e8e7419fb0c55d3c204ef. DEC-KIS-001 separately records the explicit owner-review choice. WO approval grants the bounded execution operations in DR-015; this transition records no implementation result, assurance acceptance or external action."
scope_paths = [".github/CODEOWNERS", ".github/PULL_REQUEST_TEMPLATE.md", ".github/workflows/candidate-evidence.yml", ".github/workflows/engineering-harness.yml", ".github/workflows/pages-publication.yml", ".github/workflows/publish-dashboard-pages.yml", ".github/workflows/publish-pypi.yml", "docs/engineering/harness-simplification/decisions/DEC-KIS-001.md", "docs/engineering/harness-simplification/evidence/WO-KIS-012/", "docs/engineering/harness-simplification/requirements/REQ-KIS-012.md", "docs/engineering/harness-simplification/specifications/SPEC-KIS-006.md", "docs/engineering/harness-simplification/verification-records/VREC-KIS-012.md", "docs/engineering/harness-simplification/verification/VER-KIS-006.md", "docs/engineering/harness-simplification/work-orders/WO-KIS-012.md", "docs/notes/recovery-integration-controls.md", "plugins/verity-plane/common/skills/change/references/authority.md", "plugins/verity-plane/common/skills/evidence/references/external-actions.md", "templates/repository/standard/docs/engineering/DECISION_RIGHTS.md", "templates/repository/standard/docs/engineering/QUALITY_GATES.md", "templates/repository/standard/docs/engineering/templates/WORK_ORDER.template.md", "tests/test_instruction_architecture.py", "tests/test_workflow_documentation_contract.py"]
+++

# Match repository protection to the stated approval policy

## Objective and scope

Implement SPEC-KIS-006 for REQ-KIS-012; meet VER-KIS-006. The work addresses assessment findings
F1, F2, F5, F6. Fix only the specified behavior, its affected existing tests and
its candidate-policy/plugin explanations. The exact admitted paths are above.

## Decision envelope

This draft proposes the listed work; it records no approval or execution grant.
After actual WO approval, the executor may make local implementation choices,
edit the named paths, run checks, retain evidence, record qualifying completion
and prepare required verification through the installed single procedure.
The assurance classification above is proposed for the engineering owner's
approval; no owner decision has been fabricated by writing it.

## Limits and dependencies

Read-only inventory and drafting can proceed independently. Approval and execution of this chain wait for DEC-KIS-001. Live settings changes require a concrete owner-authorized proposal; do not silently block the other three chains.

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

Meet VER-KIS-006. Run focused affected checks and the repository-required
regression, package, CLI, graph, doctor and phase-appropriate preflight checks
at the applicable implementation boundaries. Use the selected released
evaluator for governing operations; candidate runs establish proposed behavior
only. Use the existing supported Windows/Linux CI routes rather than adding
a qualification pipeline.

Keep one concise evidence summary under evidence/WO-KIS-012/ with the
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
