+++
id = "SPEC-IAR-010"
type = "specification"
title = "Typed temporal reassessment predicate"
status = "implemented"
owners = ["technical-owner", "quality-owner", "repository-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
specifies = ["REQ-IAR-018"]
+++

# Specification: Typed temporal reassessment predicate

## Lifecycle

Approved on 2026-08-16 through the repository owner's instruction to create a branch and implement the reviewed Phase 1 correction.

## Scope

Refine the existing Harness Explorer `W-HEX-003` producer. The rule remains a derived, warning-only inspection observation and the existing `reassess-dependent-artifact` suggestion remains non-authoritative. This change narrows when the observation exists; it adds no validator rule, lifecycle state, score, automatic fix, or provenance claim.

## Behavioral rules

1. Evaluate only relations whose `authority` is `declared` and whose target exists.
2. Evaluate only a relation named in this source-type catalog:

   | Source type | Supported relation names |
   | --- | --- |
   | `capability` | `derives_from` |
   | `requirement` | `derives_from` |
   | `specification` | `specifies` |
   | `architecture` | `addresses`, `conforms_to`, legacy `constrains` |
   | `adr` | `decides` |
   | `verification` | `verifies` |
   | `release_contract` | `gates` |
   | `operating_contract` | `assures` |
   | `work_order` | `implements`, `specifications`, `architecture`, `verification` |

3. Never evaluate `verification_record` or `release_record` as a source. Their immutable candidate identity and eligibility are governed by dedicated provenance rules.
4. Skip any source in `rejected` or `superseded` state.
5. Evaluate a `work_order` only in `draft`, `approved`, or `in_progress`. Its `implemented`, `verified`, and `released` states record completed historical scope and must not be reopened by a date comparison.
6. Emit one finding per distinct `(source, relation, target)` only when both ISO dates are present and `source.updated < target.updated`.
7. Retain rule ID `W-HEX-003`, severity `warning`, authority `derived`, and the source and target artifact references. The message and evidence identify the declared relation name and the date comparison.
8. Bump the findings-rules version from `harness-findings-v6` to `harness-findings-v7` because repository findings change deterministically.

## Output contract

The finding message is:

`<SOURCE> predates newer declared <RELATION> target <TARGET> and may require reassessment.`

Evidence contains `relation=<RELATION>` and `source.updated < target.updated`. Existing deterministic finding ordering and JSON fields remain unchanged. The inspection suggestion catalog continues to select this rule by `W-HEX-003`; it does not independently reinterpret the predicate.

## Error and recovery behavior

Missing dates, unknown source types, unknown relations, derived relations, and missing targets produce no temporal finding. They do not fail generation or infer a fallback meaning. Formal structural errors remain the validator's responsibility.

## Compatibility and migration

- Existing output consumers continue to receive the same schema and rule ID.
- Counts may decrease because false-positive historical and derived observations disappear.
- Root and canonical generator copies, package data, lock metadata, and standard installation must remain synchronized.
- No stored artifact migration is required.

## Examples and counterexamples

- An implemented architecture dated before its declared conforming specification is eligible.
- An implemented work order dated before its verification contract is not eligible.
- A ready VREC dated before a verification contract is not eligible.
- An architecture connected only by `conforms_transitively_to_requirement` is not eligible.
- A superseded artifact connected by `superseded_by` is not eligible.

## Explicitly unspecified decisions

Implementation may choose immutable table types, helper names, and internal ordering. It may not broaden the table, infer semantics from prose, change another finding, add a fallback relation, or create a dedicated provenance rule in this work order.
