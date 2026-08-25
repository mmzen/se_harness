+++
id = "REQ-RSK-005"
type = "requirement"
title = "Trace mitigation to governed work and list risks in a release"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a risk is disposed as mitigating, avoided, or mitigated, THE SYSTEM SHALL validate its mitigated_by targets as work orders, requirements, verification contracts, or operating contracts and its avoided_by target as one architecture decision record, and WHEN a release record is prepared, THE SYSTEM SHALL derive lists_risks naming every accepted or mitigated risk that threatens the released work and SHALL refuse preparation while any raised or mitigating risk threatens it."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T13:25:29Z"
decided_by = "requirements-steward"
+++

# Requirement: Trace mitigation to governed work and list risks in a release

## Rationale

Mitigation that is not itself governed work is a promise. Naming the work
order, requirement, verification contract, or operating contract makes the
promise a traceable obligation with its own approval and evidence. A release
that names the risks it ships with is what an attestation of "risks
identified and mitigated or accepted" rests on.

## Preconditions and trigger

Validation of a disposed risk; `harnessctl prepare-release`.

## Required response

- Relations `threatens` (RISK -> any active artifact, stage-matched),
  `mitigated_by` (RISK -> WO | REQ | VER | OPS), `avoided_by` (RISK -> ADR),
  `lists_risks` (RLS -> RISK), added to `TRACEABILITY.md` as
  `TRC-REL-020` to `TRC-REL-023`.
- `prepare-release` derives `lists_risks` from the released work set and
  writes it into the ready record; the record's body carries a risk table.
- A `mitigated_by` work order must be active; a `mitigated` risk's work
  orders must each be covered by a verified VREC at any commit.

## Failure and boundary behavior

An undeclared relation pair is rejected (`TRC-002`). A release record whose
`lists_risks` omits a qualifying risk is a governance error.

## Constraints

Historical release records are unaffected.

## Acceptance examples

### Example: normal behavior

**Given** `RISK-X-001` mitigated by `WO-X-002` (verified) and accepted
`RISK-X-002`, both threatening `WO-X-001`

**When** `prepare-release` includes `WO-X-001`

**Then** the ready RLS lists both risks.

### Example: failure behavior

**Given** `RISK-X-001` still `mitigating`

**When** `prepare-release` includes `WO-X-001`

**Then** no record is written and `QGP-G5P-RISK` names the risk.

## Open decisions

None.
