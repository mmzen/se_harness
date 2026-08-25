+++
id = "REQ-RSK-003"
type = "requirement"
title = "Dispose a raised risk by the owner of the stage it threatens"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN a risk is raised, THE SYSTEM SHALL require an explicit transition to accepted, avoided, mitigating, or withdrawn exercised under DR-RISK-DISPOSE by the accountable owner of the risk's stage, SHALL require a non-empty rationale, a named avoided_by ADR for avoided, at least one mitigated_by artifact for mitigating, and SHALL permit mitigating to become mitigated only when every named work order is covered by a verified verification record and the residual score is recorded."
verification_method = "automated-test-and-manual-review"
[relations]
derives_from = ["CAP-RSK-001"]
+++

# Requirement: Dispose a raised risk by the owner of the stage it threatens

## Rationale

`DR-001` requires every decision to name artifact, target, actor, and
meaning; `DR-010` stops the workflow when the role is ambiguous. Resolving the
disposer from the threatened stage keeps the role catalogue closed and puts
the risk in front of the person who already owns the thing at risk. Owner
decision 2026-08-25: no dedicated risk-owner role.

## Preconditions and trigger

A `harnessctl transition` on a risk artifact.

## Required response

- Lifecycle family `risk`: `identified -> {raised, accepted, withdrawn}`;
  `raised -> {accepted, avoided, mitigating, withdrawn}`;
  `mitigating -> {mitigated}`; `accepted`, `avoided`, `mitigated`, and
  `withdrawn` are terminal.
- Decision right `DR-RISK-DISPOSE`; accountable role by stage: definition ->
  product or domain owner; architecture -> technical owner; implementation ->
  engineering owner; verification -> assurance owner; release -> release
  owner; operation -> service owner. A risk threatening two stages is disposed
  by the higher stage's owner and the reason names both.
- `identified -> accepted` is permitted to the same role (below-level risks
  may be accepted at the owner's next decision); it is never automatic.
- `mitigated` requires `residual_likelihood` and `residual_impact`; a residual
  score at or above the level requires the word "accepted" and the reason in
  the same transition.

## Failure and boundary behavior

A transition by any other actor, without a reason, or without the required
relation is refused before writing. A `mitigating` risk whose named work
order is not yet covered by a verified VREC cannot become `mitigated`.

## Constraints

Disposing changes only the risk (`WFL-002`).

## Acceptance examples

### Example: normal behavior

**Given** `RISK-X-001` raised at stage implementation

**When** `transition --set RISK-X-001=mitigating --decision RISK-X-001=engineering-owner --reason "RISK-X-001=mitigated_by WO-X-002"`

**Then** the risk is `mitigating` with `mitigated_by = ["WO-X-002"]`.

### Example: failure behavior

**Given** the same risk

**When** the decision actor is `release-owner`

**Then** the transition is refused naming the accountable role.

## Open decisions

None.
