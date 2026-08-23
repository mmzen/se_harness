+++
id = "SPEC-REB-009"
type = "specification"
title = "Canonical lifecycle state registry and rejected-history semantics"
status = "approved"
owners = ["technical-owner", "quality-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
specifies = ["REQ-REB-018", "REQ-REB-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "technical-owner"
+++

# Specification: Canonical lifecycle state registry and rejected-history semantics

## Scope

This specification replaces the standalone transition map in workflow contract v2 with one strict lifecycle-state registry in `se-harness-workflow-v3`. The registry is the sole normative data source for admitted states, transition edges, authority effect, release-version reservation, terminal behavior, historical visibility, and immediate-predecessor adapter need.

The packaged contract and installed managed contract remain byte-identical copies of one distribution artifact. Package code reads the packaged copy. The standalone managed validator reads the installed copy beside it. Neither consumer imports the other across the released-evaluator boundary.

## Contract shape

The workflow contract replaces top-level `transitions` with top-level `lifecycles`. `lifecycles` contains exactly four families: `definition`, `work_order`, `verification_record`, and `release_record`. Every family contains one object per admitted state. Every state object contains exactly:

- `transitions_to`: a unique ordered array of states in the same family;
- `grants_authority`: Boolean;
- `reserves_version`: Boolean;
- `transitionable`: Boolean;
- `must_remain_visible`: Boolean;
- `predecessor_adapter`: either `none` or `required`.

`transitionable` is true exactly when `transitions_to` is non-empty. All states must remain visible. `reserves_version` may be true only for release-record states. A transition target must exist in the same family. Unknown families, states, fields, values, duplicates, and inconsistent flags invalidate the contract.

## Required state semantics

| Family | State | Transitions to | Authority | Reserves version | Transitionable | Predecessor adapter |
| --- | --- | --- | --- | --- | --- | --- |
| definition | `draft` | `approved`, `rejected` | no | no | yes | none |
| definition | `ready` | none | no | no | no | none |
| definition | `approved` | `implemented`, `rejected` | yes | no | yes | none |
| definition | `in_progress` | none | yes | no | no | none |
| definition | `implemented` | none | yes | no | no | none |
| definition | `verified` | none | yes | no | no | none |
| definition | `released` | none | yes | no | no | none |
| definition | `superseded` | none | no | no | no | none |
| definition | `rejected` | none | no | no | no | none |
| work order | `draft` | `approved`, `rejected` | no | no | yes | none |
| work order | `ready` | none | no | no | no | none |
| work order | `approved` | `in_progress`, `rejected` | yes | no | yes | none |
| work order | `in_progress` | `implemented`, `rejected` | yes | no | yes | none |
| work order | `implemented` | `verified`, `released` | yes | no | yes | none |
| work order | `verified` | `released` | yes | no | yes | none |
| work order | `released` | none | yes | no | no | none |
| work order | `superseded` | none | no | no | no | none |
| work order | `rejected` | none | no | no | no | none |
| verification record | `ready` | `verified`, `rejected`, `superseded` | no | no | yes | none |
| verification record | `verified` | none | yes | no | no | none |
| verification record | `released` | none | yes | no | no | none |
| verification record | `superseded` | none | no | no | no | none |
| verification record | `rejected` | none | no | no | no | required |
| release record | `ready` | `released`, `rejected` | no | yes | yes | none |
| release record | `released` | none | yes | yes | no | none |
| release record | `rejected` | none | no | no | no | required |

The `released` verification-record state is retained as valid terminal legacy assurance history even though the current transition engine does not create it.

The additional terminal definition/work-order rows are compatibility vocabulary,
not new workflow edges. They preserve existing repository history and validator
fixtures while ensuring the registry, rather than a global fallback set, owns
their authority and visibility semantics.

## Consumers and dependency rules

1. `se_harness.workflow_contract` strictly validates workflow v3 and exposes immutable state/transition indexes and semantic queries.
2. `se_harness.workflow` consumes those indexes for every lifecycle edge and for authority-sensitive VREC/RLS eligibility. It has no independent transition table.
3. `se_harness.provenance` uses `reserves_version` for release-preparation uniqueness and uses registry authority semantics where it selects formal authority. It retains separate completion predicates when a rule concerns implementation completion rather than authority.
4. The standalone candidate validator loads adjacent managed `WORKFLOW.json`, validates the lifecycle registry before parsing artifacts, derives the global state vocabulary and per-family vocabularies, and uses `reserves_version` for E010 same-version checks.
5. Managed dashboard and inspection code may reuse validator-exported derived indexes; they must not redefine rejected records as active authority.
6. The migration rehearsal may observe `predecessor_adapter`, but production adapter construction and lifetime remain outside this packet.
7. The root `scripts/` copies, root lock/configuration, and exact released 0.5 evaluator remain unchanged.

## Rejected-record rules

- A rejected VREC or RLS must have non-empty rejection actor/reason, a canonical UTC rejection timestamp, and a latest lifecycle event whose source, target, actor, timestamp, and reason agree with the top-level fields.
- No outgoing transition is legal from rejected.
- Rejected records remain discoverable, renderable, and relation-valid history.
- Rejected records cannot satisfy assurance, release, active-coverage, or external-action gates.
- Rejected RLS records do not participate in active-version uniqueness or block preparation of a distinct same-version successor.
- Ready and released RLS records do participate in active-version uniqueness.
- No consumer may delete, omit, rewrite, reopen, or silently supersede rejected history to obtain success.

## Failure behavior

Contract failure is fail-closed and precedes governed mutation. Human and JSON diagnostics identify the contract path and first deterministic schema or consistency error without echoing untrusted body content. No fallback constants, previous schema interpretation, best-effort partial index, or candidate-to-predecessor import is allowed.

Workflow v1/v2 may remain readable only in explicitly versioned historical fixtures or predecessor processes. Successor v3 production consumers must not accept v2 as if it carried v3 semantics.

## Compatibility boundary

The state registry records that rejected VREC/RLS states require an explicit immediate-predecessor adapter because 0.5 cannot parse them. This fact does not identify omitted paths, construct a compatibility view, authorize its use, or claim full predecessor validation. Those responsibilities remain with the migration contract and issue #104's shared production service.
