+++
id = "WO-PLG-020"
type = "work_order"
title = "Implement explicit evaluator migration of retained skill ownership"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-12"
updated = "2026-09-12"
[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Later repository connection, integrity, recovery, upgrades, and release decisions rely on the correctness of changed evaluator behavior and ownership records."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/release_qualification.py",
  "se_harness/engine/generate_harness_dashboard.py",
  "se_harness/engine/dashboard_bundle.py",
  "se_harness/engine/dashboard_snapshot.py",
  "tests/test_report_output_safety.py",
  "se_harness/engine/validation_evidence.py",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "tests/test_harnessctl.py",
  "tests/test_workflow_documentation_contract.py",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-024.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-012.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-012.md",
  "docs/engineering/portable-managed-integrity/specifications/SPEC-PMI-001.md",
  "docs/engineering/plugin-integration/decisions/DEC-PLG-007.md",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-015.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-015-evaluator.json",
  "se_harness/cli.py",
  "se_harness/installer.py",
  "se_harness/integrity.py",
  "se_harness/preflight.py",
  "se_harness/mutation_guard.py",
  "se_harness/skill_ownership.py",
  "se_harness/skill_ownership_contract.json",
  "pyproject.toml",
  "tests/test_skill_ownership.py",
  "tests/fixtures/skill_ownership/",
  "tests/test_integration_package.py",
  "tests/test_mutation_guard.py",
  "tests/test_integrity_primitives.py",
  ".github/workflows/candidate-evidence.yml",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-020.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-020/",
  "docs/engineering/plugin-integration/README.md",
  "docs/notes/plugin-ownership-migration-2026-09-12.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-028.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-029.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-030.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-031.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-020.md",
  "docs/engineering/plugin-integration/architecture/ARCH-PLG-003.md",
  "docs/engineering/plugin-integration/architecture/adr/ADR-PLG-003.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-020.md",
  "docs/engineering/agentic-execution/requirements/REQ-AEX-009.md",
  "docs/engineering/agentic-execution/specifications/SPEC-AEX-005.md",
  "docs/engineering/technical-communication/requirements/REQ-TCM-004.md",
  "docs/engineering/technical-communication/specifications/SPEC-TCM-001.md",
  "docs/engineering/ci-pipeline/specifications/SPEC-CIP-003.md",
  "tests/test_ci_pipeline.py",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-027.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-016.md",
  "docs/notes/harnessctl-reference.md",
  "tests/test_cli_shape.py",
  "docs/engineering/ci-pipeline/requirements/REQ-CIP-009.md",
  "docs/engineering/ci-pipeline/verification/VER-CIP-003.md",
  "docs/notes/ci-pipeline.md",
  "docs/notes/developing-se-harness.md"
]

[relations]
implements = ["REQ-PLG-028", "REQ-PLG-029", "REQ-PLG-030", "REQ-PLG-031"]
specifications = ["SPEC-PLG-020"]
architecture = ["ARCH-PLG-003", "ADR-PLG-003"]
verification = ["VER-PLG-020"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-12T12:56:34Z"
decided_by = "engineering-owner"
reason = "The operator selected the reviewed WO-PLG-020 packet and execution delegation on 2026-09-12 with \"take the delegated route\", then approved its supplemental DEC-PLG-007 reconciliation and amendments with \"i approve DEC-PLG-007\u2019s `narrow-schema4-exception` with amendements\". Record only WO-PLG-020 approval as engineering-owner. The reviewed packet at 2d32b57bcdf805a83d5902fb37a3d2b7580c16e0 supplies the selected scope, eight applicability amendments, and candidate policy text. Implementation, assurance, release, and integration results are not recorded by this approval."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-12T13:27:35Z"
decided_by = "delegated-executor"
reason = "Delegated DR-WO-START under [delegation] class 'execution': required check 'validate' success at 6559568e995fc6e28f64e6bc5a6d4a6dc5dcf7de (check-run 103560311357, source github-checks). Begin the approved bounded evaluator migration after PR #461 merged."
+++

# Work Order: Implement explicit evaluator migration of retained skill ownership

## Lifecycle

The operator selected "take the delegated route" on 2026-09-12 in response to the reviewed packet approval and implementation question.
This selects the execution delegation class for WO-PLG-020. On 2026-09-12 the operator also approved DEC-PLG-007 and its amendments, resolving the additional lock-schema conflict.
The released evaluator records the nine selected packet approvals; the class can take effect only at the PR base with the required live candidate check.
Once this class-bearing WO is approved at the PR base and the exact candidate has a successful live GitHub validate check, delegated-executor may start, complete, and prepare the ready verification record.
Verification, release, integration, and external actions remain separately authorized decisions. A branch cannot activate its own delegation.

## Objective

Supply the released-evaluator capability required by DEC-PLG-004 and WO-PLG-009: reviewed migration from retained repository skills to an explicit plugin ownership binding.
The implementation includes safe restoration and ownership-aware integrity and upgrade behavior.

## In scope

- The new ownership command, bounded data-only plugin binding verification, versioned lock representation, shared effective inventory, and recoverable installer transaction.
- Both currently retained skills: harness-orient and harness-operator-brief; the seven current managed repository files and applicable existing host surfaces.
- Default installation regression, stale-input and concurrency protection, Windows/Linux fault injection, and non-promotable candidate package acceptance.
- Exact applicability amendments listed in the packet review, including the additional schema-floor reconciliation governed by DEC-PLG-007.
- Evaluator-evidence matching on a plugin-owned lock and recovery refusal after intervening owner changes or hostile recovery metadata.
- This work order's governing chain, retained evidence, and concise domain index entry.

## Out of scope

- WO-PLG-009 setup integration, native host configuration, real repository migration, user-home changes, plugin installation, global skill cleanup, or credentials.
- The three retired writing skills, unrelated skills, changes to retained core semantics, or changes to existing plugin hook behavior.
- Public release, promotable release build, version reservation, release adoption, support-profile expansion, and any change to the accepted C10/C11 limitation.
- Editing this checkout's hash-locked root installation, any existing VREC/RLS, or the terminal DEC-PLG-004 decision.

## Authorized decision envelope

After approval and an eligible delegated start, choose implementation decomposition, internal names, fixtures, and diagnostics within SPEC-PLG-020 and ADR-PLG-003.
Keep one standard governance contract; ownership is an explicit installation property, not an alternative policy profile.
Do not choose a new owner decision, weaken a refusal, widen the catalog, or silently add another installer mode.
DEC-PLG-007 selects the approved narrow schema-4 exception, recorded in all eight prior-contract applicability amendments. All other reviewed design choices retain their selected meaning.

## Constraints and dependencies

Baseline is main `3bf0ef2a7a2b4008efaa3cb79431d526d3f6f600`, after PRs #456, #457, #458, and #459.
The root is governed by released evaluator 0.17.0; candidate source is 0.18.0 and is not an installed governor.
Start requires approval of REQ-PLG-028 through REQ-PLG-031, SPEC-PLG-020, ARCH-PLG-003, ADR-PLG-003, VER-PLG-020, this WO, and the exact prior-contract applicability amendments, including disposition of DEC-PLG-007.
Read CAP-DST-001, INT-DST-001, SPEC-PLG-012, and all eight prior contracts named in the packet review before implementation.

DEC-PLG-004 at proposal commit `17382d8e7f7a5709f4f55facfe875fbf455e5794` already selected supported migration; its immutable decision remains unchanged.
WO-PLG-009 explicitly excludes evaluator-core changes and therefore cannot substitute for this work order.
WO-PLG-009 remains draft and ineligible for live connection until the new evaluator is independently verified, released, and adopted.
This packet introduces no release WO or version reservation. VREC-PLG-015 and its evaluator sidecar are reserved paths only; neither record is prepared yet.
The repository-owned governor-transition assessor remains schema-3-only; this WO supplies no schema-4 support claim for that separate tool.

## Expected change surface

Only the exact paths in execution_scope may change. Tests use disposable repositories and external temporary non-promotable package environments.
The implementation does not migrate the current checkout or remove its managed skill files.
If additional inventory consumers, managed policy sources, recovery facilities, or package entry points must change, revise this scope before editing them.

## Required verification

Satisfy VER-PLG-020's complete acceptance and fault matrix, repository-required tests, package checks, and released-evaluator review, scope, and handoff checks.
Compare candidate-source and isolated candidate-package behavior without external metadata contaminating source runtime identity.
Record Windows/Linux evidence and leave native host qualification explicitly outside this result.

## Evidence to record

Retain exact inputs, plan digests, before/after bytes, refusal outputs, crash/recovery observations, command arguments, candidate identities, and CI references under this WO's evidence directory.
Preparation notes and this packet are not implementation evidence; accountable definition approvals are recorded in the selected artifacts.

## Stop and escalate conditions

Stop for scope expansion, unresolved contract applicability, conflicting ownership, incomplete recovery, unsafe paths, unverified evaluator identity, or a required test failure.
Missing or unproven external provider identity cannot be relabeled as plugin readiness.
Failed native enforcement remains governed by DEC-PLG-006, not by this ownership change.

## Completion report format

Report actual ownership behavior, exact catalog, candidate identity, evidence and failures, retained limitations, lifecycle state, and one evaluator-derived next accountable step.
Do not claim release availability, WO-PLG-009 completion, native discovery, or a public rollout.


## Approved supplemental scope — 2026-09-12

At `2026-09-12T14:49:44Z`, the operator approved supplement revision 2 as engineering-owner for its ten exact scope additions, requirements-steward for REQ-ECP-027 and REQ-CIP-009, technical-owner for SPEC-ECP-016 and SPEC-CIP-003, and assurance-owner for VER-CIP-003's applicability amendment. The recorded instruction was: "i approve supplement revision 2 to reconcile the CI/CLI contracts and ten required scope additions".

The approved proposal has SHA-256 `6fa1ee1b63c28cb4a406834987911822659792194f100f45a856a89561814ff1` and is retained with the decision receipt under `docs/engineering/plugin-integration/evidence/WO-PLG-020/governance/`. The additional paths reconcile the Python 3.13 ownership acceptance, explicit command target and transaction outcomes, and corresponding CI/CLI documentation and tests. VER-PLG-020 remains unchanged. This approval records definitions and scope only; WO-PLG-020 remains in progress. Delegated completion and VREC preparation still require their live candidate gates; verification and release remain separate decisions.


## Approved legacy-reader reconciliation — 2026-09-12

The operator approved the four exact OWN07 appendices with "i approve the 4 amendements"; the approval was recorded at `2026-09-12T18:28:18Z`. The technical-owner decisions apply to SPEC-PLG-020, ARCH-PLG-003 and ADR-PLG-003, and the assurance-owner decision applies to VER-PLG-020. The reviewed proposal has SHA-256 `c7224fdd0dc6136753a1e2d42528a571ef2ffae185693e2f34a0b9ab9c7c2020`. Its exact bytes and the approval receipt are retained under this work order's governance evidence.

The approved boundary permits only the separately observed evidence/report behavior while retaining required refusal of installation, lock and formal-artifact mutations by the incompatible evaluator. The expanded real-command census and the required source/package/platform acceptance must pass before completion or VREC preparation. No lifecycle state, execution-scope path, release authority or native-host claim changes through this approval.

## Authorized report-output repair — 2026-09-12

After reviewing the two reproduced output-path failures, the operator instructed
"ok, fix both problems then". This authorizes repairing qualification output
protection on failure and dashboard output overlap protection in the candidate.
The necessary additional execution paths are
`se_harness/engine/dashboard_snapshot.py`,
`se_harness/release_qualification.py`,
`se_harness/engine/generate_harness_dashboard.py`,
`se_harness/engine/dashboard_bundle.py` and `tests/test_report_output_safety.py`;
the CLI, ownership acceptance tests, notes and this evidence directory are
already within scope. This records the concrete repair scope under the user's
instruction; it is not another compatibility exception or an assurance decision.

Keep normal report destinations usable, refuse protected destinations before
writing and recheck before output promotion, and retain candidate-source and
isolated-package regression evidence.
Published 0.17 bytes and their contrary observations remain unchanged. This
repair cannot establish that unpatched 0.17 now refuses those operations.
WO-PLG-020 remains in progress and its existing completion conditions remain.
