+++
id = "VER-REB-011"
type = "verification"
title = "Simple evaluator upgrade assurance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

[relations]
verifies = ["REQ-REB-027", "REQ-REB-028"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T15:20:02Z"
decided_by = "quality-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', on the owner's direction that the evaluator upgrade must be simple: the MG007 work-order packet and the MG004 and RID022 archive-digest requirements are retired, the installed evaluator's version and payload digest are its identity, index installs pass the managed lane, and the candidate-evidence lane selects the acceptance operation by the verifier's capability. REQ-REB-005 is superseded under WO-REB-027."
+++

# Verification Contract: Simple evaluator upgrade assurance

## Independence

Upgrade, identity and root-qualification cases run the evaluator from an
external environment; the candidate checkout supplies fixtures and
non-authoritative comparison only.

## Requirement-to-evidence matrix

| Requirement | Method | Pass condition |
| --- | --- | --- |
| REQ-REB-027 | fixture roots at an older lock; `upgrade` plan and `--apply` from an installed newer evaluator, with and without `--evidence-output`; customization and conflict fixtures | the transaction applies without a packet, the lock names the installed version and payload, evidence is written only when requested, refusals unchanged |
| REQ-REB-028 | `identity` and `qualify released-root` against installs with and without a PEP 610 archive digest; mismatch fixtures | pass without a digest; `RID022` only on a recorded digest that differs; `RID021` on a payload mismatch; `MG004` only when the evaluator cannot identify itself |

## Required cases

- Index-installed evaluator upgrades a schema-3 root in one `--apply`; the
  lock's `archive_sha256` is `null`; replay is a no-op.
- Wheel-file-installed evaluator does the same and records the digest.
- `--work-order` is no longer an option; the packet loader is gone; the
  `MG007` code is not emitted by any path.
- Candidate source as the runtime is still refused (`RID018`).
- The managed template's `qualify released-root` step passes on an index
  install (hosted candidate lane).
- The candidate-evidence lane runs `qualify candidate-package` with a
  verifier that carries it and the legacy bootstrap otherwise, asserting the
  result shape of the operation that ran.
- Existing evidence documents and historical `[evaluator_upgrade]` tables
  validate unchanged.

## Hosted evidence

The pull request's candidate lanes, including the managed lane on the
template under test where the repository's own root allows it.

## Evidence retention

`docs/engineering/released-evaluator-boundary/evidence/WO-REB-027-verification.md`.
