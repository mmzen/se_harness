+++
id = "SPEC-CIP-004"
type = "specification"
title = "Issue #433 pipeline repair: the renamed rehearsal job in two approved definitions"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-10"
updated = "2026-09-10"
contract = "The two approved pipeline definitions name the rehearsal job by its current name and carry an amendment record explaining the rename and the reconcile job's removal."

[relations]
specifies = ["REQ-CIP-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T10:19:05Z"
decided_by = "technical-owner"
reason = "Approved on 2026-09-10 by the accountable owner by selecting the presented option 'Approve both packets (Recommended)', given after the two issue #433 packets (the wave 5 leftovers: TRC-008 still describing the retired constrains relation, the completion boilerplate contradicting the delegation class, and the two ci-pipeline definitions naming the old job) were presented with the released 0.17.0 evaluator reading 0 errors and 0 advisories. Approval of a definition authorizes no work. Rules CIP-AMD-001 to CIP-AMD-005."
+++

# Specification: Issue #433 pipeline repair: the renamed rehearsal job in two approved definitions

## In plain words

One architecture and one requirement describe a job under a name the
workflow no longer uses. Each is corrected in prose and carries a record
saying when and under which work order the name changed.

## Scope

`ARCH-CIP-001` and `REQ-CIP-002`, both `approved` with lifecycle events, and
the test that pins the result. The workflows themselves were repaired by
`SPEC-CIP-003`; the managed templates are `SPEC-DST-028`'s.

## Terms

- **Amendment record.** A dated section at the end of an approved artifact
  that states what changed in its prose and under which work order. Every
  identifier, statement and relation stays in place, as in `SPEC-CIP-001`
  and `SPEC-ECP-006`.

## Rules

**CIP-AMD-001.** `ARCH-CIP-001` MUST name the rehearsal consumer
`upgrade-rehearsal` in its Components section and carry an amendment record
giving the former name, the renaming work order and the date.

**CIP-AMD-002.** `REQ-CIP-002` MUST describe the rehearsal job as
`upgrade-rehearsal` and the reconcile job as removed under `WO-CIP-001`, in
prose, with an amendment record that dates both.

**CIP-AMD-003.** Neither amendment MAY move an identifier, the `statement`, a
relation, a lifecycle event or the `decision_assessment`; `updated` takes the
amendment date.

**CIP-AMD-004.** After the amendments, `governance-migration` MUST occur under
`docs/engineering/ci-pipeline/architecture/` and `requirements/` only inside
an amendment record, and a test MUST pin it.

**CIP-AMD-005.** The domain index MUST say the two definitions are repaired,
and this work MUST NOT change a workflow, a script or a managed path.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| the old name occurs outside an amendment record in either directory | the definitions test fails naming the file and line | test failure |
| an amendment moves the statement, a relation or a lifecycle event | the released evaluator's graph or lifecycle check reports the file | `validate` error |
| a workflow, script or managed path is in the change set | the scope check reports the path | `WEX201` |

## Examples

**Given** the repaired `ARCH-CIP-001`, **when** its Components section is
read, **then** the rehearsal consumer is `upgrade-rehearsal` and the amendment
record below names `governance-migration` as the former name (CIP-AMD-001).

**Given** the repaired `REQ-CIP-002`, **when** `governance-migration` is
searched, **then** the only hits are inside its amendment record
(CIP-AMD-002, CIP-AMD-004).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-CIP-010` | CIP-AMD-001, CIP-AMD-002, CIP-AMD-003, CIP-AMD-004, CIP-AMD-005 |

## Not decided here

- The wording of the two amendment records and of the corrected prose.
- Whether the rationale of `REQ-CIP-002` keeps describing the state the
  requirement was written against, provided the old name occurs only in the
  amendment record.
- Where in `tests/test_ci_pipeline.py` the definitions test lives.
