```toml
artifact = "WO-CIP-007"
checkpoint = "handoff"
formal_snapshot_sha256 = "d1fad6639e5c22d8869f6707ccc0b50a3246f931ee6e126507c48f8dac8f51f0"
rebound_at = "2026-09-08T20:48:46Z"
```

# WO-CIP-007 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

A pull request's head commit is qualified once and tested once. The
rehearsal's candidate leg replays the bound recipe and nothing else — its
qualification, suite and smoke step carries `if: inputs.mode ==
'release-record'` and the runner skipped it on this pull request while the
release-record leg ran it — so `candidate-evidence.yml` is the one lane that
qualifies the complete candidate graph and runs the suite for the commit
under review. Two inline re-checks that restated
`scripts/check_portable_release_surface.py` are gone. Every public action
takes the pin form (52 of 52, from 28; floating tags 18 to 0), every
`python-version` is `"3.11"`, the integration toolchain is one `env` block,
every Pages deployment queues behind one group, and `publish-pypi.yml` passes
the payload digest unconditionally. The `governance-migration` job is
`upgrade-rehearsal` and the predecessor assessment is named after the
predecessor evaluator down to its temporary files; four lines in one file
still name a retired term, all the path or the emitted schema string of the
script this work order may not rename. No schema-1 bundle manifest can be
written. The note, `SPEC-CIP-001`'s amendment record and the domain index
say so. No managed path moved.

## Evaluators

- Governing: released `se-harness 0.16.0` installed from the wheel file
  outside the checkout (`C:/Users/mathi/se-harness-eval-0160`), run `-I`,
  for `validate`, `doctor`, `evidence` and the handoff check.
- Candidate: this checkout, branch `wo/cip-007-pipeline-hygiene`, off `main`
  at `fae52e1b` with `main` at `560973cf` (the merge of #414) merged in
  before the implementation commits. The four implementation commits are
  `bcc0c04b` (the eight workflows), `49b563ad` (the manifest writer),
  `cbc20e1d` (the tests) and `e96160af` (the notes, the amendment record and
  the index); the implementation head is `e96160af`.
- Run observations: GitHub's runs and jobs API for pull request #419 and, as
  the before-reading, for #413, the last unstacked pull request merged before
  this branch.
- Negative controls: a scratch copy of the tree outside the checkout, one
  file mutated at a time; see `negative-controls.md`.

## Rule-to-case map (SPEC-CIP-003)

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `CIP-ONE-001` | `release-qualification.yml` lines 127, 166, 205: the qualification, suite and smoke step, the bundle verification and the transfer guarded by `if: inputs.mode == 'release-record'` | `test_the_qualification_definition_qualifies_and_tests_release_records_only`; mutation 1 fails it naming the file; `lanes-at-head.md`: step 6 skipped in the candidate leg, success in the release-record leg |
| `CIP-ONE-002` | `candidate-evidence.yml` `candidate-source` is the only job on a `pull_request` event that runs `qualify complete-candidate` or the suite | `test_candidate_source_is_the_only_lane_that_qualifies_and_tests_a_pull_request`; `run-lists.md`: head qualifications 2 → 1, head suite runs 2 → 1 |
| `CIP-ONE-003` | the `zipfile` assertion after the `--wheel` call is gone; `FORBIDDEN_MEMBERS` still holds the names | `test_no_step_restates_a_check_a_script_already_performs` |
| `CIP-ONE-004` | the `--help` grep and its message are gone; `FORBIDDEN_CLI` still holds the name | the same test; `retired-names.md` |
| `CIP-ONE-005` | `"3.11"` on every `python-version`, once as `publish-pypi.yml`'s `PYTHON_VERSION`; `"3.11.9"` gone from two files | `test_one_python_version_string`; `pin-and-version-inventory.md` |
| `CIP-ONE-006` | 52 of 52 public `uses:` lines `@<40-hex> # vX.Y.Z`, one digest per action per file; every digest resolved from its tag on 2026-09-08 | `test_every_public_action_takes_the_pin_form`; mutation 2 names file and line; the inventory's digest table |
| `CIP-ONE-007` | `integration-package-build` `env`: `INTEGRATION_BUILD_VERSION`, `INTEGRATION_SETUPTOOLS_VERSION`, `INTEGRATION_WHEEL_VERSION`, read by the install and the three `--expect-*-version` arguments | `test_the_integration_build_toolchain_is_stated_once`; `test_integration_package` |
| `CIP-ONE-008` | `pages-publication.yml` `deploy`: `group: se-harness-pages-deploy`, `cancel-in-progress: false` | `test_every_pages_deployment_queues_behind_one_group`; inspection; no live observation until the next release (`VER-CIP-003`, residual uncertainty) |
| `CIP-ONE-009` | `publish-pypi.yml` passes `--evaluator-payload-sha256 "$EVALUATOR_PAYLOAD_SHA256"` unconditionally; `identity_args` and the `identity --help` probe are gone | `test_the_payload_digest_is_probed_only_where_the_evaluator_may_predate_it`; `test_pypi_publishing` |
| `CIP-ONE-010` | `pages-publication.yml` keeps its probe with the comment naming why (the released record's own root may predate the flag) | the same test |
| `CIP-ONE-011` | workflow `Predecessor Evaluator Assessment`, group `predecessor-evaluator-assessment-${{ github.ref }}`, job, artifact and temporary files renamed | `test_no_retired_name_survives_in_a_repository_owned_workflow`; `retired-names.md`; run 34275597679 under the new name |
| `CIP-ONE-012` | job `upgrade-rehearsal`, artifact `upgrade-rehearsal-<platform>`, the `needs` entry and both outputs | the same test; `test_standard_repository_lifecycle`; run 34275597729's two `Upgrade rehearsal` jobs and the integration build on their outputs |
| `CIP-ONE-013` | `--build-recipe` `required=True`; `create_manifest` raises on `None`; schema unconditionally v2; reading unchanged | `test_manifest_producer_refuses_to_write_a_schema_1_bundle`; `manifest-refusal.md`: exit 2, no git call, no file |
| `CIP-ONE-014` | `docs/notes/ci-pipeline.md` "After `WO-CIP-007`": nine workflows, pins 52 of 52 from 28, YAML 2,082 → 2,137, the per-pull-request table | inspection; `test_active_repository_checker_rejects_retired_evaluator_contracts` passes over the note |
| `CIP-ONE-015` | `SPEC-CIP-001` `## Amendment record`: CIP-QLF 2 and 3 (the candidate leg), CIP-ART 3 and 5 (the job name); rule text verbatim, `updated` bumped | inspection; `validate` 0 errors with it |
| `CIP-ONE-016` | `PipelineHygieneTests`, ten methods, parsing the YAML as text and as job and step blocks; every test naming a retired name names the new one | `validate-and-doctor.md`, "Changed assertions"; 35 tests in the module |
| `CIP-ONE-017` | every one of the eight headers names the file's purpose, its trigger policy and the note section, `SPEC-CIP-001` CIP-DOC 4 | `test_every_repository_owned_workflow_carries_a_header_comment` |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate .` | exact 0.16.0, Windows | PASS, 1,431 artifacts, 0 errors, 44 warnings (all `W013`, none on a path this work order touches), 0 advisories |
| `doctor .` | exact 0.16.0 | exit 0, 97 `PASS`, 44 `WARN W013`; every managed path `matches distribution` |
| `scripts/validate_release_distributions.py --root .` | candidate | PASS, 13 distribution-bearing records |
| `python -m se_harness --help` | candidate | exit 0 |
| `python scripts/run_tests.py --workers 4` | candidate, Windows 11 | 1,087 tests, 93 s, 1 failure, 1 error, 23 skips: the two documented Windows baseline names, both present on `main` |
| discovered tests, base `560973cf` vs candidate | `unittest` discovery, a throwaway worktree | 1,076 vs 1,087; +10 in `test_ci_pipeline`, +1 in `test_release_orchestration`, no other module moved |
| the five changed modules alone | candidate | 35, 24, 29, 15, 7 tests, each OK |
| `check --checkpoint handoff --from-git 560973cf` | exact 0.16.0 | the retained `handoff.json` beside this file |
| run list, #413 head `02357f7f` (before) | GitHub | 2 qualifications and 2 suite runs of the head; 3 and 3 in total |
| run list, #419 head `e96160af` (after) | GitHub | 1 qualification and 1 suite run of the head; 2 and 2 in total; the candidate leg's qualification step skipped, 106 s → 28 s |
| lanes at `e96160af` | GitHub | Candidate Evidence, Publication Rehearsal, Predecessor Evaluator Assessment, CodeQL: success; Engineering Harness: `QGP-G4I-EVIDENCE` blocked on the handoff evidence this commit adds, `QGP-G4I-PATHS` pass |
| pins | `git grep` both refs | 52 of 52 in pin form, from 28; floating 15 → 0; digests with an inexact tag comment 9 → 0 |
| retired-name lines | `git grep` both refs | 28 → 4, all in `predecessor-evaluator-assessment.yml`, all the two exempt literals |
| negative controls | scratch copy | mutation 1: 3 failures naming `release-qualification.yml`; mutation 2: the file and the line; mutation 3: exit 2; mutation 4: a retired name in a comment fails |

## Change set

Against `main` at `560973cf`, 21 files, 586 insertions and 177 deletions
before this packet:

| Path | + | − | What |
| --- | ---: | ---: | --- |
| `.github/workflows/candidate-evidence.yml` | 61 | 55 | pins, the `env` block, the two removed re-checks, `upgrade-rehearsal`, the header |
| `.github/workflows/release-qualification.yml` | 21 | 9 | the release-record guards, pins, `"3.11"`, the two-mode header |
| `.github/workflows/predecessor-evaluator-assessment.yml` | 29 | 25 | the renames, pins, the header |
| `.github/workflows/publish-pypi.yml` | 23 | 20 | the unconditional flag, pins, the exact tag comment, the header |
| `.github/workflows/pages-publication.yml` | 15 | 2 | the `deploy` concurrency group, the probe comment, the header |
| `.github/workflows/release-candidate-replay.yml` | 13 | 3 | pins, `"3.11"`, the header |
| `.github/workflows/publication-rehearsal.yml` | 7 | 3 | the header |
| `.github/workflows/publish-dashboard-pages.yml` | 5 | 2 | the header's trigger-policy clause only |
| `repository_tools/release_distribution.py` | 24 | 15 | `create_manifest` requires the recipe |
| `scripts/create_release_bundle_manifest.py` | 2 | 1 | `--build-recipe` required |
| `tests/test_ci_pipeline.py` | 167 | 11 | `PipelineHygieneTests`, the renamed keys |
| `tests/test_release_orchestration.py` | 60 | 4 | the manifest refusal; two tests pass a recipe |
| `tests/test_integration_package.py` | 14 | 7 | `upgrade-rehearsal`, the v4.4.0 digest, the `INTEGRATION_*` reads |
| `tests/test_pypi_publishing.py` | 9 | 5 | the unconditional flag, `# v1.14.2` |
| `tests/test_standard_repository_lifecycle.py` | 9 | 5 | `upgrade-rehearsal`; 0 floating and 6 pinned checkouts |
| `docs/notes/ci-pipeline.md` | 69 | 0 | "After `WO-CIP-007`" |
| `docs/notes/developing-se-harness.md` | 4 | 4 | `upgrade-rehearsal` ×4; the candidate-leg sentence |
| `docs/notes/release-publication-rehearsal.md` | 1 | 1 | the candidate-mode bullet |
| `docs/engineering/ci-pipeline/specifications/SPEC-CIP-001.md` | 41 | 1 | `## Amendment record`; `updated` |
| `docs/engineering/ci-pipeline/README.md` | 4 | 3 | the wave 5 entry; the draft-authorizes-nothing paragraph |
| `docs/engineering/ci-pipeline/work-orders/WO-CIP-007.md` | 8 | 1 | the start event |

Plus this packet: `run-lists.md`, `pin-and-version-inventory.md`,
`retired-names.md`, `manifest-refusal.md`, `validate-and-doctor.md`,
`negative-controls.md`, `lanes-at-head.md`, this file and `handoff.json`.
Every path is inside `[execution_scope]`; the hosted lane's `QGP-G4I-PATHS`
passed at `e96160af`.

## Disclosures

1. `main` moved from `fae52e1b` to `560973cf` (#407, #412, #414) while this
   work order was in progress and was merged in, never rebased. No path this
   work order changes moved on `main` (`git diff fae52e1b 560973cf` is empty
   over `.github/`, `scripts/`, `repository_tools/release_distribution.py`
   and the five test modules), and every reading in this packet was taken
   again after the merge. The before-figures are stated at both refs.
2. The before run-list reading is #413's, not #414's: #414 was the top of a
   three-deep stack and its head carried two `pull_request` runs of every
   workflow at the same second, which doubles every count for a reason
   outside `SPEC-CIP-003`.
3. `WO-CIP-007`'s "Completion report format" ends "the completion decision is
   the engineering owner's", while its approval reason and `[delegation]
   class = "execution"` delegate `DR-WO-COMPLETE` to `delegated-executor`
   under the green `validate` gate, and the start event was already taken on
   that route. The two sentences of one work order disagree; this handoff
   proceeds on the delegated route the lifecycle events and the approval name,
   and the owner may refuse the completion by rejecting the pull request. The
   sentence is a candidate for the amendment record of a later repair.
4. `ARCH-CIP-001` line 43 and `REQ-CIP-002` lines 27, 29, 41 and 49 still
   describe the job as `governance-migration`. Neither path is in
   `[execution_scope]`, which admits `specifications/`, `REQ-CIP-008` and
   `REQ-CIP-009` only; both are owed an amendment under a later work order.
5. Three headers (`publish-dashboard-pages.yml`, `publish-pypi.yml`,
   `release-qualification.yml`) gained an explicit `Trigger policy
   (SPEC-CIP-001 CIP-TRG):` clause that the header test requires and the
   files did not carry; `publish-dashboard-pages.yml` changes for that
   clause alone. `CIP-ONE-017` obliges every changed header to describe the
   file per CIP-DOC 4, which names the trigger policy.
6. Workflow YAML grew, 2,082 to 2,137 lines: the guards, the `env` block and
   the headers are text and only two inline re-checks were deleted. The
   work order's "about sixty lines across eight workflows" undercounted; the
   diff is 174 insertions and 119 deletions across them, most of them pins.
7. Cross-file action majors still differ by design: the two candidate lanes
   are on `actions/checkout` v4.4.0 and `actions/setup-python` v5.6.0, the
   five release-path files on v7.0.1 and v7.0.0. The test enforces one
   digest per action inside one file, which is what `SPEC-CIP-003`'s "Not
   decided here" leaves to this work order.
8. `test_every_public_action_takes_the_pin_form`'s pattern admits a
   `.postN` suffix on the tag (`# v1.2.3.post1`) that `VER-CIP-003`'s
   `# v\d+\.\d+\.\d+` does not spell out; such a tag is still "the exact tag
   the digest was peeled from" (`SPEC-CIP-003`, Terms). No pin carries one.
9. Mutation 4 of `negative-controls.md` was not planned by `VER-CIP-003`: the
   retired-name test bit on a literal inside a comment while this change was
   being drafted, which is recorded because it proves the guard reads prose.
10. The suite's two Windows-only names are this machine's documented
    baseline (`WO-TST-004`; the handoffs of `WO-AUT-004`, `WO-ECP-012`,
    `WO-CIP-006`): the `AGENTS.md` owner region reads 6,024 CRLF bytes
    against a 6,000 bound and is 5,969 as committed LF, and an `rmtree` of a
    temporary `.git` raises `WinError 5`. `AGENTS.md` is not in the change
    set; the hosted Linux lane is the governing suite reading and passed.
11. The managed lane at `e96160af` is red for `QGP-G4I-EVIDENCE` only: the
    handoff evidence did not yet exist in the tree. The scope predicate
    passed. The lane is read again at the commit that adds this packet and
    at the record head, and its readings go in the completion and
    preparation events.
12. The Pages concurrency group is verified by test and inspection only; its
    first live observation is the next release or dashboard publication, as
    `VER-CIP-003`'s residual uncertainty records.
13. The message of commit `bcc0c04b` says "floating tags 18 to 0". Measured
    at `560973cf`, the 24 lines not in the pin form were 15 floating tags and
    9 digests with an inexact tag comment; the message overcounted the first
    class. The note, the inventory and this file carry the measured figures,
    and the commit is left as written rather than rewritten on a pushed
    branch whose lanes have already read it.
