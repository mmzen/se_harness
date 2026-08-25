+++
id = "WO-ADS-002"
type = "work_order"
title = "Close the reading manifest, minimise the operating card, and retire the repository-context file"
status = "in_progress"
owners = ["engineering-owner"]
created = "2026-08-25"
updated = "2026-08-25"
[assurance]
commit_bound_verification = "required"
rationale = "The work changes preflight manifests, a managed template, the owner instruction region, and a governing requirement's lifecycle. Future engineering decisions depend on exact candidate behaviour and therefore require commit-bound assurance."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/preflight.py",
  "se_harness/workflow_contract.py",
  "templates/repository/standard/ENGINEERING_HARNESS.md.tpl",
  "templates/repository/standard/docs/engineering/OPERATING_CARD.md",
  "AGENTS.md",
  "docs/engineering/REPOSITORY_CONTEXT.md",
  "docs/engineering/README.md",
  "docs/notes/developing-se-harness.md",
  "docs/notes/harnessctl-reference.md",
  "docs/engineering/instruction-architecture/requirements/REQ-IAR-020.md",
  "tests/test_instruction_architecture.py",
  "tests/test_context_routing_retirement.py",
  "tests/test_repository_context_retirement.py",
  "tests/test_workflow_execution.py",
  "tests/fixtures/repository_context_retirement/",
  "docs/engineering/agent-directive-surface/evidence/",
]

[relations]
implements = ["REQ-ADS-007"]
specifications = ["SPEC-ADS-002"]
verification = ["VER-ADS-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-25T11:40:02Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-25T11:42:35Z"
decided_by = "engineering-owner"
+++

# Work Order: Close the reading manifest, minimise the operating card, and retire the repository-context file

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the assurance-owner decision, integration, and release are
separate decisions by the roles that own them. Approval of `REQ-ADS-007` is a
separate act by its owner and is required before this work order can be
approved.

## Objective

Finish what `WO-ADS-001` left open: make the bounded read real, remove the
duplication the operating card introduced, and retire the repository-context
file that the candidate harness withdrew under `WO-DST-021`.

## In scope

- `READING_PATHS` in `se_harness.preflight`; manifest derived from it.
- `render_operating_card` reduced to header, stop conditions, and traps;
  bound lowered to 1,024 bytes; template regenerated.
- Router template sentence per `ADS-RDS-003`.
- Owner region per `ADS-RDS-004`; note section per `ADS-RDS-005`; removal of
  `docs/engineering/REPOSITORY_CONTEXT.md` (staged with `git rm`) and its index line.
- `REQ-IAR-020` transitioned to `superseded` by the requirements steward,
  body unchanged, using the released evaluator.
- Test and inventory updates per `ADS-RDS-007`, including the retirement
  fixture baseline if it pins the manifest prefix.
- Reference note updated where it describes the manifest.
- Work-order-keyed evidence.

## Out of scope

- Approving or transitioning any other definition; editing root managed
  copies or the lock; changing the 6,000-byte owner-region bound; any change
  to `WORKFLOW.json`, gates, decision rights, traceability, or skills.

## Authorized decision envelope

The implementation agent may decide the header wording of the card, test
names, and the note section's internal layout. It may not change the closed
manifest set, the card bound, the note anchor, or the superseded status.

## Constraints

- Stage the file removal before any preflight or check runs; `hash_bound.assess`
  reads every index-tracked path.
- Use the exact external released evaluator for identity, integrity, graph,
  focus, preflight, and the `REQ-IAR-020` transition.
- LF line endings; assert bytes against blobs.

## Expected change surface

Preflight, card renderer, router template, card template, owner region, one
note, one index, one historical requirement's status, four test modules and
one fixture baseline, evidence.

## Required verification

Execute `VER-ADS-002` completely plus the repository-required checks; run the
complete suite on Windows and Linux with figures labelled per platform.

## Evidence to record

Under `docs/engineering/agent-directive-surface/evidence/WO-ADS-002/`: commands
and results, card bytes and size, manifest listings for both phases, owner
region byte count, per-platform test figures, complete changed-path set.

## Stop and escalate conditions

Stop if the owner region cannot carry every remaining `REQ-IAR-020` fact
under 6,000 bytes, if `REQ-IAR-020` cannot transition to `superseded` under
the released evaluator, or if any path outside scope must change.

## Completion report format

Return the `harnessctl check . --artifact WO-ADS-002 --checkpoint handoff`
schema-2 block verbatim with the complete changed-path set asserted, and its
`result_sha256`.
