# Publication lock correction review

WO-RLO-010 corrects the two publication readers that rejected the valid
schema-4 plugin-owned lock. Both readers use one small local schema/provider
check; they preserve the existing identity, evidence, integrity and provenance
checks. No candidate-package or plugin code is imported.

## Observed results

- Before the fix, three selected regression methods reproduced both refusals
  (four errors, including the historical-binding subcase).
- All 65 focused publication tests passed.
- The full source suite passed on Windows Python 3.14.6 at implementation
  commit `8ac5a9d0aafb4f15b54f8907b081eb2c84e25d33`: 1,126 tests, 16 skips,
  full scale, four workers, 207.515 seconds.
- The released 0.18.0 evaluator passed doctor, graph validation, review
  preflight and the Git-derived scope check. Distribution validation and
  candidate CLI help passed.
- Evaluator acquisition and full release-plan resolution passed against the
  unchanged merged governance snapshot `523ff825773e05c970c041ecee5c22bfabedaa3f`.
  The plan retains candidate `30d4dba2a088c4f83756c1241b76cdab40f796bd`,
  version 0.19.0, tag v0.19.0 and every reviewed distribution digest.

## Review and limits

LOCK01-LOCK04 in VER-RLO-007 are covered by the focused regressions and frozen
snapshot observations. LOCK05 is covered by the full suite, repository checks,
preservation review and governed handoff. The four added test methods exercise
the real compatibility failures and distinct refusal boundaries. Existing
publication tests still run; no assertion or skip was removed or weakened.

The source suite ran in an isolated checkout with command-local
`core.autocrlf=false`, using the committed fixture bytes, and
`core.longpaths=true` for retained historical long paths. The first checkout
attempt failed on one such long path; Git removed that incomplete checkout
before the successful retry. No fixture or persistent Git setting changed.
The known converted-Windows-checkout fixture limitation is not fixed by this
work. All 16 existing platform skips remain visible in the retained result.

All pre-existing formal records, the root lock, the release candidate and
archive identities remain unchanged. The final candidate may add completion
and evidence after the tested implementation; its executable blobs must match
that tested commit. This is a repository publication-helper correction, not a
new checker build. No merge, tag, publication or deployment is performed.
Hosted CI remains required before integration. The ready VREC will require the
human assurance decision; this report does not supply it.
