# WO-RSK-001 implementation evidence

artifact: WO-RSK-001
checkpoint: handoff
formal_snapshot_sha256: 6b2fad40306d5b560403460a36723a1e937eff05ab4f93c3e697aff5eb83d50c

Retained by the implementation actor on 2026-08-25. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.
  The candidate validator, contracts, and commands are exercised against
  installed targets in `tests/test_risk_management.py`; this repository's own
  root keeps the 0.6.0 copies and contains no risk artifact.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-RSK-001 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 893 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_engineering_artifacts.py --root .` | candidate | PASS, 893 artifacts, 0 errors, 50 warnings |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | candidate | exit 0 |
| `cmp` packaged vs template `WORKFLOW.json` and `QUALITY_GATES.json` | bytes | identical |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-RSK-001 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `6b2fad40306d5b560403460a36723a1e937eff05ab4f93c3e697aff5eb83d50c` |
| `python -m unittest tests.test_risk_management` | candidate | 9 tests, OK |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 1011 tests in 342.883s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards. Two earlier runs surfaced twelve tests that pinned template-equals-root or a four-family matrix; each was redirected to the candidate copies or extended for the fifth family, and the third run is the figure |
| Linux lane | `.github/workflows/candidate-evidence.yml` | not run locally; the pull-request run is the Linux figure |

## Scenario 2 transcript (from `tests/test_risk_management.py`)

1. `WO-001` in progress with scope `src/`; `raise-risk` → `RISK-PRD-001`
   `raised`, score 12 at level 1, `decided_by = "harnessctl"`.
2. `check --checkpoint handoff --changed-path src/main.py --changed-path
   docs/engineering/product/risks/RISK-PRD-001.md --changes-complete`:
   `QGP-G4I-PATHS` pass (scope exception), `QGP-G4I-RISK` fail naming
   `RISK-PRD-001 (raised, score 12 at level 1)` and `engineering-owner`.
3. `transition --set RISK-PRD-001=mitigating --decision RISK-PRD-001=engineering-owner
   --reason "RISK-PRD-001=mitigated_by WO-001: …" --apply` → `mitigating`,
   `mitigated_by = ["WO-001"]`.
4. Handoff check: `QGP-G4I-RISK` pass; the disposed risk file is no longer an
   admitted changed path (`QGP-G4I-PATHS` fail).
5. `mitigated` refused until `VREC-001` verified covers `WO-001`; refused when
   the residual reaches the level without "accepted"; applied with
   `residual 2x3 accepted …` → `residual_likelihood`, `residual_impact` set.
6. `prepare_release` with a raised risk threatening `WO-001` refuses.
7. `risks`, `focus`, `inspect` (`dispose-risk` in "Decision required"), and
   `dashboard` (0 errors) all surface the register.

## Complete changed-path set

```
docs/engineering/risk-management/evidence/WO-RSK-001/WO-RSK-001-verification.md
docs/notes/README.md
docs/notes/harnessctl-reference.md
docs/notes/risk-management.md
se_harness/artifact_layout.py
se_harness/cli.py
se_harness/provenance.py
se_harness/quality_gates_contract.json
se_harness/workflow.py
se_harness/workflow_compliance.py
se_harness/workflow_contract.json
se_harness/workflow_contract.py
templates/repository/standard/.engineering-harness.toml.tpl
templates/repository/standard/docs/engineering/DECISION_RIGHTS.md
templates/repository/standard/docs/engineering/QUALITY_GATES.json
templates/repository/standard/docs/engineering/QUALITY_GATES.md
templates/repository/standard/docs/engineering/TRACEABILITY.md
templates/repository/standard/docs/engineering/WORKFLOW.json
templates/repository/standard/docs/engineering/WORKFLOW.md
templates/repository/standard/docs/engineering/templates/RISK.template.md
templates/repository/standard/scripts/artifact_layout_registry.py
templates/repository/standard/scripts/inspect_engineering_artifacts.py
templates/repository/standard/scripts/validate_engineering_artifacts.py
tests/test_artifact_authoring.py
tests/test_artifact_catalog.py
tests/test_lifecycle_state_contract.py
tests/test_risk_management.py
tests/test_validation_taxonomy.py
tests/test_workflow_execution.py
tests/test_workflow_procedures.py
```

Every path is admitted by `[execution_scope].paths` of `WO-RSK-001`. Scoped
paths left untouched: `templates/repository/standard/scripts/generate_harness_dashboard.py`,
`templates/repository/standard/scripts/harness_explorer/`,
`templates/repository/standard/.agents/skills/`, `se_harness/workflow_procedures.py`,
`se_harness/preflight.py`, `se_harness/installer.py`, `se_harness/skill_contract.py`,
`pyproject.toml` (the new template file is covered by the existing
`docs/engineering/templates/*` data-files wildcard).

## Rule coverage

| Rule | Implemented by | Test evidence |
| --- | --- | --- |
| `RSK-ART-001..004` | `risk` type in both layout registries, `RISK.template.md`, `validate_risks` (`E-RSK-001/002`) | `test_raise_risk_computes_score…`, `test_validator_rejects_score_stage_and_stale_status_defects` |
| `RSK-LCY-001..004` | `risk` family in `WORKFLOW.json`; `WFL-RISK-RAISED`, `WFL-RISK-MITIGATING`, `PROC-RISK-DISPOSE`, `PROC-RISK-MITIGATED`; `DR-RISK-DISPOSE` and the stage table in `DECISION_RIGHTS.md`; `_validate_risk_edge` and `_mutate` in `workflow.py` | `test_disposition_is_refused_for_the_wrong_role…`, `test_mitigated_requires_verified_coverage…`, `test_risks_command_focus_inspect…` (focus) |
| `RSK-GTE-001..003` | evaluator `undisposed_risks_threatening_scope`; seven predicates; corrective escalations on the five gated command steps | `test_raised_risk_blocks_handoff_until_disposed…`; `test_every_gated_command_step_declares_one_distinct_corrective_per_predicate` (existing) |
| `RSK-CMD-001..004` | `raise-risk`, `risks`; `lists_risks` and refusal in `prepare_release`; scope exception `undisposed_risk_paths` | `test_raise_risk_refuses_unknown_targets…`, `test_prepare_release_refuses_undisposed_risks`, handoff test |
| `RSK-CFG-001` | `[risk]` in the installation template; `load_risk_policy` / `E-RSK-007` | `test_configured_level_keeps_a_low_risk_identified…`, defects test |
| `RSK-TRC-001` | `TRACEABILITY.md` type row and `TRC-REL-020..023`; `RELATION_TARGET_TYPES` | `test_released_policy_copies_match_with_declared_candidate_exceptions` (declares the rows), validator tests |
| `RSK-SRF-001..002` | `inspect` queue `dispose-risk`; generic dashboard rendering; `STEP-WO-START-RISKS`, `STEP-WO-IMPLEMENT-RISKS` | `test_risks_command_focus_inspect…`, `test_standard_start_procedure_has_exact_order_and_argv` |

## Material deviations from SPEC-RSK-001

1. `RSK-SRF-002` asks for a `RISKS` reading step in every stage procedure.
   Added to `PROC-WO-START` and `PROC-WO-IMPLEMENT` only. The decision-only
   procedures (VREC, RLS, definition) have a single decision step; prepending
   a command step would change every existing restitution for those states
   (their `Next` would become "run the risks command"). The register reaches
   those stages through the `*-RISK` predicate message instead.
2. `RSK-ART-001` places residual fields in `[risk]`; they are top-level
   (`residual_likelihood`, `residual_impact`, written as quoted numerals by
   `_set_scalar`). The transition writer can only set top-level scalars, and
   `validate_risks` accepts numerals in string or integer form.
3. `RSK-CMD-001` says `raise-risk` runs under its own mutation-guard operation.
   `mutation_guard.py` is outside this work order's scope, so the command runs
   under the registered `create-artifact` operation, which is what it does.
4. `RSK-CFG-001` names a `doctor` check `C-RSK-001`. An invalid `[risk]`
   section is reported by the validator as `E-RSK-007` on the policy plane,
   which every gate and CI run evaluates; `doctor` itself is unchanged.
5. `RSK-SRF-001` asks for an Explorer register view. The dashboard generator
   is untouched: `tests/test_dashboard_webui.py` pins the template byte-equal
   to the released root copy, and the generator already renders a risk through
   its generic artifact and relation model (the risk test generates a
   dashboard with 0 errors). No dedicated view was added in this increment.
6. The skill cores (`.agents/skills/`) are unchanged: their manifest digests
   are pinned by `tests/fixtures/agentic_execution/canonical_vectors.json`,
   and the capability the work order describes ("draft and execute may raise")
   is available to any agent through the CLI; no skill can dispose. Recording
   the skill-core update as follow-up work.
7. `RSK-LCY-002` reserves `identified -> raised` to computation. `transition`
   accepts that edge for any actor; the validator's `E-RSK-003` and the
   computed status at raise time are the enforcement. Not special-cased.

## Deviation acceptances

Recorded on 2026-08-25 from the owner's interactive answers, before the
completion decision. These are the owner's statements; the assurance decision
on `VREC-RSK-001` remains separate.

| Deviation | Owner answer |
| --- | --- |
| 1 — `RISKS` reading step only in the work-order procedures | Accept: the predicate message already surfaces the register at decision-only stages; unchanged restitution is worth more than a redundant step. |
| 2 — residual fields top-level, quoted numerals | Accept: validation enforces the invariant; the field placement is a schema detail the spec can be amended to match. |
| 7 — `identified -> raised` not special-cased in `transition` | Accept: `raise-risk` computes it and `E-RSK-003` refuses a stale status. |
| 3 — `raise-risk` under the `create-artifact` guard operation | Accept: same protection through in-scope surfaces; a dedicated operation can follow under a later work order. |
| 4 — invalid `[risk]` section is validator `E-RSK-007`, not a `doctor` check | Accept: every gate and CI run evaluates it; a doctor check can follow. |
| 5 — no dedicated Explorer register view | Accept as follow-up work: the generator is pinned to the released root and renders risks generically. |
| 6 — skill cores unchanged | Accept as follow-up work: `raise-risk` is reachable through the CLI and no skill may dispose. |

Follow-up work recorded for a later work order: dedicated `raise-risk` guard
operation, `doctor` check for `[risk]`, Explorer register view, skill-core
update with regenerated digests, `RISKS` step in decision-only procedures if
their restitution baseline is revised, and the `SPEC-RSK-001` amendments
matching deviations 1, 2, and 7.

## Not done

Linux figure pending the pull-request lane. Scenario 6 (blinded review of
disposition rationales) requires reviewers the implementation actor cannot
supply; the assurance owner decides whether it is required before verification.
