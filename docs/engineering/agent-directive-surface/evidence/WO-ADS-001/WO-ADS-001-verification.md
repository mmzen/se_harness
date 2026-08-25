# WO-ADS-001 implementation evidence

artifact: WO-ADS-001
checkpoint: handoff
formal_snapshot_sha256: 46ebbb428945fb61b5c5e61200ff36740b0f33fd02766525fecd11bd5108be08

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
| `harnessctl preflight . --work-order WO-ADS-001 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 858 artifacts, 0 errors, 50 warnings (same 50 as before the packet) |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python scripts/validate_engineering_artifacts.py --root .` | candidate | PASS, 858 artifacts, 0 errors, 50 warnings |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (1 distribution-bearing record) |
| `python -m se_harness --help` | candidate | exit 0 |
| `git diff --check` | git | clean |
| `harnessctl check . --artifact WO-ADS-001 --checkpoint handoff --changed-path … --changes-complete --json` (complete set below) | released 0.6.0 and candidate | before this file existed: blocked only by `QGP-G4I-EVIDENCE`; both evaluators report formal snapshot `46ebbb428945fb61b5c5e61200ff36740b0f33fd02766525fecd11bd5108be08` |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11, CPython 3.14 | `Ran 991 tests in 321.199s` — `OK (skipped=23)`; the 23 skips are the Windows-only guards |
| Linux lane | `.github/workflows/candidate-evidence.yml` | not run locally; the pull-request run is the Linux figure |

## Complete changed-path set

```
AGENTS.md
README.md
docs/engineering/agent-directive-surface/evidence/WO-ADS-001/WO-ADS-001-verification.md
docs/notes/harnessctl-reference.md
pyproject.toml
se_harness/cli.py
se_harness/github_ci.py
se_harness/preflight.py
se_harness/workflow_compliance.py
se_harness/workflow_contract.json
se_harness/workflow_contract.py
se_harness/workflow_procedures.py
se_harness/workflow_result.py
templates/repository/standard/.github/PULL_REQUEST_TEMPLATE.md.seed
templates/repository/standard/.github/workflows/engineering-harness.yml
templates/repository/standard/ENGINEERING_HARNESS.md.tpl
templates/repository/standard/docs/engineering/OPERATING_CARD.md
templates/repository/standard/docs/engineering/WORKFLOW.json
templates/repository/standard/docs/engineering/WORKFLOW.md
templates/repository/standard/scripts/select_harness_work_order.py
tests/test_context_routing_retirement.py
tests/test_instruction_architecture.py
tests/test_workflow_execution.py
```

Every path is admitted by `[execution_scope].paths` of `WO-ADS-001`. Scoped
paths left untouched: `se_harness/workflow.py`, `se_harness/installer.py`,
`docs/engineering/README.md`, `docs/engineering/REPOSITORY_CONTEXT.md`,
`docs/notes/developing-se-harness.md`, `docs/notes/README.md`,
`tests/test_preflight.py`, `tests/test_github_ci.py`,
`tests/fixtures/agent_directive_surface/`.

## Requirement coverage

| Requirement | Implemented by | Test evidence |
| --- | --- | --- |
| `REQ-ADS-001` | `corrective` forms on the five gated command steps of `WORKFLOW.json` (template and packaged copy byte-identical); loader `WEX-ADS-001`; `corrective_response` in `workflow_procedures.py`; blocked rendering in `check_workflow` with a runtime self-loop guard | `AgentDirectiveSurfaceTests.test_every_gated_command_step_declares_one_distinct_corrective_per_predicate`, `…_contract_without_corrective_forms_fails_to_load_with_wex_ads_001`, `…_blocked_handoff_check_never_renders_its_own_command_as_the_retry` |
| `REQ-ADS-002` | `focus --result-schema` defaults to 2; schema 1 prints `WEX-ADS-002` on stderr; `focus_schema2` and `check_workflow` resolve rule and procedure through the same `select_rule` + `resolve_procedure` pair | `…_focus_defaults_to_schema_two_and_marks_schema_one_as_not_restitution`, `…_focus_and_check_resolve_the_same_next_step_for_one_state` |
| `REQ-ADS-003` | `render_operating_card` in `workflow_contract.py`; managed template `docs/engineering/OPERATING_CARD.md` (1791 bytes, limit 3072); card in `REQUIRED_PATHS` and second in `POLICY_PATHS`; router template reading instruction; wheel data-file entry | `…_operating_card_template_equals_its_contract_rendering_and_stays_bounded`, `AgentDirectiveSurfaceRouterTests.test_router_states_the_scope_of_its_obligations_after_the_invariants` |
| `REQ-ADS-004` | `carriage_return_trailer_offsets` and the `W-ADS-001` selection error in `github_ci.py` and the template selector; `check --pull-request-body`; `orphaned_ready_records` and `W-ADS-002` in review preflight and handoff check | `…_carriage_return_trailer_is_named_with_its_offset`, `…_handoff_check_reports_a_carriage_return_trailer_from_a_body_file`, `…_orphaned_ready_record_blocks_review_preflight_and_handoff`, `AgentDirectiveSurfaceRouterTests.test_review_preflight_reports_an_orphaned_ready_record_for_the_selected_work_order` |
| `REQ-ADS-005` | `result_sha256` and `canonical_block_bytes` in `workflow_result.py`; `select-work-order --field restitution-digest`; `Harness-Restitution:` in the pull-request template seed; recomputation step in the managed workflow template | `…_result_digest_binds_the_canonical_block_bytes`, `…_carriage_return_trailer_is_named_with_its_offset` (digest selection) |
| `REQ-ADS-006` | `## Scope of these obligations` in the router template | `AgentDirectiveSurfaceRouterTests.test_router_states_the_scope_of_its_obligations_after_the_invariants` |

## Material deviations from SPEC-ADS-001

Each is a conscious exception recorded for the assurance owner; none is hidden.

1. `ADS-RST-001` names two corrective kinds. A third kind, `response`, was
   needed for `QGP-G4I-EVIDENCE`: no `harnessctl` command writes evidence, and
   an escalation would misname a mechanical step as a decision. The renderer
   substitutes only the measured formal-snapshot digest into it.
2. `ADS-RST-002` says the corrective is rendered for "the first failing
   predicate"; when the blocking finding is a trap diagnostic (`W-ADS-001`,
   `W-ADS-002`) or a graph error with no failing predicate, the renderer
   escalates to `DR-REMEDIATION-SCOPE` instead.
3. `ADS-NXT-003` asks for byte-identical `Next` and `Command or response`
   between `focus` and `check`. `Next` procedure and step are identical; the
   command differs by design once `check` is blocked, because it then carries
   the corrective form. The test asserts the step identity.
4. `ADS-RDM-001` closes the manifest to router, card, chain, and owner file.
   The manifest still lists the routed policies: `tests/test_repository_context_retirement.py`,
   outside this work order's scope, binds the manifest prefix to `POLICY_PATHS`.
   The card is second in that prefix and the router names it as the read.
5. `ADS-RDM-002` says the installer renders the card. The card is a managed
   template file whose bytes a test proves equal to `render_operating_card()`;
   the installer copies it like every managed file. Same bytes, no installer change.
6. `ADS-DGN-003` calls the diagnostics warnings that leave exit status alone.
   Preflight has no warning tier and `check` has no observation slot, so both
   are reported as diagnostics/blockers, scoped to records that verify the
   selected work order so unrelated history cannot trip them.
7. `ADS-SCP-001` places the section before the invariants and quotes `HRN-003`.
   The router isolation tests require each rule ID to appear once and forbid
   command names in the router, so the section sits after the invariants,
   refers to "the bounded-scope invariant above", and names "work-readiness
   preflight" rather than the command.
8. Owner-region retirement of `docs/engineering/REPOSITORY_CONTEXT.md` did not
   happen: the released 0.6.0 lock still seeds and checks that path (its
   candidate preflight failed `QGP-G4I-PREFLIGHT` on the missing file), and the
   owner region is bounded to 6000 bytes. `AGENTS.md` now states accurately
   what the file carries and when it retires.

## Scenario 8 review

Not run in this increment: the blinded three-reviewer classification needs
reviewers the implementation actor cannot supply. The rendered paragraph and
its position are asserted mechanically; the assurance owner decides whether
the manual scenario is required before verification.
