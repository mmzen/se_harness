+++
id = "WO-HUP-002"
type = "work_order"
title = "Adopt exact public 0.6.0 as the standard root evaluator"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T17:17:09Z"
decided_by = "repository-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-23T17:21:15Z"
decided_by = "engineering-owner"

[assurance]
commit_bound_verification = "required"
rationale = "Every later root lifecycle action and managed CI gate depends on the exact public evaluator, schema-3 lock, and complete-graph validation established by this transaction."
decided_by = "repository-owner"

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af"
target_version = "0.6.0"
target_payload_sha256 = "c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42"
target_archive_name = "se_harness-0.6.0-py3-none-any.whl"
target_archive_sha256 = "2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7"
publication = "immutable"
authorized_by = "repository-owner"

[execution_scope]
paths = [
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  ".gitattributes",
  ".github/workflows/engineering-harness.yml",
  "AGENTS.md",
  "CLAUDE.md",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/DECISION_RIGHTS.md",
  "docs/engineering/QUALITY_GATES.json",
  "docs/engineering/QUALITY_GATES.md",
  "docs/engineering/README.md",
  "docs/engineering/REPOSITORY_CONTEXT.md",
  "docs/engineering/TRACEABILITY.md",
  "docs/engineering/WORKFLOW.json",
  "docs/engineering/WORKFLOW.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/capabilities/CAP-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-verification.md",
  "docs/engineering/repository-harness-upgrade/intent/INT-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-004.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-005.md",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-006.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-002.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-002.md",
  "docs/engineering/templates/RELEASE_RECORD.template.md",
  "docs/engineering/templates/VERIFICATION_RECORD.template.md",
  "docs/engineering/templates/WORK_ORDER.template.md",
  "docs/notes/developing-se-harness.md",
  "scripts/generate_harness_dashboard.py",
  "scripts/harness_explorer/index.template.html",
  "scripts/inspect_engineering_artifacts.py",
  "scripts/validate_engineering_artifacts.py",
  "tests/test_artifact_catalog.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_dashboard_webui.py",
  "tests/test_instruction_architecture.py",
  "tests/test_predecessor_assessment_contract.py",
  "tests/test_revision_provenance.py",
  "tests/test_standard_repository_lifecycle.py",
  "tests/test_validation_taxonomy.py",
]

[relations]
implements = ["REQ-HUP-004", "REQ-HUP-005", "REQ-HUP-006"]
specifications = ["SPEC-HUP-002"]
architecture = ["ARCH-HUP-002"]
verification = ["VER-HUP-002"]

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-23T19:14:40Z"
decided_by = "engineering-owner"
+++

# Work Order: Adopt exact public 0.6.0 as the standard root evaluator

## Lifecycle

The repository owner approved the exact packet and bounded transaction on 2026-08-23. The work order records the exact observed public identity, prior lock, managed dry-run, and integration boundary; execution starts only through its separately recorded `approved` to `in_progress` transition. After the public 0.6.0 handoff gate exposed the packet's missing machine scope, the repository owner explicitly authorized the exact `[execution_scope]` amendment and corrections to the affected files on 2026-08-23 without changing lifecycle status.

## Objective

Use exact public 0.6.0 outside the checkout to replace the released 0.5.0 schema-2 standard root with one evidence-bound schema-3 root candidate, without changing product, release, publication, deployment, maintenance, or history.

## In scope

- Prove public wheel and installed payload identity.
- Run current-governor/predecessor-compatible start observations and public-0.6 dry-run review.
- Move only the three post-release migration LF rules outside the public 0.6-managed `.gitattributes` block, preserving their order and semantics.
- Apply the exact public managed plan with this work order and canonical evidence output.
- Update owner context only where required to state the new selected governor truthfully.
- Run complete local qualification and retain a changed-surface ledger.
- Transition only `WO-HUP-002` to `implemented` after all local gates pass, under explicit authority.

## Out of scope

Product source/templates or version changes; RLS, VREC, REL, candidate, tag, release, PyPI, Pages, publication-workflow, maintenance, branch-policy, credential, external-policy, deployment, root-history rewrite, compatibility-history deletion, commit, push, PR, merge, or assurance transition.

## Expected change surface

- The 18 public-0.6 update/add paths listed by `SPEC-HUP-002` and installer-owned `.engineering-harness.lock`.
- `.gitattributes` only for the exact marker-boundary adjustment.
- `docs/engineering/REPOSITORY_CONTEXT.md` and `docs/notes/developing-se-harness.md` only if necessary to state the selected governor accurately.
- The owner-controlled region of `AGENTS.md` only to identify the 0.6.0 governor and all lock-managed paths accurately.
- This nine-artifact HUP packet, HUP README/index updates, canonical transaction JSON, human-readable evidence, and this work order's authorized lifecycle state.
- The eight exact regression-test files named in `[execution_scope]`, only to replace pre-upgrade root assumptions with released-root/candidate-source identity-aware assertions.

## Constraints

- Applying runtime must be the exact public identity in `[evaluator_upgrade]`.
- Any plan path outside the reviewed set stops for amendment.
- No `customized` or `conflict` action may be waived.
- Complete graph must pass public 0.6.0 directly after apply.
- Existing migration LF rules must remain effective and candidate template bytes must remain unchanged.

## Required verification

Execute `VER-HUP-002`, including identity, plan/apply/no-op, canonical evidence, lock schema and digests, doctor, complete validate, inspect, dashboard, preflight/review, full tests, workflow parsing, diff checks, secret/path review, and non-root preservation comparisons.

## Stop conditions

Stop on wrong identity, prior-lock mismatch, plan drift, customization, conflict, partial transaction, evidence collision, failed graph/test, unexpected warning, product/release change, or any need for an excluded lifecycle or external action.

## Approval requested

Approve `INT-HUP-002`, `CAP-HUP-002`, `REQ-HUP-004` through `REQ-HUP-006`, `SPEC-HUP-002`, `ARCH-HUP-002` including its no-significant-decision assessment, `VER-HUP-002`, and `WO-HUP-002`; authorize their draft-to-approved transitions, `WO-HUP-002` start, the exact `.gitattributes` integration adjustment, and the bounded public-0.6 `upgrade --apply` transaction with retained evidence. Commit, push, PR, merge, VREC transition, release, publication, deployment, maintenance mutation, credentials, and external policy remain separate.
