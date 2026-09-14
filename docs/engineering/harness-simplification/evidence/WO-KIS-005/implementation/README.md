# WO-KIS-005 implementation evidence

Source candidate: `3c4da9abda8cdd77da21dbf83bd4fa1cffc640dd`. Base: `0f9aa9bae7795034b21b5743a0e51e5c12b6133b`. Governing checker: isolated released 0.17.0.
Work is implemented through delegated completion; owner verification is pending.

| Check | Simpler behavior | Observed result |
| --- | --- | --- |
| K25 | Snapshot only disposable package-test targets. Reject scenario targets outside that directory. | The real installed runner passed all ten scenarios with a 256 MiB unrelated checkout file. Largest target snapshot: 228,470 bytes. The outside-target attempt was refused. |
| K26 | Skip deterministic candidate replay on ordinary runtime/documentation changes. | Tests of real Git changes and the CLI report a successful skip; packaging changes and explicit release preparation select replay. Removed build inputs also select replay. |
| K27 | Skip earlier-release qualification on ordinary changes. | The shared decision selects both legs for publication implementation/workflows and explicit preparation. Candidate jobs retain read-only permissions; source tests and Windows/Ubuntu package jobs remain. |
| K28 | Resume an incomplete unpublished draft by uploading only missing required assets. | A simulated interrupted upload retained its successful file, uploaded only the remaining file on retry, and made no changes to an exact published release. Conflicting required hashes and incomplete published releases were refused. |
| K29 | Ignore unrelated GitHub Release attachments. | All required files plus a screenshot passed classification. Wrong required bytes failed. The PyPI download step selects only wheel, sdist and SHA256SUMS. |

Source validation: **1,092 tests run, 16 skipped**, full scale, on Windows/Python 3.14.
Command: `python scripts/run_tests.py --workers 4 --scale full --timings ../work/kis005-final-timings.json`.
Recorded duration: 127.923 seconds; this is not a before/after speed measurement.

Real installed acceptance used Python 3.12 and a non-promotable wheel built from
`3c4da9abda8cdd77da21dbf83bd4fa1cffc640dd`, SHA-256 `cfc53430122344bb1c58a88cc9c888dccb13caf8716ebe90403e6cbad27d5f20`. The new runner was exercised
from that installed candidate; this test does not make 0.18.0 a released governor.
Actual checker origin and each target snapshot size are in installed-acceptance.json.
The supplied checkout file was not part of any snapshot. No copied repository or
wheel is retained in this evidence directory.

The first real installed run failed at safe-upgrade: Windows console wrappers drop
`.exe` from their reported name, and the selected-route check looked for a missing
file (MG005/RID011). The one-file scope amendment adds the existing executable lookup.
The final full suite and fresh installed wheel include that fix. Required origin
checks remain active. The initial source suite also exposed one obsolete workflow
header assertion; the short header now states its trigger policy.

Candidate/released graph, released review/scope and all 14 distribution records
passed. Root managed files and historical VREC/RLS records are unchanged.
All hosted checks passed, including Linux and Windows package/upgrade checks and both release rehearsals. Exact check URLs are in ci-implementation.json.

Ordinary PRs now skip up to four deterministic release builds and the earlier
release's qualification/tests. This PR changes publication code, so it should
exercise both rehearsals. The selector uses shallow history and one shared path
decision; the final check reports skipped legs explicitly. Source regression and
installed-package coverage still run on ordinary PRs.

Source lines: 112 added, 15 removed.
Test lines: 176 added, 8 removed.
This cut removes repeated work; the small selector and retry implementation add code.
No live release, PyPI upload, root upgrade or owner verification was performed.
Publication retry tests use a simulated provider; real publishing remains a separately
authorized release action behind the existing permissions and environment decisions.
