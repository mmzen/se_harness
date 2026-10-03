# Verification requested: plugin 0.2.5

**Decision:** verify VREC-PLG-032 for candidate
`164286460d77c94e173ff12d9133ba95ef9c8692` as assurance owner.

Both plugin packages contain the exact public evaluator 0.22.0 wheel and shared
assets from the approved release source. Windows and Linux package checks pass.
Codex CLI passed startup, activation, manual and automatic compaction, resume,
session isolation, and new/resumed work through the delivery authority boundary.
The capture rechecked package contents and retained evidence hashes at this commit.

**Claude Code host tests and Codex Windows desktop tests were not run and remain
unverified**, under your recorded instruction in DEC-RLS-005/006. Earlier Claude
authentication failure remains in the evidence. Neither portable adapter tests
nor Codex CLI results establish those omitted host results.

The workflow test also found a limitation recorded in **RISK-RLS-006**: an absent
future file in a draft's `evidence_paths` can crash an unrelated transition preview.
The test passed after keeping that future destination in the draft body until
the file exists. The evaluator was not fixed; the crash remains visible for follow-up.
No acceptance of that separate risk is inferred from the host-test omission.

Read the [qualification review](qualification-review.md) for the check matrix,
preserved failures and raw evidence. Windows retained 2 skips and Linux 1.
The native test profile was restored. The published evaluator and plugin package
bytes were not changed by this qualification work.

Verification accepts this exact evidence and candidate. After your decision,
the agent records it in the final review commit and continues the authorized
marketplace delivery. Merge remains your decision. Public fresh/update checks,
documentation closeout and latest/last are still downstream under WO-RLS-036.

Suggested response: **I verify VREC-PLG-032 as assurance owner.**
