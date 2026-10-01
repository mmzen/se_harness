# WO-RLO-012 verification assessment

The bounded publication correction passes VER-RLO-009 on Windows. The
governing evaluator is exact public 0.20.0, outside the checkout. The final
implementation and tests were exercised at
49c3878ff6bc05168903b39d2b9158546aebaf96. `tested-files.json` proves their
bytes; later completion/evidence commits preserve them. The prepared VREC
will also run the focused suites against its exact committed candidate.

| Criterion | Result | Retained evidence |
| --- | --- | --- |
| PUB01: first complete released binding | Pass | `correction030-focused-final2-1001.json`: 69 tests; correction is found without replaying a lifecycle transition, and later unrelated history is not selected. |
| PUB02: maintenance identity and refusals | Pass | The same suites accept the exact candidate lock and reject malformed governance identities, wrong evidence digests, identities matching neither lock, missing proof, duplicates and mismatched tags. |
| PUB03: preserve release and verification | Pass | `tag-correction.json`, `RLS-SEH-030-before.txt`, `preservation.json`: only the tag line was added; the VREC and both evaluator evidence files remain byte-identical. |
| PUB04: real record resolution | Pass, local rehearsal | `correction030-final-rehearsal-1001.json` and `publication-plan.json`: v0.20.1, candidate b9af631b850c495eace9807361ed3ec3e36a10b2 and the original wheel, sdist and evaluator evidence digests. This disposable local main is not merged authority. |
| PUB05: repository checks and instructions | Pass locally | `correction030-full-final-1001.json`: 1,189 tests, 18 skips. Validation: zero errors and 54 unrelated warnings. Review preflight passes. The release instructions name --tag and the actual before-dispatch resolver command. |

## Review and recovery

The first three regression cases failed against the original helpers as
expected. Initial repair passed the focused and full suites. Review then
found that an empty main evaluator identity could reach the candidate fallback;
`correction030-review-empty-lock-1001.json` retains that reproduction.
The stricter guard first changed two existing selection error messages;
`correction030-focused-final-1001.json` retains those failures. The final
guard applies to evidence matching only, preserving selection diagnostics.
Final focused and full suites pass. No failed observation was replaced.

The change reuses the existing one-record publication interface. Candidate
locks are read as inert Git data only. Existing evidence schema, digest,
environment, archive, tag, main-history and distribution checks remain.
No template, packaged runtime, workflow privilege or current evaluator changed.

## Limits and pending decisions

The 18 full-suite skips are retained in the runner verdict; no skipped check
is claimed as executed. Hosted CI, human verification, push/PR, merge and
publication are not established by these local results. No live release tag,
GitHub Release, PyPI package, marketplace branch or latest/last marker changed.
RLS-SEH-030 remains released with its original decision and candidate. The
correction itself requires the separate human decision on VREC-RLO-012.
