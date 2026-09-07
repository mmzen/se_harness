# WO-RSK-010 verification evidence

Retained under `VER-RSK-010` for the risk artifact, its raise and the decision
pairing. Measurements were taken on Windows 11 at candidate revision `b6843d8`
on branch `wo/rsk-010-risk-artifact`, whose base is `main` at `008c7b9`. The
governing evaluator is released 0.16.0 in `C:/Users/mathi/se-harness-eval-0160`,
run with `-I` from outside the checkout; an in-tree run of the candidate is a
control and never the record. The Linux readings of the hosted lanes are added
below when the pull request's runs complete; the hosted lane is the record for
the test suite, and the local Windows run is its control.

## Authorization

- 2026-09-07: the owner approved the packet and `WO-RSK-010` by selecting the
  presented options; the approval was the delegating act under `DR-015`.
- 2026-09-07: `DR-WO-START` was applied by the `delegated-executor` role while
  the required check `validate` read `success` at `008c7b98…` (check-run
  `101864362911`, source `github-checks`).
- 2026-09-07: two scope amendments under `DR-REMEDIATION-SCOPE`, each by the
  owner selecting the presented option, are recorded in the work order's
  Amendment record: the kernel's closed family set, the edge bindings, the
  transition writer and the diagnostic-code registry; then two pinning tests.

## Rule-to-case citation map

Every case is in `tests/test_risk_management.py` unless a module is named.
The rules assigned to this work order are RSK-MGT-001 to RSK-MGT-021,
RSK-MGT-026, RSK-MGT-027, RSK-MGT-031, RSK-MGT-033, RSK-MGT-034 and
RSK-MGT-036.

| Rule | Covering case |
| --- | --- |
| RSK-MGT-001 | `RiskArtifactTests.test_layout_registry_templates_and_policy_route_the_risk_type` |
| RSK-MGT-002 | `RiskArtifactTests.test_each_missing_field_draws_e_rsk_001_naming_it_and_no_other_code` |
| RSK-MGT-003 | `RiskArtifactTests.test_measurement_boundaries_draw_e_rsk_002_naming_the_field`; `RaiseTests.test_every_in_range_pair_stores_its_product` |
| RSK-MGT-004 | `RiskArtifactTests.test_stage_category_one_sentence_and_no_decision_field` |
| RSK-MGT-005 | the same case |
| RSK-MGT-006 | the same case |
| RSK-MGT-007 | `RiskArtifactTests.test_the_workflow_contract_declares_the_family_with_exactly_the_state_model`; `tests/test_lifecycle_state_contract.py` (`EXPECTED["risk"]`) |
| RSK-MGT-008 | the same two cases (no state grants authority; four terminal states) |
| RSK-MGT-009 | `RaiseTests.test_raise_risk_writes_one_raised_file_with_the_hand_computed_score_and_refuses_out_of_range` |
| RSK-MGT-010 | the same case (out of range, and an identifier declared already); `SecurityTests.test_a_crafted_identifier_is_refused` |
| RSK-MGT-011 | `RaiseTests.test_no_configuration_key_governs_the_raise` |
| RSK-MGT-012 | `BorrowedStopTests.test_a_raised_risk_needs_exactly_one_pending_decision_whose_blocks_equal_its_threatens` |
| RSK-MGT-013 | the same case (`E-RSK-004` names both sets) |
| RSK-MGT-014 | `BorrowedStopTests.test_no_predicate_or_gate_group_is_added_and_the_risk_edges_bind_none`; `BorrowedStopTests.test_the_paired_decision_stops_the_work_order_naming_the_decision_and_not_the_risk` |
| RSK-MGT-015 | `BorrowedStopTests.test_the_paired_decision_stops_the_work_order_naming_the_decision_and_not_the_risk` (the three options, `blocks` equal to `--threatens`) |
| RSK-MGT-016 | `DisposalTests.test_disposing_the_decision_moves_the_risk_in_the_same_act_for_each_option` |
| RSK-MGT-017 | `DisposalTests.test_a_deferral_leaves_the_risk_raised_and_admits_only_the_scoped_transition` |
| RSK-MGT-018 | `DisposalTests.test_a_hand_written_disposition_is_e_rsk_005`; `DisposalTests.test_only_the_transition_path_writes_a_disposition_and_the_decision_module_never_reads_risks` |
| RSK-MGT-019 | `DisposalTests.test_disposing_the_decision_moves_the_risk_in_the_same_act_for_each_option` (revisit copied); `DisposalTests.test_refused_answers_write_nothing`; `DisposalTests.test_a_past_revisit_on_an_accepted_risk_is_a_maintenance_warning_until_a_decision_concerns_it_again` |
| RSK-MGT-020 | `DisposalTests.test_disposing_the_decision_moves_the_risk_in_the_same_act_for_each_option` (`mitigated_by`, `avoided_by`); `DisposalTests.test_refused_answers_write_nothing` |
| RSK-MGT-021 | `DisposalTests.test_a_bare_transition_never_raises_or_answers_a_risk_but_withdraws_one_with_a_reason` |
| RSK-MGT-026 | `ScopeAdmissionTests.test_an_added_risk_file_of_the_work_orders_domain_is_admitted_and_only_that_file` |
| RSK-MGT-027 | `ScopeAdmissionTests.test_an_unrelated_added_file_and_a_modified_or_deleted_risk_file_still_need_a_declared_path`; `ScopeAdmissionTests.test_another_domains_risk_and_an_approved_work_order_are_not_admitted`; `ScopeAdmissionWithoutGitTests` |
| RSK-MGT-031 | `RiskArtifactTests.test_layout_registry_templates_and_policy_route_the_risk_type` (`TRC-REL-023` to `TRC-REL-025`, the catalog row, `TRC-016`) |
| RSK-MGT-033 | `BorrowedStopTests.test_risks_lists_the_threats_to_an_artifact_and_its_chain_and_writes_nothing` |
| RSK-MGT-034 | `DisposalTests.test_no_command_deletes_or_rewrites_a_terminal_risk` (second clause); the first clause names `renumber-artifacts`, retired on `main` by `WO-ECP-030` during this work, and is the subject of `DEC-RSK-001`, disposed `amend` |
| RSK-MGT-036 | the whole module run against `main`'s code, below |

### RSK-MGT-036: the cases fail on the code before the change

The module was copied into a clean worktree of `main` at `008c7b9` and run
there with `main`'s package on the path. `main` has no `se_harness.risks`, so
the module's one import of it was shimmed with the four fixture constants it
supplies (the measurement range, the option-to-state map, the option labels
and the product); nothing else changed. Reading: 31 cases ran; 30 failed or
errored (19 failing and 27 erroring sub-cases); 1 passed,
`ScopeAdmissionTests.test_another_domains_risk_and_an_approved_work_order_are_not_admitted`,
which asserts only refusals, and the code before the change refused every
undeclared path too. Its rule, RSK-MGT-027, is also carried by
`test_an_unrelated_added_file_and_a_modified_or_deleted_risk_file_still_need_a_declared_path`,
which fails before the change because it needs the admission of the added
file first. On the candidate all 31 pass.

## Verbatim refusal texts

The refusal a threatened work order receives when its handoff transition is
asked for, from the released evaluator's own result rendering in a fixture
repository (the two other predicates named are the fixture's, not the
risk's):

```text
QGP-G4I-DECISION: DEC-PRD-001 is open and blocks WO-001: How is the threat 'Config drift' (score 12) answered: accept, avoid or mitigate? Options: accept: Accept the threat; record a residual and a revisit trigger.; avoid: Avoid the threat by a design change recorded in an ADR or a decision.; mitigate: Mitigate the threat through a work order; the risk closes under verified coverage.. Decider: engineering-owner, owner. Next: harnessctl decide . --artifact DEC-PRD-001 --option OPTION-ID --decision ROLE --reason TEXT
```

The refusal names the decision, its three options and the deciding roles; it
does not name the risk.

A bare `transition` asked to answer a risk:

```text
WEX201: transition RISK-PRD-001: a risk is raised with harnessctl raise-risk and answered by disposing the decision that names it, with harnessctl decide . --artifact DEC-... --option accept|avoid|mitigate --decision ROLE --reason TEXT
```

A raise with a measurement outside the range, exit 2, nothing on standard
output and nothing written:

```text
harnessctl: likelihood must be an integer from 1 to 5, not 6
```

A `mitigate` answer without the work order that reduces the threat:

```text
WEX201: mitigating RISK-PRD-001 requires --mitigated-by WO-... naming the work order that reduces the threat
```

## Predicate identifier sets against `main`

Both quality-gates contract copies, `se_harness/quality_gates_contract.json`
and `templates/repository/standard/docs/engineering/QUALITY_GATES.json`, were
compared with `origin/main`'s copies by loading each and sorting the predicate
identifiers of every gate group.

| Copy | Predicate identifiers equal `main` | Count | Gate groups equal `main` | Count |
| --- | --- | --- | --- | --- |
| package | yes | 45 | yes | 11 |
| template | yes | 45 | yes | 11 |

The two copies are byte-identical. The `risk` family adds six transition
bindings, one per target state, each with `predicates = []` and
`structural = ["QGS-EDGE"]`; the kernel refuses to load a lifecycle edge
without a binding (`WEX-ECP-030`), which is why they exist.

## Configuration reading

`templates/repository/standard/.engineering-harness.toml.tpl` declares five
keys and no other table: `tool_version`, `installed_at`, `project_name` under
`[harness]`, and `required_for_verified_work`, `required_for_release` under
`[revision_provenance]`. No module under `se_harness/` reads a raise
threshold or an acceptance level; `tests/test_configuration_surface.py` passed
unchanged in the suite run below.

## Governing readings, Windows (control)

Released 0.16.0, `-I`, from outside the checkout, at `b6843d8`:

| Command | Reading |
| --- | --- |
| `validate .` | `Artifacts: 1384 \| Errors: 0 \| Warnings: 73 \| Advisories: 0` (the 73 warnings are `main`'s legacy `W013`/`W014`/`W015` set) |
| `preflight . --work-order WO-RSK-010 --phase review` | `PASS` |
| `check . --artifact WO-RSK-010 --checkpoint scope --from-git origin/main` | `QGP-G4I-SCOPE pass`, `QGP-G4I-COMPLETE pass`, `QGP-G4I-PATHS pass`; change set complete |
| `check . --artifact WO-RSK-010 --checkpoint handoff --from-git origin/main` | recorded in the handoff evidence beside this file |

Candidate, in-tree: `python -m se_harness --help` lists `raise-risk` and
`risks`; `python scripts/validate_release_distributions.py --root .` reads
`PASS (13 distribution-bearing records)`; `python -m se_harness doctor .`
reads the known `FAIL distribution:.engineering-harness.toml` of the pending
root adoption (`DST-CFG-015`), unrelated to this work.

Test suite, `python scripts/run_tests.py`: 1318 tests, 26 skipped (the
Windows-only guards), 2 failures, both present on a clean `main` worktree run
as the control and therefore not this work's:
`test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`
(6024 bytes under CRLF) and
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
(`PermissionError` removing read-only Git objects). `tests/test_risk_management.py`:
31 cases, 31 pass.

### After merging live `main`

`main` moved to `34193ca` (`WO-ECP-029`, the `adopt` alias removal) while the
work was in progress and was merged into the branch at `7d531be` with no
conflict. Re-measured there with the same evaluator: `validate .` reads
`Artifacts: 1385 | Errors: 0 | Warnings: 73 | Advisories: 0`; `preflight
--phase review` PASS; the scope and handoff checkpoints pass every predicate,
change set complete at 33 paths, and the handoff packet was rebound to the new
formal snapshot by the self-binding run. The suite reads 1317 tests (the merge
removed one `adopt` case), 26 skipped, and the same two control-confirmed
Windows failures; `tests/test_risk_management.py` 31 of 31.

### After merging live `main` a second time

`main` moved again to `edeb4f8` (`WO-ECP-030`: `renumber-artifacts`,
`rehearse-recovery`, the journal and the unreachable `QG-G0-INTENT` gate
retired) and was merged at `175ac62`, with conflicts resolved in
`se_harness/cli.py`, `tests/test_cli_shape.py`, `tests/test_validation_taxonomy.py`
and the regenerated `docs/notes/diagnostic-codes.md`. Two consequences were
handled explicitly. The renumber case of `tests/test_risk_management.py` drove
a retired command and was replaced by `test_no_command_deletes_or_rewrites_a_terminal_risk`.
`RSK-MGT-034`'s first clause names the retired command, so, as the work order's
stop condition requires, the deviation `DEC-RSK-001` was raised against
`SPEC-RSK-010#RSK-MGT-034`, blocking `WO-RSK-010`; the owner disposed it
`amend` by selecting the presented option, and the rule's text is repaired
under a later repair work order. Re-measured at that tree: the predicate
identifier sets of both quality-gates copies equal `main`'s, now 43
identifiers in 10 gate groups; `validate .` reads `Artifacts: 1387 | Errors: 0
| Warnings: 73 | Advisories: 0`; `preflight --phase review` PASS; the handoff
checkpoint passes every predicate with a complete change set of 34 paths; the
suite reads 1287 tests (the merge removed thirty retired cases), 26 skipped,
and the same two control-confirmed Windows failures; `tests/test_risk_management.py`
31 of 31.

### After merging live `main` a third time

`main` moved to `a6b9aed` (`WO-ECP-028`, the dead-code cleanup) and was merged
with one conflict, in `tests/test_fixture_support.py`, where the cleanup had
removed the installed-file-count pin this work amended; the removal stands. The
cleanup also deleted `BLOCKABLE_TYPES` from `se_harness/decisions.py` as unused
code, which `risks.py` imported, so `risks.py` now declares the six-type set of
`SPEC-DCM-001` rule 4 itself; `decisions.py` stays untouched by this work and
the validator's `E011` remains the enforcement. Re-measured: `validate .` reads
`Artifacts: 1388 | Errors: 0 | Warnings: 73 | Advisories: 0`; `preflight
--phase review` PASS; the scope and handoff checkpoints pass every predicate
with 33 paths; the predicate sets equal `main`'s at 43 in 10 groups; the suite
reads 1282 tests, 26 skipped, and the same two control-confirmed Windows
failures; `tests/test_risk_management.py` 31 of 31.

## Governing readings, Linux (record)

Added when the pull request's hosted lanes complete: the `validate` check-run
identifier and the candidate-evidence lane's suite reading.

## Findings for the accountable owner

1. The admission of RSK-MGT-026 covers the risk file alone, as the rule says.
   The decision that `raise-risk --with-decision` writes beside it is an
   added file too; a work order whose scope excludes its own domain directory
   must declare `docs/engineering/<domain>/decisions/` or raise without the
   flag. `VER-RSK-010` acceptance scenario 1 assumes the scope checkpoint
   passes for both files; every work order of this repository declares its
   domain directory, so the scenario holds here. Whether to widen the
   admission to the paired decision is a definition question, not this work
   order's to decide.
2. `renumber-artifacts` renumbers only artifacts in `draft`, `approved`,
   `in_progress` or `implemented` (`ELIGIBLE_STATUSES` in
   `se_harness/renumber.py`, outside this scope), so no risk state is
   renumberable. RSK-MGT-034 holds for prefix compatibility and for never
   rewriting a terminal risk; renumbering a live risk needs an eligibility
   amendment.
3. `mitigating -> mitigated` is a declared edge with no coverage guard until
   `WO-RSK-011` delivers RSK-MGT-022 to RSK-MGT-025; a bare `transition` can
   apply it today.
4. `SPEC-ECP-016` rule ECP-CLI-001 enumerates the repository commands and
   already lacked `decide`; it now also lacks `raise-risk` and `risks`. The
   test pins the parser, not the prose.
5. `E-RSK-003` tripped zero times during the work itself; the pairing rule's
   ergonomics stay unproven in operation, as `VER-RSK-010` records.
