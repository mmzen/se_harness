+++
id = "ARCH-HUP-012"
type = "architecture"
title = "Adopt 0.14.0 through the existing standard-root boundary, without a packet"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
addresses = ["REQ-HUP-029", "REQ-HUP-030", "REQ-HUP-031", "REQ-HUP-032"]
conforms_to = ["SPEC-HUP-015", "SPEC-HUP-016"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-011: one released evaluator outside the checkout writes the managed root through the installer's transaction from a wheel-file install that records its archive pair. Nothing leaves the managed set and the new root carries no behavioural change. No trust boundary moves."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T11:42:30Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented option 'Approve, start, complete on green, prepare and verify the VREC' for WO-HUP-015: the adoption of exact public 0.14.0 (RLS-SEH-023, released and published 2026-09-02) as the standard root the simple way, from the 0.13.0 lock 9dfec5b4, rehearsed the same day on a throwaway clone of main 25c0ef9. The unchanged standard-root boundary, no significant decision."
+++

# Architecture: Adopt 0.14.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.14.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-023`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair, plans against the installed
root, and writes the reviewed managed set atomically. The candidate source
in this checkout is evidence only and never writes the root.

## What moves

The three managed root files the plan lists, the installer-owned lock, the
owner statements that name the governor, the candidate version identity,
and the one identity-aware test assertion the evidence names. Nothing under
`templates/`, `se_harness/` (beyond the version string), `release/` or the
published 0.14.0 moves; no file leaves the managed set.

## Why no decision

`ARCH-HUP-011` established this boundary for 0.13.0 and its predecessors
for every earlier root. This adoption applies them and introduces no new
trust boundary, cross-cutting policy or hard-to-reverse choice; 0.14.0 is
0.13.0 by another version.

## Amendment record

- 2026-09-05, under `WO-HUP-016`, whose execution scope names this file,
  before its start preflight and for the owner's start decision. The
  architecture now also addresses `REQ-HUP-031` and `REQ-HUP-032` and
  conforms to `SPEC-HUP-016`: the 0.15.0 adoption crosses the same
  standard-root boundary the same way, one released evaluator outside the
  checkout writing the managed root through the installer's transaction
  from a digest-verified wheel-file install. The decision assessment is
  unchanged. Without this relation the start preflight reported `W021`,
  the selected architecture unrelated to the selected requirements; the
  0.14.0 packet had drafted this architecture for its own requirements,
  and the 0.15.0 packet reused it without extending the relation.
