# WO-KIS-004 implementation evidence

Source candidate: `7fc826459bffaa2faec880340bf05a0a8274a7b8`. Base: `4ca68474a7b3c6c74c932732a75b297aff8ba89d`. Governing checker: isolated released 0.17.0.
Work is implemented through delegated completion; owner verification is pending.

| Check | Change | Observed result |
| --- | --- | --- |
| K23 | One explicitly verified final candidate covers the whole release. Earlier records can have different commits and shared integration evidence needs no filename key. | The actual installed CLI tested two earlier changes and their final integration. Incomplete scope and an unverified final record refused release. Earlier records kept their bytes. |
| K24 | Explicit refresh creates a new ready record after comparing relevant Git entries, governing inputs and evidence. The original is preserved. | A real rebase passed on Windows. Changed code, a governing guide, a requirement or retained evidence refused reuse. Verified history refused refresh. The CLI never verified either ready record. |
| K30 | The commit-trailer census is advisory; its approval gate is removed. Old census JSON and the retired evaluator remain readable. | A fixture with four untrailed commits produced advice and prepared a release after final verification, without exemptions. Owner-scope approval and final coverage tests passed. |
| K38 | New schema-2 results declare machine-fields-v1 and hash machine data, not human prose. Retained unmarked results keep the legacy digest reader. | Wording changes preserved the digest. Candidate, state and argv changes altered it. Old human-block pins, guide-version comparison ladders and duplicate wording tests were removed. |

The committed source passed **1,085 tests, 16 skipped**, with full scale on
Windows/Python 3.14. Command: `python scripts/run_tests.py --workers 4 --scale full --timings ../work/kis004-source-timings.json`.
Recorded duration: 124.668 seconds; no speedup claim is made.

Real installed-wheel acceptance passed under isolated Python 3.12 in disposable
repositories. Wheel source: `7fc826459bffaa2faec880340bf05a0a8274a7b8`; wheel SHA-256:
`e1b77c5503c5a404db2451b58a2aaa3fc5d79cf83e53e11b9ead2747e72717c8`. Source tests and installed acceptance identify their actual
commits; runtime, templates and pyproject bytes match the selected candidate.
The wheel is non-promotable and remains outside the repository.

Released doctor, graph, review and scope checks passed. Candidate graph and all
14 distribution records passed. All hosted checks passed, including Linux and Windows upgrade and integration-package checks. Exact check URLs are in ci-implementation.json.

Missing owner verification and incomplete release scope still fail. Existing
path-boundary, atomic-write and corrupt-package tests passed. No workflow
permissions changed. Root managed files and historical VREC/RLS records are
unchanged. New ready records, historical readers and the installed 0.17.0 root
retain their distinct authority; this patch does not upgrade the live root.

Source lines: 163 added, 99 removed.
Test lines: 188 added, 325 removed.
The explicit refresh operation adds code; removing the release gate and prose
pins reduces the restrictions. No new receipt store or background watcher exists.

Initial failures came from obsolete census/wording expectations and the generated
diagnostic index. The final source run above is the passing result.
