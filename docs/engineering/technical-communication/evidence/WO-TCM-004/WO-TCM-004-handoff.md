```toml
artifact = "WO-TCM-004"
checkpoint = "handoff"
formal_snapshot_sha256 = "609bd3fd9910c82e9b2a066667c994e3d776da361a01c5de14b87e86b842d4cb"
rebound_at = "2026-09-04T07:42:41Z"
```

# WO-TCM-004 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`docs/notes/diagnostic-codes.md` now lists the decision-artifact families
`E-DCM-001..004` and `W-DCM-001..002` that `WO-DCM-001` added to the
candidate validator: 262 codes across 30 registered prefixes, up from 256
across 28. `repository_tools/diagnostic_code_index.py` carries the two
registry rows and the unregistered-family guard: a string literal with a
code of the shape `E-XXX-nnn`, `W-XXX-nnn` or `WEX-XXX-nnn` whose family is
absent from the registry makes `--check` and `--write` exit 1 naming the
family and its codes before any page is read, and
`tests/test_diagnostic_code_index.py` asserts the repository is clean of
them. The residual uncertainty `VER-TCM-002` recorded is mechanical for
those roots (`REQ-TCM-005`; `TCM-DCI-002` to `TCM-DCI-005`).

## Evaluators

- Governing: released `se-harness 0.14.0` outside the checkout, `-I`, on
  this Windows 11 checkout for every reading, the packet and the handoff
  check included.
- Candidate: this checkout, branch `wo/tcm-004-execution` off `main` at
  `7b51ab1ec7dc3a0cf5fb16782bced4cf7f57ea67` (the merge of PR #331, which
  carries the approved work order).

## Change

- `repository_tools/diagnostic_code_index.py`: registry rows `E-DCM` and
  `W-DCM` (installed validator); `_literal_codes` factored out of `scan`;
  `unregistered_families` and the guard report; `main` fails closed on
  the guard before `--write` or `--check`.
- `docs/notes/diagnostic-codes.md`: regenerated and committed.
- `tests/test_diagnostic_code_index.py`: `E-DCM-001` and `W-DCM-001` in the
  known-code set; one repository-level guard assertion; two guard tests on
  a temporary tree (an unregistered `E-ZZZ`/`W-ZZZ` pair is named and
  fails `--check` while a rule identifier and an artifact identifier in
  the same tree are not; registered families and single-root codes pass).
- `docs/notes/decision-artifacts.md`: one sentence after its diagnostics
  table pointing to the generated index.
- This domain's index paragraphs and this packet.

## Verification readings (VER-TCM-002)

- `python -m unittest tests.test_diagnostic_code_index`: 11 tests OK.
- Progressive-documentation, public-onboarding and CI-pipeline suites
  (the notes-index link test and the `repository_tools` import-barrier
  test among them): 62 tests OK.
- Full Windows suite, `python scripts/run_tests.py` (8 workers): 1209
  tests, zero failures, 1 error, 26 skips. The error is the known baseline
  `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`
  (`PermissionError` deleting a temporary `.git` object), reproduced alone
  on this tree and present on `origin/main` before this work; the skips
  are the Windows-only guards. The baseline before this work was 1206
  tests; the three new tests account for the difference.
- Two regenerations byte-identical; `--check` reports a match on the
  committed page; `unregistered_families` on the repository is empty.
- Known codes indexed, now including `E-DCM-001` and `W-DCM-001`;
  `WO-ECP-010`, `SPEC-ECP-006`, `ECP-DLG-001` and `SHA256` absent.
- Released 0.14.0 evaluator: `validate .` 1277 artifacts, 0 errors, 69
  warnings (the pre-existing maintenance-plane `W014`/`W015` set),
  0 advisories; `doctor .` 0 FAIL; `preflight . --work-order WO-TCM-004`
  PASS, phase start; `python -m se_harness --help` exit 0;
  `python scripts/validate_release_distributions.py --root .` PASS (11
  distribution-bearing records); `git diff --check` clean.
- The handoff check over the Git-derived change set (`--from-git
  origin/main`) is retained beside this file as `handoff.json`: the six
  changed paths are inside `[execution_scope].paths`; every `QG-G4`
  predicate passes.

## Material non-effects

No diagnostic code, message or emitting module changed. No hash-locked
root file changed (`git diff --stat origin/main -- scripts/
docs/engineering/*.md docs/engineering/templates/ ENGINEERING_HARNESS.md
.engineering-harness.toml .github/ AGENTS.md CLAUDE.md` is empty); the
root `scripts/` copies are not scanned. `SPEC-TCM-002` and `VER-TCM-002`
are unchanged. No other note changed.

## Disclosures for the assurance decision

1. The `E-DCM` and `W-DCM` rows show the bare code as their message text.
   The candidate validator composes those messages apart from the code
   literal, so the string-literal scanner (`TCM-DCI-001`) has nothing
   longer to show; changing the emitting module is out of this scope.
2. The guard covers the hyphenated families under the roots `E`, `W` and
   `WEX`. A wholly new single-root prefix (the shape of `MG`, `RID`,
   `JNL`) is still invisible until registered; review remains the control
   for that shape, as `VER-TCM-002` records.
3. Windows figures only. The Linux reading is the pull request's managed
   `validate` check on the head commit; the delegated completion cites it.

## Hosted lanes

Recorded on the pull request (#332) when green at the completion head.
