+++
id = "WO-PLG-020"
type = "work_order"
title = "Implement explicit evaluator migration of retained skill ownership"
status = "draft"
owners = ["engineering-owner"]
created = "2026-09-12"
updated = "2026-09-12"
[assurance]
commit_bound_verification = "required"
rationale = "Later repository connection, integrity, recovery, upgrades, and release decisions rely on the correctness of changed evaluator behavior and ownership records."
decided_by = "engineering-owner"

[execution_scope]
paths = [
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
  "tests/test_cli.py",
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
  "docs/engineering/technical-communication/specifications/SPEC-TCM-001.md"
]

[relations]
implements = ["REQ-PLG-028", "REQ-PLG-029", "REQ-PLG-030", "REQ-PLG-031"]
specifications = ["SPEC-PLG-020"]
architecture = ["ARCH-PLG-003", "ADR-PLG-003"]
verification = ["VER-PLG-020"]
+++

# Work Order: Implement explicit evaluator migration of retained skill ownership

## Lifecycle

Draft prepared at the operator's request on 2026-09-12. This request authorizes preparation, not approval of these new definitions or implementation.
No delegation class is proposed. Approval, start, completion, assurance, integration, release, and adoption are separately recorded decisions.

## Objective

Supply the released-evaluator capability required by DEC-PLG-004 and WO-PLG-009: reviewed migration from retained repository skills to an explicit plugin ownership binding.
The implementation includes safe restoration and ownership-aware integrity and upgrade behavior.

## In scope

- The new ownership command, bounded data-only plugin binding verification, versioned lock representation, shared effective inventory, and recoverable installer transaction.
- Both currently retained skills: harness-orient and harness-operator-brief; the seven current managed repository files and applicable existing host surfaces.
- Default installation regression, stale-input and concurrency protection, Windows/Linux fault injection, and non-promotable candidate package acceptance.
- Exact applicability amendments to the four approved contracts listed in the packet review, after their accountable owners accept the proposed changes.
- This work order's draft chain, retained evidence, and concise domain index entry.

## Out of scope

- WO-PLG-009 setup integration, native host configuration, real repository migration, user-home changes, plugin installation, global skill cleanup, or credentials.
- The three retired writing skills, unrelated skills, changes to retained core semantics, or changes to existing plugin hook behavior.
- Public release, promotable release build, version reservation, release adoption, support-profile expansion, and any change to the accepted C10/C11 limitation.
- Editing this checkout's hash-locked root installation, any existing VREC/RLS, or the terminal DEC-PLG-004 decision.

## Authorized decision envelope

After approval and explicit start, choose implementation decomposition, internal names, fixtures, and diagnostics within SPEC-PLG-020 and ADR-PLG-003.
Keep one standard governance contract; ownership is an explicit installation property, not an alternative policy profile.
Do not choose a new owner decision, weaken a refusal, widen the catalog, or silently add another installer mode.
The draft schema-4 and recovery design must be accepted before it is implemented.

## Constraints and dependencies

Baseline is main `3bf0ef2a7a2b4008efaa3cb79431d526d3f6f600`, after PRs #456, #457, #458, and #459.
The root is governed by released evaluator 0.17.0; candidate source is 0.18.0 and is not an installed governor.
Start requires approval of REQ-PLG-028 through REQ-PLG-031, SPEC-PLG-020, ARCH-PLG-003, ADR-PLG-003, VER-PLG-020, this WO, and the exact prior-contract applicability amendments.
Read CAP-DST-001, INT-DST-001, SPEC-PLG-012, and the four prior contracts before implementation.

DEC-PLG-004 at proposal commit `17382d8e7f7a5709f4f55facfe875fbf455e5794` already selected supported migration; its immutable decision remains unchanged.
WO-PLG-009 explicitly excludes evaluator-core changes and therefore cannot substitute for this work order.
WO-PLG-009 remains draft and ineligible for live connection until the new evaluator is independently verified, released, and adopted.
This packet introduces no release WO or version reservation.

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
Preparation notes and this packet are not implementation evidence or approval.

## Stop and escalate conditions

Stop for scope expansion, unresolved contract applicability, conflicting ownership, incomplete recovery, unsafe paths, unverified evaluator identity, or a required test failure.
Missing or unproven external provider identity cannot be relabeled as plugin readiness.
Failed native enforcement remains governed by DEC-PLG-006, not by this ownership change.

## Completion report format

Report actual ownership behavior, exact catalog, candidate identity, evidence and failures, retained limitations, lifecycle state, and one evaluator-derived next accountable step.
Do not claim release availability, WO-PLG-009 completion, native discovery, or a public rollout.
