# WO-CIP-007: the mechanical checks refuse the mutations they claim to refuse

`VER-CIP-003` acceptance scenarios 2, 3 and 4. A test that passes against the
defect it is supposed to name is no evidence, so each new check was measured
against a mutated copy of the tree.

Method: the whole worktree was copied to a scratch directory outside the
checkout (`tar` excluding `.git` and `target`), one file mutated there, and
the tests of `CIP-ONE-016` run from the scratch copy, whose
`tests/test_ci_pipeline.py` resolves `REPOSITORY_ROOT` from its own
`__file__`. Nothing ran against the real checkout, and the scratch copy is not
a Git repository.

## Control: the unmutated scratch copy

    python -m unittest \
      tests.test_ci_pipeline.PipelineHygieneTests.test_the_qualification_definition_qualifies_and_tests_release_records_only \
      tests.test_ci_pipeline.PipelineHygieneTests.test_candidate_source_is_the_only_lane_that_qualifies_and_tests_a_pull_request \
      tests.test_ci_pipeline.PipelineHygieneTests.test_every_public_action_takes_the_pin_form
    Ran 3 tests in 0.113s — OK

## Mutation 1: remove the release-record condition (`CIP-ONE-001`)

Every `if: inputs.mode == 'release-record'` line was deleted from
`.github/workflows/release-qualification.yml` — three occurrences, the
qualification step among them.

    FAILED (failures=3)
    FAIL: test_the_qualification_definition_qualifies_and_tests_release_records_only
         (command='qualify complete-candidate')
    FAIL: ... (command='unittest discover')
    FAIL: ... (command='-m se_harness --help')
    AssertionError: "if: inputs.mode == 'release-record'" not found in
      'name: Qualify the exact candidate without publication credentials …'

One subtest per command, each naming the command it looked for and printing
the step that lost its guard. The file is
`release-qualification.yml`, as `VER-CIP-003` requires.

## Mutation 2: float one pin (`CIP-ONE-006`)

`actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97 # v7.0.0` in
`.github/workflows/pages-publication.yml` became `actions/setup-python@v7`,
one occurrence.

    FAILED (failures=1)
    FAIL: test_every_public_action_takes_the_pin_form
         (workflow='pages-publication.yml', uses='actions/setup-python@v7')
    AssertionError: Regex didn't match:
      '^[\w.-]+/[\w./-]+@[0-9a-f]{40} # v\d+\.\d+\.\d+(?:\.post\d+)?$'
      not found in 'actions/setup-python@v7'

The subTest names the file and the offending line. The same test also refuses a
digest with a bare-major comment such as `# v4`, and refuses two digests for
one action inside one file.

## Mutation 3: the manifest script without its recipe (`CIP-ONE-013`)

Measured on the real checkout, since the refusal writes nothing: exit 2,
usage naming `--build-recipe`, no output file. See `manifest-refusal.md`.

## Mutation 4, unplanned: a retired name in a comment (`CIP-ONE-012`)

While the new comment in the disposable-repository step of
`candidate-evidence.yml` was being drafted it named the retired command
literally, and `test_no_retired_name_survives_in_a_repository_owned_workflow`
failed on `candidate-evidence.yml`. The comment now names the script's
`FORBIDDEN_CLI` instead. The guard bites on prose, not only on identifiers,
and it strips exactly the two exempt literals before searching.

## What no mechanical check covers

`CIP-ONE-008`, the Pages concurrency group, is verified by test and inspection
only: a group is observable only when two deployments overlap, and this work
order dispatches nothing. `VER-CIP-003` records the same residual uncertainty
and defers the first live observation to the next release.
