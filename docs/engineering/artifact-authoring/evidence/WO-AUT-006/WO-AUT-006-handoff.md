```toml
artifact = "WO-AUT-006"
checkpoint = "handoff"
formal_snapshot_sha256 = "8d6ec494906b8abf3d438d25bfb2bc691999ad5412e216d5d64537599555df81"
rebound_at = "2026-09-09T18:12:45Z"
```

# WO-AUT-006 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The four compatibility windows are closed and their codes are gone. A
`constrains` relation is an `E016` issue naming it retired, whatever the
architecture's status; an architecture without a decision assessment is
`missing` and reads `E014`; a header-less evidence packet is `not_assessable`
with `harnessctl evidence` named as the corrective; a quality-gates contract
on the retired v1 schema meets the loader's own error. `W014`, `W015`,
`W019` and `W-ECP-002` left `codes.py` and the index with no tombstone. The
two permanent branches carry a comment and the note carries their counts.
Four specifications say so by record. On this corpus the released 0.17.0
evaluator and the candidate read the same counts per code; no corpus
artifact, managed template or root managed byte changed.

## Evaluators

- Governing: released `se-harness 0.17.0` installed from the wheel file
  outside the checkout (`C:/Users/mathi/se-harness-eval-0170`), run `-I`,
  for `validate`, `doctor`, the review preflight, `evidence` and the
  handoff check.
- Candidate: this checkout, branch `wo/aut-006-close-the-windows` off
  `main` at `b11ea537`. Implementation commits `c0d06237` (the seven
  modules), `ce79ab08` (the tests and the shared fixture), `bb2e73a4` (the
  amendment records, the notes, the index); implementation head `bb2e73a4`.
- Scenarios: a scratch worktree at the implementation head, mutated one
  file at a time (`WO-AUT-006-verification.md`, "Acceptance scenarios").

## Rule-to-case map (SPEC-AUT-004)

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `AUT-WIN-001` | `architecture_traceability_state`: a `constrains` key is the issue "architecture relation 'constrains' is retired; declare addresses and conforms_to" | `test_the_retired_constrains_relation_is_refused_for_every_status`; scenario S1 |
| `AUT-WIN-002` | the four legacy states, `legacy_targets` and the `RELATION_TARGET_TYPES` entry are gone | `test_no_package_module_names_a_closed_branch`; `test_constrains_beside_typed_relations_is_still_refused` |
| `AUT-WIN-003` | `decision_assessment_state` returns `missing` for every architecture without the table | `test_completed_architecture_without_assessment_is_refused_like_any_other`; scenario S2 |
| `AUT-WIN-004` | `legacy_missing`, the `W014` branch and the legacy `E015` message gone; `E015` kept for `adr_required` without a deciding ADR | the same test; `test_dashboard_snapshot_reports_adr_coverage` (E015 still raised); `test_no_architecture_status_is_exempt_from_the_assessment` |
| `AUT-WIN-005` | the preflight reads the `typed` state alone; no `W019` | `test_completed_architecture_without_assessment_is_refused_like_any_other`; scenario S2's preflight |
| `AUT-WIN-006` | `TEMPORAL_REASSESSMENT_RELATIONS["architecture"]` is the typed pair; no `legacy_adr_*` state | `test_the_architecture_relation_set_holds_the_typed_pair_only`; `test_no_legacy_assessment_state_is_produced`; `test_temporal_reassessment_supports_only_governed_declared_dependencies` |
| `AUT-WIN-007` | `review_evidence` reads the header only; a header-less packet is `not_assessable` naming `harnessctl evidence` | `test_the_predicate_reads_the_header_never_substrings_and_refuses_a_header_less_packet`; `test_without_a_packet_nothing_is_created_and_a_headerless_packet_is_not_rewritten` |
| `AUT-WIN-008` | the substring fallback and `W_ECP_002` gone | the same tests; `test_no_package_module_names_a_closed_branch` |
| `AUT-WIN-009` | `load_quality_gate_contract` returns `_load(...)`; `RETIRED_QUALITY_GATES_SCHEMAS` gone | `test_a_v1_contract_meets_the_loaders_own_schema_error`; `test_a_retired_gate_contract_meets_the_loaders_own_schema_error`; scenario S4 |
| `AUT-WIN-010` | `WEX-ECP-030` unchanged for binding faults | `test_an_unbound_lifecycle_edge_fails_contract_loading`; `test_the_loader_carries_no_retired_schema_set` |
| `AUT-WIN-011` | the four codes gone from `codes.py` and the index | `test_the_retired_codes_left_the_registry_and_the_kept_ones_stayed`; `test_the_index_page_names_no_retired_code_and_matches_the_source` |
| `AUT-WIN-012` | comments at both branches; "Permanent branches" in `docs/notes/artifact-authoring.md` with 84 of 230 and 111 of 261 | inspection; the verification file |
| `AUT-WIN-013` | amendment records on `SPEC-ECP-002`, `SPEC-ECP-005`, `SPEC-ECP-017`, `SPEC-WEX-002`; `updated` 2026-09-09; rule text verbatim | inspection; `validate` 0 errors with them |
| `AUT-WIN-014` | the reference note's grace sentence replaced; the index regenerated and `--check` passing | inspection; `test_the_index_page_names_no_retired_code_and_matches_the_source` |
| `AUT-WIN-015` | `tests/test_compatibility_windows.py` and the rewritten pins in six modules | the module and the suite |
| `AUT-WIN-016` | released 0.17.0 and candidate both 1,450 / 0 / 46 `W013` / 0 on the same tree | the verification file, "Baseline and candidate" |
| `AUT-WIN-017` | 24 changed paths: the seven modules, nine test files, three notes, four specifications, the work order, this packet | the handoff check's `QGP-G4I-PATHS`; the ledger below |
| `AUT-WIN-018` | no template, root managed byte or corpus artifact in the diff; `TRC-008` owed | `git diff --quiet b11ea537` over the managed set and `templates/` |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate . --advisories` | exact 0.17.0, Windows | PASS, 1,450 artifacts, 0 errors, 46 `W013`, 0 advisories |
| `validate . --advisories` | candidate | the same, per code |
| `doctor .` | exact 0.17.0 | exit 0, 99 `PASS` |
| `preflight . --work-order WO-AUT-006 --phase review` | exact 0.17.0 | PASS |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS, 14 records |
| `python scripts/run_tests.py --workers 4` | candidate, Windows 11 (local control) | 1,126 tests, 99 s, 0 failures, 1 error (the documented `WinError 5` baseline), 23 skips |
| discovered tests, base `b11ea537` vs candidate | `unittest` discovery | 1,119 vs 1,126 |
| the scenarios | scratch worktree at `bb2e73a4` | S1 `E016`, S2 `E014` and no `W019`, S4 the loader's own error, S5 the traceability test fails naming the missing `E016`; S3 at the bound commit |
| `check --checkpoint handoff --from-git be8fd8a5` (`main`'s tip after the merge of 2026-09-09) | exact 0.17.0 | the retained `handoff.json` beside this file |
| lanes at the implementation head `bb2e73a4` (PR #431) | GitHub | Candidate Evidence 34386523765, Publication Rehearsal 34386524653, Predecessor Evaluator Assessment 34386523764, CodeQL 34386520900: success; Engineering Harness 34386523767: failure on the scope check, `WEX201: changed path is outside execution scope: se_harness/engine/validation_lifecycle.py` — the module the `prepared_at` comment of `AUT-WIN-012` lives in, which the approved scope omitted; remedied by the owner's scope amendment of 2026-09-09 (below), so the lanes at the packet head, the completion commit and the record head are quoted in the lifecycle events |

## Change set

Against `main` at `b11ea537`, before this packet: 24 files.

| Path | + | − | What |
| --- | ---: | ---: | --- |
| `se_harness/engine/validation_architecture.py` | 7 | 56 | the retired relation as an issue; the legacy states, `legacy_targets`, the `W015` block and the table entry gone |
| `se_harness/engine/validation_decisions.py` | 9 | 28 | `missing` for every architecture; the `W014` block gone; the permanent-branch comment |
| `se_harness/preflight.py` | 3 | 24 | the `typed` state alone; `W019` gone |
| `se_harness/workflow_predicates.py` | 11 | 27 | the header-only predicate |
| `se_harness/workflow_contract.py` | 3 | 14 | the loader without the v1 hint |
| `se_harness/engine/dashboard_snapshot.py` | 2 | 4 | the typed pair; the legacy states gone |
| `se_harness/engine/validation_lifecycle.py` | 3 | 0 | the permanent-branch comment |
| `se_harness/codes.py` | 0 | 6 | four codes gone |
| `tests/test_compatibility_windows.py` | 137 | 0 | new |
| `tests/artifact_support.py` | 22 | 2 | the typed fixture architectures |
| `tests/test_architecture_traceability.py` | 33 | 31 | the refusal pins |
| `tests/test_workflow_compliance.py` | 27 | 19 | the header-less packet; the header-bound fixtures; the re-pinned digest |
| `tests/test_workflow_execution.py` | 20 | 7 | the header-writing binder; the loader test |
| `tests/test_adr_applicability.py` | 14 | 7 | `E014`, no `W019`; every status |
| `tests/test_validation_taxonomy.py` | 2 | 2 | the sample code |
| `tests/test_dashboard_webui.py` | 1 | 1 | the typed pair |
| `docs/notes/artifact-authoring.md` | 14 | 0 | "Permanent branches" |
| `docs/notes/diagnostic-codes.md` | 7 | 11 | regenerated |
| `docs/notes/harnessctl-reference.md` | 3 | 3 | the grace sentence |
| `docs/engineering/execution-control-plane/specifications/SPEC-ECP-002.md` | 12 | 1 | amendment record; `updated` |
| `docs/engineering/execution-control-plane/specifications/SPEC-ECP-005.md` | 11 | 1 | amendment record; `updated` |
| `docs/engineering/execution-control-plane/specifications/SPEC-ECP-017.md` | 11 | 1 | amendment record; `updated` |
| `docs/engineering/workflow-execution/specifications/SPEC-WEX-002.md` | 11 | 1 | amendment record; `updated` |
| `docs/engineering/artifact-authoring/work-orders/WO-AUT-006.md` | 8 | 1 | the start event |

Plus this packet: `WO-AUT-006-verification.md`, this file and `handoff.json`.

## Disclosures

The six disclosures of `WO-AUT-006-verification.md` stand: the shared
fixture corpus had to take the typed shape, which widened the test change to
nine files and moved a pinned digest; the `not_assessable` message gained a
sentence; the first predicate rewrite crashed on header-less files before
63 tests caught it; scenario S2 ran on an approved architecture and is
repeated on an implemented one at the bound commit; a validator message
lost its "new or ongoing" qualifier; and the `TRC-008` template sentence is
owed to the next managed-template work order by the owner's choice.
