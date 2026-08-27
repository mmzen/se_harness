+++
id = "ARCH-HUP-005"
type = "architecture"
title = "Adopt 0.7.1 through the existing standard-root boundary, without a packet"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
[relations]
addresses = ["REQ-HUP-014", "REQ-HUP-015"]
conforms_to = ["SPEC-HUP-007"]
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-004: one released evaluator outside the checkout writes the managed root through the installer's transaction. What changed, the removal of the packet and the archive-digest requirement, was decided in ADR-REB-011 under WO-REB-027; this adoption exercises that decision and takes none of its own."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T17:43:24Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', for the adoption of exact public 0.7.1 as the standard root the simple way (REQ-REB-027, REQ-REB-028 shipped by RLS-SEH-016): one command from an isolated index install outside the checkout, no packet, candidate moved to 0.8.0 with its scenario in the same change. Successor to the rejected WO-HUP-006. Measured before this transition over branch state 12e9e36 carrying unmoved main 23d5781: validate PASS at 986 artifacts, 0 errors under both the governing 0.6.0 root and public 0.7.1; doctor 0 FAIL; upgrade plan 61 files, 43 add or update, 18 unchanged."
+++

# Architecture: Adopt 0.7.1 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.7.1`, installed outside the checkout
from the index) is the only writer of the managed root. It proves its own
identity by version and installed-payload digest (`ARCH-REB-011`), plans
against the installed root, and writes the reviewed managed set atomically.
The candidate source in this checkout is evidence only and never writes the
root.

## What moves

The managed root files the plan lists, the installer-owned lock, the owner
statements that name the governor, the candidate version identity with its
migration scenario, and the tests that pinned the 0.6.0 root. Nothing under
`templates/`, `se_harness/` (beyond the version string), `release/` or the
published 0.7.1 moves.

## Why no decision

`ARCH-HUP-004` established this boundary for 0.7.0; `ADR-REB-011` decided
the packet's removal. This adoption applies both and introduces no new
trust boundary, cross-cutting policy or hard-to-reverse choice.
