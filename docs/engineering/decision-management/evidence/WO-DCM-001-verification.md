# WO-DCM-001 verification evidence

Retained under `VER-DCM-001` for the decision artifact (`SPEC-DCM-001`).
Measurements were taken on Windows 11 on 2026-09-03 on the execution
branch `wo/dcm-001-execution` (PR #330) over base `56a34ea` (origin/main),
with the released 0.14.0 evaluator in `C:/Users/mathi/se-harness-eval-0140`
and the candidate source of this checkout. Every figure below is labelled
with the platform it was read on; the Linux reading is the pull request's
managed check.

## Authorization

- 2026-09-03: the repository owner instructed the creation of the packet
  after reviewing `docs/notes/decision-artifact-proposal-2026-09-03.md`, then
  approved `INT-DCM-001`, `CAP-DCM-001`, `REQ-DCM-001..003`, `SPEC-DCM-001`,
  `ARCH-DCM-001`, `ADR-DCM-001`, `VER-DCM-001` and `WO-DCM-001` with the
  instruction "i approve with execution delegation" (PR #329, merged by the
  owner).
- 2026-09-03T19:18:57Z: delegated `DR-WO-START` under the `[delegation]`
  class `execution`; required check `validate` success at
  `2f305c0b4fd5df9101f8efa46d269871d516dab7` (check-run 100781440327).
- The owner's standing instruction excludes the risk artifact from this
  work; nothing here touches it.

## Change inventory (candidate source only)

- `se_harness/decisions.py` (new): kinds, closed deviation options,
  blockable types, `against` parsing, deferral scope grammar
  `ARTIFACT-ID:FROM-TO`, deciding roles, disposition validation,
  `dispose_decision` through `plan_transition`.
- `se_harness/workflow.py`: `decision` is a primary type of `check`; a
  decision is projected over `concerns`, `blocks`, `produces` and `against`;
  `_set_disposition` writes the `[disposition]` table before the lifecycle
  events; a decision transition without a disposition is refused with the
  `harnessctl decide` corrective.
- `se_harness/workflow_compliance.py`: `blocking_decisions`,
  `decision_gate_clear`; the authoring gate reads `## Open decisions` with
  its inline code intact and accepts `None` or `DEC-` identifier lines
  (`E-DCM-004` otherwise); the checkpoint-only guard message names `decide`.
- `se_harness/workflow_contract.py`: evaluator `decision_gate_clear`; fifth
  lifecycle family `decision`.
- `se_harness/workflow_contract.json` and
  `templates/repository/standard/docs/engineering/WORKFLOW.json` (byte-identical):
  the `decision` lifecycle, `WFL-DEC-OPEN`, `WFL-DEC-CLOSED`,
  `PROC-DEC-DISPOSE`, `STEP-DEC-DISPOSE`, `DR-DECISION-DISPOSE` correctives
  on the gated command steps.
- `se_harness/quality_gates_contract.json` and
  `templates/repository/standard/docs/engineering/QUALITY_GATES.json`
  (byte-identical): `QGP-G1-DECISION`, `QGP-G2-DECISION`, `QGP-G3-DECISION`,
  `QGP-G4I-DECISION` (checkpoints pre-action, transition, handoff),
  `QGP-G4A-DECISION`, `QGP-G4V-DECISION`, `QGP-G5P-DECISION`,
  `QGP-G5D-DECISION`, each bound to its gate's transition checks; the
  decision family's structural bindings.
- `se_harness/cli.py`: `decide` (`--artifact`, `--option`, `--decision`,
  `--reason`, `--defer`, `--scope`, `--revisit`, `--withdraw`, `--apply`,
  `--json`); guard refusals exit 2, workflow refusals exit 1.
- `se_harness/artifact_layout.py` and
  `templates/repository/standard/scripts/artifact_layout_registry.py`:
  `decision` -> `decisions/`, `DEC-`, `DECISION.template.md`; reserved
  domain `decisions`; `create-artifact` writes a decision `open`.
- `se_harness/provenance.py`: `standing_deviations_for_work`; the VREC body
  gains `## Standing deviations` when any stand on the selected work.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  the fifth family; relation target types for `blocks` and `produces`;
  `validate_decisions` (`E-DCM-001..003`, `W-DCM-001..002`);
  `standing_deviations`.
- `templates/repository/standard/scripts/inspect_engineering_artifacts.py`:
  open and deferred decisions in the `decision_required` queue as
  `dispose-decision`.
- `templates/repository/standard/scripts/generate_harness_dashboard.py`:
  decision fields, `deciding_roles`, the decision trail on concerned
  artifacts, `standing_deviations` on the records that inherit them;
  compact entries carry `created`, `kind`, `deciding_roles`; metrics
  `decisions_open`, `decisions_decided`, `decision_dispose_times`.
- `repository_tools/explorer_design/build_explorer_template.py`:
  `DECISION_PATCHES` (in-flight tile with age and deciding role, record
  panel fields, decision trail, standing deviations), kept apart from
  `BASE_PATCHES` so a root released before them is compared exactly.
- `templates/repository/standard/scripts/harness_explorer/index.template.html`:
  rebuilt, 433,114 bytes, SHA-256
  `a941676b81dd2aebd5e8c6faeca83e01d9fdd80b3ac1256a3c6311196d734708`;
  `build_explorer_template --check` reports "matches its sources".
- Policy documents in the candidate templates: `TRACEABILITY.md`
  (`TRC-REL-020..022`, catalog row, `TRC-015`), `QUALITY_GATES.md`,
  `WORKFLOW.md`, `DECISION_RIGHTS.md` (`DR-DECISION-DISPOSE`),
  `ARTIFACT_AUTHORING.md` (`## decision`, Open decisions rule),
  `templates/README.md`, `templates/DECISION.template.md` (new).
- Notes: `docs/notes/decision-artifacts.md` (new, indexed),
  `harnessctl-reference.md` (`decide` row and section),
  `harnessctl-check.md` (`WFL-DEC-OPEN`, `WFL-DEC-CLOSED`).
- `SPEC-DCM-001`: one amendment record (predicate ids per gate).
- Tests: `tests/test_decision_management.py` (new, 29 tests) and declared
  candidate-versus-root exceptions in `test_artifact_authoring.py`,
  `test_artifact_catalog.py`, `test_validation_taxonomy.py`,
  `test_dashboard_webui.py`, `test_predecessor_bootstrap_retirement.py`
  (validator ledger, 11 opcodes, +175 lines), `test_fixture_support.py`
  (48 installed files), `test_cli_shape.py`, `test_workflow_execution.py`,
  `test_lifecycle_state_contract.py`.

The root managed copies are untouched: `git diff --stat origin/main --
scripts/ docs/engineering/*.md docs/engineering/templates/
ENGINEERING_HARNESS.md .engineering-harness.toml .github/ AGENTS.md
CLAUDE.md` is empty. `git diff --check` is clean.

## Test evidence (Windows 11, candidate source)

- `python scripts/run_tests.py` (8 workers): see the suite line below.
  The one error is the pre-existing Windows baseline
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
  (`PermissionError` deleting a temporary `.git` object; present on
  `origin/main` before this work). The skips are the Windows-only guards.
- `python -m unittest tests.test_decision_management`: 29 tests, OK.
- `python -m unittest tests.test_dashboard_webui tests.test_dashboard_publication`:
  54 tests, OK (1 skipped).

Suite line (final tree, Windows 11): `Ran 1206 tests in 85.927s (127
classes, 8 workers)`, `FAILED (errors=1, skipped=26)`: zero failures, the
one baseline error named above, twenty-six Windows-only skips. The same
tree read `1206 tests, errors=1, skipped=26` on the preceding run as well.

## Released-evaluator evidence (Windows 11, 0.14.0, `-I`)

- `validate .`: PASS. Artifacts 1275, errors 0, warnings 69 (all
  maintenance-plane `W014`/`W015` legacy architecture warnings that predate
  this work), advisories 0.
- `doctor .`: 0 FAIL lines; 40 `W013` location warnings on historical
  records, unchanged from `origin/main`.
- `preflight . --work-order WO-DCM-001`: PASS, phase start, work order
  `in_progress`, assurance `required` decided by `repository-owner`.
- `python -m se_harness --help`, `python -m se_harness decide --help`:
  exit 0. `python scripts/validate_release_distributions.py --root .`: PASS
  (11 distribution-bearing records).

## VER-DCM-001 matrix, row by row

| Row | Evidence |
| --- | --- |
| `REQ-DCM-001` fixture tests per blocked family | `DecisionGateFamilyTests.test_every_blockable_family_is_refused_and_nothing_is_written`: an open `DEC-001` blocking a draft requirement, specification, ADR, verification contract and an approved work order; each `transition --apply` exits 1 naming the gate's `QGP-G*-DECISION`, the decision, its question and `harnessctl decide`; every blocked file and the decision are byte-identical before and after. `DecisionManagementTests.test_an_open_decision_blocks_the_handoff_until_it_is_decided` (work order handoff, `QGP-G4I-DECISION` fail then pass). `test_a_deferral_needs_a_scope_and_a_revisit_and_admits_only_the_scoped_transition` (the scoped transition passes; `WO-001 -> verified` and `REQ-001 -> approved` still blocked). |
| `REQ-DCM-001` validator taxonomy | `test_a_well_formed_decision_validates_and_the_validator_names_each_defect` (`E-DCM-001`, `E-DCM-002`, `E-DCM-003` on each defect); `test_a_record_family_cannot_be_named_in_blocks` (`E011` on a record in `blocks`; an unknown target is a graph error). |
| `REQ-DCM-002` command tests | `test_disposition_is_refused_for_the_wrong_role_a_missing_reason_or_an_undeclared_option` (`DR-DECISION-DISPOSE` for the wrong role, `requires --reason`, `declares options keep, split`, the closed edge on a decided decision); the disposition carries option, label, role, time and verbatim reason (`test_an_open_decision_blocks_the_handoff_until_it_is_decided`); `test_withdrawal_records_a_disposition_and_closes_the_decision`; `test_a_decision_is_never_transitioned_by_hand`. |
| `REQ-DCM-002` contract tests | `test_contract_copies_carry_the_family_the_predicates_and_the_policy_rows`: both contract copies byte-identical to the package copies, the `decision` lifecycle, the eight predicates on `decision_gate_clear`, every gated transition binding of the other families carries its gate's decision predicate, `DR-DECISION-DISPOSE`, `TRC-REL-020..022`, the catalog row, `TRC-015`, `## decision`. `tests/test_lifecycle_state_contract.py` pins the decision states. |
| `REQ-DCM-003` fixture and Explorer tests | `test_an_accepted_deviation_is_time_bounded_and_stands_on_the_rule_the_work_and_its_records` (`accept` without `--revisit` refused; the wrong role refused; standing on `SPEC-001`, `WO-001`, then `VREC-001`; `W-DCM-002` on the second acceptance; `amend` closes the standing). `test_a_past_revisit_on_an_accepted_deviation_is_a_maintenance_warning` (`W-DCM-001` against a released `v1.0.0`; standing on `RLS-001`). `test_check_inspect_and_dashboard_surface_the_open_decision` (`deciding_roles`, `kind`, `decisions_open` in the bundle). `tests/test_dashboard_webui.py` metrics pins. |
| all: authoring and template tests | `test_layout_registry_and_template_route_the_decision_type` (`decisions/`, `DEC-`, `create-artifact --type decision` writes an `open` decision from the template with two options and the kind fields); `test_open_decisions_section_accepts_none_or_decision_ids_only` (`None`, a `DEC-` line, prose is `E-DCM-004`). |
| all: upgrade tests | Not executed as a live previous-release upgrade in this work order. The decision type, family, gate and template reach a consumer through the ordinary managed-file upgrade path, whose tests (`tests/test_harnessctl.py` upgrade cases) are unchanged and pass. The specific assertion "the upgrade adds the type, the family, the gate and the template" is left to the adoption work order, which runs the released 0.15.0 against this repository. Disclosed for the assurance decision. |
| Acceptance scenarios | Raise, block, defer with a scope, dispose, deviation refused for the work order's owner, Explorer bundle, full suite and released-evaluator validation: covered by the tests named above and the readings in this packet. |
| Property and invariant tests | No `--apply` on a blocked artifact changes a file (byte comparison in the family test); `build_explorer_metrics` counts and dispose times (`tests/test_dashboard_webui.py`, empty and populated snapshots); the refusal is deterministic (`test_the_refusal_is_deterministic`); a disposition without a lifecycle event is `E-DCM-003`. |
| Static and architecture checks | The root managed copies are unchanged (diff above). `test_only_the_transition_path_writes_a_disposition`: `workflow.py` is the only module that writes `[disposition]`; `decide` reaches it through `plan_transition` and the `transition-apply` mutation guard. `ARCH-DCM-001` conforms to `SPEC-DCM-001` as amended by record. |
| Security and privacy checks | `test_hostile_decision_text_stays_data`: a question carrying script tags and a `+++` sentinel validates, the bundle generates, the text is absent from `index.html` and present only as JSON data. The wrong-role and hand-written-disposition refusals are covered above. |
| Performance and resilience | The full suite runs in about 90 s on 8 workers, within the previous runs' range; the gate adds one linear pass over the catalog per predicate. No separate timing target was set. |

## Disclosures for the assurance decision

1. `SPEC-DCM-001` rule 5 names one predicate `QGP-DECISION-OPEN`; the
   quality-gates contract binds predicates per gate and requires unique
   ids, so the implementation registers one predicate per gate. Recorded as
   an amendment record on the specification, not as a silent rewrite.
2. `VER-DCM-001` row one lists "a verification record, a release record"
   among the blocked families, while `SPEC-DCM-001` rule 4 closes `blocks`
   to requirement, specification, verification, architecture, adr and
   work_order. The implementation follows the specification: a record is
   reached through the work it covers (standing deviations), never named in
   `blocks`; naming one is `E011`. The record gates carry their
   `QGP-G4A/G4V/G5P/G5D-DECISION` predicates for the deferred-scope and
   future cases. The verification contract's wording is left for the
   owner; it was not amended under this work order.
3. `repository_tools/diagnostic_code_index.py` is outside
   `WO-DCM-001`'s execution scope, so the `E-DCM` and `W-DCM` families are
   not yet listed in `docs/notes/diagnostic-codes.md`. The codes are
   documented in `docs/notes/decision-artifacts.md` and the command
   reference. Adding the two prefixes to the index generator is a
   one-line change for a later work order or an owner scope decision.
4. `decide-apply` was not added as a separate mutation-guard operation:
   the disposition is applied by the guarded `transition-apply` path.
5. Windows figures only. The Linux reading is the pull request's managed
   `validate` check on the head commit; the delegated completion cites it.
