+++
id = "WO-xxx"
type = "work_order"
title = "<Bounded implementation objective>"
status = "draft"
owners = ["<engineering owner>"]
created = "YYYY-MM-DD"
updated = "YYYY-MM-DD"

[relations]
implements = ["REQ-xxx"]
specifications = ["SPEC-xxx"]
architecture = ["ARCH-xxx", "ADR-xxx"]
verification = ["VER-xxx"]
+++

# Work Order: <title>

## Lifecycle

Use `approved` to authorize bounded execution and `implemented` after the work and retained evidence are complete. Governance-only work normally stops at `implemented`. Use `verified` or `released` only when an eligible commit-bound VREC explicitly covers this work order under the repository's configured provenance policy.

The `architecture` relation selects every applicable architecture plus every required deciding ADR. An ADR may be omitted only for a selected architecture whose accepted `decision_assessment` is `no_significant_decision`; every `adr_required` architecture needs at least one selected active ADR that decides it.

An architecture is applicable when it addresses an architecturally significant requirement implemented by this work order. Every selected architecture must conform to at least one of the selected specifications. Routine requirements without an active `addresses` edge do not require fabricated architecture coverage.

## Objective

## In scope

## Out of scope

## Authorized decision envelope

What may the implementation agent decide locally?

## Constraints

## Expected change surface

Use components rather than guessed files when the code has not yet been inspected.

## Required verification

## Evidence to record

## Stop and escalate conditions

## Completion report format
