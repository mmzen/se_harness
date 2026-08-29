+++
id = "ARCH-HUP-007"
type = "architecture"
title = "Adopt 0.9.0 through the existing standard-root boundary, without a packet"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
addresses = ["REQ-HUP-018", "REQ-HUP-019"]
conforms_to = ["SPEC-HUP-009"]
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-006: one released evaluator outside the checkout writes the managed root through the installer's transaction from a wheel-file install that records the archive pair. No trust boundary, cross-cutting policy or hard-to-reverse choice is introduced; the managed workflow the transaction installs is the one WO-ECP-003 already decided and 0.9.0 released."
assessed_by = "technical-owner"
+++

# Architecture: Adopt 0.9.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.9.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-018`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair (`ARCH-REB-011`), plans against the
installed root, and writes the reviewed managed set atomically. The candidate
source in this checkout is evidence only and never writes the root.

## What moves

The five managed root files the plan lists, the installer-owned lock, the
owner statements that name the governor, the candidate version identity, and
one test literal set. Nothing under `templates/`, `se_harness/` (beyond the
version string), `release/` or the published 0.9.0 moves.

## Why no decision

`ARCH-HUP-006` established this boundary for 0.8.0 and `ARCH-HUP-005` for
0.7.1; `ADR-REB-011` decided the packet's removal and `SPEC-REB-012` admits
a recorded or `null` archive pair. This adoption applies them and introduces
no new trust boundary, cross-cutting policy or hard-to-reverse choice.
