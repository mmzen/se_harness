# WO-VSP-003 Implementation Verification Evidence

Date: 2026-08-16

Platform: Windows, PowerShell, repository virtual environment and Python 3.11 runtime

Scope: the repository owner's explicit instruction to create a graph-maintenance branch and supersede `VREC-DST-006` by `VREC-SEH-005`

## Outcome

On branch `governance/graph-maintenance`, `VREC-DST-006` moved from `ready` to `superseded` with one declared `superseded_by = ["VREC-SEH-005"]` edge. The transition records `superseded_at = "2026-08-16T06:27:28Z"` and `supersession_authorized_by = "repository-owner"`.

The source remains historical evidence for candidate `1e3790f746e0a8fa75a00ab6b0db371a39a63675`. Verified successor `VREC-SEH-005` remains unchanged at candidate `dd06660a94f06d934adb1df0352b81e709f2ffd3`; it covers `WO-DOC-009` and conforms to `VER-DST-006`. No active release record includes `VREC-DST-006`.

No commit, push, pull request, release, tag, publication, deployment, or change to another VREC was performed under this work order.

## Provenance and field preservation

| Check | Result |
|---|---|
| Original `VREC-DST-006` SHA-256 | `fc6c793970168862acd3ca31cf9e1bfd54c784851bd3893f8a46142ef94e0086` |
| Superseded `VREC-DST-006` SHA-256 | `00bf5e364d5ca66808a8f201625674ca553c310fc509a84b62d573d508718c85` |
| Unchanged `VREC-SEH-005` SHA-256 | `53e342e7c4e455b153e40f29735e76714f29972054e1d8e642893d0e19faaa6d` |
| Successor lifecycle | `verified` |
| Source work-order coverage | `WO-DOC-009` |
| Successor work-order coverage | includes `WO-DOC-009` |
| Source verification contract | `VER-DST-006` |
| Successor verification contracts | includes `VER-DST-006` |
| Active release back-reference | none |

Comparison with the `HEAD` source bytes confirms that `commit`, `git_object_format`, `worktree_state`, `verified_at`, `artifact_snapshot_sha256`, `evidence_paths`, `verifies_work_order`, and `conforms_to` are unchanged. Only permitted lifecycle metadata, the supersession edge, `updated`, heading, and explanatory narrative changed.

## Automated verification

Both the repository virtual environment on Python 3.14.6 and the installed Python 3.11.9 runtime completed the full suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py"
& 'C:\Users\mathi\AppData\Local\Python\pythoncore-3.11-64\python.exe' -m unittest discover -s tests -p "test_*.py"
```

After rebasing the transaction onto merged `IAR-010`, Python 3.11.9 and Python 3.14.6 each passed 188 tests with 3 expected Windows symlink skips.

Formal validation passed after the complete publication envelope entered the graph with 344 artifacts, 0 errors, and 40 classified maintenance warnings. The warnings are existing advisory observations rather than blocking structure, governance, or policy findings.

Managed-integrity doctor reported 82 passes and 11 existing `W013` canonical-location advisories. Start preflight passed for `WO-VSP-003` and returned the complete governing manifest. Review preflight and final-state derived-output checks were then run after the work order reached `implemented`.

## Final-state verification

- Review preflight passed for implemented `WO-VSP-003` and returned the same complete governing manifest.
- Two `harnessctl inspect . --json` executions were byte-identical at SHA-256 `a3a124a4ab8372c103db3a494f09d0d28d2dc2390796f3d392b0d09c195a65eb`. Each reported 344 artifacts, 1,241 relations, 72 findings (43 warning and 29 informational), 0 error findings, and 15 derived suggestions. No finding references either superseded source.
- Two Explorer generations reported the same graph snapshot SHA-256 `d87ef48dd72b146c3f71f00cf43cb1ed29b52c2464ac709c1ad42c685cb84f07` and the same rendered `index.html` SHA-256 `cde34935dcd9888cc08201170f30df87b827caca3fa4a176cded9dffebd1a6b9`. Each contained 344 artifacts, 1,241 relations, 43 warnings, and 0 errors.
- `python -m unittest tests.test_revision_provenance tests.test_dashboard_webui tests.test_inspection` passed 48 focused tests with 1 expected Windows symlink skip.
- `git diff --check` passed with no whitespace errors; Git emitted only the repository's normal line-ending notices.

## Residual authority boundary

This evidence proves a current working-tree implementation, not a commit-bound assurance decision. `WO-VSP-003` honestly stops at `implemented`. Any commit, push, pull request, verification record, release decision, tag, publication, deployment, or merge requires separate accountable authority.
