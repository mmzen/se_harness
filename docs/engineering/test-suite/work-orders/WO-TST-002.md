+++
id = "WO-TST-002"
type = "work_order"
title = "The cached fixture install"
status = "implemented"
owners = ["engineering-owner"]
created = "2026-08-26"
updated = "2026-08-26"
[assurance]
commit_bound_verification = "required"
rationale = "The change touches the fixtures of about twenty-five test files; the suite's verdict on the exact commit must be shown unchanged."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "tests/",
  "docs/notes/ci-pipeline.md",
  "docs/engineering/test-suite/evidence/",
]

[relations]
implements = ["REQ-TST-003"]
specifications = ["SPEC-TST-001"]
architecture = ["ARCH-TST-001", "ADR-TST-001"]
verification = ["VER-TST-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-26T19:18:13Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-26T19:49:49Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: you can start WO-TST-002; WO-TST-001 is implemented."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-26T20:08:33Z"
decided_by = "engineering-owner"
reason = "Owner decision 2026-08-26: mark WO-TST-002 implemented, after accepting interactively the three recorded deviations (eleven fixtures converted rather than about twenty-five; a cache-naming collision fixed before commit; the serial saving is 5 s rather than about 100 s, the benefit being in the parallel runs)."
+++

# Work Order: The cached fixture install

## Lifecycle

Approval authorizes only the scope below. Follows `WO-TST-001`.

## Objective

`TST-FIX` 1–2: the session-cached standard repository and its use by every
fixture that only needs a fresh install; the byte-equality test; the
measured saving in `docs/notes/ci-pipeline.md`.

## In scope

The helper, the fixture edits, the equality test, the note.

## Out of scope

The installer; tests that assert on `init` itself; any assertion.

## Authorized decision envelope

Which existing support module hosts the helper.

## Constraints

Same verdict as before on the same commit; no change to what a test
asserts.

## Expected change surface

One helper, about twenty-five fixture edits, one test, one note, evidence.

## Required verification

`VER-TST-001` row 3; the full suite serial and parallel before and after;
handoff check.

## Evidence to record

Under `docs/engineering/test-suite/evidence/WO-TST-002/`: the list of
fixtures converted, the timings before and after.

## Stop and escalate conditions

Stop if any converted fixture changes a test's verdict.

## Completion report format

The `harnessctl check . --artifact WO-TST-002 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
