+++
id = "SPEC-VSP-002"
type = "specification"
title = "State-aware verification provenance contract"
status = "approved"
owners = ["technical-owner", "quality-owner"]
created = "2026-08-24"
updated = "2026-08-24"

[relations]
specifies = ["REQ-VSP-008"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-24T10:35:25Z"
decided_by = "technical-owner"
+++

# Specification: State-aware verification provenance contract

## Scope

Align verification-record preparation, lifecycle transition, and validation for current `prepared_at` records while preserving the historical pre-0.6.0 `verified_at` capture shape. This specification changes no lifecycle edge, successor eligibility rule, decision right, or concrete record disposition.

## Actors and external systems

Preparation actors create ready records. Assurance owners verify, reject, or supersede them. The transition command applies only the selected decision. The packaged validator assesses the resulting graph. Installed consumer repositories receive the corrected managed validator only through a later authorized release and upgrade. No network service is required.

## Inputs

- A current ready VREC with `prepared_at`, `prepared_by`, candidate identity, evidence, work-order coverage, and verification-contract coverage.
- Exactly one explicit assurance decision selecting `superseded` and one successor VREC ID.
- One distinct verified or released successor whose work-order set covers the source set.
- Historical VRECs that may omit preparation fields and retain `verified_at` as their legacy capture timestamp.

## Outputs

The transition produces a terminal superseded VREC with unchanged capture provenance plus `superseded_at`, `supersession_authorized_by`, one `superseded_by` relation, and a matching lifecycle event. Validation reports success without requiring or generating a verification decision.

## State model

1. Current preparation writes `prepared_at` and `prepared_by`; it writes neither `verified_at` nor `verified_by`.
2. `ready -> verified` adds `verified_at` and `verified_by` as the assurance decision.
3. `ready -> rejected` adds only the rejection decision fields.
4. `ready -> superseded` adds only the supersession decision fields and successor relation.
5. `rejected` and `superseded` are distinct terminal, non-authoritative outcomes.
6. A historical record without preparation fields may retain the older capture convention in which `verified_at` did not itself prove a verification decision.

## Behavioral rules

1. Presence of either `prepared_at` or `prepared_by` selects the current provenance generation and requires both fields to be valid.
2. A current prepared `ready` record must omit `verified_at` and `verified_by`.
3. A current prepared `verified` or `released` VREC must contain `verified_at` and `verified_by`, and the fields must match the applicable lifecycle decision when an event exists.
4. A current prepared `superseded` VREC must retain preparation fields, must contain the supersession fields and relation, and must omit `verified_at` and `verified_by`.
5. A superseded legacy VREC without preparation fields may retain a valid historical `verified_at` capture timestamp. The validator must not require a fabricated `verified_by`, write preparation fields, or reinterpret its history.
6. The transition mutator must not translate `prepared_at` into `verified_at` and must not create a verification event while applying supersession.
7. Existing successor type, status, work-coverage, cycle, active-release-reference, and event-consistency checks remain unchanged.
8. Rejection fields and behavior remain unchanged; automation must not replace the requested supersession with rejection.
9. Validation failure must occur before mutation, and failed apply must retain atomic rollback behavior.
10. The package template, transition planner, direct validator, installed-repository behavior, and documentation must express the same state-aware contract.

## Error and recovery behavior

Current prepared superseded records containing verification decision fields fail with a provenance diagnostic. Missing preparation or supersession fields fail under their existing validation plane. Ineligible successors and malformed events retain their existing diagnostics. Recovery is to restore the exact ready record, correct the selected successor or record shape, and rerun the supported transition; no historical field is synthesized.

## Data and interface contracts

No CLI option or lifecycle-registry change is introduced. The existing command remains:

```text
harnessctl transition . --set VREC-X=superseded --decision VREC-X=assurance-owner --reason VREC-X=VREC-Y [--apply]
```

`prepared_at`, `verified_at`, and `superseded_at` continue to use UTC `YYYY-MM-DDTHH:MM:SSZ`. Their meaning is selected by provenance generation and lifecycle state, not by a field-name alias.

## Security and privacy properties

All metadata and successor IDs remain untrusted. The correction must not weaken typed relation, coverage, cycle, evidence, actor, or active-release checks. It must not execute record prose or use Git ancestry to infer authority.

## Performance and capacity

The rule adds only constant-time field checks per VREC. Existing catalog lookup and coverage complexity is unchanged.

## Observability

Transition results continue to list exactly the written fields. Validation distinguishes a missing required decision from a fabricated decision. Inspection removes a successfully superseded record from the active assurance queue while retaining historical visibility.

## Compatibility and migration

No repository-owned historical VREC is rewritten. Current-format records are recognized by preparation fields. Legacy records without those fields preserve the historical `verified_at` capture convention. The repository root validator remains the exact released 0.6.0 copy during candidate development; the corrected template is adopted only through a later governed release and upgrade.

## Examples and counterexamples

Valid current result: `prepared_at`, `prepared_by`, `superseded_at`, `supersession_authorized_by`, and `superseded_by`, with no verification decision fields.

Valid legacy history: no preparation fields, historical `verified_at`, and complete supersession metadata.

Invalid: copying `prepared_at` into `verified_at`; adding `verified_by` during supersession; deleting legacy `verified_at`; accepting a ready successor; or changing captured candidate/evidence facts.

## Explicitly unspecified decisions

Internal helper names, diagnostic wording below the stable error code, test-fixture organization, and local factoring of validator predicates are delegated to implementation.
