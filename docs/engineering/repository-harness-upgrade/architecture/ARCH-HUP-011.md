+++
id = "ARCH-HUP-011"
type = "architecture"
title = "Adopt 0.13.0 through the existing standard-root boundary, without a packet"
status = "approved"
owners = ["technical-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
addresses = ["REQ-HUP-027", "REQ-HUP-028"]
conforms_to = ["SPEC-HUP-014"]

[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-010: one released evaluator outside the checkout writes the managed root through the installer's transaction from a wheel-file install that records its archive pair. Nothing leaves the managed set; the Explorer redesign the new root carries is released product behavior decided under WO-DST-023's own artifacts. No trust boundary moves."
assessed_by = "technical-owner"

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T08:31:12Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-02 by the accountable owner by selecting the presented option 'Approve, start, complete on green' for WO-HUP-014: the adoption of exact public 0.13.0 (RLS-SEH-022, released and published 2026-09-02) as the standard root the simple way, from the 0.12.0 lock 4d8f9d37, rehearsed the same day on a throwaway clone of main 09aa69f. The unchanged standard-root boundary, no significant decision."
+++

# Architecture: Adopt 0.13.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.13.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-022`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair, plans against the installed
root, and writes the reviewed managed set atomically. The candidate source
in this checkout is evidence only and never writes the root.

## What moves

The five managed root files the plan lists, the installer-owned lock, the
owner statements that name the governor, the candidate version identity,
and the identity-aware test assertions the evidence names. Nothing under
`templates/`, `se_harness/` (beyond the version string), `release/` or the
published 0.13.0 moves; no file leaves the managed set.

## Why no decision

`ARCH-HUP-010` established this boundary for 0.12.0 and `ARCH-HUP-009` for
0.11.0. This adoption applies them and introduces no new trust boundary,
cross-cutting policy or hard-to-reverse choice. The one visible novelty of
the new root, the designed self-contained Explorer in this repository's
own generated dashboard and, after merge, in the public demonstration, is
released product behavior decided under `WO-DST-023`, `SPEC-DST-023` and
`ADR-DST-013`; this plan only installs it.
