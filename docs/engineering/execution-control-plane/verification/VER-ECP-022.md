+++
id = "VER-ECP-022"
type = "verification"
title = "Independent evidence for the merged installation command"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-06"
updated = "2026-09-06"

[relations]
verifies = ["REQ-ECP-031"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-06T10:51:57Z"
decided_by = "assurance-owner"
reason = "Approved on 2026-09-06 by the accountable owner with the words 'i approve', given after the packet PR #359 and its summary were presented: the evidence matrix over both target states, the refusal, the diagnostic, the notes and records, and no regression; independent because the former adopt tests keep their assertions byte for byte. Approval of a definition authorizes no work."
+++

# Verification Contract: Independent evidence for the merged installation command

## Independence

The behaviour of both target states is pinned by tests written for the
previous `init` and `adopt`; only the command name in their invocations
changes, every assertion keeps its bytes. The refusal of `adopt` comes from
argparse, not from product code the work order touches. The fresh-install
bytes are additionally pinned outside the suite by the `candidate-evidence`
workflow's bare `init` and the fixture cache equality test.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-ECP-031` one name | test: the parser-shape test of `tests/test_cli_shape.py`; `--help` | the repository-command set contains `init` and not `adopt`; `--help` lists no `adopt` |
| `REQ-ECP-031` empty target | test: every existing `init` test, the fixture cache equality test, the `candidate-evidence` lane | pass unchanged; no `docs/engineering/ADOPTION_REPORT.md` in the fresh install |
| `REQ-ECP-031` existing target | test: the former `adopt` tests invoked as `init`, assertions byte for byte | owner text kept, fragments present, report written with the detected ecosystem, lock excludes the report, conflicts refuse every write with exit 1 |
| `REQ-ECP-031` refusal | test: invoke `adopt` through `main()` | exit 2, empty stdout, argparse usage error on stderr, no handler called |
| `SPEC-ECP-020` `ECP-INS-007` | test: the lock-floor test of `tests/test_harnessctl.py` | the diagnostic names `harnessctl init` and still says "re-adopt" |
| `SPEC-ECP-020` `ECP-INS-008` | inspection: `harnessctl init --help` | `--dry-run` carries its help sentence |
| `SPEC-ECP-020` `ECP-INS-009`, `ECP-INS-010` | inspection | the three notes read as stated; the seven amendment records are present, dated and name `SPEC-ECP-020` |
| `REQ-ECP-031` no regression | the full suite; `validate`; `doctor`; the mutation-guard tests | suite at its baseline; graph 0 errors; managed set untouched; guard inventory unchanged |

## Acceptance scenarios

1. A folder holding `Cargo.toml`, an owner `AGENTS.md`, `CLAUDE.md` and
   `.gitignore`: `init` exits 0, keeps the owner text first, inserts the
   markers, writes the report naming Rust, `validate` and `dashboard` pass.
2. An absent path: `init` creates it, writes the complete harness, no
   report; `doctor` passes.
3. A folder holding a repository-owned
   `.github/workflows/engineering-harness.yml`: `init` exits 1, prints
   "conflict" and "another workflow filename", writes nothing.
4. `harnessctl adopt some/path`: exit 2, usage error.

## Property and invariant tests

For any target, `init --dry-run` writes nothing and its plan equals the
plan of the following `init`; the report is planned if and only if the
target has at least one entry.

## Static and architecture checks

The parser-shape test; the source-reading test of `ECP-TMB-003` still finds
no pre-parse guard in `main()`.

## Security and privacy checks

The mutation-guard tests pass unchanged.

## Performance and resilience checks

None beyond the suite.

## Manual assessments

The three notes are read once by a reviewer for the sentences
`ECP-INS-009` names.

## Evidence retention

`docs/engineering/execution-control-plane/evidence/WO-ECP-026/`.

## Residual uncertainty

Whether any consumer outside this repository scripted `adopt`; none is
known, and the failure mode is a loud usage error.
