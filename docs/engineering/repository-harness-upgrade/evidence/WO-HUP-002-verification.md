# WO-HUP-002 implementation verification evidence

Date: 2026-08-23

## Result

The exact authorized standard-root-only transaction applied atomically and all
released-governor integrity, graph, scope, owner-preservation, replay,
inspection, dashboard, release-distribution, parsing, CLI, and complete-suite
checks now pass. The initial post-transaction suite stop is retained below as
diagnostic history; the separately approved HUP-003 compatibility work resolved
its predecessor-only assertions without changing the immutable transaction,
product runtime, or canonical templates.

The failures are boundary assertions that require the installed released root
to remain different from the packaged 0.6.0 candidate policies or from `HEAD`,
or that require owner content and test fixtures to describe the predecessor
root. The authorized transaction intentionally makes the installed root equal
to released 0.6.0, must preserve owner bytes, and must remain uncommitted. No
test, product, owner-region, scope, or history change is authorized by
`WO-HUP-002`, so no attempt was made to weaken or update those assertions.

The final evidence-aware complete suite reports 452 tests, seven skips, zero
failures, and zero errors. After `WO-HUP-003` reached `implemented`, the
engineering owner transitioned `WO-HUP-002` to `implemented`. No candidate
commit, VREC, push, pull request, merge, tag, release, publication, deployment,
credential use, issue mutation, or history rewrite was performed.

## Authority and immutable baseline

- Baseline commit: `cccbaa70a6c5a33e19decec0d78f26afd87d5f9e`.
- Baseline installed governor: released 0.5.0 with schema-2 lock SHA-256
  `c4c4191998cad431620324dba2ad205c190fcf2802847278cabec92e853989af`.
- The repository owner approved the complete HUP-002 chain, the accepted
  `no_significant_decision` assessment, `WO-HUP-002`, the exact 18-change
  managed plan, and the bound standard-root-only 0.6.0 transaction.
- At `2026-08-23T07:36:50Z`, the repository owner, release owner, security
  owner, and engineering owner declared the normal 0.5.0 full-root preflight
  deadlocked solely by the documented `RLS-SEH-009` / `RLS-SEH-012`
  predecessor semantics and authorized the bounded recovery rehearsal and
  immutable transaction for this implementation only.
- The exact 0.5.0 preflight boundary comprised one `A-E009` for rejected
  `RLS-SEH-009` and two `A-E010` duplicate-0.6.0 findings for `RLS-SEH-009`
  and `RLS-SEH-012`; no additional diagnostic was accepted.

## Released evaluator and recovery controls

The independently installed public evaluator passed runtime identity under
isolated Python 3.14.6. Its interpreter, distribution, module, templates, and
entry point all resolved below the external evaluator environment and outside
the checkout; user site was disabled and `PYTHONPATH` was absent.

| Identity item | Exact value |
| --- | --- |
| Version | `0.6.0` |
| Archive | `se_harness-0.6.0-py3-none-any.whl` |
| Archive / wheel SHA-256 | `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7` |
| Installed payload manifest | `se-harness-installed-payload-v1` |
| Installed payload SHA-256 | `c233678548fe742b7a7a5a8bd65de10156ff233edc65b68e2ed0333fbe4dea42` |
| Identity result | PASS, no diagnostics |

The mandatory no-network recovery rehearsal passed in a disposable external
directory. It rejected candidate contamination and stale or mismatched
identity, stopped conflicting predecessor chains for accountable disposition,
restored the exact pre-write snapshot after an injected interrupted
transaction, restored normal evaluator/candidate/publisher controls, proved
absence invariants, and recorded credential, network, publication, release,
tag, deployment, and external-action flags as false.

## Plan, apply, and replay

- Released 0.6.0 validated the complete pre-apply graph at 681 artifacts, zero
  errors, and 50 inherited maintenance warnings.
- The immediate dry run exactly matched the approved plan: 36 managed paths,
  18 additions or updates, and 18 unchanged paths.
- The supported `upgrade --apply` transaction reported the same 18 changes and
  atomically upgraded the installed root to 0.6.0.
- Canonical transaction evidence is
  `docs/engineering/repository-harness-upgrade/evidence/WO-HUP-002-evaluator-upgrade.json`.
- A repeated dry run reported 36 unchanged paths and did not rewrite keyed
  evidence.

## Post-transaction identities and preservation

| Item | Result |
| --- | --- |
| Schema-3 lock SHA-256 | `abcb1fe70b0eab96b106378bc1549b11e65cf5fe23d9c4cafccfdd28a3bf3f79` |
| Transaction evidence SHA-256 | `83398eb76d73a96a0aef2bc40e1d9045a8e14cf5bf74b89afe2ecbf39350c284` |
| `REPOSITORY_CONTEXT.md` pre/post SHA-256 | `4cf02b35174e95b25b785ae6b93175b86197e473173e9fb12eab92268b468d94` / same |
| `REPOSITORY_CONTEXT.md` lock state | absent, with no tombstone |
| `AGENTS.md` owner-region SHA-256 | `86e739505f0dc27f7c3ab8aa470f563172433826e6a3a0924f1d2947ea30b745` before and after |
| `CLAUDE.md` owner-region SHA-256 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` before and after |
| Lock evaluator | exact 0.6.0 archive and payload identity above |
| Lock managed integrity | PASS |

The final changed-surface audit found exactly 31 paths: the 19 authorized
transaction paths including the lock, plus the 12 authorized HUP-002 packet
and evidence paths. Missing paths: none. Unexpected paths:
none. No path under `se_harness/`, `templates/repository/standard/`, package
metadata, repository release tooling, release records, publisher or Pages
surfaces, or an unrelated engineering domain changed.

## Successful local checks

| Check | Result |
| --- | --- |
| Released 0.6.0 `doctor` | PASS; exact distribution, lock, managed content, and schema-3 integrity; 21 inherited W013 placement advisories |
| Released 0.6.0 complete validation | PASS: 681 artifacts, zero errors; structure E0/W0, governance E0/W0, policy E0/W0, maintenance E0/W50 |
| Released 0.6.0 start preflight | PASS for `WO-HUP-002` at `in_progress`; complete 16-file reading manifest; no diagnostics |
| Released 0.6.0 review preflight | PASS for `WO-HUP-002` at `in_progress`; complete 17-file reading manifest; no diagnostics; this machine result does not override the red required suite |
| Released 0.6.0 inspection | PASS observation: 681 artifacts, 2,483 relations, 135 findings (60 warning, 75 info), no pending definitions or decisions, one active work order |
| Released 0.6.0 dashboard | PASS: 681 artifacts, 2,483 relations, zero errors, 60 warnings; manifest `8c5d429eed0e247098cc1627e97234c0329faba99340107c86321e69e3e706e1` |
| Release-distribution validation | PASS: one distribution-bearing record |
| Managed JSON parsing | PASS for lock, transaction evidence, `WORKFLOW.json`, and `QUALITY_GATES.json` |
| Managed workflow YAML parsing | PASS; one `validate` job |
| CLI help | PASS; released 0.6.0 command surface loaded |
| Candidate-source identity | PASS as a separately labelled non-governing 0.6.0 source role rooted inside the checkout |
| Released-evaluator/candidate-source separation | PASS; origins are disjoint and no checkout source entered the governor runtime |
| `git diff --check` | PASS; host emitted only line-ending conversion notices |
| Exact changed-surface audit | PASS: no missing or unexpected path |

Hosted checks and a candidate-package build remain pending because they require
a separately authorized candidate commit, build, or push. The already released
0.6.0 wheel remains independently identified and verified as the governor; it
was not relabelled as a new candidate package.

## Required complete-suite stop

The first diagnostic run inherited a process-level Git configuration override
and reported 452 tests, 12 failures, one error, and seven skips. Its sole error
was environment rejection by the predecessor-publication test, so that run is
not the authoritative suite result.

The clean rerun removed the override and reported 452 tests, 10 failures, zero
errors, and seven skips. The exact failing tests were:

1. `test_artifact_catalog.ArtifactCatalogTests.test_released_policy_copies_match_while_candidate_router_remains_isolated`
2. `test_artifact_catalog.ArtifactCatalogTests.test_router_and_human_notes_point_to_the_authoritative_catalog`
3. `test_context_routing_retirement.ContextRoutingRetirementTests.test_only_recorded_files_name_the_retired_path`
4. `test_dashboard_webui.DashboardWebUIContractTests.test_candidate_topology_target_is_independent_from_the_managed_root`
5. `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_identifies_every_managed_path_from_the_lock`
6. `test_predecessor_assessment_contract.PredecessorAssessmentContractTests.test_existing_managed_workflow_remains_byte_identical_to_head`
7. `test_revision_provenance.RevisionValidatorTests.test_dashboard_projects_declared_commit_and_checkout_state`
8. `test_revision_provenance.RevisionValidatorTests.test_valid_aggregate_records_cover_all_work_at_one_commit`
9. `test_revision_provenance.RevisionValidatorTests.test_valid_sha1_and_sha256_records`
10. `test_validation_taxonomy.ValidationTaxonomyTests.test_policy_and_operator_reference_define_the_same_small_vocabulary`

Tests 1, 2, 4, 7, 8, 9, and 10 exercise the deliberate released-root versus
candidate-policy separation and now observe exact 0.6.0 convergence. Test 3
finds the newly authorized HUP-002 records that necessarily name the preserved
retired path. Test 5 expects owner-controlled instructions to name every
managed path while this transaction is required to preserve those owner bytes
as new JSON contracts enter the lock. Test 6 requires the managed workflow to
remain byte-identical to `HEAD`, while this uncommitted transaction is expressly
authorized to update it.

The released 0.6.0 record retains exact-candidate qualification (445 tests on
Windows Python 3.11.9 and 3.14.6 and Ubuntu Python 3.12.3), but that historical
assurance cannot convert this work order's explicit red complete-suite check
into a pass. Correcting or reclassifying these assertions would require an
amended work order and explicit authority for owner and/or product-test changes.

## Accountable compatibility resolution

The repository owner subsequently approved `REQ-HUP-007`, `SPEC-HUP-003`,
`VER-HUP-003`, `WO-HUP-003`, and an exact eight-path compatibility plan. That
separate work order updated only the `AGENTS.md` owner region and seven test
modules. It changed no managed root, lock, transaction evidence, `se_harness/`
runtime, canonical template, release surface, or external state.

The ten formerly failing tests then passed, all seven affected modules passed
at 110 tests with two skips, and two complete-suite runs passed at 452 tests
with seven skips. The final combined HUP-002/HUP-003 audit found exactly 43
authorized paths and no missing, unexpected, product-runtime, template,
repository-tool, release, publisher, or Pages path.

## Completion state and residual risk

The supported apply completed atomically, no rollback was necessary, and the
separately governed compatibility work resolves the only required-check stop.
Released 0.6.0 doctor, graph validation, review preflight, inspection,
dashboard, distribution validation, 36-path no-op replay, evidence scan, diff
check, and complete suite all pass. The worktree remains uncommitted and hosted
candidate checks remain unavailable until separately authorized commit and
push work; neither condition blocks the local `implemented` transition.
