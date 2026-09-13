# WO-KIS-003 implementation evidence

Candidate: `e0670743bfee3d452d5707d2479f8a8f361576da`. Base: `573c5f3c0f49c009aa13c9a3b0d8a9c9ff76162f`. Governing checker: isolated released 0.17.0.
Work is in progress pending hosted checks and delegated completion.

| Check | Observed result | Evidence |
| --- | --- | --- |
| K13 | An unrelated checksum field no longer triggers a global census. Consumed bad evidence and package hashes still fail. | LocalFormatTests; ContractTableTests; EvaluatorIdentityTests |
| K14 | Moving an effective Git attribute outside its comment block gives the same hash assessment. Incorrect attributes or bound bytes fail. | LocalFormatTests; FreshCheckoutMatrixTests; ByteExactSurfaceTests |
| K15 | A real external environment works through a Windows junction, including ordinary evidence creation. Candidate source imported as the governing checker is refused. The same real-environment test exercises a directory symlink on Ubuntu CI. | InterpreterPathsTests; installed acceptance |
| K16 | Identity returns the Python version; executable hashing and its digest field were removed. | InterpreterPathsTests; installed identity |
| K17 | An ignored PYTHONPATH pointing to the checkout passes under -I. An effective candidate import fails before writing. | InterpreterPathsTests; kiss-real-candidate-import-refused |
| K18 | The module route works with the console launcher physically absent. Explicit selection of that missing launcher fails. | kiss-capture; kiss-broken-console |
| K19 | Ordinary writes produce origin/version evidence without claiming a payload measurement. A harmless installed source comment permits an ordinary write but fails doctor. | MutationGuardTests; installed acceptance |
| K20 | A package-name installation without an archive receipt prepares a ready release in a disposable fixture. Full payload inspection remains required, as do release artifact hashes. | kiss-no-receipt-release; release qualification/distribution tests |
| K21 | Pretty-printed new JSON evidence validates with its original digest. Changed identities and duplicate keys fail. Legacy v1 keeps its canonical-byte rule. | MutationGuardTests; GitReleaseFixture; RevisionCliTests; kiss-pretty-evidence |
| K22 | Edited guides, templates and settings survive doctor and an upgrade. Explicit replacement affects the selected guide. Machine-policy edits and version mismatch fail; owner text around fragments survives. | HarnessCtlTests; ConfigurationSurfaceTests; installed acceptance |

The exact committed source suite passed **1,085 tests, 16 skipped**, on Windows/Python 3.14.
Command: `python scripts/run_tests.py --workers 4 --scale full --timings ../work/kis003-source-timings.json`.
Recorded duration: 138.496 seconds; no speedup claim is made.

A non-promotable wheel from the exact Git commit passed installed acceptance under
Python 3.12 outside the checkout. Wheel SHA-256: `e075ca9baee2f31de34c25384ea119ec77662339379773354fe44ee81d5b82de`.
The fixture has no console launcher, uses a linked environment, inherits an ignored
PYTHONPATH and installs by package name without a wheel receipt. Its ready release is
test data only. No project release or verification decision was made.

The released doctor, graph, review and scope checks passed. Candidate graph validation
and all 14 release-distribution records passed. Hosted Linux/Windows results are pending.
Root managed files and historical VREC/RLS records are unchanged; the installed root
still uses 0.17.0. Owner approval, path boundaries, atomic rollback and published package
hashes remain checked.

Locked files/fragments fall from 38 to 7 for a standard repository installation.
Source: 130 lines added, 546 removed.
Tests: 279 lines added, 1816 removed.
The interpreter helper shrank from 362 to 175 lines;
its tests from 1158 to 171.
The hash helper shrank from 584 to 387 lines.

Removed tests modelled rejected parent links, binary hashes, a global checksum-field
census and designated attribute regions. Tests for supported environments and real
failures remain. Initial test runs exposed obsolete ownership/documentation expectations
and a config newline issue; those were corrected before this passing run. Review also
found and fixed POSIX linked-launcher evidence normalization.
