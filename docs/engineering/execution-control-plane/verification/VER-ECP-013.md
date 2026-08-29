+++
id = "VER-ECP-013"
type = "verification"
title = "Independent evidence for the removal of the focus alias"
status = "approved"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[relations]
verifies = ["REQ-ECP-024"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T12:27:21Z"
decided_by = "assurance-owner"
reason = "Approved by the assurance owner on 2026-08-29 with the words 'Approve and start WO-ECP-017': refusal, orientation, vector-history and word-census scenarios; the hosted orientation of this repository stays on the 0.10.0 root copy until the next root adoption."
+++

# Verification Contract: Independent evidence for the removal of the focus alias

## Independence

Expected behaviour derives from `REQ-ECP-024` and the `ECP-RMV-` rules of
`SPEC-ECP-013`. The CLI tests drive `main()`; the skill tests rebuild the
`harness-orient` manifest from the template files and compare digests to
fixtures whose retained rows are read back byte-exact from Git; the
orientation test runs the skill's script against the fake evaluator.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-024` no second name | test: `harnessctl --help`; `focus` invocation | `tests/test_workflow_execution.py` | help lists no `focus`; `focus` exits 2, empty stdout, stderr names `check --artifact` |
| `REQ-ECP-024` projection intact | test: every state projects through `check` with no gate and no write (existing `CheckProjectionTests`) | same | unchanged assertions under `check` |
| `SPEC-ECP-013` skill on check | test: orientation against the fake evaluator advertising `check`; `no-check` mode degrades with `AEXORI030` / `focus-json` | `tests/test_agentic_execution.py` | the orientation reads the projection through `check`; degraded case unchanged |
| `SPEC-ECP-013` history retained | test: phase-1, phase-3 and phase-4 fixtures unchanged (`git diff` empty at the candidate); phase-5 `previous` equals phase-4 `orientation`; live core equals phase-5 `current` | same | all equal |
| `SPEC-ECP-013` word census | test: no contract step names `focus`; the reference has no `focus` row; the check note names it once as removed | `tests/test_workflow_execution.py` | as stated |

## Acceptance scenarios

### Scenario 1: refusal

Run `main(["focus", root, "--artifact", "WO-001"])`. Assert exit 2, stdout
empty, stderr contains `harnessctl check --artifact WO-001`.

### Scenario 2: orientation

Run `orient.py` against the fake evaluator in its default mode; assert the
`selected` projection is populated and the operations list carries a
`check`-invoking `focus-json` operation. Run it in `no-check` mode; assert
`degraded` with `AEXORI030`.

### Scenario 3: vectors

Assert the phase-5 fixture's `orientation.previous` equals the phase-4
fixture's `orientation` and its `portable_core` equals the phase-1
`portable_core`; assert the live manifest digest equals the phase-5
`orientation.current.manifest_sha256`.

## Evidence retention

Under `docs/engineering/execution-control-plane/evidence/WO-ECP-017/`.

## Pass criteria

Every deterministic test passes on the Linux lane; the Windows workstation
reading is at its baseline; `git diff --stat main -- tests/fixtures/agentic_execution/canonical_vectors.json tests/fixtures/agentic_execution/phase3 tests/fixtures/agentic_execution/phase4` is empty at the candidate. Graph and integrity readings come from the exact released evaluator, se-harness 0.10.0, installed outside the checkout.

## Residual uncertainty

The root `.agents/skills/harness-orient` copy is the released 0.10.0 one
and still invokes `focus`; it moves when the root adopts the release
carrying this change, and until then this repository's own orientation
runs the alias against the 0.10.0 evaluator, which still has it.
