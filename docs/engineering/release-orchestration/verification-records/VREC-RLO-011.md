+++
id = "VREC-RLO-011"
type = "verification_record"
title = "Verification candidate for WO-RLO-011"
status = "verified"
owners = ["Codex"]
created = "2026-09-28"
updated = "2026-09-28"
commit = "755bd0c761f2466df491d99823e279696d7796ba"
git_object_format = "sha1"
worktree_state = "clean"
prepared_at = "2026-09-28T19:54:31Z"
prepared_by = "Codex"
artifact_snapshot_sha256 = "a2a3c2115d65f66de71ce68f1c080467a6740ee83afc0beae249adeb35b2078b"
evidence_paths = ["docs/engineering/release-orchestration/evidence/WO-RLO-011-assessment.json", "docs/engineering/release-orchestration/evidence/WO-RLO-011/checks.zip"]
evaluator_evidence_path = "docs/engineering/release-orchestration/evidence/VREC-RLO-011-evaluator.json"
evaluator_evidence_sha256 = "e47384120e30c37f16266e887354cc5e0f5cb956e4d93c53fc7a5bd43ffec9c2"

verified_at = "2026-09-28T20:06:28Z"
verified_by = "assurance-owner"
[relations]
verifies_work_order = ["WO-RLO-011"]
conforms_to = ["VER-RLO-008"]

[[lifecycle_events]]
from = "ready"
to = "verified"
decided_at = "2026-09-28T20:06:28Z"
decided_by = "assurance-owner"
reason = "Human repository owner mmzen: \"I verify VREC-RLO-011\". Codex applies this human assurance decision to candidate 755bd0c761f2466df491d99823e279696d7796ba for WO-RLO-011 under VER-RLO-008 with the reviewed retained evidence and documented limits: 82 tests passed and one native symlink test was skipped because Windows denied symlink creation. Supplied delivery observations are checked locally; no live public delivery is established by this decision. The selected 0.19.0 evaluator encodes the assurance right as assurance-owner; mmzen is the decision-maker. Only VREC-RLO-011 changes state. This decision does not authorize push, merge, release or publication."
+++

# Verification Record Candidate

This ready record binds retained evidence for `WO-RLO-011` to candidate commit `755bd0c761f2466df491d99823e279696d7796ba`. Preparation uses each selected work order's recorded execution approval. An accountable assurance owner must review the evidence and transition the record to `verified`; this command did not approve, commit, tag, release, or publish anything.

The record is intentionally created after the candidate commit it names, avoiding self-referential commit metadata.

## Candidate test run

Commit: `755bd0c761f2466df491d99823e279696d7796ba`. Exit status: 0.

Command arguments: `["C:\\Users\\mathi\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe", "-m", "unittest", "tests.test_release_delivery", "tests.test_release_orchestration", "tests.test_dashboard_publication", "-v"]`.

```text
ed_public_install_role (tests.test_release_orchestration.ReleaseWorkflowPolicyTests.test_public_observation_uses_the_typed_public_install_role) ... ok
test_repository_policy_is_explicit_and_imported_only_from_trusted_main (tests.test_release_orchestration.ReleaseWorkflowPolicyTests.test_repository_policy_is_explicit_and_imported_only_from_trusted_main) ... ok
test_the_publication_path_has_no_predecessor_view_adapter (tests.test_release_orchestration.ReleaseWorkflowPolicyTests.test_the_publication_path_has_no_predecessor_view_adapter) ... ok
test_exact_standard_evaluator_is_accepted (tests.test_dashboard_publication.EvaluatorDescriptorTests.test_exact_standard_evaluator_is_accepted) ... ok
test_legacy_or_incomplete_lock_is_rejected (tests.test_dashboard_publication.EvaluatorDescriptorTests.test_legacy_or_incomplete_lock_is_rejected) ... ok
test_mismatch_unknown_field_and_retired_descriptor_are_rejected (tests.test_dashboard_publication.EvaluatorDescriptorTests.test_mismatch_unknown_field_and_retired_descriptor_are_rejected) ... ok
test_plugin_owned_evaluator_preserves_schema3_identity (tests.test_dashboard_publication.EvaluatorDescriptorTests.test_plugin_owned_evaluator_preserves_schema3_identity) ... ok
test_plugin_owned_evaluator_rejects_invalid_inputs (tests.test_dashboard_publication.EvaluatorDescriptorTests.test_plugin_owned_evaluator_rejects_invalid_inputs) ... ok
test_duplicate_released_records_for_one_tag_fail_closed (tests.test_dashboard_publication.GitReleaseFixture.test_duplicate_released_records_for_one_tag_fail_closed) ... ok
test_evaluator_evidence_must_match_locked_identity (tests.test_dashboard_publication.GitReleaseFixture.test_evaluator_evidence_must_match_locked_identity) ... ok
test_exact_manual_replay_is_accepted_and_later_commit_is_rejected (tests.test_dashboard_publication.GitReleaseFixture.test_exact_manual_replay_is_accepted_and_later_commit_is_rejected) ... ok
test_later_evaluator_upgrade_does_not_rewrite_release_history (tests.test_dashboard_publication.GitReleaseFixture.test_later_evaluator_upgrade_does_not_rewrite_release_history) ... ok
test_later_record_relocation_does_not_change_the_integration_commit (tests.test_dashboard_publication.GitReleaseFixture.test_later_record_relocation_does_not_change_the_integration_commit) ... ok
test_malformed_inputs_and_non_main_ref_are_rejected (tests.test_dashboard_publication.GitReleaseFixture.test_malformed_inputs_and_non_main_ref_are_rejected) ... ok
test_modified_evaluator_evidence_fails_publication_replay (tests.test_dashboard_publication.GitReleaseFixture.test_modified_evaluator_evidence_fails_publication_replay) ... ok
test_new_evidence_accepts_whitespace_and_no_unused_archive_or_console (tests.test_dashboard_publication.GitReleaseFixture.test_new_evidence_accepts_whitespace_and_no_unused_archive_or_console) ... ok
test_partial_evaluator_binding_fails_publication_replay (tests.test_dashboard_publication.GitReleaseFixture.test_partial_evaluator_binding_fails_publication_replay) ... ok
test_plugin_lock_binding_preserves_identity_and_evidence_checks (tests.test_dashboard_publication.GitReleaseFixture.test_plugin_lock_binding_preserves_identity_and_evidence_checks) ... ok
test_resolver_selects_integration_commit_not_tag_or_later_head (tests.test_dashboard_publication.GitReleaseFixture.test_resolver_selects_integration_commit_not_tag_or_later_head) ... ok
test_tag_candidate_mismatch_fails_closed (tests.test_dashboard_publication.GitReleaseFixture.test_tag_candidate_mismatch_fails_closed) ... ok
test_actions_are_immutable_reviewed_pins (tests.test_dashboard_publication.PagesWorkflowPolicyTests.test_actions_are_immutable_reviewed_pins) ... ok
test_permissions_environment_and_concurrency_are_bounded (tests.test_dashboard_publication.PagesWorkflowPolicyTests.test_permissions_environment_and_concurrency_are_bounded) ... ok
test_snapshot_digest_reads_an_emitted_output (tests.test_dashboard_publication.PagesWorkflowPolicyTests.test_snapshot_digest_reads_an_emitted_output) ... ok
test_standalone_workflow_is_a_caller_of_the_one_pages_definition (tests.test_dashboard_publication.PagesWorkflowPolicyTests.test_standalone_workflow_is_a_caller_of_the_one_pages_definition) ... ok
test_workflow_has_only_main_controlled_replay_trigger (tests.test_dashboard_publication.PagesWorkflowPolicyTests.test_workflow_has_only_main_controlled_replay_trigger) ... ok
test_workflow_preserves_evaluator_generator_and_payload_boundaries (tests.test_dashboard_publication.PagesWorkflowPolicyTests.test_workflow_preserves_evaluator_generator_and_payload_boundaries) ... ok
test_github_release_metadata_must_be_final_and_exact (tests.test_dashboard_publication.PayloadPackagingTests.test_github_release_metadata_must_be_final_and_exact) ... ok
test_manifest_declared_raw_evidence_is_hash_verified_and_published (tests.test_dashboard_publication.PayloadPackagingTests.test_manifest_declared_raw_evidence_is_hash_verified_and_published) ... ok
test_notice_boundary_is_bound_to_both_real_templates (tests.test_dashboard_publication.PayloadPackagingTests.test_notice_boundary_is_bound_to_both_real_templates) ... ok
test_notice_is_inserted_after_either_accepted_boundary_only (tests.test_dashboard_publication.PayloadPackagingTests.test_notice_is_inserted_after_either_accepted_boundary_only) ... ok
test_packaging_adds_constant_notice_and_exact_manifest (tests.test_dashboard_publication.PayloadPackagingTests.test_packaging_adds_constant_notice_and_exact_manifest) ... ok
test_packaging_is_repeatable_for_identical_source_and_provenance (tests.test_dashboard_publication.PayloadPackagingTests.test_packaging_is_repeatable_for_identical_source_and_provenance) ... ok
test_unexpected_file_and_revision_mismatch_fail_closed (tests.test_dashboard_publication.PayloadPackagingTests.test_unexpected_file_and_revision_mismatch_fail_closed) ... ok

----------------------------------------------------------------------
Ran 83 tests in 55.099s

OK (skipped=1)

```
