# WO-ECP-007 implementation review

The remaining product-boundary correction is implemented and tested locally.
WO-ECP-007 remains `in_progress`. One definition-content finding remains open;
no completed handoff, ready verification record or review PR is claimed here.

## Result

The graph viewer now selects verification records from their type, status and
links. Previously it excluded `VREC-SEH-021` from its preferred verified record
selection. Equivalent records now receive equivalent treatment.

The existing wheel check now rejects repository artifact-ID literals in Python,
JavaScript, HTML (including embedded JavaScript) and JSON. It identifies the
member and location. Historical Markdown and package-description references
remain permitted. Existing package limits and retirement checks remain active.

The installation guide now states the existing readiness rule: default `init`
writes two selection files; a Git repository needs effective evidence attributes
before `doctor` passes, even before the first evidence file. Both explicit Git
integration and an equivalent owner rule were tested with an installed wheel.

## Tested identities

- Source commit: `49b4f3fb7715d42d8c096a3fdcc57ca4bc7d2e71`.
- Tree: `64f7745a96452c395efbd48815446afb11c86b2c`.
- Non-promotable candidate wheel: `se_harness-0.23.1-py3-none-any.whl`.
- Wheel SHA-256: `57bfed79d107021fb0ea3136709cf71edf57ef0db497de87719cb78d92daaaf7`.
- Formal checks used separately installed released evaluator `0.23.0`.

The wheel came from an exact Git export using the existing offline build tools.
It was installed outside disposable consumers on both platforms. Source, wheel
and installed CLI were test subjects; they did not govern this repository.

## Observed checks

| Check | Result |
| --- | --- |
| Full Windows suite, full-scale mode | 1,349 tests; exit 0; 24 skips. |
| Affected Windows modules | 120 tests; exit 0; two skips. |
| Affected Linux modules, exact commit with Git metadata | 120 tests; exit 0; no skips. |
| Installed consumers, Windows and Linux | Two-file init, missing attributes, explicit integration, owner rule, damaged attributes and owner-content preservation passed. |
| Packaged viewer, Windows and Linux | Four ID/status combinations passed on each platform; an unrelated linked record was not selected. |
| Exact wheel and installed CLI surface checks | Passed on both platforms. |
| Contaminated executable members | Python, JavaScript, HTML and JSON fixtures were rejected with a member and location on both platforms. |
| Viewer generation | Two builds and the checked-in generated file have equal bytes; builder check passed. |
| Distribution validation | All 24 distribution-bearing records passed. |
| CLI smoke | Passed. |
| Released artifact validation | 2,022 artifacts; zero errors; 65 existing warnings. |
| Historical preservation | 12,475 existing evidence paths and retained design exports unchanged; seven original definitions preserved byte-for-byte. |

Installed init and successful doctor calls each took less than 1.3 seconds on
Windows and less than 0.4 seconds on Linux, within the selected 60-second bound.
Windows skips remain skips. No full Linux suite or unrelated skill qualification
is claimed.

## Review findings and resolution

1. **Open: REQ-ECP-012 statement field.** The activated revision's body records
   the human's Git-readiness choice, but its frontmatter still contains the old
   unconditional init/commit/doctor statement. The agent omitted that field in
   the reviewed amendment. An exact statement-only correction and provenance
   link were prepared outside the repository and submitted for human authority.
   They have not been applied. Complete handoff and review publication remain
   pending this correction.
2. **Resolved: repository-ID exception.** A count-checked patch in the existing
   builder removes the exception. The retained design export is unchanged. The
   behavioral regression fails on the old viewer and passes on the generated
   candidate. No new parser, service or selection framework was introduced.
3. **Resolved: package-check coverage.** The existing bounded member scan now
   checks the specified executable suffixes. Its archive limits, dependency
   boundary, active qualification commands and adoption checks remain intact.
4. **Resolved: test setup failures.** The first Linux consumer probe followed
   the environment interpreter symlink to system Python. The retained probe now
   preserves the absolute environment path. Linux source tests were moved from
   the slow Windows filesystem mount to native storage. Two existing tests then
   required Git metadata; an independent copy of the exact commit supplied it.
   Failed transfers caused by Windows worktree and object-alternate paths are
   retained alongside the successful run. These changes affected test setup.

The implementation uses one existing builder patch and extends one existing
wheel scan. The added tests demonstrate the actual defect and its failure
boundary. Installation behavior did not need a product-code change.

## Evidence

- [Qualification summary](qualification-2026-10-17/summary.json).
- [Actual commands and results](qualification-2026-10-17/commands.json).
- [Raw transcripts, including failures](qualification-2026-10-17/transcripts.zip)
  and their [byte inventory](qualification-2026-10-17/transcript-index.json).
- [Candidate build](qualification-2026-10-17/candidate-build.json).
- Installed consumers: [Windows](qualification-2026-10-17/installed-consumer-windows.json),
  [Linux](qualification-2026-10-17/installed-consumer-linux.json).
- Actual packaged viewer outcomes and member inventory:
  [Windows](qualification-2026-10-17/packaged-viewer-windows.json),
  [Linux](qualification-2026-10-17/packaged-viewer-linux.json).
- [Preservation check](preservation.json) and the
  [authorized definition activation](definition-revisions/2026-10-17/activation.json).

The initial restrictive-shell failure, CLI-preview usage error, expected
pre-fix failures, interrupted run and later corrections remain in the raw
transcripts. A passing rerun does not erase those observations.
