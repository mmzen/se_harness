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

Results stay in the existing CI artifacts: `qualification-candidate-<sha>`,
`qualification-release-record-<RLS>` and `release-bundle-<RLS>` (two-day retention).

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
