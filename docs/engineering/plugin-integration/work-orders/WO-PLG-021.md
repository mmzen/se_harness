+++
id = "WO-PLG-021"
type = "work_order"
title = "Simplify plugin migration, setup and checks"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[delegation]
class = "execution"

[assurance]
commit_bound_verification = "required"
rationale = "Later plugin use and release decisions depend on changed migration, setup, executable integration, packaging, CI and contracts."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/plugin-integration/requirements/REQ-PLG-032.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-033.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-034.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-035.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-036.md",
  "docs/engineering/plugin-integration/requirements/REQ-PLG-037.md",
  "docs/engineering/plugin-integration/specifications/SPEC-PLG-021.md",
  "docs/engineering/plugin-integration/architecture/ARCH-PLG-004.md",
  "docs/engineering/plugin-integration/architecture/adr/ADR-PLG-004.md",
  "docs/engineering/plugin-integration/verification/VER-PLG-021.md",
  "docs/engineering/plugin-integration/work-orders/WO-PLG-021.md",
  "docs/engineering/plugin-integration/README.md",
  "docs/engineering/plugin-integration/evidence/WO-PLG-021/",
  "docs/engineering/plugin-integration/verification-records/VREC-PLG-016.md",
  "docs/engineering/plugin-integration/evidence/VREC-PLG-016-evaluator.json",
  "se_harness/cli.py",
  "se_harness/installer.py",
  "se_harness/integrity.py",
  "se_harness/preflight.py",
  "se_harness/mutation_guard.py",
  "se_harness/skill_ownership.py",
  "se_harness/skill_ownership_contract.json",
  "se_harness/engine/dashboard_snapshot.py",
  "repository_tools/plugin_distribution.py",
  "scripts/build_plugin_archives.py",
  "pyproject.toml",
  "plugins/verity-plane/",
  "tests/plugin_integration/",
  "tests/test_skill_ownership.py",
  "tests/fixtures/skill_ownership/",
  "tests/test_harnessctl.py",
  "tests/test_mutation_guard.py",
  "tests/test_report_output_safety.py",
  "tests/test_integration_package.py",
  "tests/test_cli_shape.py",
  "tests/test_ci_pipeline.py",
  "tests/test_integrity_primitives.py",
  "tests/test_workflow_documentation_contract.py",
  ".github/workflows/candidate-evidence.yml",
  "templates/repository/standard/docs/engineering/WORKFLOW.md",
  "docs/notes/plugin-simplification-2026-09-13.md",
  "docs/notes/plugin-simplification-work-order-2026-09-13.md",
  "docs/notes/plugin-ownership-migration-2026-09-12.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harnessctl-reference.md",
  "docs/notes/ci-pipeline.md",
]

[relations]
implements = ["REQ-PLG-032", "REQ-PLG-033", "REQ-PLG-034", "REQ-PLG-035", "REQ-PLG-036", "REQ-PLG-037"]
specifications = ["SPEC-PLG-021"]
architecture = ["ARCH-PLG-004", "ADR-PLG-004"]
verification = ["VER-PLG-021"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T06:30:56Z"
decided_by = "engineering-owner"
reason = "The owner accepted the complete plugin simplification proposal on 2026-09-13 and requested its artifact packet and work order through the delegated route: \"i accept this proposal, let's go you can create the artifact packet and work order (delegated route)\". Record the engineering-owner approval of WO-PLG-021 for that accepted scope, including explicit checks instead of blocking hooks and SPEC-PLG-021's applicability table. The retained proposal and 50-scenario coverage map identify the accepted behavior. This approves a definition or the bounded execution delegation only; it records no implementation start, completion, verification result, release, merge, publication or live adoption."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-13T07:26:30Z"
decided_by = "engineering-owner"
reason = "The owner selected the exact minimal package-checkout CI fix with \"ok go\" on 2026-09-13. Start only this owner-directed prerequisite under the recorded scope amendment. The remaining plugin work retains its delegated route; this decision does not complete or verify the work order."
+++

# Work Order: Simplify plugin migration, setup and checks

## Lifecycle

The owner accepted the complete simplification proposal and selected the delegated route on 2026-09-13.
This work order carries execution delegation under DR-015. The approval of this exact work order records that delegation.
It becomes usable only after the approved definition packet is present at the PR base and the live required candidate check succeeds.
The released evaluator determines the permitted start, completion and verification-preparation actions.

## Objective

Deliver the accepted KISS proposal for the owner's single early-stage development installation.
Replace the old skill copies, simplify setup, remove blocking hooks, and cut redundant plugin packaging and CI work.

## In scope

- All 50 scenarios in the retained proposal: 43 accepted removals or simplifications and seven useful protections to keep.
- Disposable migration and restoration, schema-4 compatibility, provider-aware doctor and upgrade, and ordinary path protection.
- Repairable private setup, normal instruction reading, explicit checker use, removal of automatic hooks and frozen host profiles.
- Development copy/archive assembly, safe output reuse, one package-content validation and the smaller acceptance plan.
- Removal of obsolete tests, fixtures and current instructions associated with the removed behavior.
- The new governing chain, its prior-contract applicability table, concise evidence and domain index entry.

## Out of scope

- Changing the root's installed managed files, general lifecycle authority, release rules or the separate governor-transition assessor.
- Installing the plugin into real host settings, migrating the owner's live repositories, changing user-home files or removing unrelated skills.
- Publishing or building promotable releases, changing unrelated CI jobs, and revising historical decisions or verification/release facts.
- Starting, completing or widening any older work order by inference.

## Authorized decision envelope

Choose straightforward internal names, decomposition, fixtures and diagnostics within SPEC-PLG-021.
Use the earlier local migration prototype as input after reviewing its diff against the approved scope.
Remove automatic blocking hooks; this is the selected proposal direction, not an unresolved alternative.
Do not retain the old machinery as an additional mode or add replacement locks, journals, signatures or qualification frameworks.
Preserve the listed seven useful protections and the existing evaluator's authority for actual governed decisions.
The owner explicitly treats contents of the four replaced skill directories as disposable; unrelated customizations remain protected.

## Constraints

The packet starts from main 66a4b8a43409320d01cfe5c67cc9657600ed4681, including verified WO-PLG-020 history.
The installed governor is released 0.17.0; candidate source and development wheels cannot approve their own work.
Read CAP-DST-001, INT-DST-001, this complete packet and the SPEC-PLG-021 compatibility table before execution.
The table is the explicit replacement contract for this delivery, not a request to satisfy contradictory earlier scenarios.
Existing archive identities, version-floor checks and ordinary managed-content safeguards remain outside the stated plugin exceptions.
The implementation branch cannot activate its own delegation. Use the base approval and live check required by DR-015.
No subagent, external service or Git authority is granted by the delegation class itself.

## Expected change surface

The execution_scope lists exact files and the two plugin implementation/test components inspected during preparation.
Within tests/plugin_integration, change only tests and fixtures for the behaviors covered by this packet.
Retained engineering evidence under older work orders is excluded, even when a test used to regenerate it.
The reserved VREC-PLG-016 paths allow later preparation; no record exists or is verified by this packet.
Additional files need a scope amendment before modification.

## Required verification

Meet VER-PLG-021, the normal repository checks, and the released evaluator's phase-appropriate checks.
Use disposable repositories and explicitly non-promotable candidate wheels outside the checkout for acceptance.
Keep the full source suite and existing publication checks, while removing the plugin-only duplicate matrix.

## Evidence to record

Retain one concise log per check, exact candidate identity, CI references and the completed 50-scenario coverage map.
The proposal and earlier prototype results document the starting point; they do not prove completion of this larger work order.

## Stop and escalate conditions

Stop for a required failed check, an unsafe destination, an unresolved material contract conflict or a necessary change outside this scope.
Do not recreate a removed scenario merely to preserve an old test. Apply the replacement criteria in SPEC-PLG-021 and VER-PLG-021.
Do not label unavailable host acceptance, unrun platforms or incomplete implementation as passed.

## Completion report format

State what became simpler, the observed code/test/CI reduction, the checks that passed, and any material limitation.
Use the released evaluator's schema-2 handoff for WO-PLG-021 and report exactly its next action.
Completion is not assurance, release, publication, live adoption or repository integration.

## Owner-directed CI prerequisite — 2026-09-13

After the package job exceeded the released verifier's snapshot limit, the owner selected the proposed minimal checkout with "ok go".
This records the engineering-owner scope amendment and direct start instruction for that bounded prerequisite.
The candidate-package job checks out only scripts/check_portable_release_surface.py and consumes the already-built wheel.
Source and governance jobs retain their full checkouts. Package identity, acceptance, checkout immutability and downstream checks remain enabled.
The workflow and CI test paths are already in execution_scope; SPEC-PLG-021 PLG-KIS-033 and VER-PLG-021 K13 state the added behavior.
This owner-directed prerequisite may start before the packet reaches main. It does not activate branch-local delegation.
The remaining plugin implementation retains the selected delegated route. Completing this prerequisite does not complete the whole work order.
