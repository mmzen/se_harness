# Approval request: restore the README word budget

PR #533's candidate-source suite ran 1,262 tests with two skips and one failure:
the README contains 690 words, exceeding the existing 650-word limit.
VREC-RLS-001 records mmzen's verification of the unchanged evidence candidate;
the PR remains draft because this integration failure still needs correction.

## Proposed change

Replace only the new Claude follow-up paragraph with:

> [Claude follow-up](../WO-RLS-038/README.md): Windows installation, update and session checks passed. Codex desktop, the full Claude workflow and long paths remain unverified. Historical decisions and accepted risks are unchanged.

The actual root-relative link is retained in [the exact patch](proposed-readme.patch).
This makes the README **644 words**, with 104 lines. The test that failed in CI
passes against the proposed text in a transient rehearsal. The repository's
README remains unchanged until approval. [Proposal check](proposal-check.json)
and [original CI failure](ci-failure.log) retain these results.

## Approval requested

Approve [WO-RLS-039](../../work-orders/WO-RLS-039.md) and
[VER-RLS-003](../../verification/VER-RLS-003.md), including required verification
of the exact commit. Permit the paragraph edit, unchanged documentation tests,
full source regression, evidence retention and a fresh combined verification
record for WO-RLS-038/039.

Include ordinary review pushes to `mmzen/se_harness`, source
`work/claude-025-evidence-followup`, base `main`, in existing PR #533, followed
by the later human-verification decision push. Acceptance of the corrected
candidate and merge remain separate decisions.

The drafts validate with zero errors and 61 existing repository warnings. Every
planned path is covered. Approval currently awaits the human's assurance
classification (`QGS-ASSURANCE`); the proposal is **required** because integration
and public guidance rely on correct presentation and coverage claims.

No test threshold, package, native-test result, old risk, old decision or
VREC-RLS-001 evidence changes. The existing completed work order cannot be reused
for implementation; this new bounded work order preserves its history.
