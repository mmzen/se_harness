# WO-TCM-007 verification evidence

Retained under `VER-TCM-004` for the reader-first intent shape, the
operational success-measure rule and the Explorer's outcome line
(`REQ-TCM-009`, `REQ-TCM-010`, `REQ-TCM-011`; `SPEC-TCM-004` rules
`TCM-RFI-001` to `TCM-RFI-007`). Measurements were taken on Windows 11 on
2026-09-04 on the execution branch `wo/tcm-007-execution` (PR #341) over
base `1e2462b` (origin/main, the merge of PR #340), with the released
0.14.0 evaluator in `C:/Users/mathi/se-harness-eval-0140` and the candidate
source of this checkout. Every figure is labelled with the platform it was
read on; the Linux reading is the pull request's managed check.

## Authorization and decisions taken on the way

- 2026-09-04: the repository owner approved the packet with "i appprove
  the packet" (PR #340, merged as `1e2462b`). The packet was drafted on the
  three recommendations of the assessment
  `docs/notes/assessment-intent-readability-2026-09-04.md`: the outcome as
  a front-matter field, success measures observed in operation only,
  advisories first with blocking a later owner decision.
- Delegated `DR-WO-START` under the `[delegation]` class `execution`;
  required check `validate` success at `4afadac` (check-run 101150403167).
- No scope amendment and no pending decision. Every changed path is inside
  the seven declared prefixes; `se_harness/` was declared and not needed.

## Change inventory (candidate source only)

- `templates/repository/standard/docs/engineering/templates/INTENT.template.md`:
  the `outcome` field with its rule as a comment; the four sections
  `In plain words`, `Problem`, `Success measures` (columns `Measure`,
  `Today`, `When reached`, `Observed`) and `Not this`; the comment saying
  where the retired sections went (`TCM-RFI-001`).
- `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`:
  the intent checklist rewritten line by line with the mechanical
  counterpart named after each line, and the two guidance sentences on when
  a new intent is warranted and when a capability under the existing intent
  is enough (`TCM-RFI-005`). The requirement section is untouched.
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `_intent_authoring` and `_success_measure_rows`, the intent constants
  (outcome 30 words, body 200, Problem 120 words or five sentences, two
  code identifiers), the path and line-range patterns and the acceptance
  vocabulary. `outcome` present but empty or not a string is `E-AUT-002`
  on any status (`TCM-RFI-002`). On intent drafts only: `W-AUT-011`
  (outcome missing, over 30 words, or citing a code identifier),
  `W-AUT-012` (Problem budget), `W-AUT-015` (a repository path or source
  line range cited), `W-AUT-013` (one per success-measure row whose
  `Observed` cell contains a word of the acceptance vocabulary, naming the
  measure), `W-AUT-014` (the section exists and its table has no data row,
  or is malformed), and the shared `W-AUT-005`, `W-AUT-007`, `W-AUT-008`,
  `W-AUT-009` with the intent constants (`TCM-RFI-003`, `TCM-RFI-004`).
  The requirement branch, its constants and `_reader_first_advisories`
  are byte-identical to `WO-TCM-005`'s.
- `templates/repository/standard/scripts/generate_harness_dashboard.py`:
  `outcome`, `plain_words` (through the helper `WO-TCM-005` added) and
  `success_measure_rows` projected on intent records; the G0
  `intent_quality` condition, "Outcome stated with a success measure",
  reads `satisfied` when at least one reachable active intent carries an
  outcome and a measure row, `not_assessable` otherwise, with the measured
  intents as its evidence (`TCM-RFI-006`). It stays a derived observation
  inside a derived grouping.
- `repository_tools/explorer_design/build_explorer_template.py`:
  `INTENT_PATCHES`, four count-asserted patches applied after the
  readability patches: the `outcome` value on the record panel; an
  `Outcome` blockquote with the plain words beneath it, placed after the
  statement blockquote (which an intent never has) and before the decision
  trail; the `outcome` on the lineage card of an intent, rendered under its
  title. `index.template.html` rebuilt from the sources; `--check` matches.
  The design sources are unchanged.
- `docs/notes/artifact-authoring.md` (an `Intents` section),
  `docs/notes/harnessctl-reference.md` (the advisory sentence names
  intents), `docs/notes/diagnostic-codes.md` regenerated: 273 codes, the
  `W-AUT` family at 15.
- Tests: `tests/test_reader_first_intents.py` (new, 13 tests) and the
  candidate-versus-root ledger of
  `tests/test_predecessor_bootstrap_retirement.py` regenerated (16 opcodes,
  line delta 354, the comment naming `WO-TCM-007`).
- This domain's index and this evidence packet.

The root managed copies are untouched: `git diff --stat origin/main --
scripts/ docs/engineering/*.md docs/engineering/templates/
ENGINEERING_HARNESS.md .engineering-harness.toml .github/ AGENTS.md
CLAUDE.md` is empty. `git diff --check` is clean. No approved intent is
edited.

## Test evidence (Windows 11, candidate source)

- `python -m unittest tests.test_reader_first_intents`: 13 tests, OK.
- `python -m unittest tests.test_reader_first_intents tests.test_reader_first_requirements tests.test_predecessor_bootstrap_retirement tests.test_artifact_authoring_policy tests.test_diagnostic_code_index tests.test_dashboard_webui tests.test_progressive_documentation tests.test_artifact_catalog`:
  119 tests, OK (1 skipped), after two assertion fixes in the new module
  (a regex without the multiline flag; advisories are sorted, not in row
  order).
- `python scripts/run_tests.py` (8 workers, final candidate tree before
  this packet was written): `Ran 1243 tests in 114.488s (131 classes, 8
  workers)`, `FAILED (errors=1, skipped=26)`: zero failures, the one
  baseline error named below, twenty-six Windows-only skips. The suite left
  no file behind.

The one error is the pre-existing Windows baseline
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
(`PermissionError` deleting a temporary `.git` object; present on
`origin/main` before this work and recorded by `WO-TCM-005` and
`WO-TCM-006`). The skips are the Windows-only guards.

## Released-evaluator evidence (Windows 11, 0.14.0)

- `validate .`: PASS. Artifacts 1293, errors 0, warnings 69 (the
  maintenance `W014`/`W015` legacy architecture warnings that predate this
  work), advisories 0.
- `doctor .`: 0 FAIL lines.
- `preflight . --work-order WO-TCM-007`: PASS, work order `in_progress`.
- `check . --artifact WO-TCM-007 --checkpoint handoff --from-git origin/main --pull-request-body <PR #341 body>`:
  compliance `pass`, change set from Git, complete, inside the declared
  scope; `QG-G4-IMPLEMENTATION-EVIDENCE` with its eight predicates `pass`;
  no `W-ADS-001` (the fetched body carries no carriage return). The
  retained result is `handoff.json` beside this file; the first run's
  response named the required check at head `801b988` as `failure`, which
  is the delegated-start commit checked before this packet existed
  (`QGP-G4I-EVIDENCE`, no readable evidence), the same reading
  `WO-TCM-005` and `WO-TCM-006` recorded at the same point.

The candidate validator on this repository (`--root . --advisories`):
PASS, 1293 artifacts, 0 errors, 69 warnings, 0 advisories. The 33 approved
intents raise nothing.

## VER-TCM-004 matrix

| Row | Evidence |
| --- | --- |
| `REQ-TCM-009` template | `test_the_intent_template_is_reader_first_with_an_outcome_field` (the four sections in order, `outcome` in the front matter, no retired heading, `create-artifact` produces the shape). |
| `REQ-TCM-009` field | `test_the_outcome_field_is_accepted_optional_and_refused_when_empty` (valid, absent, and empty: the last is `E-AUT-002`). |
| `REQ-TCM-009` advisories | `test_each_budget_raises_exactly_its_advisory_with_the_measured_value` (one fixture per budget, each raising exactly its code with file, budget and value); `test_a_reader_first_draft_within_every_budget_raises_no_advisory`; `test_no_shape_advisory_fires_on_an_approved_intent_or_on_a_requirement` (an approved intent over every budget raises nothing; a requirement draft over the intent constants raises no intent code and keeps its own constants); `test_validation_still_passes_with_advisories`. |
| `REQ-TCM-009` corpus | `test_the_corpus_of_approved_intents_raises_nothing` (the 33 intents of this repository: zero advisories, zero errors). |
| `REQ-TCM-009` checklist | `test_the_authoring_checklist_names_the_shape_and_when_a_new_intent_is_warranted`, and the inspection above: every checklist line matches `TCM-RFI-001`, mechanical lines name their code, the two sentences of `TCM-RFI-005` are present. |
| `REQ-TCM-010` acceptance | `test_an_acceptance_check_in_the_table_is_reported_once_per_row` (four acceptance rows named, the operational row, the honest baseline and the zero target silent); `test_an_honest_baseline_and_a_zero_target_raise_nothing`. |
| `REQ-TCM-010` empty | `test_an_empty_or_malformed_table_is_one_advisory` (`W-AUT-014` once for a header-only table and once for a two-column table). |
| `REQ-TCM-011` projection | `test_the_explorer_projects_the_outcome_and_plain_words_of_an_intent` (`outcome`, `plain_words` and `success_measure_rows` on the intent record, absent on a legacy intent and on a requirement). |
| `REQ-TCM-011` rendering | the same test on the built template: `{{outcome}}` precedes the intent's `{{plainWords}}`, both precede `Decision trail`, `{{c.outcome}}` is on the lineage card, and the `WO-TCM-005` ordering of `{{statementNodes}}` before the first `{{plainWords}}` is kept. |
| `REQ-TCM-011` condition | `test_the_g0_intent_quality_condition_is_derived_from_outcome_and_a_measure_row` (`satisfied` with evidence `INT-001`; `not_assessable` with an outcome and no row; `not_assessable` for a legacy intent, `intent_chain` unchanged). |
| all: existing suite | the suite line above and the pull request's Linux lane. |

## Disclosures for the assurance decision

1. The rendering row is proved on the built template's text and order, not
   in a browser: the record panel and the lineage card are asserted by the
   position of their placeholders, as `WO-TCM-005` asserted its plain-words
   line. The design sources are untouched; the patches are count-asserted.
2. The G0 condition's label changed from "Outcome quality and stakeholder
   agreement" to "Outcome stated with a success measure", which is what it
   now measures; `SPEC-TCM-004` names the condition, not its label, and no
   test pinned the old label.
3. The acceptance vocabulary is a closed, case-insensitive word list
   (`CI`, `test`, `tests`, `validator`, `validate`, `verification`,
   `implementation review`, `acceptance run`, `regression run`,
   `transaction`), as `SPEC-TCM-004` declares; a row observed by a check
   named in other words is not reported, as `VER-TCM-004` records.
4. Two assertions in the new test module were corrected during execution
   before any commit: a regex asserted without the multiline flag, and an
   advisory order the report does not promise. Neither touched the
   candidate code.
5. Windows figures only. The Linux reading is the pull request's managed
   `validate` check on the head commit; the delegated completion cites it.
