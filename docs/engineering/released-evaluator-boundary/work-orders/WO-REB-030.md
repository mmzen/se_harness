+++
id = "WO-REB-030"
type = "work_order"
title = "Keep interpreter_safety.evaluate, delete its declaration apparatus and the repository_tools copy"
status = "draft"
owners = ["engineering-owner"]
created = "2026-08-28"
updated = "2026-08-28"

[assurance]
commit_bound_verification = "required"
rationale = "The rule is a trust-boundary rule every evaluator identity check passes through; the work removes the apparatus around it and must prove, at the exact commit, that no refusal or acceptance changed and that the wheel and the import barrier are as declared."
decided_by = "engineering-owner"

[execution_scope]
paths = [
  "se_harness/interpreter_safety.py",
  "se_harness/interpreter_safety.json",
  "repository_tools/interpreter_safety.py",
  "tests/test_interpreter_safety.py",
  "pyproject.toml",
  "scripts/check_portable_release_surface.py",
  "docs/notes/developing-se-harness.md",
  "docs/engineering/released-evaluator-boundary/",
]

[relations]
implements = ["REQ-REB-030"]
specifications = ["SPEC-REB-015"]
architecture = ["ARCH-REB-013", "ADR-REB-013"]
verification = ["VER-REB-014"]
+++

# Work Order: Keep `interpreter_safety.evaluate`, delete its declaration apparatus and the `repository_tools` copy

## Lifecycle

This work order requires the accountable engineering owner's approval before
start preflight or any declared work. Its authoritative state, and the
timestamp and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It resolves issue #220 (complexity audit
P1-8), whose sequencing condition — "after P0-2" — `WO-REB-028` satisfied.

Commit-bound verification is `required`.

## Objective

Keep the interpreter-safety rule exactly as it behaves and remove the
apparatus built to make two runtimes agree on it, now that one runtime with
one boundary remains: the JSON declaration, the loader and its `ISD`
validators, the boundary registry, the `ISC` corpus accessors, the
`repository_tools` mirror and the tests that exist only for those.

## Rehearsal, 2026-08-28

On a throwaway export of `main` at `f62256f` with the change applied:
`se_harness/interpreter_safety.py` 593 → 381 lines, `tests/test_interpreter_safety.py`
1,386 → 1,176; `tests.test_interpreter_safety` 65 tests OK (3 platform
skips); 0.8.0 `validate` 0 errors, `doctor` 0 FAIL; portable-surface
`--repository` PASS and `--wheel` PASS on a 106-member wheel carrying no
`interpreter_safety.json`; full suite 989 tests (1,009 before: the three
deleted classes) with only the known workstation file-mode failure that
passes hosted.

## In scope

- `se_harness/interpreter_safety.py`: delete `_unique_object`, `_exact_keys`,
  `_text`, `_declaration_path`, `declaration_bytes`, `load_declaration`,
  `_validate_cases`, `_validate_boundaries`, `_validate_corpus`,
  `declared_cases`, `declared_boundaries`, `declared_corpus`,
  `boundary_identifiers`, the declaration constants and the `json`/`re`/typing
  imports they used; rewrite the module docstring; keep everything else
  byte-for-byte in behaviour (`SPEC-REB-015` rules 1, 3, 4).
- Delete `se_harness/interpreter_safety.json` and
  `repository_tools/interpreter_safety.py`; drop the JSON from `pyproject.toml`
  package data and from `REQUIRED_INTERPRETER_SAFETY_MEMBERS` in
  `scripts/check_portable_release_surface.py` (rule 6).
- `tests/test_interpreter_safety.py`: add the corpus inventory
  (`CORPUS_CONSTRUCTABLE_ON`, `CORPUS_UNCONSTRUCTABLE_REASON`) the declaration
  carried; delete `DeclarationShapeTests`, `BidirectionalCorpusTests`,
  `BoundaryRegistryTests`; make `RuleEvaluationTests`' `_require`/`_both`
  and `JunctionPredicateTests`' loops single-loader; `LOADER_MODULES` names
  one module; replace the two package-data/surface-list tests with their
  negative forms; keep every behavioural test (rule 5).
- Governance by dated amendment: retire `REQ-REB-026`; amend `SPEC-REB-011`
  (rules 12–13 and 21–26 retired, 1–11 and 14–20, 27 remain), `ARCH-REB-010`
  (superseded for the two-runtime components by `ARCH-REB-013`),
  `VER-REB-010` (the four `REQ-REB-026` rows retired), `SPEC-REB-013` rule 7
  and `VER-REB-012`'s two lines that name the declaration; index the domain
  README; correct `docs/notes/developing-se-harness.md` where it names the
  declaration.
- Retain evidence at
  `docs/engineering/released-evaluator-boundary/evidence/WO-REB-030-verification.md`.

## Out of scope

`se_harness/runtime_identity.py`; any `EPS` case, message or order; the
`RuntimeIdentity` schema; `templates/`; the released 0.8.0 and the lock;
`hash_bound.py` and its declaration (a different, still-consumed data
document); historical evidence that quotes `ISD`/`ISC` codes.

## Authorized decision envelope

The exact test-helper shapes, provided each behavioural test still builds
its form and asserts its case; the amendment wording; the order of
readings.

## Constraints

- No accepted path becomes refused and no refused path becomes accepted;
  the behavioural suite is the proof.
- The 0.8.0 root governs every reading; a refusal is a stop.
- `repository_tools` imports only the standard library and its own package
  before and after.

## Required verification

`VER-REB-014` in full; the full suite; the pull request's lanes green on
Linux and Windows; the handoff check over the complete changed-path set.

## Stop and escalate conditions

A behavioural test that changes outcome, a lost `EPS` identifier, any caller
of a withdrawn name outside `docs/`, a wheel still carrying the JSON, or a
need for authority beyond the approved stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
