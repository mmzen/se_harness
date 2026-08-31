+++
id = "REQ-ECP-028"
type = "requirement"
title = "The Git-derived handoff check declares its result in one run"
status = "approved"
owners = ["product-owner", "requirements-steward"]
created = "2026-08-31"
updated = "2026-08-31"
statement = "WHEN a Git-derived handoff check evaluates a work order with a bound evidence packet, THE SYSTEM SHALL rebind the packet to the current formal snapshot and evaluate the change set at its fixed point in one run, so that the first run is the declared result and a repeat yields the same result_sha256."
verification_method = ["test"]
priority = "must"
source = "Issue #280 (functional assessment of 2026-08-30, sections 2.1 and 3.3), part b"

[relations]
derives_from = ["CAP-ECP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-31T07:44:38Z"
decided_by = "requirements-steward"
reason = "Approved by the requirements steward on 2026-08-31 by selecting the presented option 'Approve and start WO-ECP-023': the Git-derived handoff check rebinds the packet to the current formal snapshot and evaluates the change set at its fixed point in one run; issue #280 part b."
+++

# Requirement: The Git-derived handoff check declares its result in one run

## Rationale

Today the handoff digest is only stable after two runs of `check
--checkpoint handoff --from-git BASE`: the first run retains its result as
`handoff.json`, which then joins the Git-derived change set, so the second
run computes a different `result_sha256` and only that one can be declared.
Separately, after any merge from the base branch the evidence packet must be
re-bound by hand with `harnessctl evidence`, or `QGP-G4I-EVIDENCE` reads
`not_assessable`. The assessment of 2026-08-30 lists both among the hidden
prerequisites, and issue #280 measures the cost: two of the fifteen commits
of one small change exist only because of these tool mechanics.

Both facts are knowable inside the check itself: the current formal snapshot
is computed by the run, and the retained result path is derived from the
work order's identity. Binding the packet and closing the change set over
the run's own write makes one run the declared result, with nothing for the
operator to re-run or re-bind.

## Behavior

- Trigger: `check --checkpoint handoff --from-git BASE` selects an
  `in_progress` work order whose handoff evidence packet exists with a
  machine header naming that work order and checkpoint.
- Response: the run binds the packet header to the current formal snapshot
  before evaluating any predicate, preserving the owner-authored body byte
  for byte, and evaluates the change set with the retained result path
  included; a completed run retains its result, and running the same check
  again over the unchanged tree yields the same `result_sha256`.
- On failure: a missing packet is not created and the evidence predicate
  keeps naming `harnessctl evidence` as the corrective command; a packet
  whose header names another artifact or checkpoint, or whose line endings
  a `.gitattributes` rule would convert, is refused with the same codes the
  `evidence` command uses, and nothing is written.

## Assumptions and dependencies

- The retained-result rules are unchanged: only a completed Git-derived
  handoff check retains `handoff.json`, and the `scope` checkpoint writes
  nothing (`ECP-PRB-002`, `ECP-SCP-004`).
- The declared change-set forms (`--changed-path`, `--changes-complete`,
  `--change-manifest`) stay read-only; self-binding is a property of the
  Git-derived handoff check only.
- The root evaluator governing this repository keeps the released two-run
  behaviour until the next root adoption.

## Acceptance examples

Executable scenarios live in the covering verification contract,
`VER-ECP-019`.

### Example: normal behavior

**Given** an `in_progress` work order with a bound evidence packet, an
in-scope working-tree change, and a merge from the base branch that moved
the formal snapshot.

**When** `check --checkpoint handoff --from-git BASE` is run once.

**Then** the run completes: the packet header carries the current formal
snapshot with its body unchanged, `handoff.json` is retained, and a second
identical run reports the same `result_sha256`.

### Example: failure behavior

**Given** the same work order with no evidence packet written.

**When** the same check is run.

**Then** the run is blocked with `QGP-G4I-EVIDENCE` reporting
`not_assessable`, no packet is created, and the corrective command is
`harnessctl evidence`.

## Open decisions

None.
