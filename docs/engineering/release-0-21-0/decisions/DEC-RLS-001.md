+++
id = "DEC-RLS-001"
type = "decision"
title = "Accept the unverified desktop qualification risk for 0.21.0"
status = "decided"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
kind = "deviation"
question = "May WO-RLS-031 continue the 0.21.0 release qualification with Codex Windows desktop unverified and its residual risk accepted?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-IAR-016#IAR-EXT-010"
observed = "Native Codex Windows desktop qualification required by VER-IAR-021 and carried into VER-RLS-030 and REL-SEH-033 remains unavailable. Codex CLI/app-server and Claude evidence does not prove the desktop path."

[[options]]
id = "accept"
label = "Accept only the desktop qualification gap for WO-RLS-031 and the 0.21.0 release; retain unverified status and the residual risk."

[[options]]
id = "stop"
label = "Keep release qualification blocked until native desktop evidence or another formal resolution is available."

[relations]
concerns = ["RISK-RLS-001", "WO-RLS-031", "SPEC-IAR-016", "VER-IAR-021", "VER-RLS-030", "REL-SEH-033"]
blocks = ["WO-RLS-031"]

[disposition]
option = "accept"
label = "Accept only the desktop qualification gap for WO-RLS-031 and the 0.21.0 release; retain unverified status and the residual risk."
decided_by = "mmzen"
decided_at = "2026-10-02T04:01:56Z"
reason = "regading WO-RLS-031  : i accept that we keep the Codex Windows desktop  unverified  and the associated risk"
revisit = "Before a subsequent release, before claiming verified Codex Windows desktop support, or before adoption relying on desktop replacement delivery, whichever occurs first."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-02T04:01:56Z"
decided_by = "mmzen"
reason = "regading WO-RLS-031  : i accept that we keep the Codex Windows desktop  unverified  and the associated risk"
+++

# Accept the unverified desktop qualification risk for 0.21.0

## Exact human decision

Human mmzen stated:

> regading WO-RLS-031  : i accept that we keep the Codex Windows desktop  unverified  and the associated risk

This record applies that decision to the missing desktop qualification only.
The selected governing evaluator remains released 0.20.1.

## Scope of the departure

IAR-EXT-010 requires qualification of the candidate wheel and both host packages.
VER-IAR-021 specifies the Codex Windows desktop path; VER-RLS-030 and
REL-SEH-033 carry that evidence obligation into this release.

For WO-RLS-031 and evaluator 0.21.0 / proposed plugin 0.2.4, accept the absence
of that native desktop evidence as a disclosed qualification deviation. Desktop
startup, selected-repository delivery, manual/automatic compaction and resume
remain **unverified**. This decision resolves the desktop-only qualification
hold for this release. It does not mark any missing check as passed.

The functional requirements remain unchanged. Preserve the approved specification,
verification contracts, release contract, work-order history and earlier evidence.
This is a release-specific accepted deviation, not a rewritten definition or a
permanent platform exemption. Existing native CLI/app-server and Claude traces
remain evidence for their own observed paths only.

## Risk and controls

RISK-RLS-001 records the possibility of undetected desktop-specific failures:
missing or incorrect instructions, lost selection, or failed recovery. Human
mmzen accepts that residual uncertainty for this release preparation.

Retain the unverified desktop row and this decision in the final qualification
assessment, the aggregate VREC evidence and the release handoff. Do not advertise
verified Codex Windows desktop support. Missing instructions still stop affected
governed work and require explicit repository/evaluator recovery.

All other required checks, exact candidate and evidence binding, native Codex CLI
and Claude qualification, independent builds, human aggregate verification,
release-record decision and external controls remain required. This decision
supplies none of those results or later decisions. It does not authorize a
marketplace action or retire repository instruction files.

## Options and revisit

- **accept:** Continue the selected release work with this disclosed limitation
  and accepted residual risk. Apply the existing supported decision operation.
- **stop:** Keep the work blocked and the risk unresolved pending desktop evidence
  or a different formal decision. Do not infer acceptance from inaction.

Revisit before a subsequent release, before a claim of verified Codex Windows
desktop support, or before adoption that relies on desktop replacement delivery,
whichever occurs first. This decision does not carry forward automatically.
A future qualification must retain matching native desktop observations.

## Preserved accepted inputs

The following full-file digests identify the authority read for this decision.
None of these files is edited by the decision operation.

| Artifact | SHA-256 |
| --- | --- |
| SPEC-IAR-016 | `1f7015733951ed72d9c5448f8dd0d22a7367100b6a147801b2697ccfa3a0c272` |
| VER-IAR-021 | `0a6a0415756a8e42b0ed363e16e1ab7ff03b1d7ce9929ac5548ac37976bcba31` |
| VER-RLS-030 | `fdc93f2925ce6370f99e60ffe03a0dccb431c9b93c88739921408cbe5d429e84` |
| REL-SEH-033 | `356f85a8c199d32b97d13d49451d33b1ad9b604e32ce9ec1b037fd74c47d0fc9` |
| WO-RLS-031 | `5b4ec08610537c2959e4d149385a02415a8829cb6c1918265355a9dc37dcbc7c` |
