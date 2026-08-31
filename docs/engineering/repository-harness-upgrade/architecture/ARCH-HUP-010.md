+++
id = "ARCH-HUP-010"
type = "architecture"
title = "Adopt 0.12.0 through the existing standard-root boundary, without a packet"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-08-31"
updated = "2026-08-31"
[relations]
addresses = ["REQ-HUP-025", "REQ-HUP-026"]
conforms_to = ["SPEC-HUP-013"]
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-009: one released evaluator outside the checkout writes the managed root through the installer's transaction from a wheel-file install that records its archive pair. Nothing leaves the managed set, so even the previous adoption's owner-side removal workaround is not needed; no trust boundary moves."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T13:13:31Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-31 by the accountable owner by selecting the presented option 'Approve, start, complete on green' for WO-HUP-013: the unchanged standard-root boundary, no significant decision."
+++

# Architecture: Adopt 0.12.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.12.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-021`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair, plans against the installed
root, and writes the reviewed managed set atomically. The candidate source
in this checkout is evidence only and never writes the root.

## What moves

The eight managed root files the plan lists, the installer-owned lock, the
owner statements that name the governor, the candidate version identity,
and the identity-aware test assertions the rehearsal names. Nothing under
`templates/`, `se_harness/` (beyond the version string), `release/` or the
published 0.12.0 moves; no file leaves the managed set.

## Why no decision

`ARCH-HUP-009` established this boundary for 0.11.0 and `ARCH-HUP-008` for
0.10.0. This adoption applies them and introduces no new trust boundary,
cross-cutting policy or hard-to-reverse choice; the one behavioral novelty
of the new root — the installer's own `remove` action (`WO-DST-022`) — is
released product behavior decided under its own artifacts, and this plan
exercises none of it.
