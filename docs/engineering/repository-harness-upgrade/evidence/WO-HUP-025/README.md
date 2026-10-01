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

Full source tests and the committed transition assessment are the next checks.
Commit-bound verification and hosted Linux/Windows checks remain pending.
This evidence does not prove native desktop delivery or compaction, qualify the
minimal-layout successor, or record human verification or merge authority.
