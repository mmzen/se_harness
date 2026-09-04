# WO-TCM-006 verification evidence

Retained under `VER-TCM-003` for the repository-owned glossary and its
drift report (`REQ-TCM-007`, `SPEC-TCM-003` rules `TCM-RFR-007` to
`TCM-RFR-010` as amended by record on 2026-09-04). Measurements were taken
on Windows 11 on 2026-09-04 on the execution branch `wo/tcm-006-execution`
(PR #337) over base `09047aa` (origin/main), with the released 0.14.0
evaluator in `C:/Users/mathi/se-harness-eval-0140` and the candidate source
of this checkout. Every figure is labelled with the platform it was read
on; the Linux reading is the pull request's managed check.

## Authorization and decisions taken on the way

- 2026-09-04: the repository owner approved the packet with "i approve the
  packet, the work orders can be start with execution delegation" (PR #335,
  merged as `cfa54b8`). WO-TCM-005 merged as `09047aa` with `VREC-TCM-005`
  verified before this branch opened.
- Delegated `DR-WO-START` under the `[delegation]` class `execution`;
  required check `validate` success at `e422274` (check-run 101113465388).
- Pending decision, packaging: the template root is packaged as an explicit
  file list in `pyproject.toml`, so the seed needs one data-files line
  there, and `pyproject.toml` was outside the work order's scope. The
  executor first raised the question as `DEC-TCM-001` (question, options
  `amend-scope`, `move-seed`, `stop`, recommendation `amend-scope`). The
  governing 0.14.0 evaluator refused the file with `E002` "unknown artifact
  type 'decision'": decision artifacts are candidate code until the 0.15.0
  adoption. The file was withdrawn and the question put to the owner in the
  ratified chat channel.
- 2026-09-04: the owner chose the glossary's location, "This repository's
  glossary moves to /GLOSSARY.md, and the notes index and the two notes
  that link it follow". `SPEC-TCM-003` carries the amendment record on
  `TCM-RFR-007` to `TCM-RFR-009`.
- 2026-09-04: the owner confirmed the scope amendment, "i confirm the scope
  amendment"; `WO-TCM-006` carries the amendment record adding
  `pyproject.toml` to its execution scope.
- 2026-09-04: the owner confirmed the second scope amendment, "amend
  scope", adding `GLOSSARY.md` and `README.md`, the paths the glossary move
  itself created; the executor should have named them with the first.

## Change inventory (candidate source only)

- `templates/repository/standard/GLOSSARY.md.seed` (new): the structure, the
  two-vocabulary rule, an empty `Terms` section and an `Upkeep` section; no
  term. Installed by `init` and `adopt` as `GLOSSARY.md` at the repository
  root in seed mode, the mode the domain index and the pull-request template
  already use: written when absent, adopted when present, never rewritten,
  recorded in the lock as `{"mode": "seed", "state": "present"}` with no
  digest, untouched by `upgrade`. No installer code change was needed.
- `pyproject.toml`: one data-files line packaging the seed, under the scope
  amendment.
- `templates/repository/standard/scripts/inspect_engineering_artifacts.py`:
  `build_vocabulary_report` (statements and bodies tokenized with code
  removed, an English stoplist, a harness-term stoplist that ships as
  exclusions only, entries read from bold heads, a bounded threshold
  `--vocabulary-threshold` 30 to 100 with default 50, at most 25 undefined
  terms named with the count of the rest, stale entries, a single note for
  a missing or unreadable glossary); the `vocabulary` section of the
  inspection JSON and its human rendering. Read-only and deterministic.
- `se_harness/cli.py`: `inspect --vocabulary-threshold` passed through to
  the distribution script.
- `templates/repository/standard/docs/engineering/ARTIFACT_AUTHORING.md`:
  the upkeep paragraph of `TCM-RFR-009` (an entry may cite the artifact
  that fixes its meaning; an amendment that changes a meaning names the
  entry; the report), and the glossary pointer at the root.
- `templates/repository/standard/docs/engineering/templates/REQUIREMENT.template.md`:
  the `In plain words` pointer repointed from `docs/notes/glossary.md` to
  `GLOSSARY.md` at the repository root.
- `GLOSSARY.md` (moved from `docs/notes/glossary.md`): the two-vocabulary
  rule in its Summary, the nine terms the assessment named (`Candidate`,
  `Digest`, `Canonical`, `Deterministic`, `Schema`, `Accountable role`,
  `Dashboard snapshot`, `Provenance`, `Predicate`), each citing the
  artifact that fixes its meaning, and an `Upkeep` section. Links in
  `README.md`, `docs/notes/README.md`, `docs/notes/getting-started.md` and
  the readability assessment follow.
- `docs/notes/harnessctl-reference.md`: the `inspect` usage line and the
  vocabulary section.
- `SPEC-TCM-003`: one amendment record (the root path).
- `WO-TCM-006`: two amendment records (`pyproject.toml`, then `GLOSSARY.md`
  and `README.md`, in scope).
- Tests: `tests/test_glossary.py` (new, 13 tests) and
  `tests/test_fixture_support.py` (49 installed files).

The root managed copies are untouched: `git diff --stat origin/main --
scripts/ docs/engineering/*.md docs/engineering/templates/
ENGINEERING_HARNESS.md .engineering-harness.toml .github/ AGENTS.md
CLAUDE.md` is empty. `git diff --check` is clean. The Explorer template and
the diagnostic-code index are unchanged and match their sources.

## Test evidence (Windows 11, candidate source)

- `python -m unittest tests.test_glossary`: 13 tests, OK.
- `python -m unittest tests.test_glossary tests.test_harnessctl tests.test_release_build tests.test_integration_package`:
  75 tests, OK (3 skipped).
- `python scripts/run_tests.py` (8 workers, final tree): `Ran 1230 tests
  in 93.099s (130 classes, 8 workers)`, `FAILED (errors=1, skipped=26)`:
  zero failures, the one baseline error named below, twenty-six
  Windows-only skips. One earlier parallel run on a near-final tree showed
  a single failure of
  `test_repository_context_retirement.test_upgrade_converges_the_four_prior_states_to_one_lock`
  that did not reproduce alone, after the new modules in one process, or in
  the rerun; it is recorded here as a one-off.

The one error is the pre-existing Windows baseline
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
(`PermissionError` deleting a temporary `.git` object; present on
`origin/main` before this work). The skips are the Windows-only guards.

## Released-evaluator evidence (Windows 11, 0.14.0, `-I`)

- `validate .`: PASS. Artifacts 1286, errors 0, warnings 69 (maintenance
  `W014`/`W015` legacy architecture warnings that predate this work),
  advisories 0.
- `doctor .`: 0 FAIL lines.
- `preflight . --work-order WO-TCM-006`: PASS, work order `in_progress`.

## This repository's own vocabulary report

`harnessctl inspect .` on this repository at the default threshold names 30
glossary entries and 25 frequent project terms without an entry, with
about 1,250 more above the threshold: `commit`, `workflow`, `authority`,
`identity`, `publication`, `boundary`, `command`, `review`, `package`,
`rule`, `policy`, `upgrade`, `version`, `assurance`, `checkout` and others.
That is the report doing its job on a corpus of 1,286 artifacts: the owner
curates from the top of the list, and the generic words that remain in it
are candidates for the English stoplist in a later work order.

## VER-TCM-003 matrix, rows for REQ-TCM-007

| Row | Evidence |
| --- | --- |
| `REQ-TCM-007` seed | `test_init_seeds_an_empty_repository_owned_glossary` (file present with the project name, empty `Terms`, lock entry seed and present, no digest); `test_an_edited_glossary_survives_upgrade_and_doctor_untouched` (byte-identical after `upgrade --apply`, `doctor` exit 0); `test_adopt_seeds_the_glossary_and_keeps_an_existing_one` (an existing glossary is adopted unchanged). |
| `REQ-TCM-007` report | `test_the_report_names_frequent_project_terms_and_stale_entries_only` (`ledger` at 80 named, `tally` at 10 and the harness terms `checkpoint`, `gate` not named, the stale `Vault` entry named, two runs identical); `test_the_threshold_is_bounded_and_the_default_is_fifty`; `test_a_missing_glossary_is_one_note_not_an_error`; `test_inspect_carries_the_vocabulary_section_in_json_and_text` (JSON and text through `harnessctl inspect`, the out-of-range threshold refused with exit 2). |
| `REQ-TCM-007` boundary | `test_no_glossary_term_ships_with_the_distribution` (the seed's `Terms` section is empty; no `Terms` section in any template carries an entry; none of this repository's 30 entry heads appears in any template); `test_the_seed_is_packaged_explicitly_at_the_template_root` (the `pyproject.toml` line, since the template root is an explicit list and the directory-coverage test alone would pass with the file missing from the wheel); `test_this_repository_glossary_defines_the_terms_the_assessment_named`. |
| all: existing suite | the suite line above and the pull request's Linux lane. |

## Disclosures for the assurance decision

1. The glossary path changed from the specification's `docs/notes/glossary.md`
   to `GLOSSARY.md` at the repository root on the owner's instruction,
   recorded as an amendment on `SPEC-TCM-003`. `REQ-TCM-007`'s Behavior row
   still reads the old path; its obligation is unchanged and approved
   requirements are not rewritten. The requirement template that
   `WO-TCM-005` shipped is repointed here.
2. The work order's scope was amended twice on the owner's instruction:
   `pyproject.toml` for the packaging line, then `GLOSSARY.md` and
   `README.md` for the root location the owner chose. Both records are on
   the work order; the second gap was the executor's miss when proposing
   the move.
3. A decision artifact could not be used for the packaging question:
   the 0.14.0 evaluator refuses the type until the 0.15.0 adoption. The
   question and its options are recorded above instead.
4. The vocabulary report on this repository is long and partly generic at
   the default threshold; it is bounded to 25 names and the rest counted.
   The stoplists are the implementation's choice under the specification's
   explicitly unspecified decisions.
5. Windows figures only. The Linux reading is the pull request's managed
   `validate` check on the head commit; the delegated completion cites it.
