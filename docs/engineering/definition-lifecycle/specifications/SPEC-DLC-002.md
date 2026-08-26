+++
id = "SPEC-DLC-002"
type = "specification"
title = "Definition lifecycle termination and derived realization"
status = "approved"
owners = ["technical-owner", "repository-owner", "quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
specifies = ["REQ-DLC-002", "REQ-DLC-003", "REQ-DLC-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T09:33:19Z"
decided_by = "technical-owner"
+++

# Specification: Definition lifecycle termination and derived realization

## Scope

This specification defines two coupled changes:

1. the reachable definition lifecycle terminates at `approved`, with `rejected`
   as its only outgoing edge; and
2. the question the retired state used to answer — has this definition actually
   been built — is answered by a derivation over work orders and verification
   records, reported and never stored.

The two are specified together because the second exists only to replace what
the first removes, and neither is complete without the other.

Out of scope: any edit to an existing artifact, any change to the definition
schema, any change to `ALLOWED_STATUSES`, any change to `DR-DEFINITION-DECIDE`,
and the whole architecture-generation question, which is `SPEC-DLC-001`.

## Actors and external systems

- The engineering owner planning or applying a definition transition through
  `harnessctl transition`.
- The workflow resolver `se_harness/workflow.py`, whose `_recommend` raises
  `RuntimeError` for an unmatched `(artifact_type, status)` pair.
- The two byte-identical contract copies: `se_harness/workflow_contract.json`
  and the standard repository template's `docs/engineering/WORKFLOW.json`.
- `harnessctl inspect`, the only reader of the derived signal in this increment.
  The dashboard and explorer surfaces are deferred to separately approved work.
- A predecessor evaluator in a consumer repository that still admits the retired
  edge.

## Inputs

For the lifecycle change: the contract's `lifecycles.definition` table only.

For the derivation: each definition's `id` and `type`; each work order's `id`,
`status`, and `implements`, `specifications`, and `architecture` relations; and
each verification record's `id`, `status`, and bound commit. Nothing else. The
derivation reads no lock, no installed evaluator identity, no environment value,
no command-line flag, and no Git state beyond the commits the records already
bind.

The derivation does not read the definition's own status. In particular the 165
existing `implemented` definitions are not inputs to it.

## Outputs

- A transition plan for `approved -> implemented` on any definition family
  fails as an illegal transition, through the ordinary legality path and with
  the ordinary diagnostic.
- A transition plan for `approved -> rejected` succeeds as today.
- Every definition carrying `implemented` continues to validate, display, focus,
  and resolve a recommendation.
- For each requirement, specification, and architecture, one derived coverage
  classification: `covered`, `partially_covered`, or `uncovered`. A `covered`
  classification names the covering verification records and the exact commit
  each binds. `covered` emits `I-DLC-001`; `partially_covered` emits
  `W-DLC-001`; `uncovered` emits nothing.

## State model

The reachable definition lifecycle after this change:

| From | To |
| --- | --- |
| `draft` | `approved`, `rejected` |
| `approved` | `rejected` |
| `rejected` | terminal |

`implemented` remains a defined, valid, authority-granting, visible state with no
inbound reachable edge — the same standing `ready`, `in_progress`, `verified`,
`released`, and `superseded` already hold in the definition family.

The derivation has no state. It is recomputed on every read and persists nothing.

## Behavioral rules

**DLC-LCY-001:** In both contract copies, `lifecycles.definition.approved
.transitions_to` is `["rejected"]`. The two files stay byte-identical.

**DLC-LCY-002:** The `implemented` row is retained with `grants_authority:
true`, `must_remain_visible: true`, `transitionable: false`, and
`transitions_to: []`. It is not deleted, not renamed, and not removed from
`ALLOWED_STATUSES`.

**DLC-LCY-003:** The `implemented` row's `predecessor_adapter` carries whatever
the migration contract requires for a state a predecessor evaluator could still
admit a transition into. It is not left at `none` by default; the value is
chosen deliberately and recorded.

**DLC-LCY-004:** `WORKFLOW.md`'s state table row for the definition family reads
`| Definition | approved | rejected |`, and the surrounding text states that
`implemented` remains accepted, visible, and authority-granting on existing
definitions.

**DLC-LCY-005:** `PROC-DEFINITION-COMPLETE` and `STEP-DEFINITION-COMPLETE` are
retired. They are the only carriers of an `implemented` outcome for a
definition, and that outcome is authorized by no decision right.

**DLC-LCY-006:** `WFL-DEFINITION-COMPLETE` keeps its identifier and its
`statuses = ["approved"]` match, and is re-pointed at the work-selection
procedure with `DR-WO-SELECT` and `QG-G3-WORK-AUTHORIZATION`. Its handoff text
covers the case where no work order names the definition yet.

**DLC-LCY-007:** `WFL-DEFINITION-WORK`, matching `implemented`, is unchanged, so
the 165 existing implemented definitions keep a resolvable recommendation.

**DLC-LCY-008:** Every `(definition family, status)` pair that occurs anywhere in
the repository resolves to exactly one recommendation rule. A conformance test
enumerates all nine families against every status in `ALLOWED_STATUSES` and
asserts that no pair occurring in the graph reaches `_recommend`'s
`RuntimeError`.

**DLC-LCY-009:** `DR-DEFINITION-DECIDE` is unchanged. No new decision right,
role, or quality gate is introduced.

**DLC-REA-001:** For each requirement, specification, and architecture, the
covering work-order set is every work order naming it through `implements`,
`specifications`, or `architecture`.

**DLC-REA-002:** The classification is `covered` when the covering set is
non-empty and every member is `verified` or `released`; `partially_covered` when
at least one member is `approved`, `in_progress`, or `implemented`; and
`uncovered` when the covering set is empty or every member is `rejected` or
`superseded`.

**DLC-REA-003:** A verification record that is `rejected` or `superseded`
contributes no coverage.

**DLC-REA-004:** A `covered` classification names each covering verification
record and the exact commit it binds. It cites the record rather than restating
its verdict, and it never presents coverage as verification.

**DLC-REA-005:** The derivation writes nothing. It stores no field, proposes no
transition, and creates no artifact. An independent write sentinel in the test
suite asserts that a derivation run leaves every file byte-identical.

**DLC-REA-006:** The derivation is idempotent and order-independent. Two runs
over the same graph produce identical findings in identical order.

**DLC-REA-007:** Adding a work order that names an already-`covered` definition
moves it to `partially_covered` on the next run, with no transition, no edit, and
no diagnostic about the earlier classification.

**DLC-REA-008:** The rendered output states that the derived result is a report:
it grants no authority, approves nothing, and transitions nothing. It does not
describe a definition as implemented.

**DLC-REA-009:** `I-DLC-001` and `W-DLC-001` join the existing shared finding
family and follow its existing rendering, ordering, and suggestion rules. No new
output plane is introduced.

**DLC-REA-011:** The derivation renders in `harnessctl inspect` only. The
dashboard and explorer surfaces are out of scope for this increment. The
derivation is surface-independent: it returns findings and holds no rendering
logic, so the deferred work adds a renderer and changes no classification.

**DLC-REA-010:** `HRN-006` holds. The derivation never synchronizes a
definition's state to its work orders' states, in either direction.

## Error and recovery behavior

An `approved -> implemented` plan fails with the existing illegal-transition
diagnostic; no special-case message is added. Recovery for an actor who wanted to
record that work is done is to complete the work order and its verification
record, which is what the derivation reads.

A definition whose covering work orders are incomplete is reported, not failed.
`uncovered` is never an error: it is the correct and permanent classification for
every intent, capability, and verification contract, and for any definition no
work order has reached yet.

If a definition carries a status for which no recommendation rule matches, the
resolver raises today and continues to raise. That is a contract defect and is
caught by the conformance enumeration before release, not at runtime.

## Data and interface contracts

The contract copies remain valid `se-harness-workflow-v3` documents. The
retirement is a within-`v3` change, decided 2026-08-26 by the repository owner:
the contract's shape does not change, so no generation bump is taken. Both copies
stay byte-identical and a governance-migration scenario covers the version pair.
Finding codes are `I-DLC-001` and `W-DLC-001`,
matching the existing `I-`/`W-` shared-family shape. No artifact field, relation
type, artifact type, role, or gate is added.

## Security and privacy properties

Both changes are pure functions of governed artifact content. No network
operation, subprocess, filesystem write, or Git mutation. Findings contain
artifact identifiers, work-order identifiers, verification-record identifiers,
and commit identifiers only.

## Performance and capacity

The derivation is linear in the number of definitions plus the total number of
work-order relations, and it runs once per `inspect` invocation.
Over the current graph — 630 definitions and 244 requirement-naming work-order
relations — it is not measurably distinguishable from the existing finding
computations it joins.

## Observability

Each run reports the number of definitions in each classification and, for the
`covered` ones, the naming records and commits. The run does not report a
migration, a state change, or a count of definitions that "became" anything.

## Compatibility and migration

- No artifact bytes change. The 165 `implemented` definitions are not migrated,
  normalized, superseded, or re-decided in either direction.
- Diagnostic counts are unchanged by this increment: 890 artifacts, 0 errors, 50
  warnings, with identical `W013`, `W014`, and `W015` identifier sets. `I-DLC-001`
  and `W-DLC-001` are `inspect` findings, not validation diagnostics, and move no
  validation count.
- The finding family appears in `inspect` and not in the dashboard until the
  deferred surface work lands. That divergence from `W-HEX-*`, `W-REB-*`, and
  `W-REV-*` is a decided deferral, not an omission, and is disclosed rather than
  resolved.
- A consumer repository that has taken the `approved -> implemented` edge keeps
  every such definition valid and authority-granting. It simply cannot take the
  edge again.
- A predecessor evaluator that still admits the edge is handled by the migration
  contract's adapter path, never by re-admitting the edge.
- `WFL-DEFINITION-COMPLETE` keeps a name that no longer matches its behavior.
  The residue is accepted because consumers pin the identifier, and it is
  disclosed in the implementation notes.

## Examples and counterexamples

Planning `REQ-TCM-001=implemented` returns `PLANNED` today and must be refused
after this change, while `REQ-TCM-001=rejected` continues to plan.
`REQ-DST-006`, named by 16 work orders, is `partially_covered` until all 16 are
verified or released, and returns to `partially_covered` if a seventeenth is
approved.

It is invalid to migrate an existing `implemented` definition, to delete the
`implemented` row from the contract, to store a coverage result in an artifact
field, to report `uncovered` as an error, or to let a rejected verification
record contribute coverage.

## Explicitly unspecified decisions

The implementation may choose the derivation's module placement, function and
dataclass names, the finding message wording, the rendering order within the
existing family, and the conformance test's organization. It may not change the
reachable transition table, retain the `approved -> implemented` edge under any
flag, delete the `implemented` row, store the derived result, read a definition's
own status in the derivation, or introduce a new decision right or gate.
