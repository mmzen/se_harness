+++
id = "WO-RLS-040"
type = "work_order"
title = "Prepare evaluator 0.22.1 and final release inputs"
status = "in_progress"
owners = ["mmzen"]
created = "2026-10-04"
updated = "2026-10-04"

[assurance]
commit_bound_verification = "required"
rationale = "mmzen confirmed required commit-bound verification because release and delivery decisions depend on these exact inputs."
decided_by = "mmzen"

[execution_scope]
paths = ["docs/engineering/release-0-22-1/", "docs/engineering/hosted-artifact-graph/", "pyproject.toml", "se_harness/__init__.py", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "se_harness/relation_policy.py", "se_harness/draft_validation.py", "se_harness/engine/validation_architecture.py", "se_harness/engine/validation_evidence.py", "se_harness/engine/validation_core.py", "se_harness/engine/validation_lifecycle.py", "se_harness/engine/validation_authoring.py", "se_harness/engine/validate_engineering_artifacts.py", "se_harness/preflight.py", "se_harness/cli.py", "se_harness/codes.py", "tests/test_draft_validation.py", "tests/test_relation_policy.py", "tests/test_artifact_authoring.py", "tests/test_authoring_gate.py", "tests/test_cli_shape.py", "tests/test_validation_taxonomy.py", "tests/test_one_validation.py", "templates/repository/standard/docs/engineering/harness/DRAFT_DEFINITIONS.md", "templates/repository/standard/docs/engineering/harness/DEFINITION_LINKS.md", "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md", "docs/notes/harnessctl-reference.md", "docs/notes/diagnostic-codes.md", "se_harness/decisions.py", "se_harness/risks.py", "se_harness/workflow_edges.py", "se_harness/workflow.py", "se_harness/engine/validation_decisions.py", "tests/test_decision_management.py", "tests/test_risk_management.py", "tests/test_workflow_execution.py", "tests/test_workflow_documentation_contract.py", "docs/notes/decision-artifacts.md", "templates/repository/standard/docs/engineering/harness/AUTHORITY.md", "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[relations]
implements = ["REQ-DST-006", "REQ-PLG-002", "REQ-RLO-018", "REQ-RLO-021", "REQ-RLO-023"]
specifications = ["SPEC-DST-001", "SPEC-PLG-001", "SPEC-RLO-006", "SPEC-RLO-007"]
verification = ["VER-RLS-036"]
architecture = ["ARCH-DST-001", "ADR-DST-001", "ARCH-PLG-001", "ADR-PLG-001", "ARCH-RLO-006", "ADR-RLO-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-10-04T18:24:52Z"
decided_by = "mmzen"
reason = "mmzen answered \"Approve preparation and review publication\" to the exact seven-artifact evaluator 0.22.1 / plugin 0.2.6 proposal: REL-SEH-035, WO-RLS-040/041/042 and VER-RLS-036/037/038, with required commit-bound verification. This approves bounded preparation and qualification of the two HAG fixes and main already-approved dashboard correction, ordinary review pushes/draft PRs from codex/release-0-22-1 to mmzen/se_harness:main, later verification-decision updates, read-only CI rehearsals and the codex/plugin-0-2-6-staging review ref. Human verification, merge, the exact complete-release decision, adoption and provider-setting changes remain separate. Reviewed draft hashes matched; only the human-confirmed assurance fields were added before preview. Reviewed SHA-256 282bf7fe002a94ac03de854c67e3a64ab1788ae8c7f69fbef84458d38e1fe7b1."
scope_paths = ["docs/engineering/release-0-22-1/", "docs/engineering/hosted-artifact-graph/", "pyproject.toml", "se_harness/__init__.py", "plugins/verity-plane/codex/.codex-plugin/plugin.json", "plugins/verity-plane/claude-code/.claude-plugin/plugin.json", "se_harness/relation_policy.py", "se_harness/draft_validation.py", "se_harness/engine/validation_architecture.py", "se_harness/engine/validation_evidence.py", "se_harness/engine/validation_core.py", "se_harness/engine/validation_lifecycle.py", "se_harness/engine/validation_authoring.py", "se_harness/engine/validate_engineering_artifacts.py", "se_harness/preflight.py", "se_harness/cli.py", "se_harness/codes.py", "tests/test_draft_validation.py", "tests/test_relation_policy.py", "tests/test_artifact_authoring.py", "tests/test_authoring_gate.py", "tests/test_cli_shape.py", "tests/test_validation_taxonomy.py", "tests/test_one_validation.py", "templates/repository/standard/docs/engineering/harness/DRAFT_DEFINITIONS.md", "templates/repository/standard/docs/engineering/harness/DEFINITION_LINKS.md", "templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md", "docs/notes/harnessctl-reference.md", "docs/notes/diagnostic-codes.md", "se_harness/decisions.py", "se_harness/risks.py", "se_harness/workflow_edges.py", "se_harness/workflow.py", "se_harness/engine/validation_decisions.py", "tests/test_decision_management.py", "tests/test_risk_management.py", "tests/test_workflow_execution.py", "tests/test_workflow_documentation_contract.py", "docs/notes/decision-artifacts.md", "templates/repository/standard/docs/engineering/harness/AUTHORITY.md", "templates/repository/standard/docs/engineering/harness/AUTHORIZE_WORK.md", "README.md", "release/plugin-marketplace/README.md", "plugins/verity-plane/codex/README.md", "plugins/verity-plane/claude-code/README.md", "docs/notes/plugin-installation-guide.md", "docs/notes/plugin-marketplace-publication.md", "docs/notes/developing-se-harness.md", "docs/notes/release-delivery-completion.md", "docs/notes/release-publication-rehearsal.md", "docs/notes/harness-installation-and-upgrades.md", "docs/engineering/plugin-integration/README.md", "docs/engineering/README.md", "tests/test_progressive_documentation.py", "tests/plugin_integration/package_assembly/test_refresh_guidance.py"]

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-10-04T18:28:48Z"
decided_by = "Codex"
reason = "Execution of DR-WO-START under recorded work-order approval; relevant local gates passed."
+++

# Prepare evaluator 0.22.1 and final release inputs

## Objective

Prepare a qualified evaluator 0.22.1 release containing standalone draft
validation and truthful decision-owner attribution, with plugin 0.2.6 staged
before final complete-release approval.

## In scope

1. Create an isolated review branch from main at
   82f5a0ed7438a73da8f03aee23ad02a9b8cc09e1. Preserve PR #535 and its target.
   Integrate only WO-HAG-002/003 correction source, tests and instructions from
   64b4feb0cbaff06111876a1d4c0cc35a6c814415. Compare exact bytes and retain their
   provenance. Do not merge the unfinished hosted branch wholesale.
2. Transport the HAG formal graph and retained evidence unchanged where needed
   for those governing chains and historical records. The HAG directory scope
   permits exact transport only; it does not authorize semantic edits there.
   Keep full Git history reachable. No server, remote adapter or hosted tests
   are included. Assess the full main comparison; no base change to hide paths.
3. Retain main's already-approved WO-DST-028 4 MiB dashboard target in release
   membership. Set/confirm both evaluator versions at 0.22.1 and both plugin
   manifests at 0.2.6. Check unused identities before build/publication.
4. Update named current guidance and its existing version expectations. Reuse
   the existing builder, CI and publisher. Do not implement new product fixes.
5. Qualify the exact combined candidate with VER-RLS-036. Combine staged plugin
   qualification from WO-RLS-041 into the final aggregate VREC. Preserve earlier
   VRECs and all bound bytes; historical acceptance is not final integration proof.
6. After human verification, prepare the tagged RLS, bind the two-build manifest,
   replay it and freeze the v2 delivery plan. Confirm actual provider readiness.
   Present one exact complete-release request covering all five surfaces.

## Expected change surface

The paths below were derived from both correction work orders and the current
release tooling, manifests, documentation consumers and existing release tests.
Correction paths permit extraction/integration of the reviewed behavior only.
The HAG directory permits unchanged records/evidence transport only. No candidate
execution is allowed to govern real artifacts.

The new release directory covers this package, its fixed evaluator companions,
build and delivery manifests, handoff/verification evidence and later decision
or publication receipts. VREC/RLS IDs are allocated only at capture/preparation;
inspect their actual returned paths. Required evidence files belong here, while
scratch scripts and builds remain outside the checkout. Existing CI/build policy
and provider settings require no edit; a discovered defect needs bounded review.

## Completion

Implementation completion means the release inputs and required qualification
evidence are prepared; it does not claim publication. VER-RLS-036 governs the
aggregate exact-candidate review. Publication and observations follow the later
matching complete-release grant through WO-RLS-042. Adoption and amendment of
the hosted evaluator pin remain separately proposed work after public delivery.

## Authority and limits

This is a draft. Propose required commit-bound verification; mmzen has not yet
confirmed this new classification or approved these work orders. No prior HAG
verification or draft-PR grant authorizes release preparation implementation.

After approval, Codex may execute local work, checks, bounded commits and record
preparation within this scope. Propose ordinary review pushes and draft PRs from
`codex/release-0-22-1` to `mmzen/se_harness:main`, including later verification
decisions and release receipts, plus existing read-only CI rehearsals. Plugin
staging may use `codex/plugin-0-2-6-staging` as a review ref; it must be an ordinary
child of the observed marketplace tip and must not update the public branch.

Human verification, merge and the final exact complete-release decision remain
separate. The latter may authorize all listed publication actions in one response
once immutable inputs, qualification and provider controls are ready. Until then,
no PyPI, release tag, latest/last, Pages or marketplace mutation is authorized.
No force-push, protection bypass, provider-setting change or adoption is covered.

Use released 0.22.0 outside the checkout as governor. Test candidate 0.22.1 only
in isolated environments. Preserve historical decisions, exact bound evidence,
and actual human attribution. Do not edit DEC-HAG-001, SPEC-HAG-003 or VER-HAG-001.

## Stop and report

Stop the affected action on missing required evidence, changed approved inputs,
uncovered files, conflicting remote state or missing provider controls. Do not
waive a required host test by borrowing a past release's accepted omission.
Report exact candidate, checks and skips, completed surfaces, outstanding work
and the evaluator's next step. No new lifecycle, service or authority format.
