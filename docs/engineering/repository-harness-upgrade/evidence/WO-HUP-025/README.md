# WO-HUP-025 adoption evidence

The reviewed public 0.20.1 wheel is installed in the existing private evaluator.
The installer applied the reviewed plan and retained the canonical transaction
in `../WO-HUP-025-evaluator-upgrade.json`. No editable seed was replaced.

`checks.json` retains actual commands, runtime identities, working directories,
exit codes and output. The pre-apply doctor had exactly the three reviewed
old-version differences. Post-upgrade doctor, complete validation, released-root
qualification, documentation tests, distribution checks and source CLI passed.
The no-op upgrade preview has no pending supplied-file changes.

`preservation.json` reports all 12,990 tracked-file comparisons. The nine
implementation files changed as approved. All other previously tracked bytes
and seven reviewed absences were preserved. Both source versions remain 0.21.0.

Review: the change reuses the released installer and existing CI. No product
code, template, gate or history was rewritten. Four current documentation files
and one existing test expectation follow the selected evaluator. Historical
adoptions retain their meaning. No new framework or test machinery was added.

The clean implementation commit `c867445598488929ffcead4f67d3894d24b3facb` passed the full-scale
source suite on Windows: 1189 tests, 1171 passed and 18 skipped.
`full-source-summary.json` retains the command, actual counts and raw-log retrieval
information. The aggregate runner does not identify individual skip reasons.
The transition assessment passed against main at
`aeebcabf8e3ed958e0166dfe2754a2af2681a59d`, using released RLS-SEH-030 and the
exact canonical installer transaction. It left the checkout unchanged.

Coverage: A0201-01 is supported by the before/after identities and installer
plan; A0201-02 by the transaction, no-op replay and file-preservation comparison;
A0201-03 by released checks and predecessor assessment; A0201-04 by the
documentation, distribution and full regression checks. A0201-05 also requires
the complete handoff, exact-candidate capture and hosted integration checks.

Commit-bound capture and hosted Linux/Windows checks remain pending at this
implementation-evidence snapshot. VREC-HUP-024, when prepared, records the
exact assessed candidate; its human decision remains separate.
This evidence does not prove native desktop delivery or compaction, qualify the
minimal-layout successor, or record human verification or merge authority.
