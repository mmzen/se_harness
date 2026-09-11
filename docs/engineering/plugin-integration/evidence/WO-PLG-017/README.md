# Windows evidence-path repair

The approved repair moves 56 retained WO-PLG-011 files to short paths without
changing their bytes. The original 55-file plan and map remain unchanged; the
operator-approved extra JSON has its own pinned plan and supplemental map.
VREC-PLG-008, its sidecar and historical C/G commits are preserved.

Independent Windows staging reproduced the extra-path failure at 261 characters,
then succeeded at the same 77-character root with a maximum full path of 259.
Long paths were disabled. Linux reconciled all 56 payloads and protected files.
The corrected checker rejected byte corruption and coordinated plan/map tampering.
All 13 hosted checks passed at e5b48a16, including Windows and Linux upgrade
rehearsals and downstream integration. The released evaluator applied delegated completion; WO-PLG-017 is **implemented**. See [the applied result](governance/completion/wo017-completion-applied.json).

- [Original approved plan](path-plan.json), [approval](approval/) and [start](start/).
- [Approved extension](scope-extension.md), [decision](approval/scope-extension.json), and [supplemental map](staging-path-map.json).
- [Original 55-file acceptance](acceptance/independent/REPORT.md).
- [Extension acceptance](acceptance/extension/REPORT.md), [inventory](acceptance/extension/inventory.json), and [retention audit](checks/extension-retention.json).
- [Independent extension review](checks/independent-review/extension-28b4d2e.json) and [Git-reader correction review](checks/independent-review/blob-read-e5b48a16.json).
- Full CI: [28b4d2e](checks/ci-extension-28b4d2e/result.json) and [corrected e5b48a16](checks/ci-extension-e5b48a16/result.json).
- Original [PR445 checkout failure](pr445-windows-checkout.log), [PR446 failure](pr446-windows-checkout.log), and [deeper staging failure](checks/ci-rehearsal-failed/result.json).

The matched-depth staging observation binds 28b4d2e. Corrected-checker tests use
e5b48a16 checker bytes against unchanged 28b4d2e data; hosted CI independently
qualifies the complete e5b48a16 revision. Two whole-repository archive streams are
omitted from the extension package to avoid recursive evidence copies. Their
hashes, immutable source commits and reproduction commands remain retained.

Earlier failures remain unchanged: local Windows source testing hit WinError5 in
fixture cleanup (one error, 23 skips), and the original staging and Git-show
checks failed. Successful source CI ran 1,134 tests with four skips. Candidate
doctor still shows six known candidate/root differences; released integrity and
graph checks pass. These are separate observations.

WO011's earlier completion used incomplete CI information. Its ready record still
binds that original candidate and is not rewritten by this repair. An aggregate
VREC covering WO011 and WO017 requires explicit preparation authority. Assurance,
supersession, release and GitHub merge remain separate decisions.
