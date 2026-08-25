+++
id = "REQ-ADS-001"
type = "requirement"
title = "A blocked or failed checkpoint names a distinct corrective step"
status = "draft"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-25"
updated = "2026-08-25"
statement = "WHEN `harnessctl check` reports a blocked or failed outcome for a selected artifact, THE SYSTEM SHALL render under `Next` and `Command or response` either one command that differs from the evaluated command and addresses the first reported failing predicate, or one accountable escalation naming the role; it SHALL NOT render the evaluated command unchanged."
verification_method = "automated-test"
[relations]
derives_from = ["CAP-ADS-001"]
+++

# Requirement: A blocked or failed checkpoint names a distinct corrective step

## Rationale

The router's failure procedure requires "one safe retry or one accountable
escalation". At `0276dd7`, `harnessctl check . --artifact WO-TCM-001
--checkpoint handoff` reported `Blocked` on `QGP-G4I-COMPLETE`, `QGP-G4I-PATHS`
and `QGP-G4I-EVIDENCE` and rendered the identical command as `Next`. An agent
that obeys `WFL-003` re-runs the same command and loops. The corrective
arguments (`--changed-path`, `--changes-complete`, an evidence path bound to
the formal snapshot) exist but are only discoverable in `--help`.

## Preconditions and trigger

A `check` invocation at any checkpoint whose aggregate outcome is `blocked` or
`failed` under `QG-009` ordering.

## Required response

For the first failing predicate in aggregation order, render the corrective
form declared for that predicate in `WORKFLOW.json`. Where no corrective
command exists, render the accountable escalation naming the decision-right
role. The rendered command must differ from the evaluated command in at least
one argument.

## Failure and boundary behavior

A predicate without a declared corrective form fails contract loading with a
stable diagnostic; the renderer never falls back to the evaluated command.
`not_assessable` follows the same rule as `fail`.

## Constraints

Rendering changes no lifecycle state and exercises no decision right. The
corrective command is a suggestion carried by the contract, not authority.

## Acceptance examples

### Example: completeness not asserted

**Given** `WO-X-001` is `in_progress` and `check --checkpoint handoff` is run
without `--changed-path` or `--changes-complete`

**When** `QGP-G4I-COMPLETE` fails

**Then** `Command or response` renders the same invocation with
`--changed-path <path>` placeholders and `--changes-complete` appended, and
`Next` names `STEP-WO-IMPLEMENT-CHECK` with the corrective form.

### Example: failure behavior

**Given** a contract where a predicate has no corrective form

**When** the contract is loaded

**Then** loading fails with one stable diagnostic and no restitution is rendered.

## Open decisions

None.
