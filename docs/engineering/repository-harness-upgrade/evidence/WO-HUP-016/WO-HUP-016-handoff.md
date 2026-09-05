```toml
artifact = "WO-HUP-016"
checkpoint = "handoff"
formal_snapshot_sha256 = "e1bdca2d982919f9554b8e54e4855839a3b62711d4c07d9eb666138b2dcb0843"
rebound_at = "2026-09-05T09:23:44Z"
```

# WO-HUP-016 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root is exact public 0.15.0: lock schema 3, `tool_version
0.15.0`, archive `eb09343f…` equal to the wheel `RLS-SEH-024` binds,
payload `11e4ad03…`, written by the simple upgrade from the isolated
wheel-file environment in one atomic transaction (48 managed files, 19
updated, 1 added, 1 adopted, replay 48 unchanged; nothing left the managed
set). The candidate moved to 0.16.0. The 0.15.0 gate reads this graph with
its new rules and finds the same numbers the 0.14.0 gate read: 0 errors, 71
warnings, 0 advisories; the Explorer generates identically twice. This is
the first root of this repository that reads decision artifacts and the
reader-first templates; no `DEC-` artifact is raised by this work order.

## Evaluators

- Predecessor (approval, start): released `se-harness 0.14.0` outside the
  checkout (`C:/Users/mathi/se-harness-eval-0140`), wheel-installed.
- Governor from the transaction onward: released `se-harness 0.15.0`
  outside the checkout (`C:/Users/mathi/se-harness-eval-0150`), installed
  from the wheel file downloaded from PyPI and verified against
  `RLS-SEH-024` before install; every later reading, this packet and the
  handoff check included.
- Candidate: an LF clone of `main` at `cfd9c4d`
  (`core.autocrlf=false`), branch `governance/hup-016-adopt-0-15-0`; the
  transaction commit is `a3b5c12a`; `pyproject.toml` reads 0.16.0
  after rule 8. The LF clone was chosen so the transaction document's prior
  lock digest is the committed blob's, `0425fccf…`, and no line-ending
  deviation has to be recorded.

## Readings (VER-HUP-016)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| wheel SHA-256 before install | workstation | `eb09343f65a52ecc7511aacbe7f4cc546cfe4bf28eeed62cf3ff2bccf838d947`, equal to `RLS-SEH-024`'s distribution table |
| `upgrade .` plan | exact 0.15.0 | 48 files, 19 `update` (the nineteen of SPEC-HUP-016 rule 3), 1 `add` (`DECISION.template.md`), 1 `adopt` (`GLOSSARY.md`, bytes unchanged), 27 unchanged, no `customized`/`conflict`/`remove`; equal to the rehearsal |
| `upgrade . --apply --evidence-output …` | exact 0.15.0 | transaction complete; `WO-HUP-016-evaluator-upgrade.json` retained: prior lock `0425fccf0578c52f…` (the committed 0.14.0 LF blob), prior `tool_version 0.14.0`, target 0.15.0 with archive `eb09343f…` and payload `11e4ad03…`, postconditions `lock_matches_target`, `no_op_replay`, no external action, no product release |
| `upgrade .` replay | exact 0.15.0 | 48 unchanged |
| lock | exact 0.15.0 | `tool_version 0.15.0`, archive pair recorded, `GLOSSARY.md` recorded as `{"mode": "seed", "state": "present"}` |
| root copies vs candidate templates | workstation | the 17 files without substitutions byte-equal to `templates/repository/standard/`; `ENGINEERING_HARNESS.md` equals its template with the project name and version substituted; `.engineering-harness.toml` reads `tool_version = "0.15.0"` |
| `validate --advisories` | exact 0.15.0 | 1,315 artifacts, 0 errors, 71 warnings (42 `W013`, 15 `W015`, 14 `W014`, all pre-existing), 0 advisories |
| `doctor` | exact 0.15.0 | 116 PASS, 0 FAIL |
| `qualify released-root .` | exact 0.15.0 | PASS; `RR001` runtime matches the target root lock, `RR002` 116/116 managed checks, `RR003` artifacts 1,315 errors 0 warnings 71, `RR004` target state unchanged |
| `inspect` | exact 0.15.0 | exit 0 |
| `dashboard` twice | exact 0.15.0 | 1,562 resources, resource digest `dd5e785fc18e5cdd…` identical across both runs; the generation summary alone carries a timestamp |
| review preflight `--work-order WO-HUP-016` | exact 0.15.0 | PASS |
| `identity --role released-evaluator` | exact 0.15.0, Windows | `passed: true` with the evaluator environment as `--expected-root` and the clone as `--checkout-root`, isolated Python required; archive `eb09343f…`, payload `11e4ad03…`. Naming the checkout as the expected root instead reports `RID003`, `RID004` and `RID005`: a misuse of the command, recorded so the next adoption does not repeat it |
| `evaluator_facts derive` | candidate | `PRE008` with the candidate still at 0.15.0, as rehearsed; the 0.15.0 to 0.16.0 pair after rule 8 |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.14.6) | section below |

### The Windows suite

Both runs on this commit's tests, Windows 11, CPython 3.14.6, 8 workers:

| Run | Root | Result |
| --- | --- | --- |
| moved root (this clone, after rules 8 to 10) | exact 0.15.0 | 1,249 tests, 1 error, 26 skipped |
| same-commit control (workstation checkout of `main` at `cfd9c4d`) | exact 0.14.0 | 1,249 tests, 1 error, 26 skipped |

The one error is the same name on both roots,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
the workstation baseline error the release readings also carry (it needs a
path outside every checkout that this workstation does not provide). The
26 skips are the Windows-only guards; the Linux lane skips none. Beyond the
identity-aware edits below, the failure set is the control's, rule 10
satisfied. The moved root's own `validate` and Explorer steps in the runner
preamble read PASS.

## Identity-aware edits (rules 8, 9, 10)

- `pyproject.toml`, `se_harness/__init__.py`: 0.16.0. The README no longer
  pins a version in its install lines since `WO-DOC-014`, so it does not
  move.
- `AGENTS.md` owner region: the evaluator instruction reads
  `se-harness==0.15.0`.
- `docs/notes/developing-se-harness.md`: the candidate/root identity
  paragraph names the 0.16.0 candidate and the 0.15.0 root; the "Advancing
  the root evaluator" paragraph states 0.15.0 adopted by this work order
  from the wheel `RLS-SEH-024` binds, with `WO-HUP-015` joining the list of
  earlier adoptions.
- `tests/test_instruction_architecture.py`: `managed_count_by_root` gains
  `"0.15.0": 41`, the 40 managed files of 0.14.0 plus
  `DECISION.template.md`.
- `tests/test_validation_taxonomy.py`: the three predicate-row pins on the
  root `QUALITY_GATES.md` assert the row prefix every root carries, since a
  root of 0.15.0 or later appends the gate's `QGP-G*-DECISION` predicate.
  Its equality branch compares the canonical and root copies directly on
  this root.
- `ARCH-HUP-012` was amended by record before the start preflight so that
  it addresses `REQ-HUP-031` and `REQ-HUP-032` and conforms to
  `SPEC-HUP-016`; the start preflight had reported `W021` because the
  packet reused the 0.14.0 architecture without extending its relation.
  The rehearsal on a throwaway clone of `main` at `e4192ed` predicted every
  test edit above; its one further failure, the Explorer's source URL
  assertion, was the clone's local remote and did not recur here.

## Material non-effects

No product byte beyond the version identity; no candidate template byte
under `templates/`; no release, tag, publication, Pages or maintenance-line
change; the published 0.15.0 did not move. `RLS-SEH-024` and `VREC-SEH-024`
are unchanged. No decision artifact was raised.

## Hosted lanes

LANES-SECTION
