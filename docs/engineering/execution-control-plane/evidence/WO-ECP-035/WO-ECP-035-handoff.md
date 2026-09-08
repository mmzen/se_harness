```toml
artifact = "WO-ECP-035"
checkpoint = "handoff"
formal_snapshot_sha256 = "c0487b5ed49718378a78b4ef647bcb6a5becf4694c7de3d282424d09eb3b2f33"
rebound_at = "2026-09-08T18:06:18Z"
```

# WO-ECP-035 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

Each governance command validates the repository at most once, and a
command that validates does so exactly once. The report travels: `run_preflight`,
the generator's `generate_bundle`, provenance's catalog and the qualification
check take the in-process `ValidationReport`; the checkpoint context carries it
so no gate predicate validates again; `check` retains its own Git-derived
handoff result; `capture-verification` and `prepare-release` hand their one
validation to the writer and to the prepared result, which parses the new
record alone; `doctor` reads `W013` from the layout pass without the graph
passes; `inspect` derives its report from one validation and writes no bundle.
Preflight classifies candidate-versus-released skew apart and never blocks on
it, and the check applies the same classifier. Provenance reads the
validator's metadata and parses no TOML a second time. Every recorded output
is byte-identical to the group A code's on this repository.

## Evaluators

- Governor: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel `a969d6ab…`, the digest
  `RLS-SEH-025` binds), `-I`, for every reading, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/ecp-035-one-validation`, stacked on
  the group A branch at `c751b640`; the code commit is `51f25a22`.
- Byte identity: the group A head (`c751b640`, a worktree) and the candidate,
  each run on the same target checkout at the same revision.
- Validation counts: `tests/test_one_validation.py` and the same harness run
  by hand, a counting patch on `validate_repository` in the validator and in
  the generator, every governance command on a fixture repository.
- Duplication scan and complexity: `pylint 4.0.8` and `radon 6.0.1` in a
  scratch environment outside the checkout.

## Rule-to-case map

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `ECP-ENG-010` | one validation per invocation: `check` (every checkpoint and the projection), `transition`, `evidence`, `pr-body`, `preflight`, `validate`, `inspect`, `dashboard`, `capture-verification` and `prepare-release`; `doctor` and `create-artifact --dry-run` none | `ValidationCountTests.test_each_governance_command_validates_at_most_once`; the counts below |
| `ECP-ENG-011` | `run_preflight(..., report=)`, `generate_bundle(..., report=)`, `provenance._validation_catalog(root, report)`, `release_qualification._validation_check(root, id, report)`; provenance's catalog holds the validator's `Artifact` objects and `_load_metadata` returns their metadata, `standing_deviations_for_work` reads it, `_decision_metadata` and the second `front_matter.read` are gone | `ReportTravelsTests` (a second validation or a re-parse raises under a patch) |
| `ECP-ENG-012` | `validate_engineering_artifacts.canonical_layout_diagnostics` loads the artifacts and runs the layout pass alone; `doctor` reads it | `test_doctor_reads_the_layout_pass_alone_and_agrees_with_the_full_run`; the byte-identity reading of `doctor --json` |
| `ECP-ENG-013` | `inspect` runs `generate_snapshot` once and writes no bundle, as before; the count reads one | the counts below |
| `ECP-ENG-014` | `preflight.lifecycle_relevant` and `lock_files` are the classifier; `run_preflight` splits `diagnostics` (blocking) from `skew` and `ready` reads the blocking set; `workflow_compliance.lifecycle_relevant_diagnostics` applies the same classifier; the rendering and the JSON carry the skew apart | `test_preflight_reports_skew_apart_and_the_check_reads_the_same_verdict`; `tests/test_workflow_execution.py` (a faked skew report still passes the transition) |
| `ECP-ENG-015` | `_generate_snapshot(root, report)` calls `generate_bundle(root, report=report)`; the generator's `main` calls the same function with no report | `test_the_snapshot_builder_and_qualification_take_the_report`; `tests/test_revision_provenance.py` |
| `ECP-ENG-016` | every recorded output equal between the group A code and the candidate on the same target and revision | the byte-identity readings |
| `ECP-ENG-023`, `-024` | `CONTRACT_SHA256` equal (`a443e93d…`); no contract JSON, template, recipe or lock byte changed | `git diff --name-only c751b640..HEAD` |
| `ECP-ENG-025` | `SPEC-ECP-005` carries the amendment record for `ECP-KRN-007`, whose filter now lives in preflight | `validate --advisories` 0 errors |
| `ECP-ENG-026` | the suite at its baseline; `validate`, `doctor`, the lanes | the suite reading; the pull request's checks |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| validations per command, base | counting patch, fixture repository | `check --checkpoint start` 2, `capture-verification` 3 (the governed checkpoint, the catalog, the generator), `prepare-release` 3, `check` projection 2 when the reading manifest ran preflight; every other command 1; `doctor` 1 |
| validations per command, candidate | counting patch, fixture repository | every validating command 1; `doctor` 0; `create-artifact --dry-run` 0 |
| `validate --json`, `validate --advisories`, `inspect --json`, `doctor --json` | base vs candidate, same target | byte-identical |
| `dashboard --json` manifest | base vs candidate | `dashboard-manifest.json` byte-identical, digest `e9567fb12aa83ce2…` |
| `check --checkpoint start --json` on `WO-ECP-035`, `WO-ECP-034`, `VREC-ECP-038` | base vs candidate | byte-identical |
| `check --checkpoint handoff --from-git` formal snapshot | base vs candidate | `c0487b5ed4971837…` both |
| `preflight --work-order WO-ECP-035 --phase review` | base vs candidate, this repository | base `FAIL` with 10 diagnostics, candidate `PASS` with the same 10 items listed under the skew heading and 0 blocking; every one is a `distribution:` or unrecorded `lock-entry:` item the check already admitted (disclosure 1) |
| wall clock, `check --checkpoint start` on this repository | warm cache, alternating runs | about 3.0 s on both sides: the second validation was not the command's cost here; cold, the first run read 17.6 s to 5.2 s but that is the cache, not the code |
| `validate --advisories` | exact 0.16.0 | 1,428 artifacts, 0 errors, 73 warnings (the pre-existing maintenance set), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| `preflight --work-order WO-ECP-035 --phase review` | exact 0.16.0 | PASS |
| `check --checkpoint handoff --from-git wo/ecp-034-engine-import-surface` | exact 0.16.0 | Completed; all nine `QGP-G4I-*` predicates pass, every one of the 16 changed paths inside the declared scope; `complete: true`; the schema-2 result is retained beside this packet as `handoff.json` |
| `CONTRACT_SHA256` | candidate | `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75` |
| `pylint --enable=duplicate-code --min-similarity-lines=8` | scratch environment | 0 blocks, as at the group A head |
| `radon cc`, functions above 60 | scratch environment | 10, as at the group A head; group C's |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | 1,068 tests, 1 error, 22 skipped: the workstation baseline (`errors=1, skipped=22`) at `51f25a22`; 5 tests added |

### The Windows suite

The one error is the standing Windows baseline,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
whose teardown removes a read-only `.git` tree; it fails the same way on
`main`. The 22 skips are the platform set.

## Behaviour changes, each where a copy was wrong or a form was inconsistent

- `preflight` no longer fails on candidate-versus-released skew; it lists
  those items under "Candidate-versus-released skew (not blocking)" and the
  JSON gains a `skew` member after `diagnostics`. On this repository the
  review preflight of every wave 3 work order turns from FAIL to PASS on
  the ten skew items; `check --checkpoint start` already admitted them.
- `doctor` reports `W013` for an artifact the full run rejects for another
  reason (the full run hides layout warnings of erroring artifacts); on a
  clean graph the two agree byte for byte.
- `capture-verification` and `prepare-release` project the prepared record
  from the pre-write validation plus the parsed record, not from a second
  validation of the written tree; the result is unchanged for a valid graph.
- A dashboard generation fault inside `capture-verification` now names the
  fault in the refusal, where the subprocess's exit code said only that it
  failed.

## Disclosures

1. `preflight`'s verdict is not a recorded output under `SPEC-ECP-024`'s
   Terms, and `ECP-ENG-014` changes it by design; the items are the same on
   both sides and only their classification moves. The payload key pin of
   `tests/test_repository_context_retirement.py` gains the `skew` member.
2. The wall-clock reading shows no gain at warm cache on this workstation:
   validating this repository costs tens of milliseconds against a three-second
   command, so the count, not the clock, is the evidence of `ECP-ENG-010`.
3. `ECP-KRN-007` of `SPEC-ECP-005` named `workflow_compliance.py` as the
   filter's home; the classifier moved to preflight so both readers share it,
   and the specification carries the dated record.
4. `tests/test_mutation_guard.py` faked provenance's catalog as JSON
   dictionaries and patched `_load_metadata`; it now fakes the validator's
   artifact shape and needs no metadata patch.
5. `release_qualification._validation_check` accepts a report but its two
   legs validate their selected root once each already; the parameter is the
   rule's, unused by the legs.
