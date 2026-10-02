+++
id = "RISK-RLS-003"
type = "risk"
title = "Unverified Claude public-route native sessions in plugin 0.2.4"
status = "accepted"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
description = "Public fresh installation and update of plugin 0.2.4 on Claude Code pass exact-byte and offline setup checks. Native init-only bootstrap passes, but authenticated startup, activation, compaction and resume tests remain unavailable. Undetected Claude-specific delivery or session recovery defects may remain."
action = "Retain Claude results as unverified with accepted residual risk for WO-RLS-033 only; restore authentication and perform the native matrix before a later release or a claim of verified Claude support."
raised_by = "operator"

[relations]
threatens = ["WO-RLS-033"]

[disposition]
option = "accept"
label = "Accept the missing Claude native tests for WO-RLS-033 only, retaining unverified results and residual risk."
decided_by = "mmzen"
decided_at = "2026-10-02T07:08:23Z"
reason = "Human mmzen: Continue, mark claude lack of tests as accepted. Accepts only the disclosed missing Claude native public-route tests and residual risk for WO-RLS-033, plugin 0.2.4 at 7e366438165a40a14783bac650a2887e7ec8bc75. Keep results unverified; Codex obligations and other decisions remain separate."
revisit = "Before the next plugin release, before claiming this Claude route is verified, or before adoption that depends on verified Claude delivery, whichever occurs first."


[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-02T07:07:17Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."

[[lifecycle_events]]
from = "raised"
to = "accepted"
decided_at = "2026-10-02T07:08:23Z"
decided_by = "mmzen"
reason = "Human mmzen: Continue, mark claude lack of tests as accepted. Accepts only the disclosed missing Claude native public-route tests and residual risk for WO-RLS-033, plugin 0.2.4 at 7e366438165a40a14783bac650a2887e7ec8bc75. Keep results unverified; Codex obligations and other decisions remain separate."
+++

# Risk: Unverified Claude public-route native sessions in plugin 0.2.4

## Description

Public fresh installation and update of plugin 0.2.4 on Claude Code pass exact-byte and offline setup checks. Native init-only bootstrap passes, but authenticated startup, activation, compaction and resume tests remain unavailable. Undetected Claude-specific delivery or session recovery defects may remain.

## Next action

Retain Claude results as unverified with accepted residual risk for WO-RLS-033 only; restore authentication and perform the native matrix before a later release or a claim of verified Claude support.
