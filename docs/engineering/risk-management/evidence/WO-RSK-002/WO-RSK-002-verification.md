# WO-RSK-002 implementation evidence

artifact: WO-RSK-002
checkpoint: handoff
formal_snapshot_sha256: ee78ba68c17556793a7f1c3864c2527f5e2952a3853c377e6eca529ab33dfe4e

Retained by the implementation actor on 2026-08-25. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Candidate: this checkout, `python -m se_harness` from the repository root.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-RSK-002 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 903 artifacts, 0 errors, 50 warnings |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python -m se_harness doctor .` | candidate | `PASS risk-policy: C-RSK-001: [risk] absent; default acceptance level 1` (this root has no `[risk]` section yet) |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | candidate | exit 0 |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-RSK-002 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both report formal snapshot `ee78ba68c17556793a7f1c3864c2527f5e2952a3853c377e6eca529ab33dfe4e` |
| `python -m unittest tests.test_risk_management` | candidate | 14 tests, OK (9 from WO-RSK-001, 5 new) |
| `python -m unittest tests.test_mutation_guard` | candidate | 11 tests, OK; `raise-risk` enumerated among the public mutators that reject before any write |
| `python -m unittest tests.test_agentic_execution tests.test_risk_management tests.test_hash_bound_integrity tests.test_standard_repository_lifecycle tests.test_harnessctl tests.test_release_qualification` | candidate | 212 tests, OK, 4 skips |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 1016 tests in 353.383s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards |
| Linux lane | `.github/workflows/candidate-evidence.yml` | not run locally; the pull-request run is the Linux figure |

## Complete changed-path set

```
docs/engineering/risk-management/evidence/WO-RSK-002/WO-RSK-002-verification.md
docs/notes/agentic-execution-skills-mvp.md
docs/notes/risk-management.md
se_harness/artifact_layout.py
se_harness/mutation_guard.py
se_harness/preflight.py
se_harness/skill_contract.py
templates/repository/standard/.agents/skills/harness-draft-change/SKILL.md
templates/repository/standard/.agents/skills/harness-draft-change/scripts/guard.py
templates/repository/standard/.agents/skills/harness-draft-change/skill-contract.json
templates/repository/standard/.agents/skills/harness-execute-work-order/SKILL.md
templates/repository/standard/.agents/skills/harness-execute-work-order/scripts/check_scope.py
templates/repository/standard/.agents/skills/harness-execute-work-order/skill-contract.json
templates/repository/standard/.agents/skills/harness-prepare-assurance/SKILL.md
templates/repository/standard/.agents/skills/harness-prepare-assurance/skill-contract.json
tests/fixtures/agentic_execution/phase3/portable_vectors.json
tests/test_agentic_execution.py
tests/test_mutation_guard.py
tests/test_risk_management.py
```

Every path is admitted by `[execution_scope].paths` of `WO-RSK-002`. Scoped
paths left untouched: `se_harness/cli.py`, `docs/notes/harnessctl-reference.md`.

## Rule coverage

| Rule | Implemented by | Test evidence |
| --- | --- | --- |
| `RSK2-GRD-001` | `raise-risk` in `PUBLIC_MUTATION_OPERATIONS`; `create_risk` requests that operation | `test_raise_risk_is_a_registered_guard_operation_and_uses_it` |
| `RSK2-DOC-001` | `risk_policy_check` (`risk-policy`, detail `C-RSK-001: …`) appended to `inspect_installation` before the hash-bound checks; preflight surfaces it as `I001` through the existing path | `test_doctor_reports_c_rsk_001_only_for_an_invalid_risk_section`; `test_hash_bound_integrity` still sees the hash-bound checks last |
| `RSK2-SKL-001` | `raise-risk` in the draft-change and execute-work-order profiles and contracts; effect class `risk-raise` in both profiles, contracts, and helpers (`check_scope.py` `AEXEXE011`, `guard.py` `AEXDRF013`: only new risk artifact paths); one procedure sentence each in `SKILL.md` | `test_skill_contracts_require_the_risk_operations_and_permit_risk_raise`, `test_helpers_admit_risk_raise_only_for_new_risk_paths` |
| `RSK2-SKL-002` | `risks` in the prepare-assurance profile and contract; one procedure sentence | same contract test |
| `RSK2-SKL-003` | contract versions `1.0.1 -> 1.0.2`; `phase3/portable_vectors.json` regenerated with `build_skill_manifest` and `canonical_json_bytes`; Claude adapters untouched | `test_all_four_portable_cores_match_retained_phase3_vectors`, `test_closed_phase3_contracts_and_manifests_validate` |
| `RSK2-AMD-001..003` | already the shipped behaviour of `WO-RSK-001`; now specified | `test_amendments_are_the_shipped_behaviour`, existing `RiskManagementTests` |

## Material deviations from SPEC-RSK-002

1. `RSK2-DOC-001` names the check `C-RSK-001`. The check's name in the
   installation-check list is `risk-policy` and its detail begins with
   `C-RSK-001:`, following the existing convention that check names are
   descriptive and codes live in the detail; `doctor` prints
   `PASS|FAIL risk-policy: C-RSK-001: …`.
2. `RSK2-SKL-001` describes the helpers admitting risk paths "as an effect
   path". The implementation introduces an explicit effect class
   `risk-raise` in both helpers, profiles, and contracts so that a risk path
   cannot be smuggled under `implementation-write` and a `risk-raise` effect
   cannot touch anything but a risk file. The spec did not name the class.

## Note on the first full-suite run

The first full run failed six tests for two causes, both in test code: the
helper-admission test imported the skill helpers and thereby wrote
`__pycache__` into the portable cores, whose manifests bind every file; and
the mutation-guard enumeration did not yet list `raise-risk`. The test now
executes the helper sources without bytecode, the enumeration includes the
operation with an on-disk threatened artifact, and the caches were removed.
The figure above is the rerun.

## Not done

Linux figure pending the pull-request lane. `harnessctl-reference.md` was
not edited: the guard operation and the doctor check add no command or flag.
