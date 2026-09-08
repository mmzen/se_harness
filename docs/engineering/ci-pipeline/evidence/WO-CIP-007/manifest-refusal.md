# WO-CIP-007: the bundle manifest writer refuses schema 1

`SPEC-CIP-003` `CIP-ONE-013`; `VER-CIP-003`'s "manifest schema" row and its
fourth acceptance scenario.

## What changed

`repository_tools.release_distribution.create_manifest` took
`build_recipe: PurePosixPath | None`. With `None` it wrote a
`se-harness-release-bundle/v1` manifest and bound no recipe; with a path it
wrote `/v2` and bound the recipe and the toolchain lock. Two callers exist and
both pass a recipe: `scripts/create_release_bundle_manifest.py`, whose
`--build-recipe` was optional, and the release-qualification workflow through
that script.

After this work order there is no writer of a schema-1 manifest:

- the script's `--build-recipe` is `required=True`, so `argparse` refuses
  before `main()` runs and before any Git call;
- `create_manifest` keyword `build_recipe` is `PurePosixPath` and the function
  raises `ReleaseDistributionError` on `None` as its first statement, before
  `repository.resolve()`;
- the `schema` key is unconditionally `BUNDLE_SCHEMA_V2` and the
  recipe-binding block runs unconditionally.

Reading is untouched. `read_bundle_manifest` still accepts
`BUNDLE_SCHEMA_V1`, which is what the released schema-1 records carry
(`release-0.2.0` to `release-0.4.1`), and `validate_release_distributions.py`
still passes over all thirteen distribution-bearing records.

## Measured, 2026-09-08, Windows workstation

The script, with every other required argument present:

    $ python scripts/create_release_bundle_manifest.py \
        --commit 0000000000000000000000000000000000000000 --version 1.2.3 \
        --wheel se_harness-1.2.3-py3-none-any.whl \
        --sdist se_harness-1.2.3.tar.gz --output target/should-not-exist.json
    usage: create_release_bundle_manifest.py [-h] [--repository REPOSITORY]
                                             --commit COMMIT --version VERSION
                                             --wheel WHEEL --sdist SDIST
                                             --build-recipe BUILD_RECIPE
                                             --output OUTPUT
    create_release_bundle_manifest.py: error: the following arguments are required: --build-recipe
    exit=2
    no file written

`--build-recipe` appears in the usage line, the exit status is 2 as
`SPEC-CIP-003`'s failure table requires, and the output path does not exist:
the refusal precedes the resolution of the repository and every `git` call.

The module:

    >>> create_manifest(Path("."), "0"*40, "1.2.3", Path("w.whl"),
    ...                 Path("s.tar.gz"), build_recipe=None)
    ReleaseDistributionError: a bundle manifest must bind a candidate build
    recipe; schema-1 manifests are historical and no longer written

`BUNDLE_SCHEMA_V1` is still exported and still read:
`se-harness-release-bundle/v1`; the writer's schema is
`se-harness-release-bundle/v2`.

## Tests

`tests/test_release_orchestration.py`: 24 tests, OK (was 23).

- `test_manifest_producer_refuses_to_write_a_schema_1_bundle` is new: it runs
  the script as a subprocess from the repository root, asserts exit 2, asserts
  `--build-recipe` in `stderr`, asserts the output file was not created, and
  asserts the module raises on `build_recipe=None`.
- `test_manifest_producer_hashes_exact_files_and_candidate_tree` now passes
  `build_recipe=PurePosixPath("release/build-recipe.json")` and asserts the
  schema is v2 and `build_recipe` is bound.
- `test_schema_1_is_historical_released_only` keeps its meaning: its scratch
  repository now also holds `release/build-recipe.json` and
  `release/build-toolchain.lock`, and what the test proves is unchanged — a
  released record's `[distribution] schema = 1` is historical and still
  validates.
- `test_bundle_manifest_binds_version_commit_epoch_and_checksum_bytes` still
  builds a schema-1 payload and reads it, so the reader's schema-1 path stays
  covered by a test that does not write one.
