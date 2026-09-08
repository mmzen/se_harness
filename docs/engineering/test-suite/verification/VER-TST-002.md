+++
id = "VER-TST-002"
type = "verification"
title = "Verify wave 4: one run per test, shared support modules, one retired-surface table, cited pins"
status = "draft"
owners = ["assurance-owner", "quality-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-TST-004"]
+++

# Verification Contract: Verify wave 4: one run per test, shared support modules, one retired-surface table, cited pins

## Independence

Expected values come from `REQ-TST-004`, the rules of `SPEC-TST-002` and the
counts the assessment of 2026-09-07 recorded, re-measured on `main` at
`50f9cda5`. The `unittest` loader is the oracle for the run count; the serial
`unittest discover` on the same commit is the oracle for the verdict. Wall
times are read from the hosted `candidate-evidence` job and the workstation,
never from the changed code.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| `REQ-TST-004` re-runs | test: the loader's discovered count against the defined count; the runner's class timings | discovered equals defined; no class under `tests/` subclasses a test-carrying class (TST-HYG-001, TST-HYG-002) |
| `REQ-TST-004` support modules | readings of `def invoke`, `def git`, `def _git`, `def write`, `def formal`, `sys.path.insert` and `from tests.test_` under `tests/`; the support modules' own tests | one definition each, in its support module; no test module imports another; a `SystemExit` inside `main` returns a code through `invoke` (TST-HYG-003 to TST-HYG-008) |
| `REQ-TST-004` tombstones and source reading | readings of `assertFalse(` with `exists()`, `assertNotIn(` on a `source` or `text` variable, and `read_text` on a `tests/` path | every tombstone in `test_retired_surface.py`; no test reads another test's source; each product-source read names a rule (TST-HYG-009 to TST-HYG-011) |
| `REQ-TST-004` pins | inspection of every `assertIn` on a note, a router or a fragment; the three specification-cited tests | each remaining pin names a rule; the README budget, the expertise labels and the reference-covers-parser tests present and passing (TST-HYG-012 to TST-HYG-014) |
| `REQ-TST-004` counts and structure | test: the managed count derived at run time; readings of `len(` on same-module tuples and of `unittest.main()` | no literal file count; no self-length assertion; at most one final `main()` per module (TST-HYG-015 to TST-HYG-017) |
| `REQ-TST-004` fixtures and lane | `fixture_support.initialisations()` after a full run; the lane YAML | one initialisation per process for default-name fixtures; a timings path in the suite step and its persistence named (TST-HYG-018, TST-HYG-019) |
| `REQ-TST-004` regression | serial `unittest discover` and the parallel runner on the candidate; `validate`; `doctor`; the hosted lanes | failure set equals the baseline on Windows and Linux; the Linux-lane wall time lower and recorded; graph 0 errors; every lane green (TST-HYG-020) |

## Acceptance scenarios

- Count defined and discovered tests with the loader on `main` and on the
  candidate; record both readings in the evidence packet.
- Subclass a test-carrying class in a scratch copy: the loader-count test
  fails and names the class.
- Run the suite with `commit.gpgsign=true` in the global Git configuration:
  every fixture commit succeeds.
- Change one sentence of `docs/notes/harness-overview.md` in a scratch copy:
  no test fails.
- Read the hosted `candidate-evidence` suite step's duration on the base and
  on the candidate head.

## Evidence retention

One evidence packet under `docs/engineering/test-suite/evidence/WO-TST-004/`,
holding the loader counts, the readings before and after, the serial and
parallel verdicts, the wall times with their lane ids, and the `validate` and
`doctor` readings.

## Pass criteria

Every row of the matrix passes on the Windows workstation and on the hosted
Linux lane; the released 0.16.0 evaluator's `validate` reports 0 errors; the
pull request's lanes are green through completion and the record head; no
product module and no managed path changes.

## Residual uncertainty

The Windows baseline carries one teardown `PermissionError` in
`test_artifact_authoring` that predates this work and stays in the failure
set. The persistence of the timings file on the lane depends on the
mechanism the executor chooses. `tests/skill_contract_support.py` stays as
it is.
