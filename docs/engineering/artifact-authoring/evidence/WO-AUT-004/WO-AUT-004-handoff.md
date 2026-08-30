```toml
artifact = "WO-AUT-004"
checkpoint = "handoff"
formal_snapshot_sha256 = "76dbc1d4da4b7adb2bb98e9ce9e3ff1e8d4dfd94eed4ede80c20befcf5c1b148"
rebound_at = "2026-08-30T10:02:05Z"
```

# WO-AUT-004 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The validator report carries a third class, *advisory*, and the `W-AUT-*`
family lives there: raised only while a requirement is `draft`, counted
and listed apart from errors and warnings, shown with `--advisories`,
always present in the JSON. `harnessctl validate` passes the flag through.
`inspect`, `check`, `preflight` and `doctor` are unchanged and no longer
see the family, because it is no longer in `warnings`. `REQ-AUT-002` and
`SPEC-AUT-001` carry amendment records saying the four codes are
advisories (`REQ-AUT-007`; `AUT-ADV-001` to `AUT-ADV-007`).

## Evaluators

- Governing: released `se-harness 0.11.0` outside the checkout, `-I`, on
  this Windows checkout for every reading, the packet and the handoff check
  included. Its validator is the 0.11.0 root copy and still reports the
  family as warnings.
- Candidate: this checkout, branch `wo/aut-004-advisories` off `main` at
  `d42ab2f`, with `main` at `2f91797` (pull requests #290 and #291, notes
  only) merged in without conflict; the suite and the demonstration run the
  candidate template script.

## Change

- `templates/repository/standard/scripts/validate_engineering_artifacts.py`:
  `validate_authoring` returns `(errors, warnings, advisories)` and runs the
  four checks only when `artifact.status == "draft"`; `ValidationReport`
  gains `advisories` (default empty, so every existing constructor call
  stands); `to_dict` adds `advisories` and `advisory_count`;
  `render_human(report, show_advisories=False)` prints the fourth number
  and, on request, an `Advisories:` section in the warning format;
  `--advisories` on the script. 46 lines net, 22 opcodes against the
  0.11.0 root copy, declared in the ledger.
- `templates/repository/standard/scripts/inspect_engineering_artifacts.py`:
  unchanged; it reads `errors` and `warnings` from the report object.
- `se_harness/cli.py`: `validate --advisories`.
- Tests: `tests/test_artifact_authoring_policy.py` (the helper returns
  three lists; the shape, vocabulary and attribute tests assert advisories
  on a draft and no `W-AUT` warning; two new tests: draft-only, and the
  summary/listing/JSON/CLI rendering); `tests/test_predecessor_bootstrap_retirement.py`
  (an opcode ledger, `AUT004_CANDIDATE_VALIDATOR_EDITS`, and the
  `_assert_root_plus_declared_edits` helper). `tests/test_validation_taxonomy.py`,
  `tests/test_inspection.py` and `tests/test_harnessctl.py` needed no change
  and pass.
- Notes: `harnessctl-reference.md` (synopsis and one paragraph),
  `harnessctl-check.md` (one sentence).
- Amendment records on `REQ-AUT-002` and `SPEC-AUT-001`; the domain index.

## Tests

- A draft requirement with an unknown opener, two `SHALL`s, 301 characters
  and a free-text `verification_method`: four advisories, no `W-AUT`
  warning; the same requirement `approved`: no advisory.
- The five clean shapes on a draft: no advisory (except the pre-existing
  `W-AUT-004` when the fixture's vocabulary is a string).
- Rendering: `Artifacts | Errors | Warnings | Advisories` in the summary;
  the `Advisories:` section only with `show_advisories`; `Planes:`
  unchanged; JSON `advisory_count` and `advisories` present,
  `warning_count` equal to the sum of the plane warning counts.
- CLI: `harnessctl validate` without the flag prints the summary and no
  section; with `--advisories` the section and `[W-AUT-002]`; `--json`
  carries the count.
- Ledger: the candidate validator equals the 0.11.0 root copy plus the
  `WO-ECP-018` insertions plus the 22 declared opcodes.

## Suite readings

Windows workstation, candidate source, `scripts/run_tests.py`: 1152 tests, 1 error, 26 skipped, the error being the baseline `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref` that precedes this work order; the six suites this work order touches or pins (artifact authoring policy, validation taxonomy, inspection, harnessctl, predecessor bootstrap retirement, progressive documentation): 94 tests, OK, 1 skipped. Linux: the pull request's lanes at the completion commit.

## Demonstration on this repository

- Candidate template script over this tree: `Artifacts: 1172 | Errors: 0
  | Warnings: 69 | Advisories: 0`; `Planes: … maintenance E0/W69`; the 69
  are `W013` (34), `W015` (15), `W014` (14), `W024` (6). `--advisories`
  lists nothing, because every requirement is past `draft`. `--json`:
  `warning_count 69`, `advisory_count 0`. `inspect .` reads the same
  warning count.
- Released 0.11.0 evaluator over the same tree: `Artifacts: 1172 | Errors:
  0 | Warnings: 485` — the root validator copy predates this change, as
  `VER-AUT-002` states.

## Readings under the 0.11.0 root

- `validate .`: 1172 artifacts, 0 errors, 485 warnings.
- `doctor .`: 0 FAIL.
- `validate_release_distributions.py`: PASS (8 records).
- Start preflight for `WO-AUT-004`: PASS with no diagnostics over `c17d2cc`.

## Scope amendment and its evidence

At the first packet head `6cff19b` the two governance-migration lanes read
`successor-validate-after: no validation summary was printed`:
`repository_tools/upgrade_rehearsal.py` matched the summary line with an
expression anchored at its end. On the owner's decision of 2026-08-30 the
scope was amended with that file and `tests/test_upgrade_rehearsal.py`;
the expression accepts an optional `| Advisories: N` tail and the test's
fake successor prints the four-number form (one new test). No other
consumer of the summary line exists in the repository.

## Deviations, recorded for the completion decision

None beyond the scope amendment above. The inspect script, admitted to the
scope in case the report renamed a key, needed no edit.

## Complete changed-path set

Every path this work order changed since `main` at `2f91797`, packet
included, as Git derived it; the handoff check completed at its fixed point
with every predicate of `QG-G4-IMPLEMENTATION-EVIDENCE` passing, run by
the released 0.11.0 evaluator on this Windows checkout: see `handoff.json`
beside this file.
