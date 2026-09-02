+++
id = "VER-ECP-016"
type = "verification"
title = "Independent evidence for the context fold and the alias retirement"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-025"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T18:39:39Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-29 with the words 'Approve and start WO-ECP-019': context, default-artifact, alias byte-identity, corrective, retired-alias, writes-nothing and word-census rows; the root WORKFLOW.md stays the 0.11.0 copy until the next root adoption and the alias keeps its instruction valid."
+++

# Verification Contract: Independent evidence for the context fold and the alias retirement

## Independence

Expected behaviour derives from `REQ-ECP-025` and the `ECP-CTX-` rules of
`SPEC-ECP-014`. The CLI tests drive `main()` over the workflow fixture
repository; the context assertions compare against `run_preflight`'s
manifest and the checkpoint `check`'s step, never against `next`'s own
output; the word-census tests read the template and the notes.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-025` context on the projection | test: `check --artifact ID --json` for a WO, a VREC and an RLS | `tests/test_workflow_execution.py` | `context` present with the six members; `context.next` equals the step the transition-checkpoint `check` selects; `reading_manifest` equals preflight's for the implied phase; `operation.kind == "check"` |
| `REQ-ECP-025` default artifact | test: `check .` with one, zero and two `in_progress` work orders | same | one: selected; zero and two: `blocked`, `WEX-ECP-001` with the count; with a checkpoint and no `--artifact`: refused |
| `REQ-ECP-025` no `next` | test: `--help`; invocation | same | help lists no `next`; invocation exits 2, empty stdout, stderr names `harnessctl check` (amended under `WO-ECP-020`; the row first asserted a byte-identical alias) |
| `REQ-ECP-025` corrective | test: blocked `check --checkpoint start` on an `implemented` WO | same | corrective argv is `harnessctl check . --artifact ID` |
| `REQ-ECP-025` no `accept-candidate` | test: `--help`; invocation | `tests/test_release_qualification.py` | help lists no `accept-candidate`; invocation exits 2, empty stdout, stderr names `qualify candidate-package`; the `qualify candidate-package` tests are unchanged |
| `REQ-ECP-025` writes nothing | test: tree digest before and after `check .` | `tests/test_workflow_execution.py` | equal |
| `SPEC-ECP-014` word census | test: the template `WORKFLOW.md` names no `harnessctl next`; the reference has no `accept-candidate` row, no `next` row and no `next` synopsis line | same | as stated |
| `SPEC-ECP-014` workflow unchanged | test: existing candidate-evidence workflow assertions | `tests/test_release_qualification.py`, `tests/test_standard_repository_lifecycle.py` | unchanged and passing |

## Acceptance scenarios

### Scenario 1: one call

With `WO-001` `in_progress`, run `main(["check", root, "--json"])`. Assert
outcome `completed`, `scope.selected == "WO-001"`, and `context.next.argv`
equals `restitution.command_or_response.argv`.

### Scenario 2: the retired projection alias

Run `main(["next", root, "--artifact", "WO-001", "--json"])`. Assert exit 2,
stdout empty, stderr contains `harnessctl check`.

### Scenario 3: the retired alias

Run `main(["accept-candidate", "--wheel", "x.whl"])`. Assert exit 2, empty
stdout, stderr contains `harnessctl qualify candidate-package`.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-019/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline. Graph and integrity readings come from the exact
released evaluator, se-harness 0.11.0, installed outside the checkout.

## Residual uncertainty

The root `WORKFLOW.md` is the released 0.11.0 copy and names `next` until
the next root adoption; the 0.11.0 evaluator that governs it still has the
command, and the adoption replaces both together.

## Amendment record

**The alias row is a refusal row, proposed 2026-08-29 under `WO-ECP-020`.**
`ECP-CTX-004` as amended makes `next` a refused command rather than an
alias, so the matrix row, scenario 2, the word census and the residual
uncertainty are restated; every other row and its pass condition is
unchanged and stays satisfied by `WO-ECP-019`'s evidence.

**The "no `next`" and "no `accept-candidate`" rows' invocation halves are superseded, proposed 2026-09-02 under `WO-ECP-025` (`VER-ECP-021`).** `--help` still lists neither name; the invocations now assert argparse's refusal, not a named replacement, in `test_retired_names_are_unknown_to_the_parser`. Every other row is unchanged.
