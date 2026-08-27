+++
id = "REQ-RSK-004"
type = "requirement"
title = "Block a threatened stage while a risk is undisposed"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a gate is evaluated for a selected artifact, THE SYSTEM SHALL fail the gate when a risk in status raised threatens the selected artifact or its governing chain, SHALL additionally fail release preparation and release decision gates when a risk in status mitigating threatens the released work, SHALL pass when no such risk exists, and SHALL render the disposing role as the corrective escalation."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "requirements-steward"
+++

# Requirement: Block a threatened stage while a risk is undisposed

## Rationale

`HRN-008`: gates fail closed; a warning is not acceptance. A raised risk
that did not block would be a warning by another name. Blocking the stage the
risk threatens, and only that stage, keeps the effect bounded (`HRN-003`).
Owner decision 2026-08-25: `mitigating` blocks release, so a release ships
either with mitigation verified or with an explicitly accepted residual.

## Preconditions and trigger

`harnessctl check`, `transition`, `capture-verification`, `prepare-release`.

## Required response

- One evaluator `undisposed_risks_threatening_scope`; predicates
  `QGP-G1-RISK`, `QGP-G2-RISK`, `QGP-G3-RISK`, `QGP-G4I-RISK`,
  `QGP-G4A-RISK`, `QGP-G5P-RISK`, `QGP-G5D-RISK` in the corresponding gates.
- `raised` blocks everywhere; `mitigating` blocks only `QG-G5-*`.
- Corrective form for every `*-RISK` predicate: escalation to
  `DR-RISK-DISPOSE`; at `QG-G5-*` for a `mitigating` risk, the command that
  focuses the first named mitigation work order.
- An empty register passes.

## Failure and boundary behavior

A malformed risk in scope is `not_assessable`. `identified` risks never
affect a gate.

## Constraints

No new gate; the restitution headings are unchanged.

## Acceptance examples

### Example: normal behavior

**Given** `RISK-X-001` raised, threatening `WO-X-001` in progress

**When** `check --artifact WO-X-001 --checkpoint handoff`

**Then** `QGP-G4I-RISK` fails naming the risk, score, and engineering owner.

### Example: failure behavior

**Given** the risk is `mitigating`

**When** `check --artifact WO-X-001 --checkpoint handoff`

**Then** `QGP-G4I-RISK` passes; `prepare-release` including `WO-X-001` fails
`QGP-G5P-RISK`.

## Open decisions

None.
