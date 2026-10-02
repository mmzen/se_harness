+++
id = "DEC-RLS-002"
type = "decision"
title = "Choose the native qualification boundary for plugin 0.2.4"
status = "decided"
owners = ["mmzen"]
created = "2026-10-02"
updated = "2026-10-02"
kind = "deviation"
question = "May WO-RLS-032 complete package qualification with exact-release Claude Code native checks and Codex Windows desktop checks explicitly unverified, with their residual risk accepted for plugin 0.2.4 only?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-IAR-016#IAR-EXT-010"
observed = "VER-RLS-031 and VER-IAR-021 require native qualification of the exact assembled package. Claude's live request fails with expired OAuth and failed refresh; the human cannot refresh authentication now. Codex Windows desktop evidence remains unavailable. Passing package checks and prior native traces do not establish these missing results."

[[options]]
id = "accept"
label = "Accept only these two native qualification gaps for WO-RLS-032 and plugin 0.2.4; retain unverified results, risk and follow-up."

[[options]]
id = "stop"
label = "Keep WO-RLS-032 incomplete until the missing native checks pass or another formal resolution is approved."

[relations]
concerns = ["RISK-RLS-002", "WO-RLS-032", "SPEC-IAR-016", "VER-IAR-021", "VER-RLS-031", "REL-SEH-033"]
blocks = ["WO-RLS-032"]

[disposition]
option = "accept"
label = "Accept only these two native qualification gaps for WO-RLS-032 and plugin 0.2.4; retain unverified results, risk and follow-up."
decided_by = "mmzen"
decided_at = "2026-10-02T05:35:12Z"
reason = "I accept"
revisit = "Before the next plugin release, before claiming either unverified host route is verified, or before adoption that relies on either unverified route, whichever occurs first."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-02T05:35:12Z"
decided_by = "mmzen"
reason = "I accept"
+++

# Choose the native qualification boundary for plugin 0.2.4

## Request and decision still needed

Human mmzen stated: “I can’t refresh claude auth, then continue”. This permits
continuing unaffected work. It is not recorded as accepting an unverified result
or exercising a verification, publication or adoption decision.

This open proposal makes the remaining choice explicit. No disposition has been
applied. DEC-RLS-001 remains the earlier decision for WO-RLS-031; its scope is
not extended or rewritten.

## Exact package and proposed exception

The proposal applies only to WO-RLS-032's package qualification of plugin 0.2.4,
assembled from source `4031f0fa4b5c4a95651bd928a110d8b2d94f9775` with the exact
public evaluator 0.21.0 wheel bound by RLS-SEH-031. The assembled marketplace
identity is `74f0854eadfbe962105d1aba9b594ff2f1697cd038cb27c1a01b802c1fb8d890`.

Under option `accept`, keep the following results explicitly unverified:

- Claude Code native startup, activation, session recovery, compaction and other
  native matrix observations for these exact release-package bytes.
- Codex Windows desktop native instruction delivery and recovery.

The deviation is against IAR-EXT-010 as qualified by VER-IAR-021 and VER-RLS-031.
It permits qualification to carry these disclosed omissions if the human chooses
`accept`. It does not claim that the missing tests passed, change the accepted
functional definitions, or excuse any failed portable or observed native check.

## Evidence and residual risk

The exact release assembly and independent tree check pass. The Claude manifest
validator passes. The installed-package adapter walkthrough passes all 41 steps
on both Windows and Linux. Fresh native Codex CLI/app-server observations are
retained separately, with their actual results and profile limits.

Historical Claude observations used the same runtime payload and matching adapter
files, but a different wheel archive and development packaging. Their comparison
supports the risk review only. They do not replace the missing exact-package
native qualification. A logged-in status did not establish usable credentials:
the real request failed with expired OAuth and failed refresh. Its retained stream
contains native bootstrap hook output; this limited callback observation does not
establish a successful authenticated session or the remaining native matrix.

RISK-RLS-002 records possible undetected host-specific missing instructions,
incorrect selection or failed recovery. An accepted option would accept that
residual uncertainty only for this package qualification. Missing delivery still
requires the agent to stop the affected governed action and recover explicitly.

## Controls and later work

Preserve all failures and unverified rows. Do not claim verified Claude delivery
or verified Codex Windows desktop support for this exact package. Keep normal
hook trust and authentication controls; do not bypass them.

All other applicable verification, exact commit binding and human verification
remain required. No ready VREC or verification verdict follows from creating or
disposing this proposal. Marketplace publication still needs its separate exact
authorization after qualification and verification.

WO-RLS-033's public fresh-install/update tests remain separate obligations.
This proposal does not waive those tests, authorize marketplace publication,
change latest/last, authorize repository adoption or retire repository files.

## Options and recommendation

- `accept`: Continue WO-RLS-032 with these two disclosed gaps, after recording
  the human decision and risk acceptance through the supported evaluator.
- `stop`: Keep the work incomplete until matching evidence is available or a
  different formal resolution is approved.

The proposal recommends `accept` for this bounded qualification because the
public archive identities, portable checks and retained component comparisons
provide useful coverage while authentication is unavailable. The human may
choose `stop`; the recommendation grants no authority.

Proposed revisit trigger: before the next plugin release, before claiming either
unverified host route is verified, or before adoption that relies on either
unverified route, whichever occurs first. Restore Claude authentication and
complete native testing when workstation access permits. Do not carry this
exception to another package or work order automatically.
