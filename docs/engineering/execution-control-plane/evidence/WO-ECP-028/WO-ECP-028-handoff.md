```toml
artifact = "WO-ECP-028"
checkpoint = "handoff"
formal_snapshot_sha256 = "58e067dcbee61a1a0742ad8cbf83e1b4f433ad59e5f6dd2b08a3ea585cee5d33"
rebound_at = "2026-09-07T21:45:00Z"
```

# WO-ECP-028 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The dead symbols of section 1 of the code health assessment are gone from
the package and the engine: `_finding_key`, `_status` and the
`closing_ending` local in `workflow.py`; `focus_schema2`,
`_DEFINITION_TYPES`, the write-only `CheckpointContext.report` field and
the unused `workflow_contract` unpacking in `workflow_compliance.py`;
`ensure_validated` in `workflow_procedures.py`; five unused constants in
`decisions.py`; `assert_runtime_identity` and the unreachable `except` in
`runtime_identity.py`; `InterpreterSafetyError`, `OUTCOMES` and
`EVALUATION_ORDER` in `interpreter_safety.py`; `_catalog_lookup` and its
branch in `release_unit.py` (the `lookup` parameter is now required); the
unreachable `raise` and the unused `_domain_token` parameter in
`artifact_layout.py`; the unused `lock` parameter of
`integrity.compare_lock_entry` at its five call sites and the always-true
conditional around the schema-3 checks; `write_acceptance_manifest` in
`candidate_acceptance.py`; `compute_impact` and the dashboard's
`--artifact-root` flag; `ALLOWED_STATUSES`, the `risk_acceptance` type, the
validator's `--artifact-root` flag, an unused local and three loop variables
that shadowed the `field` import. `pyflakes` reports nothing on production
code or tests, and the invalid escape in `tests/test_artifact_authoring.py`
is a raw string. Eight orphan fixtures, the `MANIFEST.in` `*.yaml` line and
its pin, `[tool.unittest]`, the vacuous `SE_HARNESS_AGENT_HOST` test and
its fixture key, three self-referential `len()` pins and the `41` file-count
pin are gone; `unittest.main()` ends `tests/test_public_onboarding.py`.
Nine unconsumed workflow outputs are gone and `candidate-package` reads the
`candidate_version` output instead of re-deriving it.

Two clauses of `SPEC-ECP-022` were withdrawn by amendment on the owner's
selection of 2026-09-07 (`WO-ECP-028` scope amendment of the same date):
`ECP-DEL-002`, because `render_operating_card` and its test are the managed
operating card's generator and its only check against the contracts (the
packet's "never generated" claim was wrong); and the inspector clause of
`ECP-DEL-006`, because `build_inspection` defaults `validation_report` to
`None` and seven tests exercise that path. `docs/notes/diagnostic-codes.md`
joined the scope and is regenerated: one `WEX-ECP-013` sample fewer.

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0160`), `-I`, wheel-installed, for every
  governing reading, this packet and the handoff check.
- Candidate: this checkout, branch `wo/ecp-028-cleanup` off `main` at
  `34193ca` (the merge of PR #390, group B).

## Readings (VER-ECP-024, group A)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.16.0 | Errors: 0, Warnings: 73 (the `main` baseline), Advisories: 0 |
| `doctor` | exact 0.16.0 | 0 FAIL |
| review preflight `--work-order WO-ECP-028` | exact 0.16.0 | PASS |
| `pyflakes se_harness scripts repository_tools tests` before | candidate | 14 findings in production code, 21 in tests |
| `pyflakes se_harness scripts repository_tools tests` after | candidate | nothing (`ECP-DEL-001`, `-007`) |
| `vulture --min-confidence 60` before, the work order's list | candidate | 17 of the listed symbols reported |
| `vulture --min-confidence 60` after | candidate | none of the listed symbols; `render_operating_card` and `OPERATING_CARD_PATH` kept by the withdrawal of `ECP-DEL-002`; the test-only chains kept for #377 |
| `python -m repository_tools.diagnostic_code_index --check` | candidate | the committed page equals the regeneration |
| `python -m unittest` over the nineteen affected modules | candidate, Windows 11 | 571 tests, the one known baseline error, 0 failures after the two withdrawals |
| `python scripts/run_tests.py` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 34193ca` | exact 0.16.0 | section below |

### The Windows suite

`python scripts/run_tests.py` on this Windows 11 workstation (CPython 3.14,
CRLF checkout), two readings:

- Before the two withdrawals: 1,281 tests, 26 skipped, 1 error and 3
  failures. Two failures were the diagnostic-code index tests: deleting
  `render_operating_card` retired `WEX-ADS-003` and the unreachable
  `artifact_layout` raise carried a `WEX-ECP-013` sample, and the page was
  outside the declared scope. The `test_inspection` module had failed in a
  targeted run because `build_inspection` reaches the inspector fallback.
- After the owner's selection of 2026-09-07 (scope widened by the page;
  `ECP-DEL-002` and the inspector clause withdrawn): 1,281 tests, 26
  skipped, 1 error and 1 failure, both the names of this machine's baseline
  on `main`
  (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  a `PermissionError` on a temporary `.git` object;
  `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`,
  the `AGENTS.md` owner region measured on a CRLF checkout, recorded on a
  fresh worktree of `main` under `WO-ECP-027`). Five tests fewer than
  `main`: the vacuous environment test, and four fixture-dependent pins
  folded into their neighbours. No other name differs.

### Handoff check

`check . --artifact WO-ECP-028 --checkpoint handoff --from-git 34193ca`,
exact 0.16.0: Completed; every `QGP-G4I-*` predicate passes; every changed
path inside the declared scope as amended; `complete: true`; the
self-binding result retained as `handoff.json` beside this packet.

## Material non-effects

No managed path moved; `RuntimeIdentity`'s fields, `CONTRACT_SHA256` and
`AcceptanceManifest` are unchanged; the `hash_bound` declared-digest chain,
`POLICY_PATHS`, `TRANSITIONS`, `RETIRED_CHECK_CODES`, the `evaluator_facts`
aliases and the `interpreter_safety` test-only helpers stay as the work
order states; groups B and C are untouched.

## Hosted lanes

Read on the pull request at the completion decision; recorded in the
completion event's reason.
