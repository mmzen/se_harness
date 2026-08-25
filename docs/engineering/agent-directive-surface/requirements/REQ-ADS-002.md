+++
id = "REQ-ADS-002"
type = "requirement"
title = "One selected state yields one canonical next step in one restitution dialect"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN `harnessctl focus` and `harnessctl check` evaluate the same selected artifact at the same formal snapshot, THE SYSTEM SHALL resolve the same `WORKFLOW.json` procedure step and render the schema-2 restitution headings by default."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-ADS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T10:36:12Z"
decided_by = "requirements-steward"
+++

# Requirement: One selected state yields one canonical next step in one restitution dialect

## Rationale

The router mandates the schema-2 headings and the owner fragment says "return
schema-2 verbatim", yet `focus` defaults to schema 1 and, for an `in_progress`
work order, recommends `preflight --phase review` while `check` recommends
`check --checkpoint handoff`. `WFL-003` tells the agent to take the first
matching recommendation; it receives two firsts.

## Preconditions and trigger

Any `focus` or `check` invocation on a selected WO, VREC, or RLS.

## Required response

Both commands resolve the ordered workflow rule and its bound procedure step
from the same contract function. `focus` renders schema 2 unless
`--result-schema 1` is passed explicitly. The `Next` and `Command or response`
values are byte-identical between the two commands for the same state and
snapshot when no checkpoint-specific argument is supplied to `check`.

## Failure and boundary behavior

Schema 1 remains available for one compatibility release and emits a `WEX`
warning stating that its block is not restitution.

## Constraints

No lifecycle state, decision right, or gate changes. The `WORKFLOW.json`
contract remains byte-identical to the packaged contract.

## Acceptance examples

### Example: normal behavior

**Given** `WO-X-001` is `in_progress`

**When** `focus . --artifact WO-X-001` and `check . --artifact WO-X-001 --checkpoint handoff` are run at the same snapshot

**Then** both render the schema-2 headings and the same `Next` step identifier.

### Example: failure behavior

**Given** `focus . --artifact WO-X-001 --result-schema 1`

**When** it renders

**Then** the output carries one warning that schema 1 is not restitution.

## Open decisions

None.
