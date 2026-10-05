# Release documentation correction for review

VREC-SEH-033 is verified by mmzen at candidate `4f640284ec496b88cd7aa4ba88ca537d9374a2f8`.
The decision is pushed in PR #536. RLS-SEH-033 is ready with the exact distributions.

## Problem and proposed change

Before freezing the complete-delivery plan, review found six current source files
that still say qualification is running or describe 0.22.0 / 0.2.5 as permanently
current. Publication instructions also name the previous release's work orders.
The complete plan locks documentation hashes, so these cannot be repaired later
as ordinary publication receipts. This omission should have been caught before
the release candidate was verified.

[WO-RLS-044](../../work-orders/WO-RLS-044.md) and
[VER-RLS-005](../../verification/VER-RLS-005.md) propose a small source-documentation
correction. The [exact patch](proposed-documentation.patch) is **unapplied**; its
[inputs](proposal-inputs.json) bind the current and proposed bytes. No product code,
package, manifest or version changes. Existing qualified package README snapshots
remain unchanged and their historical wording is disclosed in current source guides.

The patch records the verified candidate, keeps dated prior-delivery facts, and
directs publication claims to the release record, actual public identity and a
stable delivery-evidence index. That index will name the exact plan and receipt
paths once the plan is prepared. It will not assert successful unperformed tests.

The result will have its own verified documentation commit. The frozen plan can
select that commit while RLS-SEH-033 keeps the already verified binary candidate
and release membership. WO-RLS-042 keeps post-publication tests and receipts.

## Decision requested

Approve WO-RLS-044 and VER-RLS-005 with required commit-bound verification and
updates to the existing draft PR #536. This allows only the reviewed documentation,
checks and evidence. Verification acceptance and the final complete-release decision
remain separate. No merge, publication, rebinding or adoption is requested here.

The new request is needed because WO-RLS-040 has completed its verified preparation,
while WO-RLS-042 covers execution/public closeout. Their existing histories remain
unchanged. The preparation rule in released DRAFT_WORK_ORDERS.md requires a bounded
correction rather than silently changing approved scope or verified content.

## Preparation checks

Released 0.22.0 validation reports zero errors and 63 repository warnings. The scope report covers all supplied planned paths.
These checks assess the proposal; they do not execute its patch or approve it.
The [raw preparation checks](proposal-checks.zip) retain commands and results.
