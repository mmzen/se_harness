+++
id = "ARCH-HUP-009"
type = "architecture"
title = "Adopt 0.11.0 through the existing standard-root boundary, without a packet"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
addresses = ["REQ-HUP-022", "REQ-HUP-023"]
conforms_to = ["SPEC-HUP-011"]
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-008: one released evaluator outside the checkout writes the managed root through the installer's transaction from a wheel-file install that records its archive pair; the explicit removal of files the installer no longer manages is owner content under the work order's scope, a workaround for issue #271, and introduces no trust boundary."
assessed_by = "technical-owner"
+++

# Architecture: Adopt 0.11.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.11.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-020`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair (`ARCH-REB-011`), plans against the
installed root, and writes the reviewed managed set atomically. The candidate
source in this checkout is evidence only and never writes the root.

## What moves

The nine managed root files the plan lists, the installer-owned lock, the
fifteen files the previous lock managed and the new plan omits (removed by
the work order, not the installer), the owner statements that name the
governor, the candidate version identity, and the test assertions that
declared the 0.10.0 root's divergences. Nothing under `templates/`,
`se_harness/` (beyond the version string), `release/` or the published
0.11.0 moves.

## Why no decision

`ARCH-HUP-008` established this boundary for 0.10.0; `ADR-REB-011` decided
the packet's removal and `SPEC-REB-012` admits a recorded or `null` archive
pair. This adoption applies them and introduces no new trust boundary,
cross-cutting policy or hard-to-reverse choice; the installer's missing
`remove` action is a defect recorded as issue #271 for a later work order,
not a decision taken here.
