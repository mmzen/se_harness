# WO-ECP-005 implementation and verification evidence

Work-order-keyed evidence for `WO-ECP-005` (`REQ-ECP-010`; issue #212, steps
1, 2 and 4). Retained under `VER-ECP-005`, the rows that name `REQ-ECP-010`.
Readings taken on 2026-08-28 on Linux (CPython 3.12.13, Git 2.52.0) from
branch `governance/ecp-005-one-result-schema`, based on `main` at `fe9443b`
(#238 merged: the amended packet, the ECP definitions and this work order
approved) plus the start commit `8098a2d`. Windows figures come from the
hosted lanes, section 8.

## 1. Changed paths

| Path | Change |
| --- | --- |
| `se_harness/workflow.py` | `SCHEMA = 1`, `_handoff`, `_result`, `render_json`, `_render_value`, `render_human`, `_contract_match`, `_format_contract_value` and `_recommend` deleted (−284 lines net); `focus`, `plan_transition` and `preparation_result` build through `workflow_compliance.selected_result`; `failed_result` builds through `remediation_result`; the plan outcome is `completed` (schema 2 has no `planned`), with `done` stating that no file was written |
| `se_harness/workflow_result.py` | `legacy_to_schema2` deleted |
| `se_harness/workflow_compliance.py` | `selected_result` (one selector, one context builder, one result path for `focus`, `transition`, `capture-verification`, `prepare-release`) and `remediation_result` added; `focus_schema2` kept as a name for `delegated_workflow.py` and delegates to `workflow.focus`, so the validator runs once (issue #212 change 4) |
| `se_harness/workflow_contract.json`, `templates/…/WORKFLOW.json` | `handoff_fields` removed; each rule's and the failure rule's `handoff` block replaced by `restitution` carrying only `done` and `current_lifecycle_state` (textual, format-preserving edit: +16/−257); both copies byte-identical |
| `se_harness/workflow_contract.py` | loader: `handoff_fields` no longer a top-level field; every rule must declare `restitution` with exactly `done` and `current_lifecycle_state` string arrays (`RULE_RESTITUTION_FIELDS`) |
| `se_harness/cli.py` | `--result-schema` removed from `focus`, `transition`, `capture-verification`, `prepare-release` (passing it is an argument error); schema-1 renderers and `legacy_to_schema2` imports removed; `_focus` calls `focus`; `_transition` exits 0 only on `completed` |
| `templates/…/WORKFLOW.md`, `docs/notes/harnessctl-reference.md` | the handoff procedure and the reference no longer mention `--result-schema` |
| `SPEC-ADS-001`, `REQ-ADS-002`, `SPEC-WEX-002` | dated retirement amendments in the form `WO-REB-028` used |
| `SPEC-CIP-001` | the `[--result-schema 2]` that named an option `release-unit` never had is corrected |
| `tests/test_workflow_execution.py`, `tests/test_workflow_documentation_contract.py`, `tests/fixtures/workflow_execution/scenarios.json` | schema-1 assertions retargeted; three tests added (section 4) |

Not changed: `QUALITY_GATES.*`, `_validate_preconditions`, `ensure_governed_checkpoint`,
`OPERATING_CARD.md` (its contract rendering is byte-identical before and after),
the root managed `docs/engineering/WORKFLOW.json` and `WORKFLOW.md` (hash-locked
0.7.1 copies), every lifecycle edge and decision right, `result_sha256`'s
definition.

## 2. What the one result path preserves

The rule prose that schema 2 always rendered (`done`, `current_lifecycle_state`)
came from the schema-1 `handoff.completed` and `handoff.current_lifecycle_state`
templates; those two lists are what each rule now carries as `restitution`.
Everything else in the old block (`recommended_next_step`,
`human_decision_or_approval_required`, `command_or_suggested_response`,
`alternative_next_steps`) was already superseded by the bound procedure step.
The rendered block of `focus` is therefore byte-identical to what the released
0.7.1 evaluator's `focus --result-schema 2` produced.

Golden reading (issue #212, acceptance criterion 3): on the workflow test
fixture (`standard_repository` + `create_base_chain`, `WO-001` implemented),
exact public 0.7.1 outside the checkout, `focus --artifact WO-001 --json`,
`result_sha256 = d22f5e481f7b59ff444b2d6812dbacc566a2a8092e1fb522dad61f053aaa0b1f`.
The candidate reproduces that digest; `test_focus_digest_equals_the_released_evaluator_golden` pins it.

## 3. Behaviour readings (candidate, fixture repository)

| Command | Reading |
| --- | --- |
| `focus --artifact WO-001 --json` | `se-harness-workflow-result-v2`, `completed`, `result_sha256 d22f5e48…` |
| `focus … --result-schema 1` / `2` | `harnessctl: error: unrecognized arguments: --result-schema …`, exit 2, nothing on stdout |
| `focus --artifact INT-001` | `Blocked.` / `WEX101: focus accepts only WO, VREC, or RLS artifacts`, next `PROC-REMEDIATE` |
| `transition --set WO-001=verified … --json` (blocked) | schema 2, `blocked`, `blocked_by` `WEX201: work order WO-001 has no direct eligible verification record` |
| `transition` plan (read-only) | schema 2, `completed`, `done` `Planned 1 explicit lifecycle transition(s); no files were written.`, next step identical to `focus` on the resulting state |
| `harness-orient` | unaffected: it adds `--result-schema 2` only when `focus --help` advertises it, and `focus --help` no longer does (0 occurrences) |

## 4. Tests

Retargeted in `tests/test_workflow_execution.py`: every `--result-schema 1`
invocation (14) and every `result["handoff"]` assertion now reads the
schema-2 `restitution`; `planned`/`failed` outcomes read `completed`/`blocked`;
the scenario fixture carries `expected.restitution` and the schema-2 `scope`.
`tests/test_workflow_documentation_contract.py`: `handoff_fields` asserted
absent; each rule and the failure rule must carry exactly `done` and
`current_lifecycle_state` under `restitution`.

Added:

- `test_focus_emits_schema_two_only_and_refuses_the_retired_option` (VER-ECP-005 scenario 3, both values);
- `test_every_workflow_command_refuses_the_retired_result_schema_option` (`focus`, `transition`, `capture-verification`, `prepare-release`);
- `test_focus_digest_equals_the_released_evaluator_golden` (criterion 3);
- `test_transition_and_focus_agree_on_the_next_step_for_the_resulting_state` (`ECP-KRN-003`: plan `next` and `current_lifecycle_state` equal `focus` on the resulting state);
- `test_focus_rejects_a_non_primary_artifact_type` now also asserts the remediation procedure.

`python -m unittest tests.test_workflow_execution tests.test_workflow_documentation_contract tests.test_lifecycle_state_contract tests.test_harnessctl`: OK (130 tests).
Full suite `python scripts/run_tests.py`: 968 tests, 1 failure, 4 skipped; the
failure is `test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`,
a file-mode artefact of this Linux checkout that fails identically at `main`
here and passes on the hosted runner (`WO-AUT-003`, `WO-HBI-005` evidence).

## 5. Released evaluator readings

Exact public `se-harness==0.7.1` outside the checkout, run with `-I`:
`validate` 1058 artifacts, 0 errors, 471 warnings; `doctor` 0 FAIL;
`preflight --work-order WO-ECP-005 --phase review` PASS; `check --checkpoint handoff` in section 7.
Repository-required: `validate_release_distributions.py` PASS (4 records); `python -m se_harness --help` exit 0.
Parity: `se_harness/workflow_contract.json` and the template `WORKFLOW.json` are byte-identical; `render_operating_card()` equals the template `OPERATING_CARD.md`.

## 6. Disclosures

1. The root managed `docs/engineering/WORKFLOW.json` still carries the
   `handoff` blocks: it is the hash-locked released 0.7.1 copy and changes only
   when the root evaluator advances. The released evaluator loads its own
   packaged contract, so this repository's own verdicts are unaffected.
2. `focus_schema2` is retained as a name (one line delegating to `focus`) for
   `delegated_workflow.py`; renaming that caller is Phase 4 territory
   (`WO-ECP-006`).
3. The remaining `result_schema` identifiers under `se_harness/` are keys of
   unrelated contracts (`agent_contract`'s `result_schemas`, `skill_contract`'s
   and `governance_migration_contract`'s `result_schema`), not the retired option.
4. The three retired transition failure labels of `ECP-KRN-008` are not yet
   split by check: `_repository_workflow_error` still classifies by message,
   and `transition` refusals still carry `WEX201`; the SPEC assigns that to
   this work order "as far as the checks that exist before `WO-ECP-009`
   allow", and every refusal today is a `HarnessError` string with no typed
   predicate to name. Deferred to `WO-ECP-009`, where the predicates exist.
5. Windows readings are the hosted lanes'.
6. The first JSON rewrite of the contract re-serialized the file and produced
   a 300-line diff; it was replaced by a textual edit that keeps the original
   line formatting, which the lifecycle-contract test also depends on.

## 7. Handoff checkpoint binding

artifact: WO-ECP-005
checkpoint: handoff
formal_snapshot_sha256: 42d88f64c12ccdaf41699513607dd148ec447ac54d13c3dd77b30259152f7434

Rerun: completed pass 839eb402a1f2215898a0a66cc4e867b69deaff7afae7c6a70101c2245fa693a5

## 8. Hosted lanes

At head `f054a66` of #239, all thirteen checks pass: `candidate-evidence.yml`
run `33171169241` (candidate source, candidate package, deterministic
integration package, governance migration on Linux and Windows, integration
package verified on Linux and Windows, retained), `publication-rehearsal.yml`
run `33171169575` (record selection, candidate replay, release-record replay),
`validate` run `33171169324`, governor transition assessment run
`33171169339`. The Windows legs are the Windows criterion of `VER-ECP-005`'s
`REQ-ECP-010` rows: the hosted suite runs the retargeted workflow tests and
the golden-digest test on both platforms.
