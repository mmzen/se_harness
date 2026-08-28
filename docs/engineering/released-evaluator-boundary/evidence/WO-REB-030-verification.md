# WO-REB-030 implementation evidence

artifact: WO-REB-030
checkpoint: handoff
formal_snapshot_sha256: afa2f579fba34c34a8460cafb1d53b5cb19860cfde563bfa65963b2a4943d9e6

Retained by the implementation actor on 2026-08-28. This file is evidence. It
does not complete, verify, or release the work order.

## Outcome

The interpreter-safety rule stays in code, unchanged in behaviour, at its one
boundary (`se_harness/runtime_identity.py`). The apparatus `WO-REB-021` built
to make two runtimes agree on it — the JSON declaration, the loader and its
`ISD` validators, the boundary registry, the `ISC` corpus accessors and the
`repository_tools` mirror — is deleted, and the tests own the corpus. Issue
#220's acceptance criterion holds: one `interpreter_safety.py`, no JSON
mirror, the behavioural tests unchanged in what they prove and green.

## Evaluators

- Governing: released `se-harness 0.8.0` (the root since `WO-HUP-008`),
  installed outside the checkout from the digest-verified wheel, invoked
  with `-I`.
- Candidate: this checkout, branch `governance/reb-030-interpreter-safety`
  off `main` at `f62256f`; suite run with candidate source (CPython 3.12,
  this workstation).

## What changed

| Path | Change |
| --- | --- |
| `se_harness/interpreter_safety.py` | 593 → 381 lines. Deleted: `_unique_object`, `_exact_keys`, `_text`, `_declaration_path`, `declaration_bytes`, `load_declaration`, `_validate_cases`, `_validate_boundaries`, `_validate_corpus`, `declared_cases`, `declared_boundaries`, `declared_corpus`, `boundary_identifiers`; the constants `DECLARATION_SCHEMA`, `RUNTIMES`, `BOUNDARY_KINDS`, `CASE_PATTERN`, `CORPUS_PATTERN`, the `*_KEYS` sets and `DECLARATION_KEYS`; the `json`, `re`, `Iterable`, `Mapping` imports. Kept byte-for-byte in behaviour: `EVALUATION_ORDER`, `evaluate`, `SafeEntryPoint`, `refusal_case`, `normalized_origin`, `link_classification_available`, `reparse_information_observable`, `_is_symlink`, `_is_junction`, `_traverses_link`, `_digest`, the `EPS` cases and messages, `POSITION_CLASSES`, `PLATFORMS`, `OUTCOMES`, `JUNCTION_PREDICATE`. New module docstring. |
| `se_harness/interpreter_safety.json` | deleted (267 lines) |
| `repository_tools/interpreter_safety.py` | deleted (592 lines; no caller since `WO-REB-028`) |
| `tests/test_interpreter_safety.py` | 1,386 → 1,176 lines. Added `CORPUS_CONSTRUCTABLE_ON` and `CORPUS_UNCONSTRUCTABLE_REASON` (the inventory the declaration carried, ISC001–ISC018). Deleted `DeclarationShapeTests`, `BidirectionalCorpusTests`, `BoundaryRegistryTests`. `RuleEvaluationTests._require` reads the inventory; `_both` evaluates the one loader; `JunctionPredicateTests` loops over the one loader; `LOADER_MODULES` names one module; the two package-data/surface-list tests became their negative forms (`test_no_declaration_ships_and_no_second_loader_exists`, `test_the_rule_module_appears_in_the_portable_release_surface_list`); `PlatformCoverageTests` reads the inventory. Every behavioural test (`RuleEvaluationTests` ISC001–ISC018 and the seven non-corpus forms, `RecordedFactsTests`, `PurityAndCostTests`, `JunctionPredicateTests`, `ImportBarrierTests`, `StaticArchitectureTests`) is retained. |
| `pyproject.toml`, `scripts/check_portable_release_surface.py` | `interpreter_safety.json` removed from package data and from `REQUIRED_INTERPRETER_SAFETY_MEMBERS` |
| `docs/notes/developing-se-harness.md` | the `--evaluator-python` paragraph names the rule in code and the history |
| governance | `REQ-REB-026` retired by dated amendment; `SPEC-REB-011` (rules 12–13, 21–26 retired), `ARCH-REB-010` (superseded for two-runtime components), `VER-REB-010` (four `REQ-REB-026` rows retired), `SPEC-REB-013` rule 7 and `VER-REB-012` amended by date |

## Behavioural proof

`tests.test_interpreter_safety`: 65 tests OK, 3 skips (the Windows-only
forms ISC005 and ISC009 and the junction route not constructable here); every
constructable corpus form yields the same case as at the base commit (the
test bodies are unchanged; only the helper that used to compare two loaders
now evaluates one). `EVALUATION_ORDER` is unchanged; `runtime_identity.py`
is untouched.

## Readings under the 0.8.0 root, isolated mode, over the complete change set

- `validate .`: PASS; structure E0/W0, governance E0/W0, policy E0/W0,
  maintenance E0/W473.
- `doctor .`: 0 FAIL.
- `check_portable_release_surface.py --repository .`: PASS.
- Candidate wheel (`pip wheel --no-deps`, clean `build/`):
  `se_harness-0.9.0-py3-none-any.whl`, 106 members, `interpreter_safety.py`
  present and no `interpreter_safety.json`; `--wheel`: PASS. A first build
  reused a stale ignored `build/lib` from an earlier local wheel and still
  listed the JSON (107 members); the build directory was removed and the
  wheel rebuilt before the reading above. The hosted candidate-evidence lane
  builds from a clean export and is the reading of record.
- No withdrawn name remains outside `docs/`: `load_declaration`,
  `declared_*`, `boundary_identifiers`, `declaration_bytes`, `tools_safety`,
  `ISD1xx` occur only in `se_harness/hash_bound.py` and its tests (a
  different, still-consumed declaration with its own `load_declaration`)
  and in the negative assertions of `test_interpreter_safety.py`.

## Suite

`python scripts/run_tests.py --scale full` with candidate source against the
0.8.0 root: 989 tests (1,009 before: the three deleted declaration classes),
1 failure, 4 skips — the failure is
`test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`,
the workstation file-mode condition that passes hosted, unchanged. Identical
result on the throwaway rehearsal before approval.

## Handoff check

`harnessctl check . --artifact WO-REB-030 --checkpoint handoff --changed-path … --changes-complete` with released 0.8.0 outside the checkout: Completed over the 20 paths below; before this file carried the formal snapshot the only non-pass predicate was QGP-G4I-EVIDENCE. The work order's own file changes only through its recorded lifecycle transitions and is not a declared change.

## Complete changed-path set

Every path this work order changed since `main` at `f62256f`, packet, amendments and evidence included:

```
docs/engineering/released-evaluator-boundary/architecture/adr/ADR-REB-013.md
docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-010.md
docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-013.md
docs/engineering/released-evaluator-boundary/evidence/WO-REB-030-verification.md
docs/engineering/released-evaluator-boundary/README.md
docs/engineering/released-evaluator-boundary/requirements/REQ-REB-026.md
docs/engineering/released-evaluator-boundary/requirements/REQ-REB-030.md
docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-011.md
docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-013.md
docs/engineering/released-evaluator-boundary/specifications/SPEC-REB-015.md
docs/engineering/released-evaluator-boundary/verification/VER-REB-010.md
docs/engineering/released-evaluator-boundary/verification/VER-REB-012.md
docs/engineering/released-evaluator-boundary/verification/VER-REB-014.md
docs/notes/developing-se-harness.md
pyproject.toml
repository_tools/interpreter_safety.py
scripts/check_portable_release_surface.py
se_harness/interpreter_safety.json
se_harness/interpreter_safety.py
tests/test_interpreter_safety.py
```
