+++
id = "VER-ECP-023"
type = "verification"
title = "Independent evidence for the wave 0 correctness fixes"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
verifies = ["REQ-ECP-032"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-07T19:33:14Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-07 by the accountable owner with the words 'i approve', given after the packet PR #382 and its summary were presented: one before-and-after reading per rule, refusals observed at the process boundary, the subprocess timeout inspection, no regression. Approval of a definition authorizes no work."
+++

# Verification Contract: Independent evidence for the wave 0 correctness fixes

## Independence

Each fix is proven by a test that fails on the code before the change and
passes after it, recorded in the evidence packet as two readings. The
refusal paths are observed at the process boundary (exit status, standard
output, standard error), not through the functions the work order edits.
The doubled-code case is reproduced on this repository with the released
evaluator before the change and re-run with the candidate after it.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-032` one code per line | test: `check --checkpoint scope` with an unknown artifact, `--json` and human | `blocked_by` carries `WEX210: unknown artifact ID: …` once; the same for a `WEX200` path message (`ECP-COR-001`) |
| `REQ-ECP-032` guard refusals | test: `transition --apply` with `require_mutation_authority` patched to refuse; `decide`, `capture-verification`, `prepare-release` likewise | exit 2, empty stdout, `harnessctl: mutation guard …` on stderr for all four (`ECP-COR-002`) |
| `REQ-ECP-032` usage refusals | test: `transition --set BAD` | exit 2, usage message on stderr, no result on stdout (`ECP-COR-002`) |
| `REQ-ECP-032` no traceback | test: each result-building handler with `ProcedureError` and a `WEX230` `ValueError` injected | a blocked result, exit 1; `main()` with the same classes escaping a handler exits 2 with the `harnessctl:` line (`ECP-COR-003`) |
| `REQ-ECP-032` dashboard | test: engine mocked to exit 2 and to exit 1 with stderr | exit 2 with the stderr line in the refusal; exit 1 with `error` in the failed result (`ECP-COR-004`) |
| `REQ-ECP-032` pr-body | test: unknown artifact, `--json` and human | exit 1; failed command result with `WEX-ECP-014`; the one human line on stdout (`ECP-COR-005`) |
| `REQ-ECP-032` bounded launches | test: `subprocess.run` mocked to raise `TimeoutExpired` and `FileNotFoundError` for `gate_source._git`, `_run_distribution_script`, `upgrade_rehearsal.run`; inspection of every `subprocess.run` call in the package | each yields the caller's refusal; every call passes `timeout=` (`ECP-COR-006`) |
| `SPEC-ECP-021` `ECP-COR-007` | test: an `OPS-XXX-001.md` and a `DEC-XXX-001.md` committed on a second branch | `reachable_artifact_ids` contains both; `allocate_artifact_id` skips them |
| `SPEC-ECP-021` `ECP-COR-008` | test: a release record written with CRLF bytes | `_front_matter` returns the same mapping as for LF bytes |
| `SPEC-ECP-021` `ECP-COR-009` | test: a requirement with `verification_method = ["test", "inspection"]` | the snapshot item reads `"test, inspection"`; a string value is unchanged |
| `SPEC-ECP-021` `ECP-COR-010` | inspection of the two workflows; the existing workflow-pin tests | `bundle_manifest_sha256` at the three former `snapshot_sha256` reads; a pinned `setup-python` step in `github_release` and `observe`; the pin table in `tests/test_dashboard_publication.py` still holds |
| `SPEC-ECP-021` `ECP-COR-012` | inspection | the two reference rows read as stated; the two amendment records on `SPEC-ECP-016` are present and dated |
| `REQ-ECP-032` no regression | the full suite; `validate`; `doctor`; the hosted lanes | suite at its baseline; graph 0 errors; managed set untouched; every lane green |

## Acceptance scenarios

1. On this repository, `check . --artifact WO-ZZZ-999 --checkpoint scope --json`
   before the change shows the doubled code; after the change it shows one.
2. A checkout whose evaluator is not the released one: `transition --apply`
   exits 2 with the guard's refusal on standard error.
3. `pr-body . --artifact WO-ZZZ-999` exits 1 and prints one line.
4. `dashboard . --json` against a root the engine refuses exits 2.

## Property and invariant tests

For every handler and every exception class in the shared tuple, the
process ends with exit 1 and a result on stdout or exit 2 and a line on
stderr, never a traceback.

## Static and architecture checks

A source scan asserts no `startswith("mutation guard` remains in
`se_harness/cli.py` and that every `subprocess.run(` in `se_harness/` and
`repository_tools/` passes `timeout=`.

## Security and privacy checks

None beyond the timeout inspection.

## Performance and resilience checks

None.

## Manual assessments

A reviewer reads the two reference rows and the two amendment records.

## Evidence retention

`docs/engineering/execution-control-plane/evidence/WO-ECP-027/`.

## Residual uncertainty

Whether any consumer automation relied on `transition` exiting 1 for a guard
refusal; none is known, and the change moves the command onto the rule the
reference has stated since WO-ECP-022.
