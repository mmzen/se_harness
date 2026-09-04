# WO-TCM-008 verification evidence

Retained under `VER-TCM-005` for the reader-first capability shape, the
`ability` field and the graph-read derivation (`REQ-TCM-012`,
`REQ-TCM-013`, `SPEC-TCM-005` rules `TCM-RFC-001` to `TCM-RFC-007`).
Measurements were taken on Windows 11 on 2026-09-04 on the execution branch
`wo/tcm-008-execution` (PR #343) over base `15a3eec` (origin/main), with
the released 0.14.0 evaluator in `C:/Users/mathi/se-harness-eval-0140` and
the candidate source of this checkout. Every figure is labelled with the
platform it was read on; the Linux reading is the pull request's managed
check.

## Authorization

- 2026-09-04: the repository owner decided the four points of the
  capability assessment as recommended ("i follow your recommendation")
  and approved the packet with "i apprive" (PR #342, merged as `91f0bde`).
- `WO-TCM-007` merged as `15a3eec` with `VREC-TCM-007` verified before this
  branch opened; this work order stacks on the intent advisories, the
  `outcome` projection and the Explorer patches it landed.
- Delegated `DR-WO-START` under the `[delegation]` class `execution`;
  required check `validate` success at `72a0c4c` (check-run 101162456699).

## What WO-TCM-007 landed, and how this work order extends it

`WO-TCM-007` implemented the intent advisories as per-type constants
(`INTENT_*`) and one intent function beside the requirement one, not as a
single table indexed by type. `SPEC-TCM-004` rule `TCM-RFI-003` asks for
per-type constants, which is what landed, so `WO-TCM-008`'s stop condition
("a type table that WO-TCM-007 did not land in the form SPEC-TCM-004
describes") did not fire. The capability follows the same form: `CAPABILITY_*`
constants and one `_capability_authoring` function, dispatched from
`validate_authoring` beside the intent one. The shared codes `W-AUT-005`,
`W-AUT-007`, `W-AUT-008` and `W-AUT-009` fire with the capability constants
on a capability and with the intent and requirement constants on those
types, which the tests prove type by type. Folding the three functions into
one table-driven helper is left to a later maintenance work order; it is a
refactor with no behavior change and was outside this work order's
authorized envelope.

## Change inventory (candidate source only)

- `templates/repository/standard/docs/engineering/templates/CAPABILITY.template.md`:
  the `ability` field with its rule comment; the reader-first body (`In
  plain words`, `Actor and need`, `Not decided here`); the retired sections
  named in the comments with where each went; the glossary pointer at the
  repository root.
- `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`:
  the capability checklist rewritten line by line with the mechanical
  counterparts, "lists its derived requirements" removed, the two guidance
  sentences (when a capability is warranted; what it never contains).
- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `CAPABILITY_ABILITY_LIMIT` 30, `CAPABILITY_BODY_LIMIT` 150,
  `CAPABILITY_NEED_WORD_LIMIT` 60, `CAPABILITY_NEED_SENTENCE_LIMIT` 3,
  `CAPABILITY_CODE_IDENTIFIER_LIMIT` 2; `_capability_authoring`:
  `E-AUT-002` on an empty or non-string `ability`; on drafts `W-AUT-016`
  (missing, over 30 words, no `can`, no `under`, a code span; one message
  per defect), `W-AUT-017` (`Actor and need` over 60 words or three
  sentences), `W-AUT-018` (a `Candidate requirements` or `Derived
  requirements` heading), and the shared `W-AUT-005`, `W-AUT-007`,
  `W-AUT-008`, `W-AUT-009` with the capability constants. The requirement
  and intent code paths are unchanged.
- `templates/repository/standard/scripts/generate_harness_dashboard.py`:
  `ability`, `plain_words` and `derived_requirements` (sorted ids of the
  requirements whose `derives_from` names the capability, computed from the
  validation report's artifacts) on capability artifacts; `ability` on the
  compact bundle entry so the lineage board reads it like an intent's
  outcome.
- `repository_tools/explorer_design/build_explorer_template.py`:
  `CAPABILITY_PATCHES`: the record panel's `Ability` block with the plain
  words beneath it and a `Derives` row of linked ids
  (`window.HarnessExplorer.artifactHref`), placed after the outcome block
  and before the lifecycle events; the lineage second stage shows the
  ability under the title. Template rebuilt: 437,515 bytes, SHA-256
  `148e73567aed1c1699e9ff1089ca1479baf152edbff7ef41fc4a741cb3687b39`;
  `build_explorer_template --check` reports "matches its sources".
- `docs/notes/artifact-authoring.md`: a `Capabilities` section;
  `docs/notes/diagnostic-codes.md` regenerated (`W-AUT` now 18 codes;
  `--check` matches the source).
- Tests: `tests/test_reader_first_capabilities.py` (new, 9 tests);
  `tests/test_reader_first_requirements.py` (its Explorer test now selects
  the detail by artifact id, since capability details now name deriving
  requirement ids); `tests/test_predecessor_bootstrap_retirement.py`
  ledger refreshed over the 0.14.0 root copy (16 opcodes, +424 lines).

The root managed copies and `pyproject.toml` are untouched: `git diff
--stat origin/main -- scripts/ docs/engineering/*.md
docs/engineering/templates/ ENGINEERING_HARNESS.md .engineering-harness.toml
.github/ AGENTS.md CLAUDE.md pyproject.toml` is empty. `git diff --check`
is clean. Every changed path is inside the work order's execution scope.

## Test evidence (Windows 11, candidate source)

- `python -m unittest tests.test_reader_first_capabilities tests.test_reader_first_requirements tests.test_predecessor_bootstrap_retirement`:
  40 tests, OK.
- `python -m unittest tests.test_artifact_authoring_policy tests.test_reader_first_intents tests.test_reader_first_requirements tests.test_dashboard_webui tests.test_glossary`:
  75 tests, OK (1 skipped) after the detail-selection fix.
- `python scripts/run_tests.py` (8 workers, final tree): `Ran 1252 tests
  in 119.695s (132 classes, 8 workers)`, `FAILED (errors=1, skipped=26)`:
  zero failures, the one baseline error named below, twenty-six
  Windows-only skips.

The one error is the pre-existing Windows baseline
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
(`PermissionError` deleting a temporary `.git` object; present on
`origin/main` before this work). The skips are the Windows-only guards.

## Released-evaluator evidence (Windows 11, 0.14.0, `-I`)

- `validate .`: PASS. Artifacts 1299, errors 0, warnings 69 (maintenance
  `W014`/`W015` legacy architecture warnings that predate this work),
  advisories 0.
- `doctor .`: 0 FAIL lines.
- `preflight . --work-order WO-TCM-008`: PASS, work order `in_progress`.

## VER-TCM-005 matrix, row by row

| Row | Evidence |
| --- | --- |
| `REQ-TCM-012` template | `test_the_capability_template_is_reader_first_with_an_ability_field`: the three sections in order, the `ability` field, the glossary pointer, none of the retired headings, `create-artifact` writes the shape. |
| `REQ-TCM-012` field | `test_the_ability_field_is_accepted_optional_and_refused_when_empty`: valid and absent validate; empty is `E-AUT-002` naming `ability`. |
| `REQ-TCM-012` advisories | `test_a_reader_first_draft_within_every_budget_raises_no_advisory`; `test_each_budget_raises_exactly_its_advisory_with_the_measured_value` (missing ability, 33 words, no `can`, no `under`, a code span, a four-sentence need, a 160-word body, a 28-word sentence, three identifiers, three plain sentences, a legacy list; each alone with its measured value); `test_no_capability_advisory_fires_on_an_approved_capability_or_another_type` (an approved capability over every budget is silent; an intent draft over the capability constants raises none of `W-AUT-016` to `W-AUT-018` and keeps its own body budget). |
| `REQ-TCM-012` corpus | `test_this_repository_corpus_raises_no_capability_advisory`: the 36 approved capabilities raise nothing. |
| `REQ-TCM-012` checklist | `test_the_checklist_matches_the_shape`: every rule and code named, the retired line and heading absent, the two guidance sentences present. |
| `REQ-TCM-013` template | the template test above: no `Candidate requirements` or `Derived requirements` heading; the checklist test: no such line. |
| `REQ-TCM-013` projection | `test_derived_requirements_are_read_from_the_graph_never_from_a_list`: five deriving requirements against a legacy list naming two, the sorted five are projected; none deriving projects an empty list; a legacy capability without `ability` projects neither `ability` nor `plain_words`. |
| `REQ-TCM-013` rendering | `test_the_explorer_places_the_ability_the_plain_words_and_the_derives_list_before_the_events`: in the built template `{{ability}}` precedes `{{derives}}`, which precedes `{{events}}`, the plain words sit between the first two, and the lineage stage carries `{{c.ability}}`. |
| `REQ-TCM-013` legacy | the last case of the budget test: `W-AUT-018` alone on a `Candidate requirements` heading. |
| all: existing suite | the suite line above and the pull request's Linux lane. |

## Disclosures for the assurance decision

1. The per-type advisory table is three per-type functions with per-type
   constants, the form `WO-TCM-007` landed; a table-driven refactor was
   outside the envelope and is left to a maintenance work order. Behavior
   matches the specification.
2. `W-AUT-016` can fire more than once on one draft (one message per
   defect of the ability); the specification names the code, not the
   count. The tests pin one message per fixture defect.
3. The `Derives` links use the Explorer shell's `artifactHref` when present
   and fall back to plain ids; the design sources are unchanged, the
   behavior lives in `CAPABILITY_PATCHES`.
4. Windows figures only. The Linux reading is the pull request's managed
   `validate` check on the head commit; the delegated completion cites it.
