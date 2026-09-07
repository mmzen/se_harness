```toml
artifact = "WO-ECP-027"
checkpoint = "handoff"
formal_snapshot_sha256 = "51586c682da1b56bb092fd81ba89f73d18b4a491ec90a728add62b215a23a465"
rebound_at = "2026-09-07T19:58:00Z"
```

# WO-ECP-027 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

Every failing `harnessctl` path now follows the reference's two rules. One
splitter, `_split_code`, produces the result code in `check`, `evidence`,
`transition`, `decide`, the projection and both record handlers, so no line
carries a code twice; the live `WEX210: WEX210: unknown artifact ID` on the
checkpoint path is gone. The mutation guard raises `MutationGuardError`, a
`HarnessError` subclass, and the four writing handlers re-raise it by type,
so `transition` exits 2 on a guard refusal as its siblings do; `transition`
parses `--set`, `--decision` and `--reason` before any result exists, so a
syntax error is a usage refusal. Every result-building handler converts the
tuple `check` converts, and `main()` also catches `ProcedureError`, so no
traceback remains reachable for those classes. `dashboard --json` passes an
engine refusal through as exit 2 with the engine's last standard-error line
and carries the engine's standard error in `error` on a failed result.
`pr-body` renders an unknown artifact as a failed command result, exit 1.
`gate_source._git` (60 s), the four engine launches (1,800 s) and
`upgrade_rehearsal.run` (600 s) are bounded, and a source-scan test keeps
every `subprocess` call in `se_harness/` and `repository_tools/` bounded.
`REF_ARTIFACT_PATTERN` is built from `_REF_PREFIX`, so id allocation sees
`OPS-*` and `DEC-*` files on other refs; `evaluator_facts._front_matter`
reads CRLF and BOM front matter; the Explorer projects an array
`verification_method` as a joined string; `pages-publication.yml` reads
`bundle_manifest_sha256` where it read a never-emitted output; `publish-pypi.
yml` selects Python in the `github_release` and `observe` jobs. Two reference
rows and two amendment records on `SPEC-ECP-016` record the rules. No
registered command, option, result schema, contract file or managed template
changed.

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/mathi/se-harness-eval-0160`), `-I`, wheel-installed, for every
  governing reading, this packet and the handoff check.
- Candidate: this checkout, branch `wo/ecp-027-wave0-correctness` off `main`
  at `1fa0610` (the merge of the approved packet, PR #382); implementation
  commits `ce63a54` and `83df2f4`.

## Readings (VER-ECP-023)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate --advisories` | exact 0.16.0 | Errors: 0, Warnings: 73 (the `main` baseline), Advisories: 0 |
| `doctor` | exact 0.16.0 | 97 PASS, 0 FAIL |
| review preflight `--work-order WO-ECP-027` | exact 0.16.0 | PASS |
| `scripts/validate_release_distributions.py` | candidate | PASS, 13 distribution-bearing records |
| the eighteen new tests on the code before the change | candidate, Windows 11 | 12 failures, 8 errors, 0 passes: every rule's test fails before its fix (`ECP-COR-021`; list below) |
| the eighteen new tests after the change | candidate, Windows 11 | OK, 18 tests |
| `check . --artifact WO-ZZZ-999 --checkpoint scope --json` | candidate | `blocked_by` is `["WEX210: unknown artifact ID: WO-ZZZ-999"]`, the code once (`ECP-COR-001`) |
| `pr-body . --artifact WO-ZZZ-999` | candidate | one line `WEX-ECP-014: unknown artifact ID: WO-ZZZ-999` on stdout, exit 1 (`ECP-COR-011`, `-012`) |
| `subprocess` inspection | candidate | before: 7 unbounded calls (`cli.py:247,258,301,337`, `gate_source.py:117`, `upgrade_rehearsal.py:80,97`); after: 0 (`ECP-COR-013` to `-015`) |
| `python -m unittest` over the eleven affected modules | candidate, Windows 11 | 427 tests, 7 skipped, the one known baseline error (`test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`, a `PermissionError` on a temporary `.git` object), 0 failures |
| `python scripts/run_tests.py` | candidate, Windows 11 | section below |
| `check --checkpoint handoff --from-git 1fa0610` | exact 0.16.0 | section below |

### The tests, rule by rule

`tests/test_cli_shape.py`: `test_checkpoint_check_prints_each_code_once`
(ECP-COR-001), `test_result_handlers_convert_the_shared_tuple` (-002, -007),
`test_a_mutation_guard_refusal_is_an_environment_refusal` (rewritten to the
typed error, -004), `test_transition_guard_refusal_exits_2` (-005),
`test_transition_option_syntax_error_is_a_refusal` (-006),
`test_main_refuses_a_procedure_error_that_escapes_a_handler` (-008),
`test_dashboard_json_passes_the_engine_refusal_and_error_through` (-009,
-010), `test_pr_body_unknown_artifact_is_a_failed_result` (-011, -012),
`test_an_engine_launch_timeout_is_a_refusal` (-014),
`test_every_subprocess_launch_in_the_package_carries_a_timeout` (-013 to
-015). `tests/test_delegation_class.py` `GateGitLauncherTests` (-013).
`tests/test_upgrade_rehearsal.py` `RunnerTimeoutTests` (-015).
`tests/test_artifact_authoring.py`
`test_allocation_sees_operating_contract_and_decision_ids_on_another_ref`
(-016). `tests/test_ci_pipeline.py` `EvaluatorFactsFrontMatterTests` (-017).
`tests/test_dashboard_webui.py` `RequirementProjectionTests` (-018).
`tests/test_dashboard_publication.py`
`test_snapshot_digest_reads_an_emitted_output` (-019).
`tests/test_pypi_publishing.py` `PublicationJobsInterpreterTests` (-020).
`ECP-COR-003` is the unchanged `CODE_PREFIX`, pinned by the existing
projection test.

### The Windows suite

`python scripts/run_tests.py` on this Windows 11 workstation (CPython 3.14,
CRLF checkout), three readings:

- At the implementation commit `ce63a54`: 1,282 tests, 26 skipped, 1 error,
  3 failures. The error is the known Windows baseline name
  (`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
  a `PermissionError` on a temporary `.git` object). One failure,
  `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`,
  fails identically on a fresh worktree of `main` at `1fa0610` on this
  machine: the owner region of `AGENTS.md` measures over its bound only on a
  CRLF checkout, and the Linux lane measures LF bytes. The two remaining
  failures were this work order's: `tests/test_diagnostic_code_index.py`
  found that a bare `WEX-ECP-014` literal in `pr-body` moved one row of the
  regenerated code index, a page outside the declared scope.
- The `pr-body` failure now names its code through `_split_code`
  (`83df2f4`), as every other result path does, so the index page is
  unchanged; `tests.test_diagnostic_code_index` and `tests.test_cli_shape`
  pass (33 tests).
- At `83df2f4`: 1,282 tests, 26 skipped, 1 error and 1 failure, both the
  baseline names above; no other name differs from `main`.

### Handoff check

`check . --artifact WO-ECP-027 --checkpoint handoff --from-git 1fa0610`,
exact 0.16.0: Completed; every `QGP-G4I-*` predicate passes; every changed
path inside the declared scope; `complete: true`; the self-binding result
retained as `handoff.json` beside this packet.

## Material non-effects

`CODE_PREFIX` recognizes the same code families; the result schemas are
unchanged in shape (`dashboard --json` gains the optional `error` member on
a failed result, `pr-body --json` uses the failed form `init` and `upgrade`
already use). The `renumber-artifacts` output stays as it is (#376 removes
the command); the diagnostic-code registry and the single Git launcher are
#377. No managed path, contract file, skill or workflow template changed.

## Hosted lanes

Read on the pull request at the completion decision; recorded in the
completion event's reason.
