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
- `harness-draft-change` and `harness-execute-work-order` may carry a new
  `identified` or `raised` risk path inside their closed effect plans, with no
  scope decision, and the component that performs the governed-target write
  performs this one; `harness-prepare-assurance` includes the register for the
  selected work orders in its assurance packet; no skill disposes a risk, and no
  skill holds a risk-raising effect class of its own. The affected contract
  version and the portable-core digests are updated.
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

**Given** the execute skill's effect plan names a new risk path

**When** the plan also offers a risk-raising or risk-disposing effect class

**Then** the skill's guard rejects the plan before any effect and before the
component that performs the write is called.

## Open decisions

None.

## Amendment record

**The third bullet of the required response and the failure-behaviour acceptance
example, amended 2026-08-27 by the engineering owner under `WO-RSK-003`, in the
same act that amended `SPEC-RSK-002` rules RSK2-SKL-001 and RSK2-SKL-003 and
`VER-RSK-002`'s `RSK2-SKL-001/002` row and acceptance scenario 2.** Both
statements named a mechanism rather than an obligation. They were written against
the schema-v2 skill surface, in which a portable skill wrote governed targets
itself and could therefore invoke a `raise-risk` operation from its own effect
plan. `WO-AEX-006`, `WO-AEX-007` and `WO-AEX-008` replaced that surface with the
schema-v3 closed contracts of the delegated execution model, in which the
evaluator owns every governed-target write, and `_parse_v3_contract` refuses the
alternative by identifier: `SKC036` requires `client.direct_target_writes` false
and `client.target_writer` `"evaluator"`, and `SKC038` requires
`effects.permitted` to equal the closed profile exactly and requires
`"direct-target-write"` among the prohibitions.

The required response now states the obligation and leaves the mechanism to
`SPEC-RSK-002`. The obligation is unchanged and is delivered: both skills may
carry a new risk path inside a closed effect plan with no scope decision, by the
standing exception of `REQ-RSK-006` shipped under `WO-RSK-001`; the register
reaches the assurance packet; and no skill disposes. The amendment adds the
stronger statement that no skill holds a risk-raising effect class at all, and
narrows the fixture claim from "the canonical vectors" to the affected contract
version and the portable-core digests, because only one of the three contracts
changes and the Phase 3 record is frozen. The acceptance example is restated for
the same reason: an effect plan that "admits `raise-risk`" is not constructable,
so the example could not be run as written; the amended example asserts the same
refusal against a plan that is.

The `statement` field is unchanged and needs no amendment. It requires the system
to "let the draft-change and execute-work-order skills raise risks", which is
true of the delivery and does not depend on which component performs the write.
The `WHEN` clause, `verification_method`, the relations, the lifecycle events,
the rationale, the preconditions and trigger, the first, second and fourth
bullets of the required response, the failure and boundary behaviour, the
constraints, the normal-behaviour acceptance example, and the statement that
there are no open decisions are all unchanged. No permission to skip a check is
added and none is removed, no refusal becomes a warning, and no waiver is
introduced.
