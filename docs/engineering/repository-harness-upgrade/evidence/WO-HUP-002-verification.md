# WO-HUP-002 local verification ledger

## Outcome

The exact public 0.6.0 standard-root transaction applied successfully. The upgraded root passes its direct integrity, complete-graph, inspection, dashboard, preflight, handoff, distribution, and source-regression checks. The authorized amendment gives `WO-HUP-002` an exact 43-path execution scope, and the authorized expectation corrections pass all 471 source tests on Python 3.11 and 3.14. `WO-HUP-002` remains `in_progress` pending its separately controlled lifecycle transition; no VREC, commit, push, pull request, release, publication, deployment, maintenance, credential, or external-policy action occurred.

artifact: WO-HUP-002
checkpoint: handoff
formal_snapshot_sha256: 5af0730db4b119216a03f4faea3432c06e37e1c881dac7ef7353db33780e4fcd

## Repository and authorization

- Base commit: `7b5a705fbfcd91c79d660d305789dfa1772a0e12`.
- Local branch: `proposal/root-governor-0.6.0`.
- Packet approval recorded at `2026-08-23T17:17:09Z`.
- `WO-HUP-002` start recorded at `2026-08-23T17:21:15Z`.
- Prior raw lock SHA-256: `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- The public 0.6.0 start preflight could not run before installation because it required `QUALITY_GATES.json`, `WORKFLOW.json`, and schema-3 lock entries that the transaction itself installs. Released 0.5.0 has no lifecycle-transition command. The explicitly authorized start was recorded directly; after installation, exact-public 0.6.0 start and review preflights both passed with no diagnostics.

## Applying evaluator identity

- Distribution: `se_harness-0.6.0-py3-none-any.whl`.
- Wheel SHA-256: `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`.
- Installed payload SHA-256: `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42`.
- Runtime identity schema: `se-harness-runtime-identity-v3`.
- Identity result: pass with isolated Python, no `PYTHONPATH`, user site disabled, and module, distribution, templates, interpreter, and entry point under the external environment and outside the checkout.

## Integration adjustment and plan

The public 0.6.0 marker-owned `.gitattributes` fragment contains only the canonical evaluator-evidence LF rule. The three post-release governance-migration LF rules remain unchanged immediately after that marker block as repository-owned policy.

- Pre-adjustment dry run: 18 add/update, 17 unchanged, one `.gitattributes` customization.
- Reviewed post-adjustment dry run: 18 add/update, 18 unchanged, no customization or conflict.
- Apply: success, atomic transaction, only the 18 reviewed add/update paths plus the installer-owned lock.
- Replay: `summary: 36 files, 36 unchanged`.

## Transaction and resulting lock

- Canonical transaction evidence: `WO-HUP-002-evaluator-upgrade.json`.
- Transaction evidence SHA-256: `83398eb76d73a96a0aef2bc40e1d9045a8e14cf5bf74b89afe2ecbf39350c284`.
- Canonical-byte check: LF only; no carriage-return bytes.
- Resulting lock schema: `3`.
- Resulting lock tool version: `0.6.0`.
- Resulting lock SHA-256: `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79`.
- Installed `WORKFLOW.json` SHA-256: `e92adf4d81cf7147a76b20dd4c86ea90ca756b345caae50d29e4a80aec37f7b4`.
- Installed `QUALITY_GATES.json` SHA-256: `95b95015988380c3446007bca2571566c6bde11b2cccd25cb048437711ca77a0`.
- Integrated `.gitattributes` SHA-256: `926801cb3d9647f97c4474154907d838f5759cf37b73238e17b824d51e9c2e45`.

## Passing checks

- Exact-public 0.6.0 `identity`: pass.
- Exact-public 0.6.0 `doctor`: pass; every distribution and managed-integrity check passed.
- Exact-public and checkout-source complete `validate`: pass, 697 artifacts, zero errors, 50 pre-existing maintenance warnings.
- Exact-public `inspect`: pass, 697 artifacts and 2,523 relations.
- Exact-public dashboard: pass, zero errors; output manifest `215b9dd05c0412390020252333a389735eeb097d6519a1624baabc644e493f0c`.
- Exact-public start and review preflight for `WO-HUP-002`: ready with no diagnostics.
- Managed workflow selects exact `se-harness==0.6.0`, proves isolated origin, and uses isolated `python -I -m se_harness` for preflight, doctor, validate, and dashboard.
- `WORKFLOW.json` and `QUALITY_GATES.json` parse as JSON.
- Release-distribution validation: pass, one distribution-bearing record.
- `git diff --check`: pass; Git emitted only local checkout line-ending notices.
- Protected-surface comparison: no changes under `se_harness/`, `templates/`, `pyproject.toml`, `docs/engineering/release-0-6-0/`, or the publication and Pages workflows.

The 50 validator warnings are the retained maintenance findings already present in the repository: legacy architecture assessment/relation migrations and historical noncanonical VREC/RLS placement. They are not structure, governance, or policy errors and were not changed under this work order.

## Workflow handoff

The first exact-public 0.6.0 handoff observation correctly returned `not_assessable`: the work order did not yet have a machine-assessable execution scope, a complete changed-path manifest had not been supplied, and no evidence was bound to the then-current formal snapshot. The authorized amendment added an exact `[execution_scope]` containing all 43 changed paths.

The final exact-public 0.6.0 `check --artifact WO-HUP-002 --checkpoint handoff` replay supplied all 43 normalized changed paths and asserted that the list was complete. Status, graph validity, repository integrity, execution scope, change completeness, path containment, review preflight, and the snapshot-bound evidence above all passed.

## Corrective source-regression replay

The first full source replay completed 471 tests on both supported local runtimes with the same 12 failures, zero errors, and 7 skips:

1. `test_artifact_catalog.ArtifactCatalogTests.test_released_policy_copies_match_while_candidate_router_remains_isolated`
2. `test_artifact_catalog.ArtifactCatalogTests.test_router_and_human_notes_point_to_the_authoritative_catalog`
3. `test_context_routing_retirement.ContextRoutingRetirementTests.test_only_recorded_files_name_the_retired_path`
4. `test_dashboard_webui.DashboardWebUIContractTests.test_candidate_topology_target_is_independent_from_the_managed_root`
5. `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_identifies_every_managed_path_from_the_lock`
6. `test_predecessor_assessment_contract.PredecessorAssessmentContractTests.test_existing_managed_workflow_remains_byte_identical_to_head`
7. `test_revision_provenance.RevisionValidatorTests.test_dashboard_projects_declared_commit_and_checkout_state`
8. `test_revision_provenance.RevisionValidatorTests.test_valid_aggregate_records_cover_all_work_at_one_commit`
9. `test_revision_provenance.RevisionValidatorTests.test_valid_sha1_and_sha256_records`
10. `test_standard_repository_lifecycle.StandardRepositoryLifecycleTests.test_candidate_source_identity_is_deterministic_and_bounded`
11. `test_standard_repository_lifecycle.StandardRepositoryLifecycleTests.test_evaluator_evidence_bytes_are_portable_across_git_checkouts`
12. `test_validation_taxonomy.ValidationTaxonomyTests.test_policy_and_operator_reference_define_the_same_small_vocabulary`

These assertions encoded the previous root state or assumed that checkout-source candidate templates must always differ from root-managed copies. Exact public 0.6.0 adoption intentionally changes the root copies and managed workflow; convergence is also valid when the released root and candidate templates have identical canonical bytes. Under the authorized correction, the eight affected test files now check the current managed lock, convergence-aware isolation, canonical evaluator evidence, candidate-local provenance, and the 0.6.0 owner instructions.

- Python 3.11.9: 471 tests passed; 7 skipped; zero failures or errors.
- Python 3.14.6: 471 tests passed; 7 skipped; zero failures or errors.
- The focused replay of all previously failing tests also passed.

## Preserved boundaries

No candidate product or template bytes, package version, RLS/VREC/REL record, tag-related release content, publication workflow, deployment workflow, maintenance state, Git ref, external policy, or credential state was changed. All repository changes remain local and uncommitted.
