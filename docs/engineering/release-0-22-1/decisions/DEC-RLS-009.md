+++
id = "DEC-RLS-009"
type = "decision"
title = "Keep Codex Windows desktop unverified for plugin 0.2.6"
status = "decided"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"
kind = "deviation"
question = "May WO-RLS-041 complete qualification for evaluator 0.22.1 and plugin 0.2.6 with Codex Windows desktop tests not run, the remaining risk accepted for this release, and desktop support explicitly unverified?"
raised_by = "Codex"
recommendation = "accept"
against = "SPEC-IAR-016#IAR-EXT-010"
observed = "Codex Windows desktop instruction delivery and recovery have not been tested. mmzen cannot access the workstation and requested a deferral proposal, not acceptance. Actual Codex and Claude CLI qualification passes, but it does not establish desktop behavior."

[[options]]
id = "accept"
label = "Accept this release-only desktop omission and its residual risk; retain unverified desktop claims and all other checks."

[[options]]
id = "stop"
label = "Keep qualification incomplete until the required desktop tests pass or another explicit disposition applies."

[relations]
concerns = ["RISK-RLS-007", "WO-RLS-041", "WO-RLS-040", "REL-SEH-035", "SPEC-IAR-016", "VER-IAR-021", "VER-RLS-036", "VER-RLS-037"]
blocks = ["WO-RLS-041"]

[disposition]
option = "accept"
label = "Accept this release-only desktop omission and its residual risk; retain unverified desktop claims and all other checks."
decided_by = "mmzen"
decided_at = "2026-10-05T03:23:13Z"
reason = "Human mmzen: \"Accept the bounded desktop omission and risk\". This answers the reviewed DEC-RLS-009/RISK-RLS-007 proposal for evaluator 0.22.1 and plugin 0.2.6 only. Continue qualification with Codex Windows desktop not run/unverified and its residual risk accepted. Retain all CLI, public-installation, commit-bound verification and release controls; no verification, merge, release or adoption is authorized. Reviewed decision SHA-256 9d0dcccf1e61a56ce75435103932f54b20818f3363da4d66fd2329ecc48de4c8; reviewed risk SHA-256 81f4f369b793e4b40156570f89a12734d8b52ae319fc2550a5bc472049091c52."
revisit = "Before the next plugin release or before claiming Codex Windows desktop verified, whichever occurs first. Changed product scope or versions require renewed review."

[[lifecycle_events]]
from = "open"
to = "decided"
decided_at = "2026-10-05T03:23:13Z"
decided_by = "mmzen"
reason = "Human mmzen: \"Accept the bounded desktop omission and risk\". This answers the reviewed DEC-RLS-009/RISK-RLS-007 proposal for evaluator 0.22.1 and plugin 0.2.6 only. Continue qualification with Codex Windows desktop not run/unverified and its residual risk accepted. Retain all CLI, public-installation, commit-bound verification and release controls; no verification, merge, release or adoption is authorized. Reviewed decision SHA-256 9d0dcccf1e61a56ce75435103932f54b20818f3363da4d66fd2329ecc48de4c8; reviewed risk SHA-256 81f4f369b793e4b40156570f89a12734d8b52ae319fc2550a5bc472049091c52."
+++

# Proposed desktop-test omission for plugin 0.2.6

## Decision requested

Accept the Codex Windows desktop qualification omission for REL-SEH-035 only:
evaluator 0.22.1 and plugin 0.2.6. Record RISK-RLS-007 as accepted. This is a
proposal; the decision is open and the risk remains raised.

mmzen requested: "No—prepare a deferral proposal for review". That instruction
does not accept the omission. The proposed mechanism is an accepted deviation
against IAR-EXT-010 as assessed by VER-IAR-021 and VER-RLS-037, not a test pass
or an implicit change to the verification contracts.

## Exact boundary

Codex Windows desktop startup, checkout selection, instruction delivery,
compaction and resume remain **not run / unverified** for this release.
Undetected desktop-specific delivery or selection defects remain possible.
No desktop failure is claimed from the absence of a test.

The scope is the currently approved release unit in REL-SEH-035. Its current
qualified package source is 061307929c94314ccd2beb4a53f174e536fceba8; the
matching wheel is identified in ../evidence/WO-RLS-043/corrected-bundle.json.
Final candidate and package identities must still be qualified and bound in
the aggregate verification record before the human verification decision.
This exception covers that bounded release qualification. It does not cover
changed product scope, a different version, or a future release.

## Consequences of each option

- `accept`: Permit completion of WO-RLS-041 when all remaining checks pass.
  Keep the desktop omission and residual risk visible in verification, release
  and current support claims. Do not describe desktop delivery as verified.
- `stop`: Leave the affected qualification incomplete until desktop evidence
  is available or a different human disposition is recorded.

Acceptance does not complete the work order or verify the release. It permits
only the stated omission; the evaluator applies each later lifecycle action.

## Checks that remain required

Keep Codex CLI and Claude Code native checks, portable tests, exact package
comparisons, commit-bound assurance and all required gates. Retain the original
failed attempts and successful correction evidence. CLI evidence must not be
relabeled as desktop evidence.

This proposal does not waive VER-RLS-038 public-route checks. The delivery plan
must retain Codex CLI and Claude Code fresh-install and update observations,
and keep Windows desktop outside verified-host claims. It does not defer the
marketplace surface or count missing desktop evidence as public success.

Human verification, merge, the exact complete-release decision and adoption
remain separate. The existing release contract and historical decisions stay
unchanged; this new record identifies the bounded qualification departure.

## Follow-up and revisit

mmzen owns follow-up. Require desktop qualification before the next plugin
release or before claiming Codex Windows desktop verified, whichever occurs
first. Changed product scope or versions require renewed review. No automatic
extension is permitted.

The evaluator must record an accepted disposition with this revisit trigger.
No disposition or acceptance event has been inserted by hand.
