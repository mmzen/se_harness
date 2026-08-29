+++
id = "ARCH-HUP-008"
type = "architecture"
title = "Adopt 0.10.0 through the existing standard-root boundary, without a packet"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
addresses = ["REQ-HUP-020", "REQ-HUP-021"]
conforms_to = ["SPEC-HUP-010"]
[decision_assessment]
outcome = "no_significant_decision"
triggers = []
rationale = "The boundary is unchanged from ARCH-HUP-007: one released evaluator outside the checkout writes the managed root through the installer's transaction from a wheel-file install that records the archive pair. No trust boundary, cross-cutting policy or hard-to-reverse choice is introduced; the managed workflow and contracts the transaction installs are the ones WO-ECP-013 decided and 0.10.0 released."
assessed_by = "technical-owner"
+++

# Architecture: Adopt 0.10.0 through the existing standard-root boundary, without a packet

## Boundary

The released evaluator (`se-harness==0.10.0`, installed outside the checkout
from the PyPI wheel file whose digest equals `RLS-SEH-019`'s) is the only
writer of the managed root. It proves its own identity by version,
installed-payload digest and archive pair (`ARCH-REB-011`), plans against the
installed root, and writes the reviewed managed set atomically. The candidate
source in this checkout is evidence only and never writes the root.

## What moves

The six managed root files the plan lists, the installer-owned lock, the
owner statements that name the governor, the candidate version identity, and
one test literal set. Nothing under `templates/`, `se_harness/` (beyond the
version string), `release/` or the published 0.10.0 moves.

## Why no decision

`ARCH-HUP-007` established this boundary for 0.9.0; `ADR-REB-011` decided
the packet's removal and `SPEC-REB-012` admits a recorded or `null` archive
pair. This adoption applies them and introduces no new trust boundary,
cross-cutting policy or hard-to-reverse choice.
