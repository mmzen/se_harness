+++
id = "WO-ECP-037"
type = "work_order"
title = "Record the DEC-ECP-002 revisit on SPEC-ECP-023 and close the wave 3 index"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-09-09"
updated = "2026-09-09"

[assurance]
commit_bound_verification = "not_required"
rationale = "Two dated records and one index line: the deviation DEC-ECP-002 accepted against ECP-PRM-027 is discharged by a reading wave 3 already retains in its verified records, and the index gains the completion line the wave 3 work orders left to the next work order; no rule, code, template or test changes."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-023.md",
  "docs/engineering/execution-control-plane/decisions/DEC-ECP-002.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/work-orders/WO-ECP-037.md",
  "docs/engineering/execution-control-plane/evidence/WO-ECP-037/",
]

[relations]
implements = ["REQ-ECP-034"]
specifications = ["SPEC-ECP-023"]
verification = ["VER-ECP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-09T11:48:35Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-09 by selecting the presented option 'Approve; start, record and complete on this branch (Recommended)' after reviewing PR #429: two dated records and one index line, commit-bound verification not required; the same decision covers the start and the completion on this branch, each recorded as its own event."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-09T11:49:03Z"
decided_by = "engineering-owner"
reason = "Started by the accountable engineering owner on 2026-09-09 under the decision 'Approve; start, record and complete on this branch (Recommended)' (PR #429). Start preflight PASS."
+++

# Work Order: Record the DEC-ECP-002 revisit on SPEC-ECP-023 and close the wave 3 index

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `not_required`:
the change is two dated records and one index line.

## Objective

`DEC-ECP-002` accepted, for wave 2, a deviation against `ECP-PRM-027` of
`SPEC-ECP-023`: the duplication scan still reported three cross-file blocks,
each with a side inside `se_harness/engine/`, which the wave 2 work orders
were forbidden to touch. Its revisit trigger was the merge of wave 3
(#378). Wave 3 merged on 2026-09-08: `WO-ECP-034` folded the three engine
copies into the package and its verified record (`VREC-ECP-038`) retains
the scan reading 0 blocks, which `WO-ECP-035` and `WO-ECP-036` read again.
Record on the specification that `ECP-PRM-027` is met as written and the
deviation discharged, record the revisit on the decision, and give the
domain index the completion line for `WO-ECP-036` that its own work order
left to the next one.

## In scope

- An `## Amendment record` paragraph on `SPEC-ECP-023`, dated, naming this
  work order, `DEC-ECP-002`, the reading (0 blocks at `WO-ECP-034`'s head
  and at every later wave 3 head) and the rule left as written.
- A `## Revisit record` section on `DEC-ECP-002`, dated, stating that the
  trigger fired with the wave 3 merge, what the reading found, and that the
  decision stays `decided` with no successor decision needed because the
  rule is met.
- The domain index: `WO-ECP-036` implemented and `VREC-ECP-040` verified on
  2026-09-08, wave 3 merged and #378 closed, `DEC-ECP-002`'s revisit
  recorded, this work order.

## Out of scope

Any rule text, identifier or coverage row of `SPEC-ECP-023`; the
`[disposition]` table and the lifecycle of `DEC-ECP-002`, which `decide`
wrote; any code, template, test or note; the `release_build.canonical_json_bytes`
alias for `scripts/replay_release_build.py`, a release-domain follow-up.

## Authorized decision envelope

The wording of the two records and the index line.

## Constraints

- The rules section of `SPEC-ECP-023` is unchanged byte for byte.
- The front matter of `DEC-ECP-002` is unchanged byte for byte.
- The reading the records cite is the one the wave 3 evidence packets and
  verified records retain, not a new measurement.

## Expected change surface

`SPEC-ECP-023.md` (one amendment paragraph), `DEC-ECP-002.md` (one body
section), the domain index, this work order and its evidence packet.

## Required verification

The released-evaluator `validate` and `preflight`; the handoff check over
the Git-derived change set; `git diff` showing the rules section and the
decision's front matter untouched.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-037/`: the
handoff packet the gate requires at the handoff checkpoint.

## Stop and escalate conditions

A need to change a rule or a disposition; a scan reading other than 0 at
`main`'s head, which would be a new deviation, not a record.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
