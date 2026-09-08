```toml
artifact = "WO-ECP-036"
checkpoint = "handoff"
formal_snapshot_sha256 = "8a734d806bd730a04f81d0a41a4e3f7511b9680da4274d2d7316ebd6239c3234"
rebound_at = "2026-09-08T19:31:16Z"
```

# WO-ECP-036 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The three largest modules are split along their seams and the workflow
cycle is gone, with no behaviour change. The validator's eight passes live
in `se_harness/engine/validation_*.py` and its entry module keeps
`validate_repository`, `build_parser` and `main`; the generator's snapshot
and bundle builders live in `dashboard_snapshot.py` and `dashboard_bundle.py`
and its entry module keeps `generate_bundle`, `generate_snapshot` and `main`;
`workflow_compliance.py` keeps the evaluator and the packet writer, with its
change set, its evidence-packet primitives and its predicates in three seams.
The workflow's graph names have one public home in `repository_graph.py`
(`validated_repository`, `artifact_catalog`, `project_scope`,
`classify_diagnostics`, `diagnostic_payload`), its edge names in
`workflow_edges.py`, and `lifecycle_family` is the contract module's; the
compliance module imports no workflow, so the workflow binds its compliance
names at import time and its sixteen lazy imports go. No module imports a
private name across the package, no function reads above complexity 60,
and every recorded output is byte-identical to the group B code on this
repository at the same revision.

## Evaluators

- Governor: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel `a969d6ab…`, the digest
  `RLS-SEH-025` binds), `-I`, for every reading, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/ecp-036-seams`, stacked on the
  group B branch at `5c966cd1`; the code commits are `ed25cae0` (the
  validator), `79f004b5` (the generator), `68478f42` (the workflow graph
  and edges, the compliance seams) and `074fbd7b` (the extractions, the
  inventory test, the private authoring helpers made public).
- Byte identity: the group B head (`5c966cd1`, a worktree) and the
  candidate, each run on the same target checkout at the same revision,
  after each of the four steps and at the candidate head.
- Duplication scan and complexity: `pylint 4.0.8` and `radon 6.0.1` in a
  scratch environment outside the checkout; the complexity test repeats the
  reading wherever radon is installed.
- The splits: a moving tool that slices top-level definitions by name with
  their attached comments, generates each seam's imports and leaves the
  entry module re-exporting every public name; the extractions are
  pure "extract function" moves of whole blocks, each verified by the same
  byte-identity readings.

## Rule-to-case map

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `ECP-ENG-016` | every recorded output equal between the group B code and the candidate on the same target and revision | the byte-identity readings |
| `ECP-ENG-017` | `validation_core`, `validation_report`, `validation_lifecycle`, `validation_authoring`, `validation_evidence`, `validation_revision`, `validation_architecture`, `validation_decisions`, `validation_layout`; the entry module defines `validate_repository`, `build_parser`, `main` | `tests/test_module_seams.py` (`test_the_validator_is_split_along_its_eight_seams`); `tests/test_validation_taxonomy.py` reads every engine module |
| `ECP-ENG-018` | `dashboard_snapshot.build_snapshot`, `dashboard_bundle.build_dashboard_bundle`; the entry keeps `generate_bundle`, `generate_snapshot` and `main` | `test_the_generator_is_split_at_its_two_seams`; `tests/test_dashboard_webui.py` pins the topology target in the bundle seam |
| `ECP-ENG-019` | `workflow_change_set.py`, `workflow_evidence_packet.py`, `workflow_predicates.py`; neither the evaluator nor a seam nor the graph and edge modules import `se_harness.workflow` | `test_the_compliance_module_is_split_and_the_workflow_cycle_is_gone`; the lazy-import reading |
| `ECP-ENG-020` | `repository_graph.py` defines the five graph names once; `workflow_contract.lifecycle_family` is the one family reader; `_classify`, `_diagnostic`, `_catalog`, `_validation`, `_family` are defined nowhere | `test_each_workflow_graph_name_has_one_public_home` |
| `ECP-ENG-021` | every `from se_harness… import` across modules names a public name; the four authoring helpers `risks` imported privately are public in `artifact_layout` | `test_no_module_imports_a_private_name_across_the_package` (21 offenders at the base, 0 at the candidate) |
| `ECP-ENG-022` | the ten functions above 60 reduced by extraction of whole blocks into module-level helpers | `test_no_function_exceeds_complexity_sixty` (skips without radon; run in the scratch environment); the radon readings |
| `ECP-ENG-023`, `-024` | `CONTRACT_SHA256` equal (`a443e93d…`); no contract JSON, template, recipe or lock byte changed | `git diff --name-only 5c966cd1..HEAD`: 41 paths, all under `se_harness/`, `tests/`, `docs/notes/diagnostic-codes.md` and this domain |
| `ECP-ENG-025` | no approved specification names the split as operative; `SPEC-ECP-023` carries a dated record for `ECP-PRM-008`, whose writers now live in two modules | `validate --advisories` 0 errors |
| `ECP-ENG-026` | the suite at its baseline; `validate`, `doctor`, the lanes | the suite reading; the pull request's checks |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `radon cc`, functions above 60, base `5c966cd1` | scratch environment | 10: `build_findings` 105, `normalize_artifacts` 99, `validate_revision_consistency` 80, `run_preflight` 74, `build_dashboard_bundle` 74, `check_workflow` 71, `validate_risks` 69, `validate_decisions` 66, `build_readiness` 65, `build_explorer_metrics` 62 |
| `radon cc`, functions above 60, candidate | scratch environment | 0; the ten read 10, 18, 19, 39, 48, 49, 30, 30, 38, 29; the highest readings in the package are `apply_changes` 57 and `inspect_runtime_identity` 56, both untouched |
| private cross-module imports, base vs candidate | the inventory scan of `tests/test_module_seams.py` | 21 (`_catalog`/`_validation` at 8 sites, `_family`, the four authoring helpers) vs 0 |
| lazy imports of package modules (`from se_harness…` below module level), base vs candidate | `grep` over `se_harness/` | 48 vs 27; `workflow.py` 16 vs 0 |
| module sizes, base vs candidate (lines) | `wc -l` | `validate_engineering_artifacts.py` 3,324 → 261 plus nine seams of 94 to 582; `generate_harness_dashboard.py` 2,697 → 236 plus `dashboard_snapshot.py` 2,139 and `dashboard_bundle.py` 765; `workflow_compliance.py` 1,504 → 894 plus seams of 137, 253 and 310; `workflow.py` 1,033 → 707 plus `repository_graph.py` 167 and `workflow_edges.py` 234 |
| `validate --json`, `validate --advisories`, `inspect --json`, `inspect` (human), `doctor --json` | base vs candidate, same target | byte-identical |
| `dashboard --json` manifest and resources | base vs candidate | `dashboard-manifest.json` and every resource byte-identical, digest `c034708101a426a9…` at the candidate head |
| `check --checkpoint start --json` on `WO-ECP-036`, `WO-ECP-035`, `VREC-ECP-039`, `DEC-ECP-002`; `check --artifact WO-ECP-036` (projection); `transition … --json` (plan); `pr-body`; `preflight --json` and human | base vs candidate | byte-identical |
| `check --checkpoint handoff --from-git` formal snapshot | base vs candidate | `8a734d806bd730a0…` both, at the candidate head |
| `pylint --enable=duplicate-code --min-similarity-lines=8` | scratch environment | 0 blocks, as at the group B head |
| `validate --advisories` | exact 0.16.0 | 1,429 artifacts, 0 errors, 73 warnings (the pre-existing maintenance set), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| `preflight --work-order WO-ECP-036 --phase review` | exact 0.16.0 | PASS |
| `check --checkpoint handoff --from-git wo/ecp-035-one-validation` | exact 0.16.0 | see the retained `handoff.json` beside this packet |
| `CONTRACT_SHA256` | candidate | `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75` |
| `python -m repository_tools.diagnostic_code_index --check` | candidate | the page matches the source; eight attribution lines follow moved raise sites |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | 1,074 tests, 1 error, 23 skipped: the workstation baseline (`errors=1, skipped=22`) plus the complexity test, which skips where radon is absent; 6 tests added |

### The Windows suite

The one error is the standing Windows baseline,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
whose teardown removes a read-only `.git` tree; it fails the same way on
`main`. The 22 platform skips are the usual set; the twenty-third is
`test_no_function_exceeds_complexity_sixty`, which runs only where radon is
installed and passed in the scratch environment.

## Disclosures

1. The work order counted eleven functions above 60; the base reads ten,
   one having fallen below the line under group A's or B's edits. The ten
   are listed above with their readings on both sides.
2. The complexity test depends on radon, which the package does not
   require; the lanes skip it and the reading is repeated here. The other
   five seam tests run everywhere.
3. Making `_validate_changed_targets`, `_line_ending_conversion`,
   `_RFC3339`, `_review_evidence` and `_pull_request_body_findings` public
   was forced by the split: the evaluator still uses them, and
   `ECP-ENG-021` forbids importing them privately. The same holds for the
   four authoring helpers of `artifact_layout`, which the group B base
   already imported privately from `risks`. Every name a test patched by its
   private spelling follows the public one.
4. `workflow.py` now imports `workflow_compliance`, `preflight`,
   `mutation_guard`, `decisions` and `risks` at module level; `decisions` and
   `risks` keep their lazy imports of `plan_transition`, which is the one
   remaining cycle (a planner reached from the commands they implement).
   The 27 remaining lazy imports are of that shape or serve the CLI's
   startup cost.
5. The twin relation reader `workflow._targets` was
   `validation_core.relation_targets` line for line; the graph and edge
   modules import the latter.
6. The generator's manifest digest moves with the observed revision, so the
   digest above is the candidate head's; the equality that is the evidence
   is the base-versus-candidate comparison at each step.
