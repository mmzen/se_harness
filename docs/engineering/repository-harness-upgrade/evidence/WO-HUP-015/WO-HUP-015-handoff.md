```toml
artifact = "WO-HUP-015"
checkpoint = "handoff"
formal_snapshot_sha256 = "6dd0a202406468a363521401e9323a3faeaae62013771efc14eb85240699a70e"
rebound_at = "2026-09-02T11:44:48Z"
```

# WO-HUP-015 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root is exact public 0.14.0: lock schema 3, `tool_version
0.14.0`, archive `70d438b5…` equal to the wheel `RLS-SEH-023` binds,
payload `25034dc7…`, written by the simple upgrade from the isolated
wheel-file environment in one atomic transaction (46 managed files, 3
updated, replay 46 unchanged; nothing left the managed set). The candidate
moved to 0.15.0. The 0.14.0 gate reads the same numbers as 0.13.0 over this
graph: 0 errors, 69 warnings, 0 advisories; the generated Explorer is the
same designed page. No public observation belongs to this adoption.

## Evaluators

- Predecessor (approval, start): released `se-harness 0.13.0` outside the
  checkout (`C:/Users/hok/se-harness-eval-0130`), wheel-installed.
- Governor from the transaction onward: released `se-harness 0.14.0`
  outside the checkout (`C:/Users/hok/se-harness-eval-0140`), installed
  from the wheel file verified against `RLS-SEH-023` before install; every
  later reading, this packet and the handoff check included.
- Candidate: this checkout, branch `governance/hup-015-adopt-0-14-0` off
  `main` at `25c0ef9`; transaction commit `cf8de47`; `pyproject.toml` reads
  0.15.0 after rule 8.

## Readings (VER-HUP-015)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| wheel SHA-256 before install | workstation | `70d438b5…` equal to `RLS-SEH-023`'s distribution table |
| `upgrade .` plan | exact 0.14.0 | 46 files, 3 `update` (the three of SPEC-HUP-015 rule 3), 43 unchanged, no `customized`/`conflict`/`remove` |
| `upgrade . --apply --evidence-output …` | exact 0.14.0 | transaction complete; `WO-HUP-015-evaluator-upgrade.json` retained: prior lock `9dfec5b4…`, prior `tool_version 0.13.0`, target identity equal to the new lock |
| `upgrade .` replay | exact 0.14.0 | 46 unchanged |
| `validate --advisories` | exact 0.14.0 | 0 errors, 69 warnings, 0 advisories (artifact count in the readings log) |
| `doctor` | exact 0.14.0 | 0 FAIL |
| `qualify released-root .` | exact 0.14.0 | RR001 to RR004 PASS |
| `inspect` | exact 0.14.0 | exit 0 |
| `dashboard` twice | exact 0.14.0 | content digest identical across both runs; the designed page, zero remote origins |
| review preflight `--work-order WO-HUP-015` | exact 0.14.0 | PASS |
| `evaluator_facts derive` | candidate | 0.14.0 -> 0.15.0; `PRE008` with the candidate still at 0.14.0, as rehearsed |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13) | section below |

### The Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` on the moved root at
`cf8de47` (identical tests and packaged bytes at every later branch commit),
Windows 11 (CPython 3.13), LF checkout: 1,178 tests, 26 skipped, 1 error,
the known baseline name present on `main` and outside this work order
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`),
equal to the same-commit control on the 0.13.0 root and to the rehearsal
after the same edits. No other name differs.

## Identity-aware edits (rules 8, 9, 10)

- `pyproject.toml`, `se_harness/__init__.py`, README install line: 0.15.0.
- `AGENTS.md` owner region: the evaluator instruction reads
  `se-harness==0.14.0`.
- `docs/notes/developing-se-harness.md`: the candidate/root identity
  paragraph and the "Advancing the root evaluator" paragraph state 0.14.0
  adopted by this work order and the 0.15.0 candidate.
- `tests/test_instruction_architecture.py`: `managed_count_by_root` gains
  `"0.14.0": 40`. The dashboard tests' root-version guard of `WO-HUP-014`
  already admits this root. Rehearsal on a throwaway clone of `main` at
  `25c0ef9` predicted exactly this set.

## Deviation: the prior-lock digest of rule 4

`SPEC-HUP-015` rule 4 and this work order name the prior lock as
`9dfec5b4…`, the value the rehearsal's transaction document recorded. The
real transaction document records `7558ae28…`. Both are digests of the same
committed 0.13.0 lock: `7558ae28…` is the LF blob as committed
(`git show 25c0ef9:.engineering-harness.lock`), and `9dfec5b4…` is that
blob with CRLF line endings, because the throwaway rehearsal clone was
created with `core.autocrlf=true` and the transaction document hashes the
working-tree bytes it replaced. The governor-transition lane compares the
document's prior digest with the base root's committed lock and passed at
`3aa09ca`, so the real value is the correct one; the approved specification
keeps the rehearsal value as a measured statement of that rehearsal, and
this note is the record of the difference. Nothing else in the transaction
differs from the rehearsal.

## Material non-effects

No product byte beyond the version identity; no template byte; no release,
tag, publication, Pages or maintenance-line change; the published 0.14.0
did not move. `RLS-SEH-023` and `VREC-SEH-023` are unchanged.

## Hosted lanes

All lanes of pull request #317 pass at its head `3aa09ca`, including the
governor-transition lane assessing the real 0.13.0 to 0.14.0 root move with
exactly one transaction document and the released `RLS-SEH-023` supplying
the wheel, the managed lane running the 0.14.0 gate the transaction
installed, the candidate-evidence lanes with the 0.14.0 to 0.15.0 upgrade
rehearsal on both platforms, and the Publication Rehearsal in both modes.
Runs: Publication Rehearsal (pull_request, 33626221907, success); SE Harness Candidate Evidence (pull_request, 33626221673, success); Engineering Harness (pull_request, 33626221289, success); Governor Transition Assessment (pull_request, 33626221265, success).
