```toml
artifact = "WO-TST-004"
checkpoint = "handoff"
formal_snapshot_sha256 = "341d8fc31fb22d809b71fd5083bc2273984ed5147ef560004345423d88affc06"
rebound_at = "2026-09-08T15:10:44Z"
```

# WO-TST-004 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

Every defined test in `tests/` is discovered exactly once. The six base
classes that carried tests and were subclassed (`WorkflowExecutionTests`,
`WorkflowComplianceTests`, `GitDerivedChangeSetTests`,
`ScopeCheckpointTests`, `DecisionManagementTests`,
`ArtifactAuthoringPolicyTests`) are split into a test-free fixture mixin and
a test class, so 262 inherited re-runs are gone and the loader reads 1,054
discovered for 1,054 defined. Five support modules replace the copied
helpers: `tests/cli_support.py` (`invoke`, `SystemExit`-safe),
`tests/git_support.py` (`run_git`, `git`, `init_repository`, identity by
environment, signing off), `tests/artifact_support.py` (`write`, `formal`,
the chain builders and the evaluator-evidence constants that
`test_revision_provenance.py` used to lend to thirteen modules),
`patch_mutation_authority` in `tests/mutation_guard_support.py` and
`load_module` / `load_evaluator_module` in `tests/root_identity_support.py`.
`tests/test_retired_surface.py` is the one table of tombstones;
`tests/test_suite_hygiene.py` pins the suite's shape from the loaded modules.
The un-cited prose pins on the notes became structural checks (a heading
exists, a named command parses, a link and its anchor resolve); the two
handoff-wording tests name `SPEC-WEX-003` and `SPEC-IAR-011`. The managed
count per root derives from `template_files()` and the lock. Fixtures take
the cached standard repository under one default name. The
`candidate-evidence` suite step restores `target/test-timings.json` from the
previous run through `actions/cache` and passes it to the runner. No product
module, managed path or runner file changed.

## Evaluators

- Governing: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel-installed, `-I`) for
  `validate`, `doctor`, the review preflight, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/tst-004-test-suite-hygiene` off
  `main` at `13a70218` (the merge of PR #401), with `main` at `4dc59d0a`
  (wave 2: `WO-ECP-031`, `WO-ECP-032`, `WO-ECP-033`) merged in on
  2026-09-08.

## Readings (VER-TST-002)

Readings are counted by `readings.py` (a scratch script kept outside the
repository) over `tests/`, on a worktree of `main` at `13a70218` and on the
candidate. The loader readings import every module under its `tests.` name
and count `test` methods in each class's own namespace.

| Reading | `main` at `13a70218` | candidate |
| --- | ---: | ---: |
| test modules / support modules | 55 / 4 | 60 / 7 |
| discovered / defined (loader) | 1,282 / 1,020 | 1,054 / 1,054 |
| classes inheriting tests from a test-carrying base | 17 | 0 |
| `def invoke` | 22 | 1 (`cli_support`) |
| `def git`, `def _git`, `def run_git` | 12 + 1 | 1 + 1 (`git_support`) |
| `def write` / `def formal` | 9 / 5 | 1 / 1 (`artifact_support`) |
| direct `subprocess.run(["git", ...])` launches in tests | 66 | 0 |
| mutation-authority patch blocks | 20 | 0 |
| `spec_from_file_location` in test modules | 17 | 0 |
| test modules inserting into `sys.path` at import | 13 | 0 |
| test modules importing another test module | 15 | 0 |
| tests reading another test's source | 1 | 0 |
| `assertNotIn(..., source or text)` sites | 54 | 16 (the tombstone table's own loops, the `localStorage` and `shell=True` invariants, `CATALOG_BEGIN`) |
| `assertFalse(...exists())` sites | 10 | 9 (behavioural: a refused command wrote nothing) |
| `assertRaises(SystemExit)` around the command line | 8 | 2 (`parse_args` on the parser object, not the command line) |
| `standard_repository` calls passing a name | 23 | 4 (three assert on the cache by name, one on the seeded glossary title) |
| direct `init` calls in tests | 42 | 34 (`init`'s own tests, the boundary and subprocess installs) |

| Governing reading | Evaluator / platform | Result |
| --- | --- | --- |
| `validate` | exact 0.16.0 | PASS: 0 errors, 73 warnings (the `main` baseline), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| review preflight `--work-order WO-TST-004` | exact 0.16.0 | PASS |
| `python -m unittest tests.test_operating_contract_readiness` (alone) | candidate, Windows 11 | OK; on `main` it errors at import (`No module named 'validate_engineering_artifacts'`), as do `test_validation_taxonomy`, `test_work_order_assurance` and `test_inspection` |
| `python scripts/run_tests.py` | candidate, Windows 11 | section below |
| `python -m unittest discover -s tests -p "test_*.py"` | candidate, Windows 11 | section below |
| hosted `candidate-source` suite step | Linux lane | section below |

### The Windows suite

`python scripts/run_tests.py` (8 workers) on this Windows 11 workstation
(CPython 3.13, LF checkout):

| Tree | Tests | Wall | Failure set |
| --- | ---: | ---: | --- |
| `main` at `50f9cda5`, before this work order | 1,282 | 409 s | `test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound` (the `AGENTS.md` owner region, 6,024 bytes against 6,000), `test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref` (a `PermissionError` on a temporary `.git` object) |
| candidate after the wave 2 merge | 1,054 (22 skipped) | 369 s | the same two names; both predate this work order and are this machine's baseline on `main` (recorded under `WO-ECP-027`) |

`python -m unittest discover -s tests -p "test_*.py"` (the canonical serial
reference) on the candidate: 961 s (this workstation is slower than the one the earlier sections measured), the same failure set.

### The hosted lane

| Run | Suite step | Wall |
| --- | --- | ---: |
| `main` at `4dc59d0a`, run 34238078845, `--timings ""` | Run complete candidate-source regression | 51 s |
| candidate, PR #402 | Run complete candidate-source regression | 45 s (run 34242510375, 15:05:46 to 15:06:31; the first run finds no cached timings and seeds the cache for the next) |

## Rule by rule (SPEC-TST-002)

| Rule | How it is met |
| --- | --- |
| TST-HYG-001 | the six bases are `*Fixture` mixins without tests; `test_suite_hygiene` walks every class's MRO |
| TST-HYG-002 | `test_every_defined_test_is_discovered_exactly_once` compares own methods to loaded names, class by class |
| TST-HYG-003 | `artifact_support.py` holds the chain builders and the evidence constants; no `from tests.test_...` import remains |
| TST-HYG-004 | `cli_support.invoke`; 20 methods and one function deleted; the eight `SystemExit` sites on `main([...])` read the exit code |
| TST-HYG-005 | `git_support.run_git`, `git`, `init_repository`; 12 helpers and 66 direct launches converted, `binary=True` where bytes are compared |
| TST-HYG-006 | one `write` (text normalised to one newline, bytes exact), one `formal` with the `complete` form for the architecture fixtures |
| TST-HYG-007 | `patch_mutation_authority(self)` in 20 `setUp`s |
| TST-HYG-008 | `load_evaluator_module` loads the engine in dependency order under bare names; `load_module` the lane and repository scripts; 13 inserts removed |
| TST-HYG-009 | `test_retired_surface.py`: 17 paths, 21 files with phrases, 8 scans with permitted holders, the import scan, the validator names, the template inventory, the fresh install, the help and the refused commands |
| TST-HYG-010 | `test_run_tests` no longer reads `test_workflow_execution.py`; `scale_sizes` lives in `fixture_support` |
| TST-HYG-011 | every product-source read names its rule (`SPEC-HBI-001` rules 3, 5, 8, 13, 14; `SPEC-REB-013` rules 4 to 8; `ECP-TMB-001` to `-003`; `SPEC-ECP-023` rules already cited) |
| TST-HYG-012 | the two handoff-wording tests cite `SPEC-WEX-003` (`REQ-WEX-011`) and `SPEC-IAR-011` |
| TST-HYG-013 | six pin tests replaced by structural checks in `test_progressive_documentation` and `test_public_onboarding` |
| TST-HYG-014 | `test_required_documents_have_exact_expertise_labels` (`SPEC-DST-006`), the README budget (`SPEC-DST-024`) and `test_check_note_is_indexed_linked_and_names_only_contract_identifiers` (`SPEC-DST-007`) stay |
| TST-HYG-015 | `test_owner_region_identifies_every_managed_path_from_the_lock`: every lock-managed path is a managed candidate template, none pinned as a count |
| TST-HYG-016 | the one remaining self-length assertion removed |
| TST-HYG-017 | already true on `main`: every module's `unittest.main()` sits in a final guard (the mid-file call the assessment saw at `test_public_onboarding.py:221` was gone before this work order) |
| TST-HYG-018 | `standard_repository(destination, project_name="Fixture")`; seven fixtures that called `init` only for a fresh repository now copy the cache |
| TST-HYG-019 | `actions/cache@v4.2.3` (pinned by commit) restores `target/test-timings.json`; the step passes `--timings target/test-timings.json`; `target/` is ignored |
| TST-HYG-020 | the failure set equals the Windows baseline; the Linux-lane wall is in the table above |

## Disclosures

1. One direct `main([...])` stays in `tests/test_workflow_execution.py`
   (`PullRequestBodyTests.body`): `pr-body` writes bytes to
   `sys.stdout.buffer`, which `invoke`'s text capture cannot observe. The
   five other `main([` calls are the runner's, the inspector's and the code
   index's own entry points, not `harnessctl`. Three `assertRaises(SystemExit)`
   sites call `build_parser().parse_args` on the parser object.
2. `formal` merges two lineages behind one keyword: the minimal form is the
   provenance fixture (dates `2026-08-11`; the operating-contract and
   validation-taxonomy copies carried `08-16` and `08-15`, asserted by no
   test), the `complete` form the architecture fixture. The two architecture
   modules alias `complete_formal = functools.partial(formal, complete=True)`.
3. `load_module` generalises `load_evaluator_module` to the lane and
   repository scripts. `test_dashboard_webui` loads the candidate engine under
   its bare names; its alias-and-restore dance existed for roots that managed
   script copies, which the 0.16.0 root does not. `test_run_tests` puts
   `scripts/` on `sys.path` only while a test runs workers, because spawned
   workers import the runner by name. `publish_release.py` extends
   `sys.path` with `.github/scripts` at import; the hygiene test forbids only
   the engine and `scripts/` directories.
4. The tombstone table reads the retired context path and labels from the
   released 0.5.0 baseline fixture; the candidate-validator names check keeps
   the candidate side only (no root copy since 0.16.0). The
   `test_predecessor_bootstrap_retirement` tests that compare the 0.7.1 root
   copy stay where they are.
5. Wave 2's merge brought three new modules. `test_codes_and_contract_tables`
   inserted the repository root into `sys.path` at import; that line is
   removed (the root is on the path in every supported way of running the
   suite). The retired-code holders row admits `se_harness/codes.py`, as
   main's version of the moved test did.
6. `test_active_public_command_contract_uses_six_commands` pins wording of
   formal artifacts (`REQ-DST-025`, `SPEC-DST-007`, `VER-DST-007`), which
   TST-HYG-012 does not cover; it stays.
7. Windows wall times are noisy (other runs shared the machine during some
   readings); the Linux-lane reading is the one the requirement measures.
