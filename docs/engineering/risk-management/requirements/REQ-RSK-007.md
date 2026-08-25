+++
id = "REQ-RSK-007"
type = "requirement"
title = "Close the accepted deviations of the risk artifact"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN the risk artifact is installed, THE SYSTEM SHALL run raise-risk under its own registered mutation-guard operation, SHALL report an invalid [risk] section from doctor as C-RSK-001, SHALL let the draft-change and execute-work-order skills raise risks and the prepare-assurance skill include the risk register in its packet, and SHALL specify the residual fields, the computed raise, and the reading-step placement exactly as shipped under WO-RSK-001."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-RSK-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T17:15:22Z"
decided_by = "requirements-steward"
+++

# Requirement: Close the accepted deviations of the risk artifact

## Rationale

`WO-RSK-001` shipped the risk artifact with seven recorded deviations from
`SPEC-RSK-001`, each accepted by the owner on 2026-08-25 and logged in the
retained evidence. Four were accepted as work to do (a dedicated guard
operation, a `doctor` check, the skill cores) or as amendments (residual
placement, computed raise, reading-step placement); this requirement is that
work. The Explorer register view is deliberately left to a later requirement.

## Preconditions and trigger

Installation or upgrade of the standard harness; `harnessctl raise-risk`;
`harnessctl doctor`; explicit invocation of a portable skill.

## Required response

- `mutation_guard.PUBLIC_MUTATION_OPERATIONS` contains `raise-risk`, and
  `raise-risk` requests authority under that name.
- `doctor` reports `C-RSK-001` when `.engineering-harness.toml` carries a
  `[risk]` section that `load_risk_policy` rejects; the validator's
  `E-RSK-007` is unchanged.
- `harness-draft-change` and `harness-execute-work-order` may invoke
  `raise-risk` from within their closed effect plans; `harness-prepare-assurance`
  includes the register for the selected work orders in its assurance packet;
  no skill disposes. Contract versions and the canonical vectors are updated.
- `SPEC-RSK-002` records as normative: residual fields at top level as
  numerals in string or integer form; `identified -> raised` enforced by
  computation at raise time and `E-RSK-003`, not by a transition guard; the
  `RISKS` reading step present in the work-order procedures only.

## Failure and boundary behavior

An unregistered guard operation refuses before writing; a `doctor` check is a
FAIL line, not a warning; a skill that attempts to dispose a risk stops at its
existing accountable-decision stop condition.

## Constraints

No change to the artifact schema, lifecycle family, gates, or decision rights.

## Acceptance examples

### Example: normal behavior

**Given** a target with `[risk] acceptance_level = 40`

**When** `harnessctl doctor` runs

**Then** it reports `C-RSK-001` naming the invalid value.

### Example: failure behavior

**Given** the execute skill's effect plan admits `raise-risk`

**When** the plan also admits a `transition` on a risk

**Then** the skill's guard rejects the plan before any effect.

## Open decisions

None.
