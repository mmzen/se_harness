# Repository-specific Agent Instructions

## Commands

- Setup: `python -m pip install -e .`
- Test: `python scripts/run_tests.py` (parallel, same verdict); canonical serial reference `python -m unittest discover -s tests -p "test_*.py"`; `--scale full` or `SE_HARNESS_TEST_SCALE=full` for the 1,000-artifact scale tests.
- Distribution checks: `python scripts/validate_release_distributions.py --root .`
- CLI smoke check: `python -m se_harness --help`
- Lint or format: none is configured. Do not invent one as a required check.
- CLI entry point: `se_harness/cli.py`; package and script declarations: `pyproject.toml`.

The release-build, release-binding, and last-mile publication sequences are
written in `docs/notes/developing-se-harness.md#release-sequences`. Read that
section before a build, release, or publication step.

## Source layout

This checkout contains the development source for SE Harness. Product policy
documents and templates live in `templates/repository/standard/`. The evaluator's
scripts live in `se_harness/engine/` and ship inside the wheel.

Repository build and maintenance tools live in `scripts/`, including
`bind_release_distribution.py`, `check_portable_release_surface.py`,
`create_release_bundle_manifest.py`, `normalize_sdist.py`,
`replay_release_build.py`, `validate_release_distributions.py`, and the test
runner. The engineering domain index is `docs/engineering/README.md`.

## Change and test constraints

- Add deterministic boundary and failure tests for installer, integrity, preflight, provenance, workflow, and release behavior.
- Treat target paths, repository content, lock data, artifact metadata, and pull-request text as untrusted input.
- Preserve owner content during upgrades. Reject ambiguous or customized inputs before writing partially.
- Preserve unrelated changes.
