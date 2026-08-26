# CAP-RLO-003 after WO-CIP-002: how the rehearsal is evidenced

Retained under `WO-CIP-002` on 2026-08-26. This note records a change of
mechanism, not of outcome, for `CAP-RLO-003` ("rehearse the credential-free
last mile before release approval") and `WO-RLO-005`, which implemented it.

## Before

`.github/scripts/rehearse_publication.py` re-implemented the `qualify` leg of
`publish-pypi.yml` in Python and ran it on Linux and Windows; a `divergence`
job parsed `publish-pypi.yml` with a hand-written YAML reader and compared a
digest of each normalized `run:` body with
`publication_rehearsal_mechanics.json`. The evidence that the rehearsal
covered the release was the digest comparison.

## After

The qualification is one reusable workflow,
`.github/workflows/release-qualification.yml`, and both `publish-pypi.yml`
and `publication-rehearsal.yml` invoke it (`ADR-CIP-001`). The evidence that
the rehearsal covers the release is that the two callers name the same
definition; `tests/test_ci_pipeline.py::QualificationDefinitionTests` asserts
it, and the rehearsal run on every pull request executes it. The digest file,
the reader, the Python copy and `tests/test_publication_rehearsal.py` are
removed.

## What changed in coverage

- The Windows leg is gone with the legacy schema-1 build path it exercised.
  The definition runs where the release runs, on `ubuntu-latest`.
- `release-record` mode has a subject only when a ready or released schema-2
  record exists; until 0.7.0 is prepared, only `candidate` mode runs, and the
  run's summary says so.
- `candidate` mode now replays the candidate's own recipe twice, which the
  earlier rehearsal did not do.

`CAP-RLO-003` and `WO-RLO-005` are unchanged as artifacts; this note is the
disclosure their evidence trail needs.
