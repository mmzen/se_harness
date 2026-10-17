+++
id = "DEC-RLS-010"
type = "decision"
title = "Carry the two instruction findings as open release items"
status = "decided"
owners = ["mmzen"]
created = "2026-10-16"
updated = "2026-10-16"
kind = "deviation"
question = "May qualification of evaluator 0.23.0 and plugin 0.2.7 proceed with R23-NATIVE-010 and R23-NATIVE-011 retained as open, unrepaired findings?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-IAR-016#IAR-EXT-010"
observed = "In codex-reads2 the first English update was event 11 and the complete communication read was event 31. Both new-work drafts omitted fixed generated VREC destinations. Functional checks and separately seeded execution passed, but those results do not repair either finding."

[[options]]
id = "accept"
label = "Carry only the stated qualification limitations in evaluator 0.23.0 / plugin 0.2.7; preserve failed and unverified results and open follow-up."

[[options]]
id = "stop"
label = "Keep affected qualification pending until the stated limitations are resolved or a different explicit disposition applies."

[relations]
concerns = ["RISK-RLS-008", "WO-RLS-046", "WO-RLS-054", "WO-RLS-045", "REL-SEH-036", "SPEC-IAR-016", "SPEC-HAG-008", "VER-IAR-021", "VER-RLS-039", "VER-RLS-040"]
blocks = ["WO-RLS-046", "WO-RLS-054"]

[disposition]
option = "accept"
label = "Carry only the stated qualification limitations in evaluator 0.23.0 / plugin 0.2.7; preserve failed and unverified results and open follow-up."
decided_by = "mmzen"
decided_at = "2026-10-16T11:21:40Z"
reason = "Human mmzen: \"continue the release, mark the findings as open items\". Applies to disclosed R23-NATIVE-010 and R23-NATIVE-011 for evaluator 0.23.0 / plugin 0.2.7 only. Continue preparation with both remediation items open and original failures unchanged; carry their residual risk for this release. Desktop omission, final verification, merge and exact complete-release approval remain separate. Decision SHA-256 6df7709f84d1935d50db11092c4d4a808d9f3b4224fdcbd798b7702e1282db45; risk SHA-256 03eba8b5e8f432709fcb83b32f60987d636cb068c4f96d78fdd6ab16b3c4d276."
revisit = "Before the next plugin release or any claim that these cases pass, whichever occurs first; changed product bytes, versions or scope require renewed review."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-16T11:21:40Z"
decided_by = "mmzen"
reason = "Human mmzen: \"continue the release, mark the findings as open items\". Applies to disclosed R23-NATIVE-010 and R23-NATIVE-011 for evaluator 0.23.0 / plugin 0.2.7 only. Continue preparation with both remediation items open and original failures unchanged; carry their residual risk for this release. Desktop omission, final verification, merge and exact complete-release approval remain separate. Decision SHA-256 6df7709f84d1935d50db11092c4d4a808d9f3b4224fdcbd798b7702e1282db45; risk SHA-256 03eba8b5e8f432709fcb83b32f60987d636cb068c4f96d78fdd6ab16b3c4d276."
+++

# Carry the two instruction findings as open release items

## Recorded human direction

After the findings were reported, mmzen instructed: "continue the release, mark the findings as open items".
This record applies that direction to these two disclosed findings only. It does
not accept the separate desktop omission or supply the final verification decision.
The evaluator records the disposition in the metadata above.

## Exact qualification departure

The departure is from IAR-EXT-010 qualification of the exact host packages,
as assessed under VER-RLS-040 and VER-IAR-021. It covers only:

- **R23-NATIVE-010, open:** The Codex immutable read case read communication
  instructions after its first English update. All seven graph reads matched
  independent HTTP results and project version stayed 29. Full Codex and Claude
  workflows read the policy early, but the read-only failure remains a failure.
- **R23-NATIVE-011, open:** Both disposable WO-FLW-002 drafts omitted fixed
  generated verification destinations while claiming no unresolved destination.
  They remain unapproved drafts. The separate approved WO-FLW-001 execution
  cases reached ready records; they do not establish proposal completeness.

The qualified source is `bb0890045f462343ecae66ca30b20b06cf6e8ae6`. This departure covers evaluator 0.23.0 / plugin
0.2.7 under REL-SEH-036 only, including matching governance-only continuation.
Changed product bytes, versions or behavior require renewed review. Keep the
exact package hashes in the qualification evidence and final record.

## Effects and limits

`accept` permits the remaining release preparation to proceed with these two
limitations explicitly disclosed. The paired risk becomes accepted for this
release. **Both remediation items remain open.** No result becomes a pass.
`stop` leaves affected qualification pending.

Keep the actual instruction and scope rules, required gates and independent
assessments. A later agent must still read applicable instructions and stop at
unapproved evidence paths. No out-of-scope writes, invented path authority,
accepted-definition edits or new product correction are authorized here.

Desktop qualification is governed separately. Human verification, merge and the
exact complete-release decision remain separate. No public branch, package,
registry, tag or production service is changed by this decision.

## Evidence and follow-up

See [qualification report](../evidence/WO-RLS-045/qualification-progress-bb089004.md)
and [exact evidence index](../evidence/WO-RLS-054/evidence-index-bb089004.json).
Preserve earlier failures, actual command results and unsuccessful attempts.
mmzen owns follow-up. Prepare a bounded correction and requalify the affected
cases before the next plugin release or any claim that these cases pass,
whichever occurs first. No automatic extension to another release applies.

