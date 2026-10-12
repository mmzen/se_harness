# Review: complete release compatibility and instruction packaging

This expanded draft supersedes the earlier unapproved WO-RLS-048 proposal.

Two preparation gaps would prevent the new combination from working:

1. The service accepts client 0.22.2 only. The [runtime diff](runtime-proposed.diff)
   adds exactly 0.23.0 while preserving the existing client and all other checks.
2. Release packaging omits [ten existing instruction files](missing-instruction-files.json).
   The [assembly diff](plugin-assembly.diff) adds their exact existing mappings;
   it preserves the fixed inventory and every previous mapping. Development
   assembly included these files, so its earlier passes did not cover this gap.

[WO-RLS-048](../../work-orders/WO-RLS-048.md) covers these corrections and their
success/refusal and composed-link tests. It changes five implementation/test files
plus this release domain. Required commit-bound verification uses existing
VER-RLS-039/040 and the final aggregate record.

The [release-contract diff](release-contract.diff) adds only this work to release
membership. [Accepted bytes](REL-SEH-036-accepted-before.txt),
[proposed bytes](REL-SEH-036-proposed.txt) and [reviewed digests](review-binding.json)
are retained. The runtime, assembly map and accepted release contract remain
unchanged pending approval. The previous narrow proposal is preserved in
superseded-narrow-proposal.zip.

Approve this revised WO-RLS-048 and required verification, authorize the exact
bounded manual REL-SEH-036 membership amendment preserving accepted history,
and include the correction in PR #544. This grants no verification acceptance,
merge, publication, adoption or host update.

Expanded draft validation: 2,004 artifacts, zero errors, 63 existing warnings.
The evaluator covers every supplied proposed path; impact analysis remains a
human/agent review. [Actual checks](expanded-proposal-checks.zip) also retain the
failing package-link check. These observations do not verify the proposed fix.
