# Fixed integration archive capacity — verification assessment

The approved three-line correction passed its local checks and actual integration
package qualification. Verification acceptance remains a separate human decision.
This report covers WO-IPK-002 / VER-IPK-002 only.

## Exact tested identities

- Source head: `039443f333bea8aaa135526a99d7d4ead9c1e295`.
- GitHub tested merge: `fc7021c82512c3359ea54063671a9b8a97689fa3`.
- Complete Git trees are identical; ci-tree-comparison.json retains the comparison.
- [Candidate workflow](https://github.com/mmzen/se_harness/actions/runs/38221392430), attempt 1: all eight required jobs passed.
- Toolchain: Python 3.11.17, build 1.2.2.post1, setuptools 75.8.0, wheel 0.45.1.
- Retained wheel: `se_harness-0.22.2+pr543.gfc7021c82512-py3-none-any.whl`.
- Wheel SHA-256: `3a5a16f7fa52b5bcf9487f08984371150ac7c13bd11ab6aec910ba9e83c0b285`.
- The wheel is a non-promotable integration artifact, not a release or governor.

## Contract assessment

| Case | Result and evidence |
| --- | --- |
| CAP1 | PASS. Exactly the reviewed three lines; 19 Windows focused tests pass. The fixed 1,073,741,824-byte constant is used by both source archive checks. |
| CAP2 | PASS. Existing hostile-input and capacity tests pass. Member size/count, wheel budgets, paths, links and duplicate refusals remain unchanged. |
| CAP3 | PASS for the tested source above. Archive 564879360 bytes; expanded files 552422557 bytes; 17384 members; largest member 38637157 bytes. Every committed file is present. Two independent builds match. Windows and Linux install the same wheel; final retention passed. |
| CAP4 | Local checks PASS: 1,339 tests with 24 reported skips; distribution and CLI pass; released validation has zero errors and 63 existing warnings; scope/review pass. Required handoff and completion results are retained separately before capture. All 15,048 other existing Git blobs and modes are preserved. |

The first full suite and diagnostic failed because Windows Git rejected a long
temporary fixture path. The unchanged suite passed with process-local
core.longpaths=true. Both failures and the retry environment are retained.
No repository or global Git setting was changed. The original cap failure and
prototype failures remain recorded; skipped checks are not described as passes.

The CI archive contains exact commands, job results, platform logs, manifest,
checksums, source counts and preserved-blob comparison. The downloaded wheel
stays outside Git. The final verification candidate will also contain this
retained evidence and the implementation-completion record; its relationship
to the tested source must be reported explicitly. A different Git identity is
not claimed to have been tested by this run.

## Review and limits

The change reuses the existing constant, parser, refusal tests and CI jobs. It adds
no option, framework or source selection rule. The larger limit doubles the allowed
source budget. It does not fix performance or indefinite evidence growth.

The full Claude/Codex lifecycle observations and the two separate focused Claude
content failures remain unchanged. They are outside this correction's verification.
PR #543 remains draft and its incomplete HAG handoff is not waived. No merge,
release, deployment or service migration is authorized by these results.
