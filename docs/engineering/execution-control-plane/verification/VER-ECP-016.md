+++
id = "VER-ECP-016"
type = "verification"
title = "Independent evidence for the context fold and the alias retirement"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-025"]
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
| `REQ-ECP-025` alias | test: `next` and `check` for the same arguments | same | identical stdout bytes and `result_sha256`; `next` writes one stderr line naming `check`; `check` writes none |
| `REQ-ECP-025` corrective | test: blocked `check --checkpoint start` on an `implemented` WO | same | corrective argv is `harnessctl check . --artifact ID` |
| `REQ-ECP-025` no `accept-candidate` | test: `--help`; invocation | `tests/test_release_qualification.py` | help lists no `accept-candidate`; invocation exits 2, empty stdout, stderr names `qualify candidate-package`; the `qualify candidate-package` tests are unchanged |
| `REQ-ECP-025` writes nothing | test: tree digest before and after `check .` | `tests/test_workflow_execution.py` | equal |
| `SPEC-ECP-014` word census | test: the template `WORKFLOW.md` names no `harnessctl next`; the reference has no `accept-candidate` row and no `next` synopsis line | same | as stated |
| `SPEC-ECP-014` workflow unchanged | test: existing candidate-evidence workflow assertions | `tests/test_release_qualification.py`, `tests/test_standard_repository_lifecycle.py` | unchanged and passing |

## Acceptance scenarios

### Scenario 1: one call

With `WO-001` `in_progress`, run `main(["check", root, "--json"])`. Assert
outcome `completed`, `scope.selected == "WO-001"`, and `context.next.argv`
equals `restitution.command_or_response.argv`.

### Scenario 2: the alias

Run `main(["next", root, "--artifact", "WO-001", "--json"])` and the same
through `check`. Assert byte-equal stdout; assert stderr of `next` contains
`harnessctl check`.

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
the next root adoption; the alias keeps that instruction valid for the
window.
