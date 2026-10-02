# WO-RLS-032 continuation review

## Outcome

The exact plugin 0.2.4 package now has fresh Codex CLI/app-server evidence.
Claude Code remains unverified for the complete exact-package native matrix
because the live request failed authentication and the human cannot refresh it.
Codex Windows desktop remains unverified. WO-RLS-032 stays in progress.

## Completed observations

| Check | Result | Evidence |
| --- | --- | --- |
| Exact public-wheel package build and independent check | Passed | [Assembly](package-qualification.json) |
| Claude manifest validation | Passed | [Assembly](package-qualification.json) |
| Windows and Linux adapter walkthroughs | 41 steps passed on each | [Windows](portable-windows.json), [Linux](portable-linux.json) |
| Codex startup, activation after clone, manual/automatic compaction and resume | Passed | [Current native run](codex-native-current.json) |
| Two independent Codex sessions; interleaved 0.20.0 and 0.21.0 selections | Passed | [Native boundaries](codex-native-boundaries.json) |
| Switch and clear one session without changing the other | Passed | [Native boundaries](codex-native-boundaries.json) |
| Missing selected checkout and recovery | Refusal and recovery observed | [Native boundaries](codex-native-boundaries.json) |
| Retained Claude bootstrap callback | Observed before the authenticated request failed | [Original native attempt](native-observations.json) |

The successful Codex runs used the existing disposable profile's native trust for
the same hook hash. They used fresh sessions and fixtures, loaded the actual
release archive, compared every packaged file, and restored the previous test
plugin afterward. No trust bypass or real-profile change was used. The first
completely fresh profile's untrusted result remains retained as a separate fact.
These results do not claim Windows desktop delivery.

The [historical comparison](historical-native-comparison.json) finds the same
Claude adapter files and evaluator payload in earlier native observations. The
wheel archive and development/release packaging differ. This is supporting risk
evidence only; it does not turn the new Claude test into a pass.

## Required decision

[DEC-RLS-002](../../decisions/DEC-RLS-002.md) proposes accepting only the missing
Claude native and Codex Windows desktop qualification for this exact WO-RLS-032
package. [RISK-RLS-002](../../risks/RISK-RLS-002.md) records the residual risk.
The records remain open/raised. The human has not accepted this proposal.

The two options are to accept the bounded, disclosed omissions or keep the work
incomplete until matching evidence is available. All other checks and human
verification remain required. No marketplace publication or adoption is granted.
WO-RLS-033's public installation/update obligations remain separate.

## Next action

Human mmzen chooses an option for DEC-RLS-002. If acceptance is explicitly given,
apply it through the released 0.20.1 decision operation, then finish the remaining
contract assessment, commit-bound verification preparation and human review.
Do not run completion or capture merely because scope/preflight checks pass.
If no acceptance is given, retain these results and wait for the missing evidence.

No new VREC, assurance decision, marketplace write, release-marker change or
repository adoption occurred in this continuation.
