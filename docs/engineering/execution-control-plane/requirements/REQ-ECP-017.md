+++
id = "REQ-ECP-017"
type = "requirement"
title = "Harness-owned multi-file writes are journaled"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-27"
updated = "2026-08-28"
statement = "THE SYSTEM SHALL perform every harness-owned multi-file write through one journaled apply with rollback and a human-recovery stop."
verification_method = ["test"]
priority = "must"
source = "se_harness/effect_broker.py:1029-1160; tests/test_effect_broker.py:308-344"

[relations]
derives_from = ["CAP-ECP-003"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-28T12:03:40Z"
decided_by = "requirements-steward"
reason = "Approved on 2026-08-28 by the accountable owner, 'I approve the ECP definitions and WO-ECP-005', as part of the execution-control-plane definition packet of #231 with the issue #212 amendments of #238 applied. Approval of a definition authorizes no work; each work order is approved separately."
+++

# Requirement: Harness-owned multi-file writes are journaled

## Rationale

Two crash-safe writers exist: `TransitionPlan`'s staged apply with stale-input
checks (se_harness/workflow.py:753-938) and the Phase 4 broker's journal with
`human-recovery-stop` and an eleven-stage fault matrix
(se_harness/effect_broker.py:1029-1160; tests/test_effect_broker.py:308-344;
docs/notes/agentic-execution-review-2026-08.md:195-197). Eight atomic writers
exist in total (docs/notes/complexity-audit-2026-08.md:290). Both notes list the
journaled apply as the piece of Phase 4 to keep whatever else is cut, because it
is what makes a multi-file write safe on Windows, where `os.replace` can fail
mid-bundle (docs/notes/complexity-audit-2026-08.md:345-349; docs/notes/agentic-
execution-review-2026-08.md:341-343). Keeping it as the one writer is the
guarantee; keeping two is the duplication.

## Behavior

- Trigger: always: any harness command that writes more than one file in one
  operation (`transition --apply`, `capture-verification`, `prepare-release`,
  `evidence`, `init`, `upgrade --apply`).
- Response: the write is planned, journaled before the first byte changes,
  applied through one shared apply routine, and either fully applied or fully
  rolled back; when rollback itself fails, the command stops with a human-
  recovery diagnostic naming the journal and every partially written path.
- On failure: a fault at any stage leaves either the pre-write state or a
  journal that `harnessctl recover` can replay; no command reports success after
  a partial write.

## Assumptions and dependencies

- The installer's transactional core is either the same routine or a
  documented exception with its own fault tests
  (docs/notes/complexity-audit-2026-08.md:320-324).
- The fault-injection matrix from `tests/test_effect_broker.py` moves with
  the routine and runs on Linux and Windows.
- `TransitionPlan`'s stale-input check becomes a precondition of the shared
  apply, not a second writer.

## Acceptance examples

Executable scenarios live in `acceptance/REQ-ECP-017.feature` and are named by
the verification contract that covers this requirement.

### Example: normal behavior

**Given** `transition --apply` must update a work order and append to a
verification record.

**When** a fault is injected after the first `os.replace`.

**Then** both files are byte-identical to their pre-write state, the journal
records the rollback, and the exit code is non-zero with the fault named.

### Example: failure behavior

**Given** the same operation, and the rollback's own `os.replace` is made to
fail.

**When** the command runs.

**Then** it stops with a human-recovery diagnostic naming the journal path and
the one partially written file, and a following `check` reports the repository
as needing recovery.

## Open decisions

None.
