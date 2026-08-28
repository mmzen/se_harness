+++
id = "ARCH-HUP-006"
type = "architecture"
title = "Adopt 0.8.0 through the existing standard-root boundary, without a packet"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
[relations]
addresses = ["REQ-HUP-016", "REQ-HUP-017"]
conforms_to = ["SPEC-HUP-008"]
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-005: one released evaluator outside the checkout writes the managed root through the installer's transaction. Installing from the wheel file rather than the index changes only whether the archive pair is recorded (SPEC-REB-012 already admits both); no trust boundary, cross-cutting policy or hard-to-reverse choice is introduced."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T17:04:46Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-28 by the accountable owner, 'Approve and start', for the adoption of exact public 0.8.0 (RLS-SEH-017, released and published 2026-08-28) as the standard root the simple way: one command from an isolated wheel-file install outside the checkout whose digest equals the record's bound wheel, no packet, candidate moved to 0.9.0 in the same change. Measured before this transition over branch state 5a2475f carrying unmoved main 2628627: validate PASS at 0 errors under both the governing 0.7.1 root and public 0.8.0; rehearsal on a throwaway export: plan 61 files, 9 update, 52 unchanged, no customization or conflict; 0.8.0 doctor 0 FAIL after apply; nine test modules pinned."
+++

# Architecture: Adopt 0.8.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.8.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-017`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair (`ARCH-REB-011`), plans against the
installed root, and writes the reviewed managed set atomically. The candidate
source in this checkout is evidence only and never writes the root.

## What moves

The nine managed root files the plan lists, the installer-owned lock and
`.engineering-harness.toml`, the owner statements that name the governor, the
candidate version identity, and the tests that pinned the 0.7.1 root or the
0.8.0 candidate. Nothing under `templates/`, `se_harness/` (beyond the
version string), `release/` or the published 0.8.0 moves. The retained
stage-machine files of issue #210 stay until their own work order.

## Why no decision

`ARCH-HUP-005` established this boundary for 0.7.1; `ADR-REB-011` decided
the packet's removal and `SPEC-REB-012` admits a recorded or `null` archive
pair. This adoption applies them and introduces no new trust boundary,
cross-cutting policy or hard-to-reverse choice.
