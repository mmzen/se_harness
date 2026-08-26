+++
id = "VER-CIP-001"
type = "verification"
title = "Independent evidence for the pipeline simplification"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-08-26"
updated = "2026-08-26"

[relations]
verifies = ["REQ-CIP-001", "REQ-CIP-002", "REQ-CIP-003", "REQ-CIP-004", "REQ-CIP-005", "REQ-CIP-006"]
+++

# Verification Contract: Independent evidence for the pipeline simplification

## Independence

Expected values are the figures in `docs/notes/ci-pipeline.md`'s baseline
table, measured on `e98b788` before any change. Workflow assertions are
made by tests that parse the YAML with PyYAML in the test environment, not by
the workflows themselves. Run observations come from the GitHub runs API on
the pull request that carries the change.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-CIP-001` | YAML inspection test; run observation | trigger blocks and concurrency of the three workflows; two pushes to the PR | filters and groups as `CIP-TRG`; one completed and one cancelled run per workflow, no push run |
| `REQ-CIP-002` | YAML inspection test; log search | job list; `pip wheel` / `python -m build` occurrences per job | four jobs; one build, in `candidate-source`; consumers verify `SHA256SUMS` |
| `REQ-CIP-003` | YAML inspection; line count; rehearsal run | `workflow_call` file and its two callers; `.github/scripts/` line count; a PR editing one `run:` body | both lanes call the definition; ≥2,500 lines removed; no digest artefact; the edited step executes |
| `REQ-CIP-004` | derivation test on a fixture history; template inspection; validator test | tag + four merges with three trailers and one without; an approved contract with a wrong `gates` | census and `untraced` as specified; exit 1; `E-CIP-001` fires |
| `REQ-CIP-005` | YAML inspection; run observation on a dispatch | `qualify` selection; Pages callers | one qualification job; both Pages workflows call one definition |
| `REQ-CIP-006` | grep test; derivation test; failure-injection run | literals in repository-owned workflows; bump without scenario | no version or digest literal; the derivation step fails naming the path |
| all | documentation inspection | notes listed in `CIP-DOC` | each section updated in the same change; every workflow header names its note section |

## Acceptance scenarios

1. Push twice to a pull request; list runs; one completed run per workflow.
2. Read `candidate-evidence` logs; one wheel build.
3. Edit a qualification `run:` line on a branch; the rehearsal executes it.
4. Derive the 0.7.0 census over `v0.6.0..e98b788` and compare with
   `REL-SEH-016`'s `gates`; the difference is explained by trailer-less
   merges, each listed.
5. Raise the version without a scenario; the derivation step fails, nothing
   skips.
6. Read `developing-se-harness.md` after each work order and follow the
   release sequences on a scratch clone.

## Pass criteria

All deterministic tests pass on Windows and Linux; released-evaluator
validation 0 errors; every scenario recorded in the evidence; scenario 6
performed by a reader who did not implement the work order.
