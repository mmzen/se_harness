```toml
artifact = "WO-ECP-031"
checkpoint = "handoff"
formal_snapshot_sha256 = "93c37f1ab2a7da6de9849692cedab9315f8bd671708c0e839fccf1d0135b5eca"
rebound_at = "2026-09-08T10:30:08Z"
```

# WO-ECP-031 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The package launches every subprocess through `se_harness/_process.py` and
reads every front matter through `se_harness/front_matter.py`. Eleven
modules lost their private Git launcher, ten sites lost their private
delimiter search, and each caller kept its exception class and its
timeout. Where a copy was wrong the primitive is right: the delegation
gate's split is line-anchored, a CRLF checkout parses, and no launch decodes
with the locale. `repository_tools` keeps its own copies behind the import
barrier, by `DEC-ECP-001`.

## Evaluators

- Governor: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel `a969d6ab…`, the digest
  `RLS-SEH-025` binds), `-I`, for every reading, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/ecp-031-process-front-matter` off
  `main` at `50f9cda5`; the code commit is `91977392`.
- Duplication scan: `pylint 4.0.8` in a scratch environment outside the
  checkout (`C:/Users/hok/se-harness-scan`), `--enable=duplicate-code
  --min-similarity-lines=8`, over `se_harness` and `repository_tools`, on a
  detached worktree of `main` and on this branch.

## Rule-to-case map

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `ECP-PRM-001` | `_process.run`, `_process.run_git`: `stdin=DEVNULL` unless input is given, `capture_output`, `timeout`, an 8 MiB cap per stream, UTF-8 decoding through `_process.text` | `tests/test_process_primitives.py` `LauncherTests` |
| `ECP-PRM-002` | `run` catches `TimeoutExpired`, `OSError` and `SubprocessError` and raises `error(message)` naming the command; every caller passes its class or a factory building its coded refusal | `test_a_start_failure_and_a_timeout_are_the_callers_error`; `tests/test_delegation_class.py` `GateGitLauncherTests` (`WEX-ECP-040`) |
| `ECP-PRM-003` | `artifact_layout`, `gate_source`, `hash_bound`, `preflight`, `provenance`, `release_qualification`, `release_unit`, `workflow_compliance` (two) launch Git through `run_git`; `cli._launch_engine` and `candidate_acceptance` (two) launch through `run`; timeouts kept: 120, 60, 60, 60, 30, 180, 120, 120, 60, 1800, 120, 120 | `test_no_module_of_the_package_or_the_tools_launches_git_directly`; `tests/test_cli_shape.py` timeout inspection |
| `ECP-PRM-004` | `front_matter.front_matter_lines`, `parse`, `read`, `read_or_none`, `partition`, `split_document`: `utf-8-sig`, `splitlines` over CR, CRLF and LF, delimiter equal to `+++` at line start | `FrontMatterTests` (five line-ending and BOM forms, an inline `+++`, an unterminated and an invalid document) |
| `ECP-PRM-005` | `artifact_layout._existing_artifact_path`, `gate_source.class_at_base`, `hash_bound._front_matter`, `provenance._decision_metadata` and `_load_metadata`, `release_qualification._front_matter`, `workflow._split_document`, `workflow_compliance.authoring_ready` call the parser | `test_no_module_of_the_package_or_the_tools_splits_front_matter_itself`; `test_split_document_keeps_the_body_newlines_and_the_bom_for_the_write_back` |
| `ECP-PRM-018`, `-024`, `-025`, `-028` (bound on every group) | no code text or digest moved: the diagnostic-code page equals its regeneration; no contract JSON, template, recipe or lock byte changed; suite at baseline | `tests/test_diagnostic_code_index.py` OK; `git diff --stat main` names no contract, template, recipe or lock; the suite reading below |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| direct `subprocess` launches in the package | grep, `main` vs branch | 17 on `main` (in eleven modules); 1 on the branch, in `_process.py` |
| front-matter delimiter searches in the package | grep, `main` vs branch | 10 on `main`; 0 on the branch outside `front_matter.py` |
| `validate --advisories` | exact 0.16.0 | 1,396 artifacts, 0 errors, 73 warnings (the pre-existing maintenance set), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| `preflight --work-order WO-ECP-031 --phase review` | exact 0.16.0 | PASS |
| `check --checkpoint handoff --from-git 50f9cda5` | exact 0.16.0 | Completed; all nine `QGP-G4I-*` predicates pass; 22 changed paths, every one inside the amended scope; `complete: true`; the schema-2 result is retained beside this packet as `handoff.json` |
| `tests/test_diagnostic_code_index.py` | candidate | 11 tests OK; the committed page matches the source |
| `pylint --enable=duplicate-code --min-similarity-lines=8` | scratch environment, `main` worktree vs branch | 6 blocks and 6 blocks; see the disclosure |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | 1,294 tests, 1 error, 26 skipped, the baseline |

### The Windows suite

`PYTHONUTF8=1 python scripts/run_tests.py --scale full` on a detached worktree
of this branch's head, Windows 11, CPython 3.13.3, 8 workers: 1,294 tests,
1 error, 26 skipped. The error is the workstation baseline name every
reading of this cycle carries
(`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
a `PermissionError` on a read-only temporary Git object during teardown);
the 26 skips are the Windows-only guards. The count grew by the twelve
boundary tests of `tests/test_process_primitives.py`; the failure set
equals the control's (`main` at `50f9cda5`, 1,282 tests, the same one
error, the same skips). The Linux lane of PR #398 reports the suite green.

## Behaviour changes, each where a copy was wrong

- `gate_source.class_at_base` split the base copy on the first `+++`
  anywhere, so a work order whose body carried the three characters read
  its class from the wrong text; it now reads the front matter only.
- `artifact_layout._existing_artifact_path` and
  `workflow_compliance.authoring_ready` matched only `+++\n`, so a CRLF
  checkout reported "no existing artifact" and read the whole document as
  prose; both now read the normalized form.
- `gate_source._git`, `candidate_acceptance._run` and `preflight` decoded
  with the locale (`text=True`); every launch now decodes UTF-8 with
  replacement.
- `candidate_acceptance`'s scenario launch let an `OSError` or a timeout
  propagate raw; it is now a `HarnessError` naming the scenario.
- `cli._launch_engine` let an `OSError` propagate raw; it is now a
  `HarnessError` naming the script, and its timeout refusal names the script
  and the bound as before.

## Disclosures

1. `SPEC-ECP-023` assumed `repository_tools` imports the package. The
   import barrier of `ARCH-REB-013` and `SPEC-REB-015` rule 2 forbids it and
   `tests/test_interpreter_safety.py` and `tests/test_ci_pipeline.py` refuse
   it. The four tool edits were applied, refused, and withdrawn;
   `DEC-ECP-001` records the deviation, the technical owner disposed it
   `amend`, and `SPEC-ECP-023` carries the amendment record. The two
   inventory tests of this group read the package only.
2. The duplication scan reads 6 blocks on `main`, not the assessment's
   seven: wave 1 removed one. None of the six is group A's: three pair an
   engine copy with a package copy (the layout registry, the standing
   deviations, the body parser) and belong to wave 3 (#378), which the
   specification's Scope defers; three belong to groups B and C (the atomic
   writer in `artifact_layout` and `provenance`, `DEFINITION_TYPES` in
   `workflow` and `workflow_contract`, the restitution fields in
   `workflow_contract` and `workflow_result`). `ECP-PRM-027` as written
   cannot be met by wave 2 for the three engine blocks; group C's completion
   is where that rule is read, and a decision will be raised there unless
   wave 3 lands first.
3. `tests/test_hash_bound_integrity.py` pinned the literal `shell=False` to
   `hash_bound.py`; the launch now lives in `_process.py`, and the test
   reads the launcher and asserts the import.
4. `repository_tools/release_build.py` keeps `_bounded_run`, a launcher that
   streams the producer's output to temporary files and keeps the last 8 KiB
   of each; it is not a Git launch and is the tools' own by
   `DEC-ECP-001`.
