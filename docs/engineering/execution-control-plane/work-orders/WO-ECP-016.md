+++
id = "WO-ECP-016"
type = "work_order"
title = "Admit the selected work order's own verification and release records to the change set"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters the admission rule the pull-request gate and the handoff check judge every change set by; it is trusted engineering state later decisions rely on, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/workflow_compliance.py",
  "tests/test_workflow_compliance.py",
  "docs/notes/harnessctl-check.md",
  "docs/engineering/execution-control-plane/README.md",
  "docs/engineering/execution-control-plane/evidence/",
  "docs/engineering/execution-control-plane/verification-records/",
  "docs/engineering/execution-control-plane/requirements/REQ-ECP-023.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-012.md",
  "docs/engineering/execution-control-plane/specifications/SPEC-ECP-001.md",
  "docs/engineering/execution-control-plane/verification/VER-ECP-012.md",
]

[relations]
implements = ["REQ-ECP-023"]
specifications = ["SPEC-ECP-012"]
verification = ["VER-ECP-012"]
+++

# Work Order: Admit the selected work order's own verification and release records to the change set

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Extend the admitted scope `build_context` assembles for a selected work
order with the records that name it and their evaluator-evidence files
(`ECP-ADM-001` to `ECP-ADM-004`), say so in the check reference
(`ECP-ADM-005`), and record the amendment on `SPEC-ECP-001`'s
`ECP-CHG-007`. Issue #264.

## Why now

Since the 0.10.0 root the managed gate is green through completion, and
red again at the record heads unless the packet author lists a records
directory — the very kind of state-dependent red `WO-ECP-013` removed,
measured on #263 the day the root moved.

## In scope

- `se_harness/workflow_compliance.py`: `build_context` computes the own
  records from the catalog and adds their paths and evidence paths to
  `admitted_scope`, as exact paths.
- `tests/test_workflow_compliance.py`: the four scenarios of `VER-ECP-012`.
- `docs/notes/harnessctl-check.md`: the admission sentence.
- The `## Amendment record` on `SPEC-ECP-001` (`ECP-CHG-007`); the domain
  index; the evidence packet. This work order's own scope lists the
  domain's `verification-records/` because the hosted lane runs the
  released 0.10.0 evaluator, which lacks the rule; the next work order
  after the root adopts the release carrying it need not.

## Out of scope

Any contract file; the bundle manifest's admission (release work orders
declare their domain); any hash-locked root file; the release carrying
this change.

## Authorized decision envelope

The helper's name and placement; the fixture records' content; the wording
of the note's sentence and the amendment record.

## Constraints

- Admission by relation only; no directory prefix is admitted.
- `scope.declared_paths` unchanged.
- No managed or hash-locked file moves.

## Expected change surface

One product module, one test module, one note, the amendment record, the
packet, the domain index and the evidence.

## Required verification

Execute `VER-ECP-012` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/execution-control-plane/evidence/WO-ECP-016/`.

## Stop and escalate conditions

A catalog that cannot expose a record's relations or evidence path; a need
to admit a directory rather than exact paths; any need to touch a
hash-locked file.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
