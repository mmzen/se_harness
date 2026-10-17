+++
id = "DEC-RLS-011"
type = "decision"
title = "Defer Codex Windows desktop qualification for plugin 0.2.7"
status = "decided"
owners = ["mmzen"]
created = "2026-10-16"
updated = "2026-10-16"
kind = "deviation"
question = "May evaluator 0.23.0 / plugin 0.2.7 proceed with Codex Windows desktop tests not run, desktop support unverified and its residual risk carried only for this release?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-IAR-016#IAR-EXT-010"
observed = "mmzen requested deferral of Codex app tests. The prepared desktop kit was not run. Separate Codex CLI and Claude Code results do not establish desktop delivery or recovery."

[[options]]
id = "accept"
label = "Carry only the stated qualification limitations in evaluator 0.23.0 / plugin 0.2.7; preserve failed and unverified results and open follow-up."

[[options]]
id = "stop"
label = "Keep affected qualification pending until the stated limitations are resolved or a different explicit disposition applies."

[relations]
concerns = ["RISK-RLS-009", "WO-RLS-046", "WO-RLS-054", "WO-RLS-045", "REL-SEH-036", "SPEC-IAR-016", "SPEC-HAG-008", "VER-IAR-021", "VER-RLS-039", "VER-RLS-040"]
blocks = ["WO-RLS-046", "WO-RLS-054"]

[disposition]
option = "accept"
label = "Carry only the stated qualification limitations in evaluator 0.23.0 / plugin 0.2.7; preserve failed and unverified results and open follow-up."
decided_by = "mmzen"
decided_at = "2026-10-16T11:24:52Z"
reason = "Human mmzen requested \"let's defer codex app tests\" and, after the report listing desktop as deferred/unverified, instructed \"continue the release, mark the findings as open items\". Applies to evaluator 0.23.0 / plugin 0.2.7 only. Carry the desktop omission and residual delivery/selection risk for this release. Desktop testing remains open and not run/unverified. Retain CLI and public-route checks. Final verification, merge and exact complete-release approval remain separate. Decision SHA-256 ab2b9d36ba7fee637e3441af200edf9a7b9a126009f06b4cf68fe8cc8b283016; risk SHA-256 d5e1149e60a8d23d067f469ee1b756f0af04f0f057a9b325e3b1c96250b42004."
revisit = "Before the next plugin release or any claim of verified Codex Windows desktop support, whichever occurs first; changed product bytes, versions or scope require renewed review."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-16T11:24:52Z"
decided_by = "mmzen"
reason = "Human mmzen requested \"let's defer codex app tests\" and, after the report listing desktop as deferred/unverified, instructed \"continue the release, mark the findings as open items\". Applies to evaluator 0.23.0 / plugin 0.2.7 only. Carry the desktop omission and residual delivery/selection risk for this release. Desktop testing remains open and not run/unverified. Retain CLI and public-route checks. Final verification, merge and exact complete-release approval remain separate. Decision SHA-256 ab2b9d36ba7fee637e3441af200edf9a7b9a126009f06b4cf68fe8cc8b283016; risk SHA-256 d5e1149e60a8d23d067f469ee1b756f0af04f0f057a9b325e3b1c96250b42004."
+++

# Defer Codex Windows desktop qualification for plugin 0.2.7

## Recorded human direction

mmzen requested "let's defer codex app tests" and then "continue the release, mark the findings as open items".
The second instruction follows the report of the open findings and deferred
desktop test. This record applies that direction to this release only. Keep Codex Windows desktop
startup, selection, instruction delivery, compaction and resume **not run /
unverified** for evaluator 0.23.0 / plugin 0.2.7 under REL-SEH-036.

Undetected desktop-specific delivery or checkout-selection defects can remain.
CLI results cannot establish desktop behavior. No desktop failure is inferred
from the absence of a test. The prepared kit remains available for later testing.

The departure is limited to IAR-EXT-010 qualification as assessed by VER-IAR-021
and VER-RLS-040. The source is `bb0890045f462343ecae66ca30b20b06cf6e8ae6` with its exact qualified package bytes.
Matching governance-only continuation is included. Changed product scope,
versions or bytes require review. The previous release's exception is unchanged.

## Consequences

`accept` permits completion of affected preparation when all other checks pass
or have their own explicit disposition. The paired risk is accepted only for
this release. Desktop testing remains an open follow-up item; there is no pass.
`stop` keeps the affected preparation pending until desktop evidence is available.

Keep portable, native CLI, service, public-installation and update checks,
commit-bound assurance and all gates. DEC-RLS-010 separately covers the two
instruction findings; this record adds no other omission. The final VREC,
release plan and support claims must disclose the desktop limit. Human
verification, merge and exact complete-release approval remain separate.

## Follow-up

mmzen owns desktop qualification before the next plugin release or any claim
that Codex Windows desktop is verified, whichever occurs first. Retain the
not-run label until actual evidence is assessed. There is no automatic extension.
See [desktop scheduling evidence](../evidence/WO-RLS-054/desktop-deferral.json)
and [qualification report](../evidence/WO-RLS-045/qualification-progress-bb089004.md).

