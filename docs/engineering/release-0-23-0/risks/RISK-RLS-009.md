+++
id = "RISK-RLS-009"
type = "risk"
title = "Unverified Codex Windows desktop for plugin 0.2.7"
status = "accepted"
owners = ["mmzen"]
created = "2026-10-16"
updated = "2026-10-16"
description = "Codex Windows desktop startup, selection, instruction delivery, compaction and resume were not run for evaluator 0.23.0 and plugin 0.2.7. CLI evidence does not establish desktop behavior. Undetected desktop-specific delivery or selection defects remain possible."
action = "mmzen owns desktop qualification before the next plugin release or any verified-desktop claim. Retain not-run and unverified labels, exact package identity and the prepared kit; preserve all CLI and public-route checks."
raised_by = "operator"

[relations]
threatens = ["WO-RLS-046", "WO-RLS-054"]

[disposition]
option = "accept"
label = "Carry only the stated qualification limitations in evaluator 0.23.0 / plugin 0.2.7; preserve failed and unverified results and open follow-up."
decided_by = "mmzen"
decided_at = "2026-10-16T11:24:52Z"
reason = "Human mmzen requested \"let's defer codex app tests\" and, after the report listing desktop as deferred/unverified, instructed \"continue the release, mark the findings as open items\". Applies to evaluator 0.23.0 / plugin 0.2.7 only. Carry the desktop omission and residual delivery/selection risk for this release. Desktop testing remains open and not run/unverified. Retain CLI and public-route checks. Final verification, merge and exact complete-release approval remain separate. Decision SHA-256 ab2b9d36ba7fee637e3441af200edf9a7b9a126009f06b4cf68fe8cc8b283016; risk SHA-256 d5e1149e60a8d23d067f469ee1b756f0af04f0f057a9b325e3b1c96250b42004."
revisit = "Before the next plugin release or any claim of verified Codex Windows desktop support, whichever occurs first; changed product bytes, versions or scope require renewed review."


[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-16T11:16:02Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."

[[lifecycle_events]]
from = "raised"
to = "accepted"
decided_at = "2026-10-16T11:24:52Z"
decided_by = "mmzen"
reason = "Human mmzen requested \"let's defer codex app tests\" and, after the report listing desktop as deferred/unverified, instructed \"continue the release, mark the findings as open items\". Applies to evaluator 0.23.0 / plugin 0.2.7 only. Carry the desktop omission and residual delivery/selection risk for this release. Desktop testing remains open and not run/unverified. Retain CLI and public-route checks. Final verification, merge and exact complete-release approval remain separate. Decision SHA-256 ab2b9d36ba7fee637e3441af200edf9a7b9a126009f06b4cf68fe8cc8b283016; risk SHA-256 d5e1149e60a8d23d067f469ee1b756f0af04f0f057a9b325e3b1c96250b42004."
+++

# Risk: Unverified Codex Windows desktop for plugin 0.2.7

## Description

Codex Windows desktop startup, selection, instruction delivery, compaction and resume were not run for evaluator 0.23.0 and plugin 0.2.7. CLI evidence does not establish desktop behavior. Undetected desktop-specific delivery or selection defects remain possible.

## Next action

mmzen owns desktop qualification before the next plugin release or any verified-desktop claim. Retain not-run and unverified labels, exact package identity and the prepared kit; preserve all CLI and public-route checks.
