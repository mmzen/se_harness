```toml
artifact = "WO-DST-026"
checkpoint = "handoff"
formal_snapshot_sha256 = "883364d03a49a07358ff284015fa421cd190b4f82dfb8f71840c5de9fc149aa2"
rebound_at = "2026-09-08T21:56:59Z"
```

# WO-DST-026 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard template's two check steps capture the evaluator's exit status
and stderr and fail with the evaluator's own refusal when no result was
written; the header names the seven steps the file runs and the upload; the
three actions are pinned to commits with their exact tags. The installer
writes the `.gitignore` block between hash markers, and an upgrade of a
repository whose block still carries HTML comments rewrites only the block
through the existing fragment rule, every owner byte identical (measured
against a repository initialized by released 0.16.0). `SPEC-ECP-006` names
`SE_HARNESS_REHEARSAL` by amendment record, the delegation note names it
beside `local-file`, and a test pins the three environment names the package
reads against the specifications that name them. No root managed byte of this
repository moved; the root follows at the root adoption of the carrying
release (`DST-MWF-014`, carried forward).

## Evaluators

- Governing: released `se-harness 0.16.0` installed from the wheel file
  outside the checkout (`C:/Users/mathi/se-harness-eval-0160`), run `-I`, for
  `validate`, `doctor`, the review preflight, `evidence` and the handoff
  check; also the 0.16.0 installer that initialized the scenario B fixture.
- Candidate: this checkout, branch `wo/dst-026-managed-template` off `main`
  at `fd4584cc` (the merge of `WO-CIP-007`). Implementation commits
  `6a8d1dc8` (template and installer), `1836ee0c` (tests), `3dda64d1`
  (amendment record, notes, index); implementation head `3dda64d1`.
- Consumer scenarios: a non-promotable wheel `se_harness-0.17.0-py3-none-any.whl`
  (`sha256:952ec200…6bb2`) built from the tracked worktree bytes and
  installed in a virtual environment under `C:/Users/mathi/dst026-scratch`,
  outside the checkout; not a build of record.

## Rule-to-case map (SPEC-DST-027)

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `DST-MWF-001` | both `check … --json` steps: `2> "$RUNNER_TEMP/<name>.stderr" \|\| <name>_status=$?`, no `\|\| true` | `test_the_check_steps_capture_status_and_stderr` |
| `DST-MWF-002` | each embedded reader echoes the captured stderr, then on `OSError`/`ValueError` prints "wrote no result (exit status N)" and exits N, or 1 when N is 0 | `test_the_readers_fail_with_the_captured_status_and_text_on_an_empty_result`; scenario C1 to C3 |
| `DST-MWF-003` | the verdict code after the parse is unchanged | `test_the_readers_judge_a_parsed_result_as_before`; scenario C4 to C9, the same messages as before; `test_ci_pipeline.test_the_managed_workflow_enforces_scope_on_every_pull_request` still passes |
| `DST-MWF-004` | the header names the seven `name:` steps and the upload; `doctor`, `validate` and "the dashboard" are gone | `test_the_header_names_only_the_steps_the_file_runs` |
| `DST-MWF-005` | `actions/checkout@11d5960a… # v4.4.0`, `actions/setup-python@a26af69b… # v5.6.0`, `actions/upload-artifact@ea165f8d… # v4.6.2` | `test_every_action_takes_the_pin_form` |
| `DST-MWF-006` | `installer._block`: `HASH_MARKER_TARGETS = {.gitattributes, .gitignore}` take the hash pair; the Markdown fragments keep HTML | `test_block_chooses_the_marker_pair_by_target`; `test_init_writes_the_ignore_block_between_markers_git_reads_as_comments`; scenario A |
| `DST-MWF-007` | `_extract_block` unchanged, accepts both pairs | `test_upgrade_rewrites_an_html_marked_ignore_block_and_keeps_every_owner_byte`; scenario B |
| `DST-MWF-008` | the upgrade plans `.gitignore` as `update` in `fragment` mode through the existing rule; no new mode; a block edited inside is `customized` | the same test; `test_upgrade_refuses_an_ignore_block_edited_inside`; scenario B and its customized variant |
| `DST-MWF-009` | `SPEC-ECP-006` `## Amendment record`, appended entry naming the variable, `ECP-DLG-004` and `gate_source.load_configuration`; `updated` 2026-09-08 | inspection; `test_the_rehearsal_marker_is_named_where_its_exemption_lives` |
| `DST-MWF-010` | `docs/notes/delegation-class.md`, the `local-file` sentence | the same test |
| `DST-MWF-011` | `SPECIFIED_ENVIRONMENT_NAMES` = `SE_HARNESS_REHEARSAL`, `GITHUB_TOKEN`, `PYTHONPATH`; each found in a `SPEC-*.md` | `test_every_environment_variable_read_under_the_package_is_specified` |
| `DST-MWF-012` | `tests/test_managed_template_hygiene.py`, eleven tests | the module, `OK` |
| `DST-MWF-013` | `git diff --quiet fd4584cc` over the root managed set: no difference | `WO-DST-026-verification.md`, "Root managed bytes"; `doctor` reads every managed path as matching |
| `DST-MWF-014` | carried to the root-adoption work order of the carrying release | the evidence file, "Carried obligation" |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate .` | exact 0.16.0, Windows | PASS, 1,432 artifacts, 0 errors, 44 warnings (all `W013`, none on a path this work order touches), 0 advisories |
| `doctor .` | exact 0.16.0 | exit 0, 97 `PASS`, no failure; every managed path `matches distribution` |
| `preflight . --work-order WO-DST-026 --phase review` | exact 0.16.0 | PASS; commit-bound verification `required` |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS, 13 records |
| `python -m se_harness --help` | candidate | exit 0 |
| `python scripts/run_tests.py --workers 4` | candidate, Windows 11 (local control) | 1,098 tests, 96 s, 1 failure, 1 error, 23 skips: the two documented Windows baseline names, both present on `main` |
| discovered tests, base `fd4584cc` vs candidate | `unittest` discovery, a throwaway worktree | 1,087 vs 1,098; the eleven of the new module; no test deleted |
| the four named modules and the new one, alone | candidate | `test_ci_pipeline`, `test_harnessctl`, `test_standard_repository_lifecycle` OK; `test_instruction_architecture` at the baseline name only; `test_managed_template_hygiene` 11 OK |
| `check --checkpoint handoff --from-git fd4584cc` | exact 0.16.0 | the retained `handoff.json` beside this file |
| scenario A, install | candidate wheel, released-style venv | hash markers; `git check-ignore` exit 1 on both marker texts, 0 on the Explorer path; `doctor` exit 0, 99 `PASS` |
| scenario B, upgrade of a 0.16.0 fixture | released 0.16.0 `init`, candidate wheel `upgrade` | plan `update .gitignore`; apply exit 0; owner bytes identical; hash markers; `doctor` exit 0, 99 `PASS` |
| scenario B, edited inside the block | the same | plan `customized .gitignore`; apply exit 1, "no files were written"; file unchanged |
| scenario C, the embedded readers | `python`, extracted heredocs | C1/C2 the MG005 text then "wrote no result (exit status 2)", exit 2; C3 exit 1; C4 to C9 the verdicts and messages of the unchanged code; no `Traceback` |
| lanes at the implementation head `3dda64d1` (PR #420) | GitHub | Candidate Evidence 34283394471, Publication Rehearsal 34283394493, Predecessor Evaluator Assessment 34283394233, CodeQL 34283393006: success; Engineering Harness 34283394526: failure on `QGP-G4I-EVIDENCE` only ("No readable evidence for WO-DST-026, checkpoint handoff, and formal snapshot 883364d0…"), the evidence this packet adds; `QGP-G4I-PATHS` passed. The lanes at the packet head, the completion commit and the record head are quoted in the lifecycle events |

## Change set

Against `main` at `fd4584cc`, before this packet: 8 files, 458 insertions,
18 deletions.

| Path | + | − | What |
| --- | ---: | ---: | --- |
| `templates/repository/standard/.github/workflows/engineering-harness.yml` | 42 | 12 | the header, the three pins, the two captured checks and their readers |
| `se_harness/installer.py` | 9 | 1 | `HASH_MARKER_TARGETS`; `_block` chooses the pair by target |
| `tests/test_managed_template_hygiene.py` | 377 | 0 | new: eleven tests in three classes |
| `docs/engineering/execution-control-plane/specifications/SPEC-ECP-006.md` | 14 | 1 | the amendment record; `updated` |
| `docs/notes/delegation-class.md` | 5 | 2 | the `local-file` sentence names the variable |
| `docs/notes/harness-installation-and-upgrades.md` | 2 | 0 | the marker-pair paragraph |
| `docs/engineering/harness-distribution/README.md` | 1 | 1 | the wave 5 entry |
| `docs/engineering/harness-distribution/work-orders/WO-DST-026.md` | 8 | 1 | the start event |

Plus this packet: `evidence/WO-DST-026-verification.md`, this file and
`handoff.json`. Every path is inside `[execution_scope]`. No root managed
file and not the lock.

## Disclosures

The eight disclosures of `WO-DST-026-verification.md` stand; in short: the
environment inventory reads three names, not two; an empty result with status
0 fails with 1; the readers echo the captured stderr in every branch; no
existing test needed to move; `SPEC-ECP-006`'s `updated` moved with its
amendment record; the header quotes the step names verbatim; the failure
surface is exercised by running the readers, not by a live consumer refusal;
and the work order's completion sentence disagrees with its own delegation of
`DR-WO-COMPLETE`, which this handoff follows as `WO-CIP-007` did.

One more: the scenario B plan also updated `.engineering-harness.toml` and
eight other managed files and added `RISK.template.md`. Those are the
released-0.16.0-to-candidate differences that every consumer upgrade to the
carrying release will carry (`WO-DST-025`'s key removal among them), not this
work order's; the reading that belongs here is that `.gitignore` and the
workflow are `update`, nothing is `customized` or `conflict`, and `doctor`
passes afterwards.
