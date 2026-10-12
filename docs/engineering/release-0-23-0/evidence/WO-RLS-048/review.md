# Review: admit the release client

The service currently rejects 0.23.0 because it has its own fixed 0.22.2 check.
This was missed in the initial release scope. The helper correction alone cannot
make the new combination ready.

Propose [WO-RLS-048](../../work-orders/WO-RLS-048.md): accept exactly 0.22.2 and
0.23.0 while keeping the other component and private-sandbox checks. Add success
and refusal tests to the existing checks. Required commit-bound verification uses
the existing VER-RLS-039/040 and final aggregate record.

The [exact release-contract diff](release-contract.diff) adds only this work to
membership. Its [accepted bytes](REL-SEH-036-accepted-before.txt),
[proposed bytes](REL-SEH-036-proposed.txt), and [digests](review-binding.json)
are retained. REL-SEH-036 and runtime source remain unchanged pending approval.

Approve WO-RLS-048 and required verification, authorize this exact bounded manual
membership amendment preserving accepted history, and include the correction in
the existing release-preparation draft PR. This grants no verification acceptance,
merge, publication, adoption or host update.

The [proposed runtime diff](runtime-proposed.diff) adds only the exact client version.
Draft validation: 2,004 artifacts, zero errors, 63 existing warnings. All supplied
correction paths are covered. [Actual checks](proposal-checks.zip) retain original
results, including the filesystem refusal before the successful template creation.
