# WO-TCM-005 verification evidence

Retained under `VER-TCM-003` for the reader-first requirement shape and the
retirement of the `Open decisions` section (`REQ-TCM-006`, `REQ-TCM-008`,
`SPEC-TCM-003` rules `TCM-RFR-001` to `TCM-RFR-006`). Measurements were
taken on Windows 11 on 2026-09-04 on the execution branch
`wo/tcm-005-execution` (PR #336) over base `cfa54b8` (origin/main), with
the released 0.14.0 evaluator in `C:/Users/mathi/se-harness-eval-0140` and
the candidate source of this checkout. Every figure is labelled with the
platform it was read on; the Linux reading is the pull request's managed
check.

## Authorization

- 2026-09-04: the repository owner approved `REQ-TCM-006`, `REQ-TCM-007`,
  `REQ-TCM-008`, `SPEC-TCM-003`, `VER-TCM-003`, `WO-TCM-005` and
  `WO-TCM-006` with the instruction "i approve the packet, the work orders
  can be start with execution delegation" (PR #335, merged by the owner as
  `cfa54b8`).
- 2026-09-04: the owner reviewed the overlap between `REQ-TCM-008` and
  `REQ-DCM-001` and kept the requirement as approved ("ok for option 1");
  the domain index records the accepted redundancy.
- Delegated `DR-WO-START` under the `[delegation]` class `execution`;
  required check `validate` success at `6762388` (check-run 101094604662).

## Change inventory (candidate source only)

- `templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md`:
  the reader-first body (`In plain words`, `Why`, `Behavior` table,
  `Examples` with `Normal` and `Failure`); the front matter unchanged; the
  statement comment asks for the concrete component and 30 words; the
  plain-words guidance points at `docs/notes/glossary.md` as a file the
  repository writes; no `Open decisions` section. No other definition
  template carried the section.
- `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`:
  the requirement checklist rewritten for the shape, the named actor, the
  budgets, the acceptance-condition rule (one Behavior row; cases in the
  verification contract; method in the specification) and the glossary
  pointer; the guidance paragraph on pending decisions; one bullet in the
  `decision` section stating that the templates carry no `Open decisions`
  section and how a legacy one is read.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `W-AUT-003` counts words (budget 30) instead of characters; `W-AUT-005`
  body over 250 words; `W-AUT-006` `Why` over 120 words or five sentences;
  `W-AUT-007` a body sentence over 25 words; `W-AUT-008` more than three
  code identifiers; `W-AUT-009` missing or long `In plain words`;
  `W-AUT-010` a `WHEN` whose event is the act of evaluating. Words are
  counted with code spans and fences removed; every message names the
  measured value and the budget; all fire on drafts only.
- `authoring_ready` in `se_harness/workflow_compliance.py` is unchanged: it
  already checks the section only where the heading exists, so the gate
  requires nothing new and refuses nothing new (`TCM-RFR-006`).
- `templates/repository/standard/scripts/generate_harness_dashboard.py`:
  `plain_words` projected from the `In plain words` section on requirement
  artifacts, absent when the section is absent.
- `repository_tools/explorer_design/build_explorer_template.py`:
  `READABILITY_PATCHES` render `plainWords` directly beneath the statement
  in the record panel; kept apart from `BASE_PATCHES` and
  `DECISION_PATCHES`. Template rebuilt: 433,614 bytes, SHA-256
  `019a5ab5a159686564f692f243e34bfe0bf9419330d71fc8414363452283e938`;
  `build_explorer_template --check` reports "matches its sources".
- `docs/engineering/decision-management/specifications/SPEC-DCM-001.md`:
  one amendment record dated 2026-09-04 under `WO-TCM-005` making rule 11's
  second sentence a legacy rule.
- Notes: `docs/notes/artifact-authoring.md` (the shape, the seven
  advisories, the legacy reading of the section),
  `docs/notes/harnessctl-reference.md` (`E-DCM-004` on a legacy section),
  `docs/notes/diagnostic-codes.md` regenerated (`W-AUT` now 10 codes;
  `--check` matches the source).
- Tests: `tests/test_reader_first_requirements.py` (new, 13 tests);
  `tests/test_artifact_authoring_policy.py` moved to the shape (word-based
  `W-AUT-003` case, `W-AUT-010` case, the plain-words advisory filtered on
  the title-only fixture, the template pins, the approval test with a
  legacy section appended and then removed);
  `tests/test_predecessor_bootstrap_retirement.py` ledger refreshed over the
  0.14.0 root copy (15 opcodes, +252 lines).

The root managed copies are untouched: `git diff --stat origin/main --
scripts/ docs/engineering/*.md docs/engineering/templates/
ENGINEERING_HARNESS.md .engineering-harness.toml .github/ AGENTS.md
CLAUDE.md` is empty. `git diff --check` is clean. Every changed path is
inside the work order's execution scope.

## Test evidence (Windows 11, candidate source)

- `python -m unittest tests.test_reader_first_requirements tests.test_predecessor_bootstrap_retirement`:
  31 tests, OK.
- `python -m unittest tests.test_artifact_authoring_policy tests.test_reader_first_requirements`:
  23 tests, OK.
- `python scripts/run_tests.py` (8 workers, final tree): `Ran 1220 tests
  in 96.315s (129 classes, 8 workers)`, `FAILED (errors=1, skipped=26)`:
  zero failures, the one baseline error named below, twenty-six
  Windows-only skips.

The one error is the pre-existing Windows baseline
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
(`PermissionError` deleting a temporary `.git` object; present on
`origin/main` before this work). The skips are the Windows-only guards.

## Released-evaluator evidence (Windows 11, 0.14.0, `-I`)

- `validate .`: PASS. Artifacts 1285, errors 0, warnings 69 (maintenance
  `W014`/`W015` legacy architecture warnings that predate this work),
  advisories 0.
- `doctor .`: 0 FAIL lines.
- `preflight . --work-order WO-TCM-005`: PASS, phase start, work order
  `in_progress`.

## VER-TCM-003 matrix, rows for REQ-TCM-006 and REQ-TCM-008

| Row | Evidence |
| --- | --- |
| `REQ-TCM-006` template | `test_every_definition_template_has_no_open_decisions_and_the_requirement_template_is_reader_first`: the four sections in order, `Normal` and `Failure`, the glossary pointer "which this repository writes", no `Open decisions` in any definition template, `create-artifact` writes the shape. `test_template_carries_the_reader_first_shape_and_five_shapes` pins the five EARS shapes, the Behavior header and the absence of the acceptance link. |
| `REQ-TCM-006` advisories | `test_a_reader_first_draft_within_every_budget_raises_no_advisory`; `test_each_budget_raises_exactly_its_advisory_with_the_measured_value` (one fixture per budget, each advisory alone with its measured value and budget; the 260-word body also trips the sentence budget by construction); `test_no_shape_advisory_fires_on_an_approved_requirement`; `test_validation_still_passes_with_advisories`. |
| `REQ-TCM-006` actor | `test_a_named_component_is_an_accepted_opener` (`THE VALIDATOR SHALL`, `WHEN x, THE INSTALLER SHALL`, no `W-AUT-001`). |
| `REQ-TCM-006` Explorer | `test_the_explorer_projects_plain_words_beneath_the_statement`: `plain_words` equals the section text, absent without the section; the built template renders `{{plainWords}}` after `{{statementNodes}}`. |
| `REQ-TCM-008` gate | `test_approval_needs_no_open_decisions_section_and_reads_the_graph`; `test_an_open_decision_blocks_approval_through_the_decision_predicate_only` (`QGP-G1-DECISION` names `DEC-001` and `decide`; the section's absence is not mentioned); `test_a_legacy_section_with_prose_is_still_refused` (`E-DCM-004`, then approval with `None`). The pre-existing `test_approval_is_refused_while_a_placeholder_or_an_open_decision_remains` now appends a legacy section and approves after removing it. |
| `REQ-TCM-008` amendment | `test_spec_dcm_001_carries_the_rule_11_amendment`; the record names `WO-TCM-005`, `TCM-RFR-006` and "legacy rule". |
| all: existing suite | the suite line above and the pull request's Linux lane. |

## Disclosures for the assurance decision

1. `W-AUT-009` fires on any draft whose body lacks an `In plain words`
   section, including title-only fixture stubs. The spec says "missing";
   the implementation follows it. The authoring-policy tests filter it on
   their stub fixture and say so.
2. The reading grade of `In plain words` is not measured mechanically, as
   `SPEC-TCM-003` leaves it; the two-sentence budget is the mechanical
   proxy.
3. `W-AUT-003` changed meaning from 300 characters to 30 words. The
   diagnostic-code index regenerates from the source and shows the new
   message; the code was kept rather than retired so the family stays
   contiguous.
4. Windows figures only. The Linux reading is the pull request's managed
   `validate` check on the head commit; the delegated completion cites it.
