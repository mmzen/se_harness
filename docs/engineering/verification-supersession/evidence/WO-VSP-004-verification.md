# WO-VSP-004 Implementation Verification Evidence

Date: 2026-08-16

Platform: Windows, PowerShell, repository virtual environment and Python 3.11 runtime

Scope: the repository owner's explicit decision to resolve stale ready `VREC-AGR-001` after the analogous graph-maintenance cleanup

## Outcome and successor selection

On branch `governance/graph-maintenance`, `VREC-AGR-001` moved from `ready` to `superseded` with one declared `superseded_by = ["VREC-PMI-001"]` edge. The transition records `superseded_at = "2026-08-16T06:33:06Z"` and `supersession_authorized_by = "repository-owner"`.

Both proposed records technically cover `WO-AGR-001`, but `VREC-PMI-001` is the correct direct successor. `INT-VSP-001`, `REQ-VSP-002`, `REQ-VSP-006`, `SPEC-VSP-001`, `ADR-VSP-001`, and prior retained evidence explicitly define `VREC-AGR-001 -> VREC-PMI-001` as the corrective lineage. `VREC-PMI-001` adds the portable-integrity correction under `WO-PMI-001`; `VREC-SEH-001` is a later ten-work-order release aggregate and remains unchanged.

The source remains historical evidence for candidate `3f3ba521d7b19455e1f2eacb9aeea42928806aef`. Verified successor `VREC-PMI-001` remains unchanged at candidate `505e889777c3c50f544b7e6d6fe58e2f765c1fea`; it covers `WO-AGR-001` and conforms to `VER-AGR-001`. No active release record includes `VREC-AGR-001`.

No commit, push, pull request, release, tag, publication, deployment, or change to another VREC was performed under this work order.

## Provenance and field preservation

| Check | Result |
|---|---|
| Original `VREC-AGR-001` SHA-256 | `69a94e6d9782d8199a6f4733f3c895332a30aebff0e66ea1aa77ed90ae0a9557` |
| Superseded `VREC-AGR-001` SHA-256 | `b4ebb9c42ce7392987f72a0ca013b5f145319c4f9d3be85432f7d73cbaa5647b` |
| Unchanged `VREC-PMI-001` SHA-256 | `27ca3f47d9481a141f104528d1abf6b3bcdec0744fea90294619277e63cc4224` |
| Successor lifecycle | `verified` |
| Source work-order coverage | `WO-AGR-001` |
| Successor work-order coverage | `WO-AGR-001`, `WO-PMI-001` |
| Source verification contract | `VER-AGR-001` |
| Successor verification contracts | `VER-AGR-001`, `VER-PMI-001` |
| Active release back-reference | none |

Comparison with the `HEAD` source bytes confirms that `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, `evidence_paths`, `verifies_work_order`, and `conforms_to` are unchanged. Only permitted lifecycle metadata, the supersession edge, `updated`, heading, and explanatory narrative changed.

## Automated verification

Formal validation passed after the complete publication envelope entered the graph with 344 artifacts, 0 errors, and 40 existing maintenance warnings. Managed-integrity doctor passed and reported the 11 existing `W013` canonical-location advisories. Start preflight passed for in-progress `WO-VSP-004` with the complete governing manifest; review preflight passed again after rebasing onto merged `IAR-010`.

Both supported local runtimes completed the complete suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
& 'C:\Users\mathi\AppData\Local\Python\pythoncore-3.11-64\python.exe' -m unittest discover -s tests -p "test_*.py"
```

Python 3.14.6 passed 188 tests in 55.851 seconds; Python 3.11.9 passed 188 tests in 57.540 seconds. Each runtime reported 3 expected Windows symlink skips.

## Final-state verification

- Review preflight passed for implemented `WO-VSP-004` and returned the complete governing manifest.
- Two `harnessctl inspect . --json` executions were byte-identical at SHA-256 `a3a124a4ab8372c103db3a494f09d0d28d2dc2390796f3d392b0d09c195a65eb`. Each reported 344 artifacts, 1,241 relations, 72 findings (43 warning and 29 informational), 0 error findings, and 15 suggestions.
- No inspection finding references `VREC-AGR-001` or `VREC-DST-006`; both stale-ready observations are removed.
- Two Explorer generations produced the same graph snapshot SHA-256 `d87ef48dd72b146c3f71f00cf43cb1ed29b52c2464ac709c1ad42c685cb84f07` and rendered `index.html` SHA-256 `cde34935dcd9888cc08201170f30df87b827caca3fa4a176cded9dffebd1a6b9`. Each reported 344 artifacts, 1,241 relations, 43 warnings, and 0 errors.
- The focused revision-provenance, dashboard, and inspection suite passed 48 tests with 1 expected Windows symlink skip.
- `git diff --check` passed with no whitespace errors; Git emitted only the repository's normal line-ending notices.

## Residual authority boundary

This evidence proves a current working-tree implementation, not a commit-bound assurance decision. `WO-VSP-004` honestly stops at `implemented`. Any commit, push, pull request, verification record, release decision, tag, publication, deployment, or merge requires separate accountable authority.
