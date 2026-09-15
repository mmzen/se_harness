+++
id = "WO-HUP-019"
type = "work_order"
title = "Upgrade the repository evaluator from 0.17.0 to 0.18.0"
status = "implemented"
owners = ["repository-owner", "engineering-owner"]
created = "2026-09-15"
updated = "2026-09-15"
[assurance]
commit_bound_verification = "required"
rationale = "Later engineering decisions depend on the new root evaluator, its policy and retained evidence identity."
decided_by = "engineering-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "CLAUDE.md", "ENGINEERING_HARNESS.md", "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/OPERATING_CARD.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/TRACEABILITY.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-013.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-019-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-019/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-037.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-038.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-019.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-019.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-019.md", "docs/engineering/templates/ADR.template.md", "docs/engineering/templates/ARCHITECTURE.template.md", "docs/engineering/templates/CAPABILITY.template.md", "docs/engineering/templates/INTENT.template.md", "docs/engineering/templates/RELEASE_CONTRACT.template.md", "docs/engineering/templates/RELEASE_RECORD.template.md", "docs/engineering/templates/REQUIREMENT.template.md", "docs/engineering/templates/RISK.template.md", "docs/engineering/templates/SPECIFICATION.template.md", "docs/engineering/templates/VERIFICATION.template.md", "docs/engineering/templates/VERIFICATION_RECORD.template.md", "docs/engineering/templates/WORK_ORDER.template.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "pyproject.toml", "se_harness/__init__.py", "tests/"]

[relations]
implements = ["REQ-HUP-037", "REQ-HUP-038"]
specifications = ["SPEC-HUP-019"]
architecture = ["ARCH-HUP-013"]
verification = ["VER-HUP-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-15T11:01:51Z"
decided_by = "engineering-owner"
reason = "The owner replied \"i approve evaluator upgrade\" to the reviewed WO-HUP-019 scope and its five governing drafts on 2026-09-15. This records approval of the selected artifact, including the proposed architecture assessment and required assurance classification where applicable. The accepted scope authorizes start, completion only after passing checks, and ready verification-record preparation; independent verification and external integration remain separate."
scope_paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "CLAUDE.md", "ENGINEERING_HARNESS.md", "docs/engineering/ARTIFACT_AUTHORING.md", "docs/engineering/DECISION_RIGHTS.md", "docs/engineering/OPERATING_CARD.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/TRACEABILITY.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-013.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-019-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-019/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-037.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-038.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-019.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-019.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-019.md", "docs/engineering/templates/ADR.template.md", "docs/engineering/templates/ARCHITECTURE.template.md", "docs/engineering/templates/CAPABILITY.template.md", "docs/engineering/templates/INTENT.template.md", "docs/engineering/templates/RELEASE_CONTRACT.template.md", "docs/engineering/templates/RELEASE_RECORD.template.md", "docs/engineering/templates/REQUIREMENT.template.md", "docs/engineering/templates/RISK.template.md", "docs/engineering/templates/SPECIFICATION.template.md", "docs/engineering/templates/VERIFICATION.template.md", "docs/engineering/templates/VERIFICATION_RECORD.template.md", "docs/engineering/templates/WORK_ORDER.template.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "pyproject.toml", "se_harness/__init__.py", "tests/"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-15T11:04:04Z"
decided_by = "engineering-owner"
reason = "Started under the owner approval of the reviewed evaluator upgrade on 2026-09-15, which authorized execution of this scope. Start preflight passed with no diagnostics and the complete reading manifest was read."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-15T11:40:51Z"
decided_by = "codex"
reason = "Execution of DR-WO-COMPLETE under recorded engineering-owner approval; relevant local gates passed. Completed under the owner-approved WO-HUP-019 scope after the corrected full source suite passed (1068 tests, zero failures or errors, 15 skips), released 0.18.0 doctor and graph validation passed, released-root qualification and review preflight passed, replay reported 41 unchanged paths, and the complete Git-derived handoff passed. The public wheel and payload match RLS-SEH-027. Candidate source is 0.19.0; the two test corrections address only adopted-root wording and CI ownership. Retained evidence is in the WO-HUP-019 evidence directory. This records implementation only; independent assurance and external integration remain separate."
+++

# Upgrade the repository evaluator from 0.17.0 to 0.18.0

## Objective

Adopt the published, checksum-verified 0.18.0 evaluator in this repository through its installer. Keep the supplied workflow, guidance and development identity consistent.

## Lifecycle

The owner approved the reviewed evaluator upgrade on 2026-09-15 with "i approve evaluator upgrade". The front matter records the applied lifecycle decisions. Independent verification remains separate.

## In scope

- Apply the reviewed plan: 25 supplied updates, 11 preserved editable adoptions and five unchanged supplied paths.
- Select every replacement listed in SPEC-HUP-019 explicitly, preserving owner content outside managed fragments.
- Retain one transaction document with the prior committed lock and new evaluator identity.
- Advance candidate version declarations to 0.19.0 so the existing CI rehearsal has a successor pair.
- Update current owner instructions and development notes to describe 0.18.0 governance and the new ownership modes.
- Correct only demonstrated test assumptions about the root identity or supplied-file ownership.
- Run the verification contract and retain a concise result summary.

## Out of scope

Plugin installation or publication; product behavior changes; historical release or verification record edits; remote commits, pushes, pull requests, merges, tags and deployments; independent verification or release decisions.

## Authorized decision envelope

After approval, the implementer may select external runtime and log locations, write clear current instructions and make the bounded identity-only test corrections.
Changing package identity, the replacement set or product behavior requires a revised scope.

## Required verification

Execute VER-HUP-019, including the full source suite and the released evaluator's applicable gates. A ready verification record is a separate preparation action.

## Evidence to record

Use docs/engineering/repository-harness-upgrade/evidence/WO-HUP-019/ for the short summary and the sibling WO-HUP-019-evaluator-upgrade.json for the transaction.

## Stop conditions

Stop before implementation until the six draft artifacts are approved and this work order is explicitly started.
Stop for unexpected installer actions, changed digests, failing gates or corrections outside the declared scope.

## Completion report format

Report actual changed paths, checks, package identity, remaining decisions and the evaluator's selected workflow result. Preserve the real lifecycle state.

## Approval scope annotation (2026-09-15)

The 0.17.0 evaluator applied the owner's approval and start before this work
order upgraded the root. That approval explicitly covered start, completion
after passing checks and ready verification-record preparation, but 0.17.0
did not serialize the approved paths in its event.

The executor retained those exact already-approved paths as `scope_paths` in
the existing approval event for 0.18.0's execution checks. The reviewed scope,
original reason, actor, timestamp and lifecycle states are unchanged. This
annotation carries forward the owner's existing instruction; it grants no new
scope or independent assurance authority.
