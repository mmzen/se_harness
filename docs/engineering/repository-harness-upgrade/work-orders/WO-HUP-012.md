+++
id = "WO-HUP-012"
type = "work_order"
title = "Enforce the lock-schema floor"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-30"
updated = "2026-08-30"

[assurance]
commit_bound_verification = "required"
rationale = "The change alters how every operation reads the lock that carries the evaluator identity; later decisions rely on the exact candidate behaviour, so verification binds the exact candidate commit."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/integrity.py",
  "se_harness/installer.py",
  "se_harness/preflight.py",
  "se_harness/hash_bound.py",
  "se_harness/mutation_guard.py",
  "scripts/validate_governor_transition.py",
  "tests/test_harnessctl.py",
  "tests/test_mutation_guard.py",
  "tests/test_hash_bound_integrity.py",
  "tests/test_instruction_architecture.py",
  "docs/notes/harness-installation-and-upgrades.md",
  "docs/engineering/repository-harness-upgrade/README.md",
  "docs/engineering/repository-harness-upgrade/evidence/",
  "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-024.md",
  "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-012.md",
  "docs/engineering/repository-harness-upgrade/verification/VER-HUP-012.md",
  "docs/engineering/portable-managed-integrity/requirements/REQ-PMI-004.md",
  "docs/engineering/portable-managed-integrity/specifications/SPEC-PMI-001.md",
  "docs/engineering/portable-managed-integrity/architecture/adr/ADR-PMI-001.md",
]

[relations]
implements = ["REQ-HUP-024"]
specifications = ["SPEC-HUP-012", "SPEC-PMI-001"]
verification = ["VER-HUP-012"]
+++

# Work Order: Enforce the lock-schema floor

## Lifecycle

This work order requires the accountable owner's approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above.

Commit-bound verification is `required`.

## Objective

Make schema 3 the only lock schema the harness reads or writes
(`HUP-LSF-001`, `HUP-LSF-003`); delete the legacy digest machinery, labels
and advisory renderings (`HUP-LSF-002`, `HUP-LSF-004`); retire the mutation
guard's schema condition with its code reserved (`HUP-LSF-005`); delete the
legacy-newline recognition from the hash-bound component (`HUP-LSF-006`);
narrow the transition assessment script (`HUP-LSF-007`); re-pin the tests
(`HUP-LSF-008`); and record the superseded 0.2.x-era commitments on
`REQ-PMI-004`, `SPEC-PMI-001` and `ADR-PMI-001` with dated amendment
records. Issue #285 item #285a, on the owner's floor decision of
2026-08-30: "locks older than schema 3 are not read", taken as the hard
floor by the owner's selection of the same day.

## Why now

Schema-1 locks never shipped in a release consumers hold, schema 2 has not
been written by any supported path since 0.6.0, and the mutation guard
already blocks every ordinary operation on a pre-3 root — yet four modules
carry read paths, digest variants, four-way match labels, and one branch
that re-writes schema 1. Dead compatibility that can still write a dead
schema is the worst of both.

## In scope

- `integrity.py`: schema-3-only validation with the floor diagnostic;
  legacy constant, digests, variant recognition and labels deleted.
- `installer.py`: schema-3-only output; legacy branches and helper deleted;
  absent-lock handling unchanged in meaning.
- `preflight.py`: the failing floor check; advisory strings gone.
- `mutation_guard.py`: the schema condition deleted; `MG002` retired and
  reserved.
- `hash_bound.py`: `legacy-newline-variant` deleted.
- `scripts/validate_governor_transition.py`: schema 3 only.
- The four test modules; the installation note's schema paragraph; the
  three amendment records; this domain's index; the evidence packet.

## Out of scope

Schema-3 semantics, the lock writer's format, the evaluator identity block;
`se_harness/release_qualification.py` (its pre-3 refusal message follows
from the shared read path without an edit); the template validator (already
schema-3-only for the evaluator binding); every hash-locked root file; the
release carrying this change.

## Authorized decision envelope

Exact diagnostic wording beyond the elements `HUP-LSF-001` names; the
internal representation of the absent-lock state; whether a raw byte digest
helper survives for the hash-bound raw mode; test names.

## Constraints

- Every refusal is fail-closed and byte-identical.
- Retained evidence recording schema-1-era digests is never edited.
- No hash-locked root file moves.

## Expected change surface

Five product modules, one repository script, four test modules, one note,
three amendment records, the packet and the index.

## Required verification

Execute `VER-HUP-012` in full; repository-required checks; the pull
request's lanes; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-012/`.

## Stop and escalate conditions

Any need to change schema-3 semantics or the lock writer's format; any
hash-locked file in the change set; any test that can only pass by keeping
a pre-3 read path; the upgrade rehearsal failing for a cause other than an
intentionally refused pre-3 fixture.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
