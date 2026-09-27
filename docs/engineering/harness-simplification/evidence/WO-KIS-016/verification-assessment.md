# VER-KIS-009 assessment for WO-KIS-016

| Case | Observed result | Evidence |
| --- | --- | --- |
| A: named approval and start | Passed for human and agent executor previews; apply records the actual executor and preserves the approval event. | regression-before.txt; targeted-tests.txt; full-suite.json |
| B: completion and capture | Passed completion after fixture handoff and named multi-WO capture. Capture leaves the record ready and preserves the work orders. | targeted-tests.txt; full-suite.json |
| C: retained boundaries | Missing approval, missing usable scope, invalid identity, changed scope, failed completion gates and a selected WO without its grant remain blocked. | targeted-tests.txt; full-suite.json |
| D: legacy grants | Role-labelled grants and named historical explicit grants pass; absent legacy grants stay blocked. | targeted-tests.txt; full-suite.json |
| E: authority and explanation | Shared check and historical meaning retained; no new rights, schema, mode or authentication system. | implementation-review.md; complete-change-review.json |

The full Windows source suite passed at b09556ad4234c7001a4647c5522c84b5db1bc0e9 with full scale enabled.
The retained JSON records counts, skips, duration and command-local Git settings.
Distribution validation passed for all 16 distribution-bearing records.
CLI help, released doctor, graph validation and review preflight passed.
Handoff and completion results are retained separately after this assessment.

The initial regressions failed before the correction. The first full suite exposed three diagnostic-index failures; the corrected
shared refusal passed the 32 focused grant and diagnostic tests. That failure
and the operational scope-input and Git trust retries are retained and explained
in implementation-review.md.
The 52 existing graph warnings are unrelated to this selected scope.

Hosted Linux/Windows CI has not run for this branch. It remains required before
integration. Tests demonstrate candidate behavior; the installed 0.19.0 evaluator
still needs the disclosed approval encoding. No release or adoption is claimed.

Source tests run against a committed candidate in a separate checkout with Git
line-ending conversion disabled. Later evidence and lifecycle-only commits are
compared with that tested source before VREC preparation; differences are retained
in candidate-applicability.json. The VREC binds its exact final candidate commit.
