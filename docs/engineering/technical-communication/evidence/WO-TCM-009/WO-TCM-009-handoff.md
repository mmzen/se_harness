```toml
artifact = "WO-TCM-009"
checkpoint = "handoff"
formal_snapshot_sha256 = "4d9e32f49a7bb6a3059f8ad0b1bca31d1500e903d30b4d8403cba2b5e87bcfe0"
rebound_at = "2026-09-06T11:35:59Z"
```

# WO-TCM-009 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The next specification has a shape whose rules a test can cite, a work
order can execute and a deviation can name. The candidate template is a
`contract` field and eight sections; every rule leads with a stable
identifier and is one sentence with a normative keyword; the `Coverage`
table is read by the validator and shown on both sides by the Explorer;
a deviation whose `against` fragment names no rule is `E-DCM-005`. Five
advisories, `W-AUT-019` to `W-AUT-023`, and the shared budgets with
specification constants fire on specification drafts only. No approved
specification changed; the 135 of this repository validate with zero
specification advisories under the candidate, because all are approved,
implemented or superseded.

## Evaluators

- Governing: released `se-harness 0.15.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0150`), wheel-installed; every reading
  below marked "released" is its. It does not know the new rules: its
  readings prove the graph is valid and the root copies are untouched.
- Candidate: this checkout at `6d39fd5` (the candidate copy of the
  validator, generator and Explorer under `templates/repository/standard/`,
  loaded by the test suite and by the in-tree `python -m se_harness`).
- Root: hash-locked 0.15.0 copies, unchanged; the candidate-versus-root
  divergence is declared in `tests/test_predecessor_bootstrap_retirement.py`
  (five inserted blocks, 149 lines) and `tests/test_dashboard_webui.py`
  (the build without `SPECIFICATION_PATCHES` equals the root template).

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | released 0.15.0 | PASS, 1,330 artifacts, 0 errors, 71 warnings, 0 advisories |
| `doctor` | released 0.15.0 | 116 PASS, 0 FAIL |
| `preflight --work-order WO-TCM-009` | released 0.15.0 | PASS |
| candidate `validate` over this repository | candidate | 0 errors, 0 advisories: every specification is approved or later, so TCM-RFS-014 holds; no `E-DCM-005`, no deviation exists |
| contract copies | workstation | `WORKFLOW.json` and `QUALITY_GATES.json` byte-identical to the `se_harness/` copies; neither changed |
| diagnostic-code index | candidate | `--check` passes; `W-AUT-019` to `W-AUT-023` and `E-DCM-005` indexed |
| Explorer template | candidate | `build_explorer_template --check` passes; 442,561 bytes |
| Windows suite (`run_tests.py --scale full`) | candidate, Windows 11, CPython 3.14.6 | 1,263 tests (14 new in `test_reader_first_specifications.py`), 1 error, 26 skipped; the error is the workstation baseline `test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`, the skips are the Windows-only guards; the failure set equals the 0.15.0 adoption control (1,249 tests, the same error, 26 skips) beyond the 14 added tests |
| Linux lane | hosted | LANES-LINE |

## VER-TCM-006 matrix, row by row

| Row | Test or inspection | Result |
| --- | --- | --- |
| `REQ-TCM-014` template | `test_the_specification_template_is_reader_first_with_a_contract_field` | pass; the eight sections in order, `contract` in front matter, none of the nine retired sections, `create-artifact` renders it |
| `REQ-TCM-014` field | `test_the_contract_field_is_accepted_optional_and_refused_when_empty` | pass; `E-AUT-002` on an empty contract |
| `REQ-TCM-014` identity and shape | `test_rule_identity_and_shape_fire_exactly_for_their_cases` | pass; `W-AUT-020` for a paragraph without an identifier and for a duplicate; `W-AUT-021` for 40 words, two sentences, no keyword; a parenthesised short name after the identifier is accepted |
| `REQ-TCM-014` contract advisory | `test_the_contract_advisory_fires_for_each_departure` | pass; missing, 34 words, two sentences, a code span |
| `REQ-TCM-014` legacy and budgets | `test_legacy_shape_and_budgets_fire_with_specification_constants` | pass; a draft copy of `SPEC-PYP-001` draws twelve `W-AUT-020`, one `W-AUT-023`, one `W-AUT-022` (and `W-AUT-019`, `W-AUT-005`, `W-AUT-009` for its missing contract, 400-plus words of prose and missing plain words); 400 words of prose is `W-AUT-005` with the 300 budget; a 30-word sentence in `Scope` is `W-AUT-007`; a long sentence inside a rule is `W-AUT-021` and not `W-AUT-007`; forty code identifiers draw nothing |
| `REQ-TCM-014` silence | `test_no_specification_advisory_fires_on_an_approved_specification_or_another_type`, `test_this_repository_corpus_raises_no_specification_advisory` | pass; an approved fixture over every budget draws nothing; a requirement draft keeps its own `W-AUT-008`; the corpus draws zero specification advisories and zero errors |
| `REQ-TCM-014` checklist | `test_the_checklist_matches_the_shape` (inspection encoded) | pass; every line names its code, "Number rules" absent, the nine optional sections each present with when they earn their place |
| `REQ-TCM-015` coverage advisory | `test_the_coverage_table_is_checked_against_specifies_and_the_rules` | pass; a missing row, an undefined rule, a missing table, then silence |
| `REQ-TCM-015` projection | `test_rules_coverage_and_covered_by_are_projected_from_the_same_table` | pass; `rules`, `coverage`, `covered_by` equal the fixture; a requirement covered by no rule projects `[]`; a legacy specification projects no `contract` and empty lists |
| `REQ-TCM-015` rendering | `test_the_explorer_places_the_contract_the_rules_and_the_coverage_before_the_events` | pass; contract, then plain words, then rules with `id="{{r.id}}"` anchors, then coverage, all before the events; `Covered by` links before the events; `{{againstHref}}` present |
| `REQ-TCM-016` error | `test_a_deviation_names_a_rule_that_exists` | pass; an existing identifier validates; `rule-7`, another specification's identifier and a legacy specification's numbered rule are `E-DCM-005` |
| `REQ-TCM-016` amendment and link | `test_the_decision_specification_names_the_check`; the Explorer test above | pass; `SPEC-DCM-001` rule 3 shows `SPEC-TCM-006#TCM-RFS-009`, names `E-DCM-005` and `TCM-RFS-020`, and its amendment record names this work order |
| all: contract copies, index | readings above; `test_diagnostic_code_index` | pass |
| all: suite | readings above | see the suite line |

## Disclosures

1. **`SPEC-TCM-006` does not meet its own rule budget.** Read as a draft by
   the candidate, the approved specification draws five `W-AUT-021` (rules
   `TCM-RFS-003`, `-010`, `-012`, `-014` and `-018` are 31 to 39 words) and
   one `W-AUT-007` (a 40-word sentence in `Scope`). Its first example,
   "a draft written as this specification is draws no advisory", is
   therefore false as written. The specification is approved and
   `TCM-RFS-023` forbids a style rewrite; the example is corrected in the
   next amendment for another reason. The check itself behaves as
   specified: this is a finding about the artifact, not the code.
2. **The legacy parser counts list items as rules.** A numbered or
   bulleted list item under `Behavioral rules` is one rule paragraph, so a
   draft copy of `SPEC-PYP-001` draws twelve `W-AUT-020`, one per item, as
   `VER-TCM-006`'s acceptance scenario states. A first version counted the
   whole list as one paragraph; the tests caught it before commit.
3. **The decision-management fixtures moved to an identifier.** The
   deviation tests of `test_decision_management.py` named
   `SPEC-001#rule-3` on a fixture specification with no rules; under
   `E-DCM-005` that is now an error, so the fixture specification gained a
   `Rules` section defining `BASE-RUL-003` and the seven fragments name
   it. The `DECISION.template.md` comment and the decision checklist line
   of `ARTIFACT_AUTHORING.md` were updated from `#rule-N` to the identifier
   form for the same reason; both are managed template files in scope.
4. **`GLOSSARY.md` was not edited.** The work order's in-scope list names
   it "if a term of `SPEC-TCM-006` is new to it", but `GLOSSARY.md` is not
   in `execution_scope.paths`, so the three candidate terms (contract,
   rule identifier, coverage table) are left for a note-level pull request
   or a scope amendment, the owner's call.
5. **The deviation's departed rule renders as a link, not as a meta fact.**
   `TCM-RFS-022` is met by a `Departs from` block on the decision's record
   panel linking to the rule anchor; the `against` meta fact `WO-DCM-001`
   added stays as text.

## Material non-effects

No hash-locked root copy changed. No approved specification's body changed
except `SPEC-DCM-001`, amended by record under this work order's scope. No
requirement, intent or capability constant changed. No release, tag or
publication. The `se_harness/` package is unchanged; the change is entirely
in the candidate templates, the Explorer build sources, tests and notes.

## Hosted lanes

LANES-SECTION
