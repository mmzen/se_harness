+++
id = "DEC-RLS-006"
type = "decision"
title = "Disclose untested Claude and Codex desktop public routes for plugin 0.2.5"
status = "decided"
owners = ["mmzen"]
created = "2026-10-03"
updated = "2026-10-03"
kind = "deviation"
question = "May WO-RLS-036 continue without Claude host installation/update or native tests and without Codex Windows desktop tests, keeping those routes explicitly untested for plugin 0.2.5?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-RLO-006#RLO-DLV-003"
observed = "Human mmzen instructs continuing this release without testing Claude or Codex desktop and requires disclosure. Public package byte readbacks and passing Codex CLI observations cannot establish those omitted host results."

[[options]]
id = "accept"
label = "Continue the current delivery with Claude host tests and Codex Windows desktop tests not run, disclosed as unverified, and excluded from verified-host claims."

[[options]]
id = "stop"
label = "Keep the affected public delivery incomplete until these host tests pass or another formal disposition applies."

[relations]
concerns = ["RISK-RLS-005", "WO-RLS-036", "SPEC-RLO-006", "VER-RLS-035", "REL-SEH-034"]
blocks = ["WO-RLS-036"]

[disposition]
option = "accept"
label = "Continue the current delivery with Claude host tests and Codex Windows desktop tests not run, disclosed as unverified, and excluded from verified-host claims."
decided_by = "mmzen"
decided_at = "2026-10-03T04:59:55Z"
reason = "Human mmzen: \"you can continue, claude and codex desktop won\u2019t be tested: to be indicated.\" This records the current-release decision for WO-RLS-036 and exact plugin 0.2.5: Claude host installation/update and native session tests, and Codex Windows desktop tests, are not run/unverified and must be disclosed. Retain both public package byte checks; name Codex CLI only as verified-host coverage. The remaining uncertainty is retained in RISK-RLS-005. Required Codex CLI checks, human verification and publication controls remain separate."
revisit = "Before the next plugin release or before claiming either omitted host route verified, whichever occurs first."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-03T04:59:55Z"
decided_by = "mmzen"
reason = "Human mmzen: \"you can continue, claude and codex desktop won\u2019t be tested: to be indicated.\" This records the current-release decision for WO-RLS-036 and exact plugin 0.2.5: Claude host installation/update and native session tests, and Codex Windows desktop tests, are not run/unverified and must be disclosed. Retain both public package byte checks; name Codex CLI only as verified-host coverage. The remaining uncertainty is retained in RISK-RLS-005. Required Codex CLI checks, human verification and publication controls remain separate."
+++

# Disclose untested Claude and Codex desktop public routes for plugin 0.2.5

## Human instruction and boundary

Human mmzen stated: "you can continue, claude and codex desktop won’t be tested:
to be indicated." This decision records the public-route part of that instruction
for WO-RLS-036. DEC-RLS-005 covers package qualification separately.

The decision is limited to plugin 0.2.5 assembled from
`abbec12ac5524c8adfb28693f846dd59de88f759`, package identity SHA-256
`b3ce06c6f4ac9bdfed7ffd26eb16683e260814c82d7dba188f78a0180c8a4e61`,
and the evaluator 0.22.0 wheel released by RLS-SEH-032. A public commit may
transport only that exact checked package; record its resolved identity later.

## Effect of acceptance

Claude installation, update and native session checks are **not run / unverified**.
Codex Windows desktop checks are **not run / unverified**. RISK-RLS-005 records
possible undetected host-specific installation and instruction-delivery defects.

Continue under this bounded exception to RLO-DLV-003 as specified by VER-RLS-035.
Version the delivery plan so its verified-host coverage names Codex CLI only.
Keep both distributed packages and their independent public content checks.
Disclose the untested Claude and desktop routes beside support and completion
claims. Do not fabricate host observations to satisfy the delivery checker.

Codex CLI public fresh/update tests, exact public package hashes, documentation,
Pages, marker readbacks and the reserved human verification decision remain
required. This disposition supplies no test pass, verification verdict, changed
package identity, provider-setting change or repository adoption.

The exact packages can be delivered with these accepted omissions. Completion
means delivery under this disclosed boundary, not verified operation on the
omitted hosts. Existing release records and earlier evidence remain unchanged.

mmzen owns follow-up. Revisit before the next plugin release or before claiming
either omitted route verified, whichever occurs first. This exception does not
automatically apply to a future release.
