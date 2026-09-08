```toml
artifact = "WO-ECP-034"
checkpoint = "handoff"
formal_snapshot_sha256 = "2cdd557b688541fb0a5654d55ba953d70debbef98e244f9f76d9210d691f370d"
rebound_at = "2026-09-08T17:29:26Z"
```

# WO-ECP-034 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`se_harness/engine/` is an import surface. The validator, the generator and
the inspector import their siblings and the package by name; the CLI,
`preflight`, the workflow, `provenance` and `release_qualification` import
them and run them in-process; the path loader and the four command-line
assemblies are gone; each entry module still runs as
`python -m se_harness.engine.<name>`. The five twins have one definition: the
layout tables in `artifact_layout`, the lifecycle registry through
`workflow_contract.load_lifecycle_registry`, one evaluator-evidence validator
whose reasons the engine renders as its own E012 messages, the
implemented-or-later status set in `workflow_contract`, one body parser in
`front_matter` and one artifact-id pattern in `artifact_layout`. The
engine's 73 codes are named in `codes.py` and the index attributes them by
name. Every recorded output is byte-identical to the base code's on this
repository.

## Evaluators

- Governor: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel `a969d6ab…`, the digest
  `RLS-SEH-025` binds), `-I`, for every reading, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/ecp-034-engine-import-surface` off
  `main` at `0e7d718b`; the code commits are `647d666c` (the import surface
  and the loaders), `a30ecc44` (the twins, the codes, the amendment records)
  and `41c77a44` (two CLI shape tests and the `ECP-COR-014` record); `5094aea7`
  merges `main` at `517dc5f6` (disclosure 9).
- Byte identity: the base code (a worktree at the start commit `a8e9a5ca`,
  whose code equals `main`'s) and the candidate code, each run on the same
  target checkout at the same revision, so the observed revision the
  snapshot embeds is equal on both sides.
- Duplication scan: `pylint 4.0.8` in a scratch environment outside the
  checkout (`C:/Users/hok/se-harness-scan`), `--enable=duplicate-code
  --min-similarity-lines=8`; complexity: `radon 6.0.1` in the same
  environment.

## Rule-to-case map

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `ECP-ENG-001` | the three engine modules import `se_harness.engine.<sibling>`, `se_harness.artifact_layout`, `workflow_contract`, `front_matter`, `evaluator_evidence`, `integrity` and `codes`; no `spec_from_file_location`, no `sys.path` edit; `engine/__init__.py` states the import surface | `tests/test_engine_import_surface.py` `ImportSurfaceTests` |
| `ECP-ENG-002` | each entry module keeps its `main()` and `if __name__ == "__main__"`; `python -m se_harness.engine.<name> --help` exits 0 for the three | `test_each_entry_module_runs_as_a_module_with_its_arguments`; the byte-identity readings below |
| `ECP-ENG-003` | `preflight._load_validator_module` gone; `workflow._validation`, `run_preflight`, `cli` (`validate`, `dashboard`, `inspect`, `doctor`), `provenance._validation_catalog` and `_generate_snapshot`, `release_qualification._validator_report` call the engine in-process; `cli._launch_engine`, `_run_distribution_script`, `_distribution_script`, `_distribution_environment`, `ENGINE_TIMEOUT_SECONDS` and `installer.engine_script` are gone | `test_the_package_loads_no_engine_module_by_path`; `tests/test_cli_shape.py` (the two engine tests read the in-process entry) |
| `ECP-ENG-004` | `engine/artifact_layout_registry.py` deleted; the validator imports the tables and the four path functions from `artifact_layout` | `TwinTests.test_the_layout_tables_have_one_definition`; `tests/test_artifact_authoring.py` |
| `ECP-ENG-005` | the validator's `LifecycleStatePolicy`, `_load_workflow_lifecycles` and `_lifecycle_family` replaced by `workflow_contract.LifecycleState`, `load_lifecycle_registry` and `lifecycle_family`; the hand-written matrix of `tests/test_lifecycle_state_contract.py` retired, the test reading the registry | `test_the_lifecycle_registry_has_one_loader`; `tests/test_lifecycle_state_contract.py` (nine cases, two new for the status set) |
| `ECP-ENG-006` | `evaluator_evidence.validate_evaluator_evidence` is the one validator of the document, each refusal carrying a `reason`; the engine keeps its bytes, digest, path, lock and JSON checks and renders every reason as its own E012 message through `_EVIDENCE_MESSAGES`; `require_archive` and `require_isolated_python` are the engine's two stricter parameters | `test_one_evidence_validator_serves_the_engine_with_its_own_messages` (every reason mapped; eight throwaway documents); `tests/test_revision_provenance.py` E012 cases |
| `ECP-ENG-007` | `workflow_contract.IMPLEMENTED_OR_LATER_STATUSES`, checked at load: each state declared for `work_order` and the set closed under its edges; the validator, the generator, `preflight` and `provenance` import it | `test_the_status_set_the_body_parser_and_the_id_pattern_have_one_home`; two new refusal cases in the lifecycle test |
| `ECP-ENG-008` | `front_matter.body_sections` serves the validator and, through the validator's `specification_rules` and `coverage_rows`, the generator; `artifact_layout.ID_PATTERN` serves the validator, `provenance` and `workflow_procedures`; `evidence_work_order_keys` serves the validator and `provenance` | the same test; the duplication scan reading |
| `ECP-ENG-009` | 73 engine codes in `codes.py` (69 new, four already named), the engine spells none; `repository_tools/diagnostic_code_index.py` attributes a name anywhere in a call's arguments and in a dictionary key; `I-REV` registered as a prefix the page had missed | `EngineCodeTests`; `tests/test_diagnostic_code_index.py`; the page reading |
| `ECP-ENG-016` | every recorded output equal between the base code and the candidate on the same target and revision | the byte-identity readings |
| `ECP-ENG-023`, `-024` | `CONTRACT_SHA256` equal (`a443e93d…`); no contract JSON, template, recipe or lock byte changed | `git diff --name-only main..HEAD`; the digest suites in the full run |
| `ECP-ENG-025` | amendment records on `SPEC-DST-025` (`DST-ENG-003`, `DST-ENG-006`), `SPEC-ECP-021` (`ECP-COR-014` and the engine timeout row) and `SPEC-IAR-008` (rule 1, the standard-library clause) | `validate --advisories` 0 errors; disclosure 3 |
| `ECP-ENG-026` | the suite at its baseline; `validate`, `doctor`, the lanes | the suite reading; the pull request's checks |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| path loads and subprocess assemblies of the engine in the package | grep, base vs candidate | 27 sites in six modules to 1 (the `ENGINE_ROOT` constant of `installer.py`, which the tests' root-identity support reads) |
| test modules loading the engine by path or through the retired loader | grep | 22 to 0; eight modules still load other scripts by path (`.github/scripts`, `scripts/`), outside this scope |
| twins | inventory | five pairs to one definition each, plus the evidence-key function the assessment had counted as a duplicate block |
| code literals in `se_harness/engine/` | AST, the index tool's grammar | 226 sites, 73 codes to 0 |
| registry | `codes.py` | 118 to 187 constants |
| `diagnostic_code_index --check` | candidate | matches; 196 codes across 30 prefixes to 197 across 31: `I-REV-001`, the one code the page had missed; 74 rows re-attributed to `code: message` text |
| `validate --json`, `validate --advisories` | base vs candidate, same target | byte-identical |
| `inspect --json`, `inspect` | base vs candidate | JSON byte-identical; the human text identical after carriage-return normalisation (disclosure 1) |
| `doctor --json` | base vs candidate | byte-identical |
| `preflight --work-order WO-ECP-034 --phase review` | base vs candidate | byte-identical |
| `dashboard --json` manifest | base vs candidate | `dashboard-manifest.json` byte-identical, digest `54c500c243e7fac5…` |
| `check --checkpoint start --json` on `WO-ECP-034`, `WO-ECP-033`, `VREC-ECP-037` | base vs candidate | byte-identical; `result_sha256` `cab9d8e2…`, `a24e3534…`, `b4dd5fab…` |
| `check --checkpoint handoff --from-git main` formal snapshot | base vs candidate | `fe052def…` both |
| `validate --advisories` | exact 0.16.0 | 1,427 artifacts (after the merge of `main`, disclosure 9), 0 errors, 73 warnings (the pre-existing maintenance set), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| `preflight --work-order WO-ECP-034 --phase review` | exact 0.16.0 | PASS |
| `check --checkpoint handoff --from-git main` | exact 0.16.0 | Completed; all nine `QGP-G4I-*` predicates pass, every one of the 47 changed paths inside the amended scope; `complete: true`; the schema-2 result is retained beside this packet as `handoff.json`. The first run refused `se_harness/workflow_procedures.py` on `QGP-G4I-PATHS`; disclosure 8 |
| `CONTRACT_SHA256` | candidate, `main` vs branch | `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75` both |
| `pylint --enable=duplicate-code --min-similarity-lines=8` | scratch environment | 3 blocks at the base, 0 on this branch (disclosure 2) |
| `radon cc`, functions above 60 | scratch environment | 11 at the base, 10 on this branch: `_validate_evaluator_evidence_binding` fell below 60 with the fold; the rest are group C's |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | 1,063 tests, 1 error, 22 skipped: the workstation baseline (`errors=1, skipped=22`) at `5094aea7`, after the merge of `main` whose `WO-TST-004` collapsed the inherited re-runs; before the merge 1,333 tests, 1 error, 26 skipped at `41c77a44` |

### The Windows suite

The one error is the standing Windows baseline,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
whose teardown removes a read-only `.git` tree; it fails the same way on
`main`. The 26 skips are the platform set. The run at `647d666c` read
`errors=20`: one stale loader import that lost twenty modules at collection,
the bare patch target of one inspection test, and the wheel fixture of
disclosure 7; the run at `a30ecc44` read `failures=2`: the two CLI shape
tests that mocked the engine subprocess, now mocking the entry module.

## Behaviour changes, each where a copy was wrong or a form was inconsistent

- The human `inspect` rendering on Windows no longer carries a doubled
  carriage return per line: the subprocess capture translated line endings
  once in the child and once in the parent. On POSIX the bytes are equal.
- A `harnessctl init` from a wheel that lacks the engine subpackage fails at
  import; the hand-built wheel fixture of `tests/test_release_build.py`
  packed only the top-level modules and now packs the engine too. A wheel
  built by the release recipe always carried it.
- `validate_evaluator_evidence` checks in the engine's order (payload
  manifest before version, the lock last); for a document with two defects
  the package's readers may name the other defect first. Single-defect
  messages are unchanged on both sides.
- `load_lifecycle_registry` refuses a contract whose `work_order` family
  lacks `implemented`, `verified` or `released`, or whose edges leave that
  set; the shipped contract passes.
- `provenance` and `release_qualification` no longer scrub `PYTHONPATH` or
  bound a 1,800-second engine timeout: the engine runs inside the
  evaluator's own interpreter, which `-I` already isolates.

## Disclosures

1. Byte identity is read on the same target at the same revision by running
   the base code from a worktree; the first comparison against readings
   taken before the start commit differed only in the observed revision the
   snapshot embeds.
2. The duplication scan reads 0 blocks: the three engine-side blocks the
   assessment recorded were the layout registry, `evidence_work_order_keys`
   and the body parser, all folded here. `ECP-PRM-027` of `SPEC-ECP-023` is
   therefore met at this head; `DEC-ECP-002`'s revisit trigger (the merge of
   wave 3) arrives with this work order's merge.
3. `SPEC-IAR-008` is `implemented`, not `approved`; its rule 1 named the
   target-local script execution `WO-DST-024` had already retired, and it
   receives a record for completeness. `SPEC-ECP-021` `ECP-COR-014` bound the
   four engine launches to a timeout; with no launch the rule is withdrawn by
   record.
4. The `agentic_operations`-style structural check of the status set uses
   the `work_order` family's edges, not a registry flag: no flag
   distinguishes the three states from `approved` and `in_progress`.
5. `tests/test_predecessor_bootstrap_retirement.py` carries opcode fixtures
   describing the 0.15.0 root validator against the candidate; they compare
   files only when the lock names a root copy, which the 0.16.0 root does
   not, so they are unaffected and untouched.
6. `SPEC-ECP-024` names the engine `Governance command` list for group B;
   this group changes no command's number of validations.
7. The hand-built wheel fixture of `tests/test_release_build.py` packed the
   top-level modules only; a fresh `init` from it now fails at import without
   the engine subpackage, so the fixture packs `se_harness/engine/*.py` as the
   release recipe's wheel always has.
8. `se_harness/workflow_procedures.py` was outside the work order's scope though
   `ECP-ENG-008` reaches its copy of the artifact-id pattern. The handoff check
   refused it (`WEX201`); the accountable engineering owner amended the scope on
   2026-09-08 under DR-REMEDIATION-SCOPE and the work order carries the dated
   amendment. Nothing else was widened.
9. `main` moved under this branch while the group ran: the wave 5 packets
   (#409, #410, #411) and `WO-TST-004` (#402, the test-suite hygiene), which
   rewrote how twenty test modules load the engine through
   `tests/root_identity_support.load_evaluator_module`. The merge resolved
   those twenty by taking `main`'s structure and pointing the one loader at
   the package: it imports `se_harness.engine.<name>` and answers the retired
   registry name with `se_harness.artifact_layout`. `main` changed no file
   under `se_harness/` or `repository_tools/`, so the base code of the
   byte-identity comparison is still `main`'s code.
