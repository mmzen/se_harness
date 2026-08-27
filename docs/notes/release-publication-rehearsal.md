# Rehearsing the credential-free publication path

<!-- Target expertise: 6/10. The score describes the knowledge expected from the reader, not the quality or complexity of the document. -->

> This is a repository-specific control for `mmzen/se_harness`. It is not installed into consumer repositories, `harnessctl` exposes no rehearsal command, and a rehearsal result grants no verification, release, publication, deployment, or evaluator-adoption authority.

## One definition, two callers

The credential-free half of a release — resolve the record, qualify the exact candidate, replay its bound recipe twice, verify the rebuilt bundle against the record — is written once, as the reusable workflow `.github/workflows/release-qualification.yml`. Two workflows call it:

- `.github/workflows/publish-pypi.yml`, the authorized last mile, calls it in `release-record` mode for the released record it was dispatched with. That job has no steps of its own.
- `.github/workflows/publication-rehearsal.yml` calls it on every pull request and push to `main`, in `candidate` mode for the commit under review, and in `release-record` mode against the newest ready or released schema-2 record when one exists (or the one a dispatch names).

Because the release invokes the definition rather than a copy of it, what was rehearsed is what runs. This replaced, under `WO-CIP-002` and `ADR-CIP-001`, the mechanism `WO-RLO-005` introduced: a Python re-implementation of the qualification (`rehearse_publication.py`, 3,187 lines) kept aligned with the orchestrator by a hand-written YAML reader and a file of per-step digests that every workflow edit had to refresh. `CAP-RLO-003` — rehearse the last mile before release approval — is now evidenced by the rehearsal run itself, not by a digest comparison.

## What a rehearsal proves

- `candidate` mode: the commit qualifies as candidate-controlled, its suite passes, and its own `release/build-recipe.json` produces byte-identical distributions across two fresh builds on the pinned Linux/amd64 producer. A candidate that could not be released by recipe fails here, on the pull request, not during a release.
- `release-record` mode: the record resolves to one plan, the bound recipe replays byte-identically, and the rebuilt bundle matches the record's declared digests. Without a schema-2 ready or released record the job is skipped and the run's summary says why; it is not a failure.

The definition runs on `ubuntu-latest` only. The recipe producer is a Linux/amd64 container, and the release runs the same definition on the same runner type; the Windows leg of the earlier rehearsal exercised the legacy schema-1 build path, which no longer exists.

## Running it yourself

```bash
gh workflow run publication-rehearsal.yml --ref <branch>
gh workflow run publication-rehearsal.yml --ref <branch> -f release_record=RLS-SEH-013
```

Retained artifacts: `qualification-candidate-<sha>` and, in record mode, `qualification-release-record-<RLS>` and `release-bundle-<RLS>` (inert bytes, two-day retention).

## What it does not prove

It does not exercise the credentialed jobs — tag and GitHub Release, PyPI, Pages — which are reviewed as code and run only under the release dispatch and its environment decisions. It does not make any lifecycle transition.

## Operational boundary

`contents: read`, no secret input, no environment. The reusable definition declares the same and refuses a schema-1 record.
