+++
id = "RISK-RLS-005"
type = "risk"
title = "Untested Claude and Codex desktop public routes for plugin 0.2.5"
status = "accepted"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"
description = "Claude host installation/update and native session tests, and Codex Windows desktop tests, will not be run for this 0.22.0 delivery. Package byte readbacks do not prove operation on these hosts. The user explicitly instructs continuing with Claude and Codex desktop untested and disclosed."
action = "Keep these public host routes explicitly untested in current documentation and closeout; require fresh qualification before a verified-host claim or the next plugin release."
raised_by = "operator"

[relations]
threatens = ["WO-RLS-036"]

[disposition]
option = "accept"
label = "Continue the current delivery with Claude host tests and Codex Windows desktop tests not run, disclosed as unverified, and excluded from verified-host claims."
decided_by = "mmzen"
decided_at = "2026-10-03T04:59:55Z"
reason = "Human mmzen: \"you can continue, claude and codex desktop won\u2019t be tested: to be indicated.\" This records the current-release decision for WO-RLS-036 and exact plugin 0.2.5: Claude host installation/update and native session tests, and Codex Windows desktop tests, are not run/unverified and must be disclosed. Retain both public package byte checks; name Codex CLI only as verified-host coverage. The remaining uncertainty is retained in RISK-RLS-005. Required Codex CLI checks, human verification and publication controls remain separate."
revisit = "Before the next plugin release or before claiming either omitted host route verified, whichever occurs first."


[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-03T04:55:23Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."

[[lifecycle_events]]
from = "raised"
to = "accepted"
decided_at = "2026-10-03T04:59:55Z"
decided_by = "mmzen"
reason = "Human mmzen: \"you can continue, claude and codex desktop won\u2019t be tested: to be indicated.\" This records the current-release decision for WO-RLS-036 and exact plugin 0.2.5: Claude host installation/update and native session tests, and Codex Windows desktop tests, are not run/unverified and must be disclosed. Retain both public package byte checks; name Codex CLI only as verified-host coverage. The remaining uncertainty is retained in RISK-RLS-005. Required Codex CLI checks, human verification and publication controls remain separate."
+++

# Risk: Untested Claude and Codex desktop public routes for plugin 0.2.5

## Description

Claude host installation/update and native session tests, and Codex Windows desktop tests, will not be run for this 0.22.0 delivery. Package byte readbacks do not prove operation on these hosts. The user explicitly instructs continuing with Claude and Codex desktop untested and disclosed.

## Next action

Keep these public host routes explicitly untested in current documentation and closeout; require fresh qualification before a verified-host claim or the next plugin release.
