# WO-KIS-004 implementation evidence

Source candidate: `7b31e8296a90709bcd8ffcbb89db11d5a82c2635`. Base: `4ca68474a7b3c6c74c932732a75b297aff8ba89d`. Governing checker: isolated released 0.17.0.
Work is in progress pending hosted checks and delegated completion.

| Check | Change | Observed result |
| --- | --- | --- |
| K23 | One explicitly verified final candidate covers the whole release. Earlier records can have different commits and shared integration evidence needs no filename key. | The actual installed CLI tested two earlier changes and their final integration. Incomplete scope and an unverified final record refused release. Earlier records kept their bytes. |
| K24 | Explicit refresh creates a new ready record after comparing relevant Git entries, governing inputs and evidence. The original is preserved. | A real rebase passed on Windows. Changed code, a governing guide, a requirement or retained evidence refused reuse. Verified history refused refresh. The CLI never verified either ready record. |
| K30 | The commit-trailer census is advisory; its approval gate is removed. Old census JSON and the retired evaluator remain readable. | A fixture with four untrailed commits produced advice and prepared a release after final verification, without exemptions. Owner-scope approval and final coverage tests passed. |
| K38 | New schema-2 results declare machine-fields-v1 and hash machine data, not human prose. Retained unmarked results keep the legacy digest reader. | Wording changes preserved the digest. Candidate, state and argv changes altered it. Old human-block pins, guide-version comparison ladders and duplicate wording tests were removed. |

The committed source passed **1,085 tests, 16 skipped**, with full scale on
Windows/Python 3.14. Command: `python scripts/run_tests.py --workers 4 --scale full --timings ../work/kis004-source-timings.json`.
Recorded duration: 124.783 seconds; no speedup claim is made.

Real installed-wheel acceptance passed under isolated Python 3.12 in disposable
repositories. Wheel source: `7b31e8296a90709bcd8ffcbb89db11d5a82c2635`; wheel SHA-256:
`9175b5a7f20f3f79001118399c6d00da9d2dbede507cd11f5583714eccdd2fa4`. Source tests and installed acceptance identify their actual
commits; runtime, templates and pyproject bytes match the selected candidate.
The wheel is non-promotable and remains outside the repository.

Released doctor, graph, review and scope checks passed. Candidate graph and all
14 distribution records passed. Hosted Linux/Windows results are pending.

Missing owner verification and incomplete release scope still fail. Existing
path-boundary, atomic-write and corrupt-package tests passed. No workflow
permissions changed. Root managed files and historical VREC/RLS records are
unchanged. New ready records, historical readers and the installed 0.17.0 root
retain their distinct authority; this patch does not upgrade the live root.

Source lines: 157 added, 99 removed.
Test lines: 185 added, 325 removed.
The explicit refresh operation adds code; removing the release gate and prose
pins reduces the restrictions. No new receipt store or background watcher exists.

Initial failures came from obsolete census/wording expectations and the generated
diagnostic index. The final source run above is the passing result.
