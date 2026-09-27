# Progressive instruction discovery — implementation review

This is an unfinished candidate under WO-IAR-013 through WO-IAR-016. It is not
a released or installed harness. The repository's AGENTS.md, root instructions
and selected 0.18.0 lock remain unchanged. The separately reviewed source draft
in outputs/ENGINEERING_HARNESS.md is preserved.

## Delivered candidate changes

- A 1,191-word entry and 25 conditional guides. All 58 reviewed headings and
  31 main steps have a recorded disposition; links and command preservation
  checks pass. Open the [candidate entry](../../../../../templates/repository/standard/ENGINEERING_HARNESS.md.tpl).
- One additive discovery catalogue covers all 18 procedures and 23 typed steps.
  It describes evaluator-selected actions and separates instructions, formal
  records and evaluator-only inputs. Existing lifecycle contracts are unchanged.
- Fresh installation no longer generates or requires AGENTS.md or CLAUDE.md.
  New instruction guides are managed. Six old guides become compatibility
  pointers. Recognized 0.18.0 fragments preserve all owner bytes; customized,
  ambiguous or unsupported migration inputs are refused.
- Retirement requires reviewed native startup and compaction evidence bound to
  the repository, prior lock and planned root. Without it, apply preserves the
  old installation. Receipt consistency checks are not independent host proof.
- Native hook assets, thin skill routes and bounded archive validation are
  implemented. Malformed or incomplete hook packages leave existing output intact.

## Actual work-order states

| Work order | Scope | State |
| --- | --- | --- |
| [WO-IAR-013](../../work-orders/WO-IAR-013.md) | Instruction split and coverage | `in_progress` |
| [WO-IAR-014](../../work-orders/WO-IAR-014.md) | Evaluator discovery and migration | `in_progress` |
| [WO-IAR-015](../../work-orders/WO-IAR-015.md) | Host delivery and skills | `in_progress` |
| [WO-IAR-016](../../work-orders/WO-IAR-016.md) | Packaging correction | `in_progress` |
| [WO-IAR-017](../../work-orders/WO-IAR-017.md) | Proposed regression scope correction | `draft` |

No completion, verification acceptance, release or external delivery was applied.
The installed evaluator's current next command for each in-progress order is
`harnessctl check . --artifact WO-ID --checkpoint handoff`. A successful review
preflight is not a handoff pass or permission to skip remaining checks.

## Verification and limits

| Check | Observed result |
| --- | --- |
| Packaging assembly boundaries | 17 tests passed. |
| Real-wheel setup, reuse and repair | Passed. |
| Migration/discovery/route regression selection | 84 tests passed before the additional retirement-evidence guard. |
| Retirement guard and related instruction checks | 53 tests passed. |
| Final CLI, installer, discovery and source coverage selection | 50 tests passed. |
| Hook protocol and development packages | 18 tests ran: 16 passed and 2 skipped; the real-wheel skip was exercised separately. Windows test symlink creation was unavailable. |
| Isolated candidate wheel | Clean init and doctor passed. Missing native delivery evidence refused upgrade without changing any prior file. |
| Synthetic positive migration | Owner-byte, customized-input, rollback and retry tests passed. These fixtures are not native qualification. |
| Claude Code 2.1.273 / Windows | Native startup accepted the complete 8,904-character context. Current root hash and helper hash are retained. No conversation was started. |
| Claude post-compaction / Codex native delivery | Unverified. No automatic-support claim is made. |
| Linux migration | Unverified in this Windows environment. |
| Released 0.18.0 checks | Doctor, graph validation and review preflight for WO-IAR-013–016 passed. 50 unrelated findings remained separate in selected context results. |
| Repository checks | Distribution validation and CLI help passed; ordinary Git diff whitespace check passed. |

Latest full run: **Ran 1118 tests in 146.307s (175 classes, 6 workers)  FAILED (failures=21, errors=11, skipped=16)**

The suite is not passing. The remaining failures require review against the
accepted behavior, especially old instruction paths, fragment assumptions and
skill identity fixtures. Tests outside the approved scopes remain untouched.
Do not read a successful focused check as acceptance of the full evolution.

The current non-promotable wheel is at `C:\Users\mathi\AppData\Local\Temp\iar-nonpromotable-uvunsb9f\wheel\se_harness-0.19.0-py3-none-any.whl`.
Its SHA-256 is `f8ff055798b4fc4d6b0ab00b62f6bfacb152631b185d91a53b325a84f6478222`.
Its exact uncommitted source input hashes are retained with its build logs.
Earlier isolated migration logs predate the new evidence guard; the guarded
run is the current acceptance observation.

## Next accountable decision

Review and approve [WO-IAR-017](../../work-orders/WO-IAR-017.md) if the proposed test-only
correction is accepted. Its approval preview passed, but no approval or start
was applied. The current orders enumerate their allowed paths; affected
regressions elsewhere under tests/ need this separate scope. The proposal
preserves lifecycle, authority, gate, provenance and owner-byte assertions.

After that correction, finish native host/platform qualification, rerun the
required complete checks and obtain handoff results before completion and
commit-bound verification. Human verification acceptance remains separate.

## Reading cost

The six measured paths require 2,406–5,049 unique instruction words, including
the communication policy, versus 21,888 words in the reviewed source. Formal
artifact reading is additional and varies with the selected scope. These are
word counts, not measured model-token or latency guarantees. See
[the reading-cost method and scenarios](../../acceptance/progressive-discovery/reading-cost.md).

## Remaining full-suite findings

- `test_standard_repository_lifecycle.StandardRepositoryLifecycleTests.test_standard_upgrade_detects_a_customized_technical_communication_policy`
- `test_harnessctl.HarnessCtlTests.test_adopt_preserves_existing_content_and_labels_observations`
- `test_harnessctl.HarnessCtlTests.test_init_installs_complete_valid_harness_and_dashboard`
- `test_harnessctl.HarnessCtlTests.test_invalid_project_name_and_malformed_markers_fail_closed`
- `test_harnessctl.HarnessCtlTests.test_upgrade_keeps_customized_guidance_and_replaces_only_selected_files`
- `test_architecture_traceability.ArchitectureTraceabilityTests.test_managed_authoring_guidance_uses_typed_relations (path='docs/engineering/TRACEABILITY.md')`
- `test_architecture_traceability.ArchitectureTraceabilityTests.test_managed_authoring_guidance_uses_typed_relations (path='docs/engineering/QUALITY_GATES.md')`
- `test_workflow_execution.AgentDirectiveSurfaceTests.test_operating_card_template_equals_its_contract_rendering_and_stays_bounded`
- `test_agentic_execution.SkillContractTests.test_canonical_harness_orient_contract_and_manifest_validate`
- `test_agentic_execution.SkillContractTests.test_retained_phase3_vectors_are_preserved_and_orientation_is_byte_exact`
- `test_adr_applicability.AdrApplicabilityTests.test_managed_authoring_guidance_is_distributed (path='docs/engineering/WORKFLOW.md')`
- `test_adr_applicability.AdrApplicabilityTests.test_managed_authoring_guidance_is_distributed (path='docs/engineering/DECISION_RIGHTS.md')`
- `test_adr_applicability.AdrApplicabilityTests.test_managed_authoring_guidance_is_distributed (path='docs/engineering/QUALITY_GATES.md')`
- `test_adr_applicability.AdrApplicabilityTests.test_managed_authoring_guidance_is_distributed (path='docs/engineering/TRACEABILITY.md')`
- `test_decision_management.DecisionGateFamilyTests.test_contract_copies_carry_the_family_the_predicates_and_the_policy_rows`
- `test_risk_management.RiskArtifactTests.test_layout_registry_templates_and_policy_route_the_risk_type`
- `test_risk_management.RiskArtifactTests.test_the_workflow_contract_declares_the_family_with_exactly_the_state_model`
- `test_validation_taxonomy.ValidationTaxonomyTests.test_policy_and_operator_reference_document_the_machine_vocabulary`
- `test_artifact_authoring_policy.ArtifactAuthoringPolicyTests.test_installed_policy_is_routed_and_supplies_the_creation_checklist`
- `test_risk_management.BorrowedStopTests.test_no_predicate_or_gate_group_is_added_and_the_risk_edges_bind_none`
- `test_workflow_execution.CheckProjectionTests.test_nothing_names_focus_but_the_note_that_records_its_removal`
- `test_harnessctl.HarnessCtlTests.test_doctor_detects_missing_claude_import_and_ignores_the_retired_path`
- `test_harnessctl.HarnessCtlTests.test_doctor_hashes_only_the_managed_fragment`
- `test_harnessctl.HarnessCtlTests.test_lock_contains_hashes_without_generated_adoption_report`
- `test_harnessctl.HarnessCtlTests.test_upgrade_adds_cross_agent_files_without_reviving_the_retired_scaffold`
- `test_harnessctl.HarnessCtlTests.test_upgrade_preserves_claude_customization_and_owner_content_at_the_retired_path`
- `test_revision_provenance.RevisionCliTests.test_refresh_refuses_changed_code_governing_input_or_evidence (path='AGENTS.md')`
- `test_retired_surface.RetiredSurfaceTests.test_retired_phrases_are_absent_from_their_files`
- `test_artifact_catalog.ArtifactCatalogTests.test_released_policy_copies_match_with_declared_candidate_exceptions`
- `test_managed_template_texts.RetiredRelationRuleTests.test_the_rule_keeps_its_installation_sentence_and_its_neighbours`
- `test_managed_template_texts.RetiredRelationRuleTests.test_the_rule_names_the_relation_retired_and_refused`
- `test_managed_template_texts.RetiredRelationRuleTests.test_the_rule_names_the_typed_pair_and_promises_no_migration`
