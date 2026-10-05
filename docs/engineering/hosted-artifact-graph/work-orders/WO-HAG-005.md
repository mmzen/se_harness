+++
id = "WO-HAG-005"
type = "work_order"
title = "Reconcile the hosted sandbox with released evaluator 0.22.1"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because subsequent hosted work depends on the exact evaluator, revised definitions, integrated code and preserved evidence."
decided_by = "mmzen"

[execution_scope]
paths = [
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  ".github/workflows/engineering-harness.yml",
  "README.md",
  "docs/engineering/README.md",
  "docs/engineering/hosted-artifact-graph/README.md",
  "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-001.md",
  "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-002.md",
  "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-005/",
  "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-003.md",
  "docs/engineering/hosted-artifact-graph/verification/VER-HAG-001.md",
  "docs/engineering/hosted-artifact-graph/verification/VER-HAG-004.md",
  "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-005.md",
  "docs/engineering/release-0-22-1/README.md",
  "docs/engineering/release-0-22-1/decisions/DEC-RLS-009.md",
  "docs/engineering/release-0-22-1/evidence/RLS-SEH-033-evaluator.json",
  "docs/engineering/release-0-22-1/evidence/VREC-RLS-003-evaluator.json",
  "docs/engineering/release-0-22-1/evidence/VREC-RLS-004-evaluator.json",
  "docs/engineering/release-0-22-1/evidence/VREC-SEH-033-evaluator.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/WO-RLS-040-handoff.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/WO-RLS-040-pre-action.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/approval.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/build-replay.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/bundle.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/head-build-replay.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/prior-release-build-replay.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/review.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/source-summary.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-plan.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-preparation.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-readiness.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-readiness.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-build-replay.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-bundle.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-capture-observations-index.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-capture-observations.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-evidence-receipt.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-marketplace-staging.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-package-identity.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-qualification.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-review-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-verification-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/integration.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/pre-completion-packets.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/preparation-completion-observations.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-activation-observations.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-configuration-applied.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-configuration-proposal.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-observations.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/publication-hygiene.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/qualification-archive.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/qualification-initial.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/qualification-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ready-record-replay-receipt.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ready-record-replay.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ready-release-preparation.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/release-owner-correction-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/release-owner-correction-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/release-owner-correction.patch",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-040/topology-candidate-measure.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/WO-RLS-041-handoff.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-assembly-inventory.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-context-bound.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-one-final-proposal-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-one-independent-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-assembly-inventory.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-legacy-final-proposal-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-legacy-independent-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-successor-final-proposal-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-successor-independent-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/correction-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/defect-package-validate.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/defect-plan.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-acceptance-observations.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-deferral-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-proposal-preparation.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/final-staging-review-publication.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/missing-evidence-linux.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/missing-evidence-windows.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-archive.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-initial.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-walkthroughs-index.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-walkthroughs.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/package-identity.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/preparation-marketplace-commit.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-041/qualification-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/README.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/WO-RLS-042-handoff.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/claude-code-public-fresh.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/claude-code-public-update.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-assessment.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-lifecycle.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/codex-public-fresh.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/codex-public-update.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/delivery-result.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/documentation-observations.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/evaluator-public-install.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/handoff.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/integration-receipts.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/maintenance-line.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/marketplace-public-ref.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/observations.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/pages-observations.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/publisher.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-042/release-marker-receipt.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/REL-SEH-035-accepted-before.txt",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/WO-RLS-043-handoff.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/amendment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/approval-and-regressions.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/claude-one-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/claude-two-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/codex-legacy-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/codex-successor-assessment.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-build-replay.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-bundle.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-claude-assembly-inventory.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-codex-assembly-inventory.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-native-index.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-native.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-package-identity.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-qualification-review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-runtime-index.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-runtime.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-topology-candidate-measure.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/correction-qualification.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/results-publication-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-043/source-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/WO-RLS-044-handoff.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/assessment.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/completion-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/handoff.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/implementation.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/preparation-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/proposal-checks.zip",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/proposal-inputs.json",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/proposed-documentation.patch",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/review.md",
  "docs/engineering/release-0-22-1/evidence/WO-RLS-044/verification-review.md",
  "docs/engineering/release-0-22-1/release/REL-SEH-035.md",
  "docs/engineering/release-0-22-1/releases/RLS-SEH-033.md",
  "docs/engineering/release-0-22-1/risks/RISK-RLS-007.md",
  "docs/engineering/release-0-22-1/verification-records/VREC-RLS-003.md",
  "docs/engineering/release-0-22-1/verification-records/VREC-RLS-004.md",
  "docs/engineering/release-0-22-1/verification-records/VREC-SEH-033.md",
  "docs/engineering/release-0-22-1/verification/VER-RLS-004.md",
  "docs/engineering/release-0-22-1/verification/VER-RLS-005.md",
  "docs/engineering/release-0-22-1/verification/VER-RLS-036.md",
  "docs/engineering/release-0-22-1/verification/VER-RLS-037.md",
  "docs/engineering/release-0-22-1/verification/VER-RLS-038.md",
  "docs/engineering/release-0-22-1/work-orders/WO-RLS-040.md",
  "docs/engineering/release-0-22-1/work-orders/WO-RLS-041.md",
  "docs/engineering/release-0-22-1/work-orders/WO-RLS-042.md",
  "docs/engineering/release-0-22-1/work-orders/WO-RLS-043.md",
  "docs/engineering/release-0-22-1/work-orders/WO-RLS-044.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-028-evaluator.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030-evaluator-upgrade.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/WO-HUP-030-handoff.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/commands.zip",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/handoff.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/lifecycle.zip",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/preparation.zip",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/results.json",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/review.md",
  "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/verification-preparation.md",
  "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-028.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-025.md",
  "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-030.md",
  "docs/engineering/self-hosting-boundary/SELF_HOSTING.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/plugin-installation-guide.md",
  "docs/notes/plugin-marketplace-publication.md",
  "docs/notes/release-delivery-completion.md",
  "plugins/verity-plane/claude-code/.claude-plugin/plugin.json",
  "plugins/verity-plane/claude-code/README.md",
  "plugins/verity-plane/codex/.codex-plugin/plugin.json",
  "plugins/verity-plane/codex/README.md",
  "pyproject.toml",
  "release/plugin-marketplace/README.md",
  "se_harness/__init__.py",
  "se_harness/workflow.py",
  "tests/plugin_integration/package_assembly/test_refresh_guidance.py",
  "tests/test_workflow_execution.py",
]

[relations]
implements = ["REQ-HAG-007", "REQ-HAG-008"]
specifications = ["SPEC-HAG-003"]
architecture = ["ARCH-HAG-001", "ADR-HAG-001"]
verification = ["VER-HAG-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-05T12:41:38Z"
decided_by = "mmzen"
reason = "Human mmzen answered \"I approve\" to the reviewed WO-HAG-005 / VER-HAG-004 request, including DEC-HAG-002 bounded-manual-revision for the exact SPEC-HAG-003 and VER-HAG-001 replacements, required commit-bound verification, and ordinary updates to draft PR #535 in mmzen/se_harness from codex/hosted-artifact-phase1 to codex/hosted-artifact-graph-inputs, including ready-record review and the later separately supplied verification decision. The review binding SHA-256 is 2dd5104adee7a1f8cc94df384ae62f6cbc0169448d91dae738dedb7292acab0a. Earlier accepted bytes and lifecycle history are preserved. This is an explicit bounded manual amendment authorization; it grants no general amendment mechanism, verification acceptance, risk acceptance, merge, release or deployment. No machine lifecycle rule or required gate is waived."
scope_paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "README.md", "docs/engineering/README.md", "docs/engineering/hosted-artifact-graph/README.md", "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-001.md", "docs/engineering/hosted-artifact-graph/decisions/DEC-HAG-002.md", "docs/engineering/hosted-artifact-graph/evidence/WO-HAG-005/", "docs/engineering/hosted-artifact-graph/specifications/SPEC-HAG-003.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-001.md", "docs/engineering/hosted-artifact-graph/verification/VER-HAG-004.md", "docs/engineering/hosted-artifact-graph/work-orders/WO-HAG-005.md", "docs/engineering/release-0-22-1/README.md", "docs/engineering/release-0-22-1/decisions/DEC-RLS-009.md", "docs/engineering/release-0-22-1/evidence/RLS-SEH-033-evaluator.json", "docs/engineering/release-0-22-1/evidence/VREC-RLS-003-evaluator.json", "docs/engineering/release-0-22-1/evidence/VREC-RLS-004-evaluator.json", "docs/engineering/release-0-22-1/evidence/VREC-SEH-033-evaluator.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/WO-RLS-040-handoff.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/WO-RLS-040-pre-action.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/approval.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/build-replay.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/bundle.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/head-build-replay.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/prior-release-build-replay.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/review.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ci/source-summary.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-plan.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-preparation.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-readiness.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-readiness.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/complete-release-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-build-replay.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-bundle.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-capture-observations-index.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-capture-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-evidence-receipt.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-marketplace-staging.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-package-identity.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-qualification.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-review-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/final-verification-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/integration.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/pre-completion-packets.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/preparation-completion-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-activation-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-configuration-applied.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-configuration-proposal.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/provider-observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/publication-hygiene.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/qualification-archive.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/qualification-initial.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/qualification-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ready-record-replay-receipt.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ready-record-replay.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/ready-release-preparation.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/release-owner-correction-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/release-owner-correction-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/release-owner-correction.patch", "docs/engineering/release-0-22-1/evidence/WO-RLS-040/topology-candidate-measure.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/WO-RLS-041-handoff.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-assembly-inventory.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-context-bound.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-one-final-proposal-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/claude-one-independent-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-assembly-inventory.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-legacy-final-proposal-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-legacy-independent-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-successor-final-proposal-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/codex-successor-independent-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/correction-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/defect-package-validate.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/defect-plan.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-acceptance-observations.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-deferral-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/desktop-proposal-preparation.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/final-staging-review-publication.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/missing-evidence-linux.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/missing-evidence-windows.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-archive.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-initial.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-walkthroughs-index.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/native-walkthroughs.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/package-identity.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/preparation-marketplace-commit.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-041/qualification-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/README.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/WO-RLS-042-handoff.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/claude-code-public-fresh.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/claude-code-public-update.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-assessment.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/closeout-lifecycle.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/codex-public-fresh.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/codex-public-update.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/delivery-result.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/documentation-observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/evaluator-public-install.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/handoff.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/integration-receipts.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/maintenance-line.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/marketplace-public-ref.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/pages-observations.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/publisher.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-042/release-marker-receipt.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/REL-SEH-035-accepted-before.txt", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/WO-RLS-043-handoff.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/amendment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/approval-and-regressions.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/claude-one-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/claude-two-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/codex-legacy-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/codex-successor-assessment.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-build-replay.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-bundle.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-claude-assembly-inventory.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-codex-assembly-inventory.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-native-index.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-native.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-package-identity.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-qualification-review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-runtime-index.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-runtime.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/corrected-topology-candidate-measure.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/correction-qualification.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/results-publication-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-043/source-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/WO-RLS-044-handoff.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/assessment.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/completion-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/handoff.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/implementation.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/preparation-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/proposal-checks.zip", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/proposal-inputs.json", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/proposed-documentation.patch", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/review.md", "docs/engineering/release-0-22-1/evidence/WO-RLS-044/verification-review.md", "docs/engineering/release-0-22-1/release/REL-SEH-035.md", "docs/engineering/release-0-22-1/releases/RLS-SEH-033.md", "docs/engineering/release-0-22-1/risks/RISK-RLS-007.md", "docs/engineering/release-0-22-1/verification-records/VREC-RLS-003.md", "docs/engineering/release-0-22-1/verification-records/VREC-RLS-004.md", "docs/engineering/release-0-22-1/verification-records/VREC-SEH-033.md", "docs/engineering/release-0-22-1/verification/VER-RLS-004.md", "docs/engineering/release-0-22-1/verification/VER-RLS-005.md", "docs/engineering/release-0-22-1/verification/VER-RLS-036.md", "docs/engineering/release-0-22-1/verification/VER-RLS-037.md", "docs/engineering/release-0-22-1/verification/VER-RLS-038.md", "docs/engineering/release-0-22-1/work-orders/WO-RLS-040.md", "docs/engineering/release-0-22-1/work-orders/WO-RLS-041.md", "docs/engineering/release-0-22-1/work-orders/WO-RLS-042.md", "docs/engineering/release-0-22-1/work-orders/WO-RLS-043.md", "docs/engineering/release-0-22-1/work-orders/WO-RLS-044.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/VREC-HUP-028-evaluator.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030-evaluator-upgrade.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/WO-HUP-030-handoff.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/commands.zip", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/handoff.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/lifecycle.zip", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/preparation.zip", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/results.json", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/review.md", "docs/engineering/repository-harness-upgrade/evidence/WO-HUP-030/verification-preparation.md", "docs/engineering/repository-harness-upgrade/verification-records/VREC-HUP-028.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-025.md", "docs/engineering/repository-harness-upgrade/work-orders/WO-HUP-030.md", "docs/engineering/self-hosting-boundary/SELF_HOSTING.md", "docs/notes/developing-se-harness.md", "docs/notes/harness-installation-and-upgrades.md", "docs/notes/harnessctl-reference.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/release-delivery-completion.md", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "plugins/verity-plane/claude-code/README.md", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/codex/README.md", "pyproject.toml", "release/plugin-marketplace/README.md", "se_harness/__init__.py", "se_harness/workflow.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py", "tests/test_workflow_execution.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-05T12:43:11Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Reconcile the hosted sandbox with released evaluator 0.22.1

## Objective

Use released 0.22.1 for the remaining hosted sandbox work. Preserve completed
Phase 1 work, earlier decisions and exact historical evidence. This is a draft.

## Exact inputs

- HAG source: `64b4feb0cbaff06111876a1d4c0cc35a6c814415`, branch `codex/hosted-artifact-phase1`.
- Merged release/adoption: `d7eeb2ae785928925669695074be7bdd6ccb1e0a`, `main` after PR #540.
- Existing PR #535 target: `codex/hosted-artifact-graph-inputs`, `be1812e7042081014cc7682da8b9cd3822d9071f`.
- Public evaluator wheel SHA-256: `cb35c3c4eb51fe0fca575a9340b1cba6cd63b5f7133a0ebeb3fd32b4ed863053`.
- Public payload SHA-256: `0e7b7c2bc10b06150c6c1ebe88d796d047f5d906bdfb5ef4e00914a56c79e7ff`.

## In scope

1. Apply only the separately and explicitly authorized linked revisions of
   SPEC-HAG-003 and VER-HAG-001, preserving accepted bytes and lifecycle history.
   DEC-HAG-002 selects the route. Ordinary work approval alone does not grant
   the manual exception. Keep the exact replacement proposal outside the
   repository until that decision is actually given and recorded.
2. Integrate the exact main commit above into the HAG branch with a merge,
   preserving both histories. Resolve only the engineering index conflict by
   retaining both sets of entries. Do not replace the HAG tree with main.
3. Reuse main's approved 0.22.1 selection, CI pin, source 0.22.2 and plugin
   0.2.6 source metadata. Preserve the 0.22.0 environment. Activate the merged
   checkout through plugin setup and inspect its exact released identity.
4. Record mmzen's existing DEC-HAG-001 `extend-evaluator` answer using released
   `decide`, actual identity `mmzen` and established owner `engineering-owner`.
   Do not ask for that answer again or change the approved WO-HAG-001 owner.
5. Run VER-HAG-004, retain evidence, complete this work and prepare its exact
   commit-bound verification. Update the HAG index with actual results.

## Out of scope

No new product behavior, hosted service implementation, public release,
marketplace delivery, host installation, deployment, risk acceptance or merge
of PR #535. This work does not complete WO-HAG-001 or satisfy VER-HAG-001's
twelve hosted scenarios. RISK-HAG-001 remains raised and Cypher remains required.
Earlier VREC-HAG-001/002 keep their candidates, decisions and bound evidence.

## Authorized decision envelope

Propose required commit-bound verification: subsequent hosted implementation
depends on the exact evaluator, revised definitions, integrated code and
preserved evidence. Human confirmation is pending. Add the actual assurance
classification and human identity only after that confirmation.

After approval, Codex may carry out the named local integration, required
checks, evidence capture and verification preparation through released commands.
No new lifecycle rule, relation, policy exception mechanism or decision identity
may be invented. The bounded manual content amendment requires the explicit
human instruction reviewed under DEC-HAG-002; all lifecycle transitions and
decision dispositions still use the selected released evaluator.

Propose ordinary pushes to `mmzen/se_harness:codex/hosted-artifact-phase1` and
updates to existing draft PR #535, keeping target
`codex/hosted-artifact-graph-inputs`. Publish this approved package and its ready
verification record for review, then the later separately supplied verification
decision. Retain unfinished WO-HAG-001 and remaining blockers in the PR body.
No force push, target change, gate bypass, merge or public release.

## Expected change surface

The exact file list above includes 180 paths from the read-only merge
preview. Each imported path is bounded to its exact reviewed main Git blob,
except `docs/engineering/README.md`, which combines both index additions, and
the automatic merges of `se_harness/workflow.py` and
`docs/notes/harnessctl-reference.md`, which require diff and regression review.
This transports the completed release/adoption records and code; it does not
reopen their decisions or authorize edits to their content.

- `.engineering-harness.toml` / `.engineering-harness.lock`: exact main selection.
- CI, package metadata, current guides and regression files named above:
  exact merged release/adoption behavior; no unrelated correction.
- Named release/adoption formal records and evidence: preserve exact main bytes.
- `docs/engineering/README.md`: retain HAG and current release/adoption links.
- SPEC-HAG-003 / VER-HAG-001: only the exact reviewed manual replacements.
- DEC-HAG-001: only the existing choice applied by released 0.22.1.
- DEC-HAG-002, VER-HAG-004 and this work order: this bounded package and decisions.
- HAG README: link this work and actual results.
- `evidence/WO-HAG-005/`: preserved accepted `.txt` bytes, amendment binding,
  exact integration manifest, commands/results, failures and assessment.

No test file is edited beyond the reviewed main transport. Existing checks and
focused released-evaluator probes supply verification. Future VREC and evaluator
evidence destinations are unresolved until capture. Existing rules admit a
record directly verifying this WO and its declared evaluator evidence. Check
the actual returned paths before writing; no parent directory is authorized.

## Required verification and evidence

Execute VER-HAG-004. Record command argv, working directory, exits, exact package
and Git identities, preservation comparisons and failures. The old evaluator
governs preparation; 0.22.1 governs only after approved adoption/integration.
Keep the candidate source separate from both released evaluator environments.

## Stop conditions

Stop the affected action for an unapproved/manual revision, changed reviewed
inputs, extra merge conflict, uncovered path, changed historical blob, failed
required gate, unsupported decision command, or missing evidence. Preserve
unrelated untracked work in the original HAG checkout. Reassess a moved source
or target; do not alter the comparison base to hide findings.

## Completion report

State the actual integrated commit and evaluator, recorded decisions, preserved
history, checks and remaining hosted coverage. Report the evaluator's next step.
This work is complete only when reconciliation and VER-HAG-004 pass; hosted
qualification remains a separate result under WO-HAG-001.
