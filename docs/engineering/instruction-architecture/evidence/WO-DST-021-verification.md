# WO-DST-021 implementation and verification evidence (REQ-IAR-021)

## Authority and candidate state

The repository owner approved the `DST-021`/`IAR-013` packet on 2026-08-21 and authorized implementation the same day. This file records the `VER-IAR-013` execution for `REQ-IAR-021`: the managed router revision and the withdrawal of the reference-step context-action form. The `VER-DST-021` execution for `REQ-DST-065` is recorded in `../../harness-distribution/evidence/WO-DST-021-verification.md`; product code, packaging, seed, lock, payload, test-suite, and validator figures are not duplicated here.

At evidence finalization the implementation is an uncommitted working-tree candidate. No commit, push, pull request, verification transition, release, tag, publication, or deployment was performed.

## Evaluator identity

```text
../se-harness-eval-1685/Scripts/python -I -m se_harness
se-harness 0.5.0
C:\Users\mathi\se-harness-eval-1685\Lib\site-packages\se_harness
```

`HRN-*` rule identifiers and the current `AGENTS.md.fragment` do not exist in released 0.5.0, so their recorded baseline is the candidate's own prior value, captured before the edit and asserted as module constants in `tests/test_context_routing_retirement.py` rather than in the released-baseline fixture. This is stated because `VER-IAR-013` asks for an independent baseline and no independent one exists for a candidate-only surface.

## Revised HRN-002

Before, the rule named the scaffolded document and made its completeness an obligation. After, in `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`:

```text
`HRN-002` - Repository facts and commands belong in the owner-controlled region
of `AGENTS.md`. That content is repository-owned and MUST NOT grant product,
engineering, assurance, release, or external-action authority. This harness does
not scaffold, track, or require it.
```

The rule was revised in place. No `HRN-*` identifier was renamed or renumbered.

## Ordered rule-identifier invariant

```text
before: HRN-001 HRN-002 HRN-003 HRN-004 HRN-005 HRN-006 HRN-007 HRN-008
after:  HRN-001 HRN-002 HRN-003 HRN-004 HRN-005 HRN-006 HRN-007 HRN-008
```

`test_router_rule_identifiers_keep_their_recorded_order` asserts the extracted sequence equals the recorded baseline exactly and contains no duplicate, so a reordering or an inserted rule fails.

## Routing table

Before, the last row read `` | Repository-specific facts and commands | `docs/engineering/REPOSITORY_CONTEXT.md` | ``. After:

```text
| Subject | Normative owner |
| --- | --- |
| Lifecycle states, transitions, procedures, next actions, and handoff fields | `docs/engineering/WORKFLOW.md` and its machine-readable `WORKFLOW.json` |
| Roles, accountabilities, delegation, and reserved decisions | `docs/engineering/DECISION_RIGHTS.md` |
| Gate criteria, executable predicates, validation planes, pass/fail behavior, and exceptions | `docs/engineering/QUALITY_GATES.md` and `docs/engineering/QUALITY_GATES.json` |
| Normative chain, artifact applicability, relation types, and coverage | `docs/engineering/TRACEABILITY.md` |
| Artifact authoring locations and templates | `docs/engineering/templates/README.md` |
| Repository-specific facts and commands | the owner-controlled region of `AGENTS.md` |
```

Six subjects before and six after; only the owner cell of the last row changed. `test_routing_table_gives_every_subject_exactly_one_owner` asserts the subject set equals the recorded baseline and that no subject appears twice, so the change neither dropped a subject nor created a second destination for one. `test_router_routes_repository_facts_to_the_owner_region_only` asserts the router contains neither `REPOSITORY_CONTEXT` nor the lowercase phrase anywhere, and no `CTX-ACT-` prefix.

## Stop conditions

Eight before, eight after. The repository-context condition was removed and no condition was added:

```text
- managed integrity fails;
- the formal graph is invalid;
- no phase-eligible selected work order exists;
- a required governing artifact or gate is missing;
- a required check fails;
- owner instructions conflict with this contract;
- remediation would exceed the selected work order; or
- the requested action lacks the decision right or explicit authority defined
  by the routed policies.
```

`test_router_stop_conditions_retain_the_baseline_without_repository_context` asserts every baseline condition is present and that the section contains none of `REPOSITORY_CONTEXT`, `repository context`, `context is incomplete`, or `context is missing`.

## Managed fragment unchanged

`templates/repository/standard/AGENTS.md.fragment` and `templates/repository/standard/CLAUDE.md.fragment` are untouched. The packaged fragment's tracked block digest is asserted against the recorded constant `bed4eb168f7a2249eebbb8eb415bb2ce4b8791a1eada2736a900fc93c6ee0e93` by `test_packaged_fragment_block_matches_the_recorded_baseline`, and a second test asserts the installed fragment's digest equals its lock entry, so the single managed destination is proven identical from both directions.

The installed repository's own fragment digests are unchanged in both directions: `.gitignore` `1b9c8af1…`, `AGENTS.md` `bcf46d13…`, `CLAUDE.md` `a5d3b023…`. No owner-region content requirement was added to a tracked block.

## Owner-region non-interference

`test_owner_region_content_changes_no_digest_or_diagnostic` writes four owner-region probes into an installed `AGENTS.md` outside the markers and shows the tracked digest is unchanged in every case:

```text
- Test: python -m unittest
<!-- CTX-ACT-REPOSITORY-CHECKS -->
- Repository purpose: TODO[purpose]
## Local notes

TODO[unresolved]
200 repeated lines
```

The second probe matters most: text that would have been a machine-readable context-action marker, and an unresolved placeholder that would have tripped the retired readiness gate, are now inert owner content. The harness neither parses nor hashes them.

## Withdrawn action form

Released 0.5.0 ships no `se_harness.workflow_procedures`, `se_harness.workflow_contract`, or `se_harness.workflow_compliance` module, so the resolver and contract validator are candidate-only and no released consumer is affected. Both the packaged contract and the candidate template contract contain 17 procedures with 9 `command` and 14 `decision` steps and no `reference` step at all, so the withdrawn branch was unreachable in the shipped product rather than merely unused.

The rejection diagnostic and the resolved-procedure corpus digests are recorded in the harness-distribution evidence file.

## No product code path reads the retired path

`test_no_product_code_path_reads_the_retired_path` scans every module under `se_harness/` and asserts none contains `REPOSITORY_CONTEXT`, the `CTX-ACT-` prefix, `repository_commands`, or `repository_context`, so the withdrawal is a code-level property and not only a template-text property.

## Governed artifacts revised in this domain

`REQ-IAR-005` set to `superseded`. `REQ-IAR-003` example narrowed to `docs/engineering/README.md` alone, status unchanged. `SPEC-IAR-001`, `ARCH-IAR-001`, and `OPS-IAR-001` descriptive references revised; `REQ-IAR-005` removed from the `assures` relation of `OPS-IAR-001`, which measurement had shown to be the only validator consequence of the supersessions.

`docs/engineering/instruction-architecture/README.md` records the packet, and `acceptance/instruction-architecture.feature` gained one scenario:

```text
  Scenario: Repository facts route to the owner-controlled region
    Given a repository with the standard harness installed
    When an engineering agent needs the repository test command
    Then the managed router names the owner-controlled region of AGENTS.md
    And no scaffolded context document is named anywhere in the router
    And no stop condition depends on repository-context presence or completeness
    And a reference step declaring the withdrawn action identifier fails conformance
```

## Residue outside the authorized envelope

Five active artifacts in this domain and its neighbours still describe the withdrawn obligation in lowercase prose and were left unmodified because revising them is outside the authorized envelope: `REQ-IAR-006` (preflight output lists the repository-context path and the repository commands), `ADR-IAR-001` (records preserving repository context as an owner-owned seed), `INT-IAR-001` (readiness blocks on invalid repository context), `SPEC-WEX-002`, and `VER-WEX-002`. `CAP-IAR-001`, `REQ-IAR-001`, and `REQ-WEX-007` were assessed and remain accurate. The full itemization, including the harness-distribution artifacts, is in the companion evidence file. `REQ-IAR-006` is an implemented requirement whose acceptance criterion this change contradicts and is the strongest candidate for a follow-on supersession.

## Verification results

Validator: 0 errors, 44 warnings, 605 artifacts, PASS. Full suite: 403 tests, 2 known environment conditions, 5 skips. Released-evaluator `preflight` PASS for `start` and `review` while the work order was `approved`; `doctor` exit 0 with 81 PASS, 0 FAIL, 15 pre-existing maintenance warnings. New focused modules: `tests/test_context_routing_retirement.py` 11 tests OK, `tests/test_repository_context_retirement.py` 11 tests OK.

## Lifecycle transitions at closeout

`REQ-IAR-021` and `SPEC-IAR-013` are `implemented`, as is `WO-DST-021` under the harness-distribution domain. `VER-IAR-013` stays `approved`: a verification contract is not advanced by the implementation it governs, and a verification transition is a separate accountable decision that was not performed. `REQ-IAR-005` was already `superseded`.

The validator, the suite, `doctor`, and all three fragment digests were re-measured after the transitions and are unchanged. Released-evaluator `review` preflight still passes; `start` now reports `W005` start-ineligibility for an `implemented` work order, which managed `WORKFLOW.md` specifies and which the companion evidence file records in full.

`docs/engineering/instruction-architecture/README.md` now records both packets under implemented headings with implemented requirement, specification, and work-order lines, and `VER-IAR-012` and `VER-IAR-013` as approved verification contracts.
