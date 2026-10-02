+++
id = "RISK-RLS-001"
type = "risk"
title = "Unverified Codex Windows desktop delivery in 0.21.0"
status = "accepted"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
description = "Codex Windows desktop startup, repository selection and recovery after compaction or resume have not been qualified for evaluator 0.21.0 and plugin 0.2.4. Desktop-specific instruction delivery defects may remain undetected. Native Codex CLI/app-server and Claude evidence does not establish desktop support."
action = "Keep the desktop result unverified and disclose it in the release assessment. Revisit before claiming Codex Windows desktop support or a later release/adoption relying on that support."
raised_by = "Codex"

[relations]
threatens = ["WO-RLS-031"]

[disposition]
option = "accept"
label = "Accept only the desktop qualification gap for WO-RLS-031 and the 0.21.0 release; retain unverified status and the residual risk."
decided_by = "mmzen"
decided_at = "2026-10-02T04:01:56Z"
reason = "regading WO-RLS-031  : i accept that we keep the Codex Windows desktop  unverified  and the associated risk"
revisit = "Before a subsequent release, before claiming verified Codex Windows desktop support, or before adoption relying on desktop replacement delivery, whichever occurs first."


[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-02T03:59:08Z"
decided_by = "Codex"
reason = "Recorded by harnessctl raise-risk."

[[lifecycle_events]]
from = "raised"
to = "accepted"
decided_at = "2026-10-02T04:01:56Z"
decided_by = "mmzen"
reason = "regading WO-RLS-031  : i accept that we keep the Codex Windows desktop  unverified  and the associated risk"
+++

# Risk: Unverified Codex Windows desktop delivery in 0.21.0

## Description

Codex Windows desktop startup, repository selection and recovery after compaction or resume have not been qualified for evaluator 0.21.0 and plugin 0.2.4. Desktop-specific instruction delivery defects may remain undetected. Native Codex CLI/app-server and Claude evidence does not establish desktop support.

## Next action

Keep the desktop result unverified and disclose it in the release assessment. Revisit before claiming Codex Windows desktop support or a later release/adoption relying on that support.
