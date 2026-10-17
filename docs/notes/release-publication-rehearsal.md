# Release rehearsals

Ordinary PRs keep source tests, installed-package checks on Windows and Ubuntu,
and managed validation. They skip the two release rehearsals when build and
publication inputs have not changed (WO-KIS-005).

| Change | Candidate build replay | Earlier release rehearsal |
| --- | --- | --- |
| Documentation or ordinary runtime code | Skip | Skip |
| Packaging, build recipe, build scripts, or publication tests | Run | Skip |
| Publication implementation or workflows | Run | Run |
| Manual release preparation | Run | Run |

`.github/scripts/publish_release.py select-rehearsals` makes one decision from
the changed Git paths. It compares the PR base commit with the checked-out merge
commit, or the previous main commit with the new main commit. Removed and renamed
inputs count too. An unreadable comparison fails instead of claiming a skip.
The workflow uses a shallow checkout and fetches only the comparison commit.

The `Publication rehearsal` check runs even when neither leg is needed. It reports
a successful skip, or fails if a selected leg fails. No scheduled run is added.

Both selected legs still use `.github/workflows/release-qualification.yml`.
Candidate mode builds twice and compares bytes. Record mode qualifies and tests
the recorded candidate, replays its recipe, and checks the recorded hashes.
On a PR, the earlier record comes from its base commit. If no suitable record
exists, that leg is skipped with an explanation.

The earlier-record caller sets `historical: true`. It uses the same resolver,
candidate checks and recipe replay, but checks approved documentation at its
recorded commit and release integration rather than requiring today's main
documentation to match an old release. All other provenance checks remain.
The resolver's `--historical` output uses a qualification-only schema. Only
the inert bundle and manifest verifiers accept it; publication commands refuse it.
Historical rehearsal does not upload a `release-bundle-<RLS>` for publication.

The publication caller keeps the default `historical: false`. It still checks
current main's documentation against the approved inputs before delivery. A
passing historical rehearsal does not establish current publication readiness.

When the earlier-record leg is selected, the same rehearsal also runs the
complete-delivery fixture tests. These use disposable Git repositories, inert
package bytes and simulated provider responses. They exercise frozen approval
bindings, both host payloads, all five surfaces, interrupted marketplace/marker
writes, conflicting refs, unknown responses and unavailable public checks. They
reuse the publisher and delivery checker; they do not create another build lane.
The summary fails if this recovery rehearsal fails. No fixture calls a live
publication API or claims native host qualification.

Before release, explicitly run both legs:

```bash
gh workflow run publication-rehearsal.yml --ref <release-branch>
gh workflow run publication-rehearsal.yml --ref <release-branch> -f release_record=RLS-SEH-013
```

The authorized publication workflow continues to qualify the released record
before any publishing job. Rehearsals use read-only permission and have no
publication credentials or protected environment. They do not approve or publish.
The recipe runs on Linux; ordinary installed-package coverage retains both
Windows and Ubuntu.

Results stay in the existing CI artifacts: `qualification-candidate-<sha>` and
`qualification-release-record-<RLS>`. The latter retains the resolved subject
and manifest comparison. Only live qualification transfers
`release-bundle-<RLS>` (two-day retention) to publication jobs.

## Retry an interrupted draft

Rerun the authorized publication workflow. It checks the existing required assets
by name and SHA-256, then uploads only missing files to an unpublished draft.
Matching files and unrelated attachments are left alone. A conflicting required
file stops the attempt and names the file. Missing files on an already published
release cannot be added through this retry path.

The workflow checks the complete required set again before publishing the draft.
The PyPI job downloads only the required wheel, source archive and checksum file;
a screenshot attached to the GitHub Release does not become a package error.
Published package bytes remain immutable, and PyPI keeps its existing protected
environment and owner decision.
