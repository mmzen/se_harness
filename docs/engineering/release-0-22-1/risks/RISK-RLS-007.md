+++
id = "RISK-RLS-007"
type = "risk"
title = "Unverified Codex Windows desktop for plugin 0.2.6"
status = "accepted"
owners = ["mmzen"]
created = "2026-10-05"
updated = "2026-10-05"
description = "Codex Windows desktop instruction delivery and recovery have not been tested for plugin 0.2.6. Passing Codex and Claude CLI tests do not exclude a desktop-specific delivery or selection defect. mmzen cannot access the workstation and requested a deferral proposal for review; no omission has been accepted."
action = "Keep Codex Windows desktop unverified in the release review and support claims. Obtain mmzen's explicit decision on this release-only omission. Qualify desktop before the next plugin release or before any verified-desktop claim, whichever occurs first."
raised_by = "operator"

[relations]
threatens = ["WO-RLS-041"]

[disposition]
option = "accept"
label = "Accept this release-only desktop omission and its residual risk; retain unverified desktop claims and all other checks."
decided_by = "mmzen"
decided_at = "2026-10-05T03:23:13Z"
reason = "Human mmzen: \"Accept the bounded desktop omission and risk\". This answers the reviewed DEC-RLS-009/RISK-RLS-007 proposal for evaluator 0.22.1 and plugin 0.2.6 only. Continue qualification with Codex Windows desktop not run/unverified and its residual risk accepted. Retain all CLI, public-installation, commit-bound verification and release controls; no verification, merge, release or adoption is authorized. Reviewed decision SHA-256 9d0dcccf1e61a56ce75435103932f54b20818f3363da4d66fd2329ecc48de4c8; reviewed risk SHA-256 81f4f369b793e4b40156570f89a12734d8b52ae319fc2550a5bc472049091c52."
revisit = "Before the next plugin release or before claiming Codex Windows desktop verified, whichever occurs first. Changed product scope or versions require renewed review."


[[lifecycle_events]]
from = "identified"
to = "raised"
decided_at = "2026-10-05T03:12:31Z"
decided_by = "operator"
reason = "Recorded by harnessctl raise-risk."

[[lifecycle_events]]
from = "raised"
to = "accepted"
decided_at = "2026-10-05T03:23:13Z"
decided_by = "mmzen"
reason = "Human mmzen: \"Accept the bounded desktop omission and risk\". This answers the reviewed DEC-RLS-009/RISK-RLS-007 proposal for evaluator 0.22.1 and plugin 0.2.6 only. Continue qualification with Codex Windows desktop not run/unverified and its residual risk accepted. Retain all CLI, public-installation, commit-bound verification and release controls; no verification, merge, release or adoption is authorized. Reviewed decision SHA-256 9d0dcccf1e61a56ce75435103932f54b20818f3363da4d66fd2329ecc48de4c8; reviewed risk SHA-256 81f4f369b793e4b40156570f89a12734d8b52ae319fc2550a5bc472049091c52."
+++

# Risk: Unverified Codex Windows desktop for plugin 0.2.6

## Description

Codex Windows desktop instruction delivery and recovery have not been tested for plugin 0.2.6. Passing Codex and Claude CLI tests do not exclude a desktop-specific delivery or selection defect. mmzen cannot access the workstation and requested a deferral proposal for review; no omission has been accepted.

## Next action

Keep Codex Windows desktop unverified in the release review and support claims. Obtain mmzen's explicit decision on this release-only omission. Qualify desktop before the next plugin release or before any verified-desktop claim, whichever occurs first.
