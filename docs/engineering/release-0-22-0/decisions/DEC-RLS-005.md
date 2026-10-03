+++
id = "DEC-RLS-005"
type = "decision"
title = "Continue plugin 0.2.5 qualification with two untested host routes"
status = "decided"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"
kind = "deviation"
question = "May WO-RLS-035 continue with Claude Code native tests and Codex Windows desktop tests not run and explicitly unverified for plugin 0.2.5?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-IAR-016#IAR-EXT-010"
observed = "Claude's live request failed because OAuth expired and could not be refreshed. Codex Windows desktop evidence is unavailable. Human mmzen instructs continuing without testing these two host routes and requires this to be indicated. Portable checks and Codex CLI evidence do not prove the omitted native routes."

[[options]]
id = "accept"
label = "Continue this exact package qualification with the two native routes not run, their uncertainty retained and no verified-host claim."

[[options]]
id = "stop"
label = "Keep qualification incomplete until the native tests pass or another formal disposition applies."

[relations]
concerns = ["RISK-RLS-004", "WO-RLS-035", "SPEC-IAR-016", "VER-IAR-021", "VER-RLS-034", "REL-SEH-034"]
blocks = ["WO-RLS-035"]

[disposition]
option = "accept"
label = "Continue this exact package qualification with the two native routes not run, their uncertainty retained and no verified-host claim."
decided_by = "mmzen"
decided_at = "2026-10-03T04:54:37Z"
reason = "Human mmzen: \"you can continue, claude and codex desktop won\u2019t be tested: to be indicated.\" This records the current-release decision for WO-RLS-035 and exact plugin 0.2.5: retain Claude Code native tests and Codex Windows desktop tests as not run/unverified and disclose the remaining host-specific uncertainty. Codex applies the supplied human decision; required Codex CLI checks, verification acceptance and publication controls remain separate."
revisit = "Before the next plugin release or before claiming either omitted host route verified, whichever occurs first."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-03T04:54:37Z"
decided_by = "mmzen"
reason = "Human mmzen: \"you can continue, claude and codex desktop won\u2019t be tested: to be indicated.\" This records the current-release decision for WO-RLS-035 and exact plugin 0.2.5: retain Claude Code native tests and Codex Windows desktop tests as not run/unverified and disclose the remaining host-specific uncertainty. Codex applies the supplied human decision; required Codex CLI checks, verification acceptance and publication controls remain separate."
+++

# Continue plugin 0.2.5 qualification with two untested host routes

## Human instruction

Human mmzen stated: "you can continue, claude and codex desktop won’t be tested:
to be indicated." This record expresses that supplied decision. The evaluator
applies its disposition; this draft does not write it by hand.

## Exact boundary

This deviation applies to WO-RLS-035, plugin 0.2.5 assembled from
`abbec12ac5524c8adfb28693f846dd59de88f759`, and the public evaluator 0.22.0
wheel bound by RLS-SEH-032. The checked package identity SHA-256 is
`b3ce06c6f4ac9bdfed7ffd26eb16683e260814c82d7dba188f78a0180c8a4e61`.

Claude Code native startup, activation, manual/automatic compaction, resume,
parallel sessions and work handoff are **not run / unverified**. Codex Windows
desktop instruction delivery and recovery are **not run / unverified**.
The failed Claude authentication attempt remains failed evidence.

Acceptance permits these omissions against IAR-EXT-010 as specified by
VER-IAR-021 and VER-RLS-034. RISK-RLS-004 records the remaining possibility of
undetected host-specific delivery or recovery defects. Keep this limitation
visible in the verification review and current support claims.

## Remaining obligations

Codex CLI qualification, portable checks, package identity, human verification
and publication controls remain required. Observed failures are not changed
to passes. The long-path Claude delivery bound remains a disclosed limit.
The existing released definitions and prior release records remain unchanged.
Public-route omissions for WO-RLS-036 are recorded separately against its rule.

mmzen owns follow-up. Revisit before the next plugin release or before claiming
either omitted route verified, whichever occurs first. No automatic extension
to a different package or future release is allowed.
