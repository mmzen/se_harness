+++
id = "DEC-RLS-004"
type = "decision"
title = "Choose the Codex Windows desktop evidence boundary for public delivery"
status = "decided"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
kind = "deviation"
question = "May WO-RLS-033 retain Codex Windows desktop delivery as unverified with its residual risk accepted for public plugin 0.2.4?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-RLO-006#RLO-DLV-003"
observed = "WO-RLS-033 retains the Codex Windows desktop native evidence requirement. CLI and app-server checks do not prove desktop startup, compaction or resume. Prior desktop risk acceptance applies to WO-RLS-031 and WO-RLS-032; the latest human instruction accepts only the Claude gap in WO-RLS-033."

[[options]]
id = "accept"
label = "Accept only the remaining Codex Windows desktop evidence gap for WO-RLS-033 and plugin 0.2.4; keep the desktop unverified."

[[options]]
id = "stop"
label = "Keep WO-RLS-033 pending until desktop evidence or another formal resolution is available."

[relations]
concerns = ["WO-RLS-033", "VER-RLS-032", "SPEC-RLO-006", "REL-SEH-033"]
blocks = ["WO-RLS-033"]

[disposition]
option = "accept"
label = "Accept only the remaining Codex Windows desktop evidence gap for WO-RLS-033 and plugin 0.2.4; keep the desktop unverified."
decided_by = "mmzen"
decided_at = "2026-10-02T07:18:45Z"
reason = "Human mmzen: I accept. Accepts the reviewed DEC-RLS-004 Codex Windows desktop evidence gap for WO-RLS-033 and public plugin 0.2.4 only. Desktop results remain unverified; no VREC acceptance, external action, marker update or adoption is implied."
revisit = "Before the next plugin release, before claiming verified Codex Windows desktop support, or before adoption depending on verified desktop delivery, whichever occurs first."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-02T07:18:45Z"
decided_by = "mmzen"
reason = "Human mmzen: I accept. Accepts the reviewed DEC-RLS-004 Codex Windows desktop evidence gap for WO-RLS-033 and public plugin 0.2.4 only. Desktop results remain unverified; no VREC acceptance, external action, marker update or adoption is implied."
+++

# Choose the Codex Windows desktop evidence boundary for public delivery

## Decision needed

The proposal concerns only public plugin 0.2.4 at
`7e366438165a40a14783bac650a2887e7ec8bc75`, evaluator 0.21.0 and WO-RLS-033.
Earlier desktop decisions remain unchanged. DEC-RLS-003 records the human's
separate acceptance of the missing Claude tests.

Desktop startup, activation, compaction and resume remain unverified. Public
fresh installation and update, exact package bytes and offline setup pass.
Codex CLI/app-server observations are separate evidence. They cannot establish
desktop behavior. The residual risk is an undetected desktop-specific failure
to deliver or restore the selected instructions.

## Options

- `accept`: Permit this disclosed desktop omission under WO-RLS-033. Preserve
  unverified status and all passing/failing evidence. Human mmzen owns the risk.
- `stop`: Keep completion pending until matching desktop evidence exists or a
  different formal resolution is approved.

Acceptance would not supply human verification of a VREC, publication, a marker
change or adoption. It would not make missing tests pass or permit a verified
desktop-support claim. Complete delivery must still disclose unresolved surfaces.

## Recommendation and revisit

Recommend `accept`, consistent with the exact package's previous desktop risk
boundary, while keeping the separate work-order scope explicit. All other
required checks and commit-bound verification remain required.

Proposed revisit: before the next plugin release, before claiming verified
Codex Windows desktop support, or before adoption depending on verified desktop
delivery, whichever occurs first. Retain desktop as unverified until observed.

No disposition has been applied. The human must choose; the evaluator records it.
