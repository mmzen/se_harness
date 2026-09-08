```toml
artifact = "WO-ECP-032"
checkpoint = "handoff"
formal_snapshot_sha256 = "2ab44c6b207ab320635381328f9b38a2b4a37c145c54c0a142eafc1b8d1d8412"
rebound_at = "2026-09-08T11:58:00Z"
```

# WO-ECP-032 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

`integrity.py` is the one home of the digest, canonical-text, JSON,
duplicate-key, staging and atomic-write primitives and of the configuration
reader; the package's private copies are gone and every caller keeps the
bytes it wrote and the refusal it named. The checkpoint and definition-type
sets are defined once in `workflow_contract.py`; the checkpoint, phase,
install-mode and change-action values are typed; both wheel parsers apply
one grammar; one environment builder serves the two qualification runtimes;
the transition planner reads the revision policy once. No recorded digest
moved. `repository_tools` keeps its own copies behind the import barrier
(`DEC-ECP-001`); its recipe serializer is renamed with its bytes unchanged.

## Evaluators

- Governor: released `se-harness 0.16.0` outside the checkout
  (`C:/Users/hok/se-harness-eval-0160`, wheel `a969d6ab…`, the digest
  `RLS-SEH-025` binds), `-I`, for every reading, this packet and the handoff
  check.
- Candidate: this checkout, branch `wo/ecp-032-integrity-primitives`,
  stacked on the group A branch at `3d2bee39`; the code commits are
  `06026f86` (the primitives) and `b72c9652` (two test-time corrections,
  disclosures 5 and 6).
- Duplication scan: `pylint 4.0.8` in a scratch environment outside the
  checkout (`C:/Users/hok/se-harness-scan`), `--enable=duplicate-code
  --min-similarity-lines=8`, over `se_harness` and `repository_tools`.

## Rule-to-case map

| Rule | Where it is met | Evidence |
| --- | --- | --- |
| `ECP-PRM-006` | `integrity.raw_sha256`, `canonical_text`, `canonical_text_bytes`, `canonical_json_bytes`, `pretty_json_bytes`, `unique_object_hook`, `stage_bytes`, `atomic_write_bytes`, `atomic_create_bytes`, `read_toml` | `tests/test_integrity_primitives.py`; `test_no_package_module_hashes_or_serializes_privately`, `test_no_package_module_keeps_a_private_atomic_writer_or_a_tmp_stage` |
| `ECP-PRM-007` | `canonical_json_bytes(value, ensure_ascii=…)` and `pretty_json_bytes(value, ensure_ascii=…)`; the package passes `True` everywhere it did, `cli` passes `False` for the inspection report as before | `SerializerTests`: both forms equal the pre-change bytes |
| `ECP-PRM-008` | `atomic_write_bytes` stages, fsyncs and replaces; `installer._atomic_write` is that function; the three inline writers of `workflow_compliance.py` and the qualification and record writers call the shared ones; `workflow._stage` stages through `stage_bytes` | `AtomicWriterTests`: an interrupted replace leaves the target untouched and no temporary file; `tests/test_workflow_execution.py` rollback and staging cases |
| `ECP-PRM-009` (amended) | `release_build.recipe_json_bytes`, bytes unchanged; `canonical_json_bytes` kept as an alias for the lane script `scripts/replay_release_build.py`, outside this scope | `tests/test_release_build.py`; the hosted rehearsal legs at the head replay the bound recipe of `RLS-SEH-025` |
| `ECP-PRM-010` | seven inlined `\r\n` normalizations call `canonical_text`; a lone `\r` folds the same way everywhere | `test_canonical_text_folds_crlf_and_lone_cr`; grep, 17 sites on `main` to 2 (the two primitives) |
| `ECP-PRM-011` | `integrity.read_toml` (`utf-8-sig`) serves `installer.plan_install`, `mutation_guard._configured_version` and `workflow._revision_policy`; `plan_transition` reads once and passes `policy` to `_validate_edge` and `structural_precondition_results` | `ConfigurationReaderTests`; `tests/test_mutation_guard.py`; `tests/test_workflow_execution.py` |
| `ECP-PRM-012` | `workflow_contract.CHECKPOINT_ORDER`, `CHECKPOINTS`, `EVIDENCE_CHECKPOINTS`, `DEFINITION_TYPES`; `cli.py`, `workflow.py` and `workflow_compliance.py` import them | `ClosedSetTests`: no literal checkpoint or definition-type set outside the contract module |
| `ECP-PRM-013` | `workflow_contract.Checkpoint`, `preflight.Phase`, `installer.InstallMode` and `ChangeAction`; `CheckpointContext.checkpoint`, `run_preflight(phase=…)` and `Change.action` typed | `test_typed_value_sets_exist` |
| `ECP-PRM-014` | `integrity.WHEEL_VERSION_PATTERN` is the pattern both `candidate_acceptance` and `release_qualification` apply | `test_both_wheel_parsers_apply_one_grammar`; the verdict change below |
| `ECP-PRM-015` (amended) | `candidate_acceptance.safe_environment`, an allow-list of ten keys, `PYTHONPATH` removed, `PYTHONNOUSERSITE=1`; `release_qualification._safe_environment` is that function; the acceptance adds its two pip keys | `test_one_environment_builder_denies_pythonpath_and_user_site_for_both_runtimes` |
| `ECP-PRM-024`, `-025`, `-028` | `CONTRACT_SHA256` equal on `main` and the branch (`a443e93d…`); no contract JSON, template, recipe or lock byte changed; the lock bytes, the evaluator-evidence bytes and the payload-manifest bytes are produced by the same `json.dumps` arguments as before | `DigestPreservationTests`; `tests/test_evaluator_identity.py`, `tests/test_hash_bound_integrity.py`; `git diff --stat` names no contract, template, recipe or lock |

## Readings

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| private digest helpers in the package (`hashlib.sha256(`) | grep, `main` vs branch | 24 to 4: `integrity.raw_sha256`, the block-streaming digest of `workflow_compliance`, and the two digests of `interpreter_safety`, kept by `SPEC-REB-015` rule 2 (disclosure 5) |
| canonical serializers (`sort_keys=True`) | grep | 23 to 8: the two primitives and six non-canonical or stdout `json.dumps` calls, named below |
| duplicate-key hook definitions | grep | 7 to 0 outside `integrity.py`; 11 to 7 call sites, each passing the shared hook |
| private temporary-file writers (`mkstemp(`, `os.fsync(`) | grep | 6 to 2, both in `integrity.py` |
| inlined `\r\n` normalizations | grep | 17 to 2, the two primitives |
| `tomllib.loads(` | grep | 12 to 5: `integrity.read_toml`, the front-matter parser, the owner-owned delegation file, and two in-memory TOML parses of already-split front matter |
| `VERSION_PATTERN = re.compile` | grep | 6 to 3: the identity grammar (`integrity`), the wheel grammar (`integrity`), the release-version grammar (`provenance`) |
| literal checkpoint sets | grep | 5 to 2: `CHECKPOINT_ORDER` and its `Checkpoint` type in `workflow_contract.py` |
| `validate --advisories` | exact 0.16.0 | 1,397 artifacts, 0 errors, 73 warnings (the pre-existing maintenance set), 0 advisories |
| `doctor` | exact 0.16.0 | 0 FAIL |
| `preflight --work-order WO-ECP-032 --phase review` | exact 0.16.0 | PASS |
| `check --checkpoint handoff --from-git 3d2bee39` | exact 0.16.0 | Completed; all nine `QGP-G4I-*` predicates pass; 26 changed paths, every one inside the amended scope; `complete: true`; the schema-2 result is retained beside this packet as `handoff.json`. The first run refused `se_harness/preflight.py` on `QGP-G4I-PATHS`; disclosure 7 |
| `CONTRACT_SHA256` | candidate, `main` vs branch | `a443e93d6da7d0538bdf790a16f4dea49ac7a6ede384c65e40362627d7a84b75` both |
| `pylint --enable=duplicate-code --min-similarity-lines=8` | scratch environment | 6 blocks on `main`, 4 on this branch: the atomic-writer block (`artifact_layout` and `provenance`) and the `DEFINITION_TYPES` block (`workflow` and `workflow_contract`) are gone; see the disclosure |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | 1,309 tests, 1 error, 26 skipped: the workstation baseline (`errors=1, skipped=26`), at `b72c9652` in a detached worktree |

### The Windows suite

The one error is the standing Windows baseline,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
whose teardown removes a read-only `.git` tree; it fails the same way on
`main` and on the group A branch. The 26 skips are the platform set (POSIX
modes, hosted-only legs). The run before the two corrections of `b72c9652`
read `failures=1, errors=3`: the barrier test and the two rollback cases of
disclosures 5 and 6, and nothing else.

## Behaviour changes, each where a copy was wrong

- A pre-release wheel such as `0.5.0a1` is now accepted by `qualify
  candidate-package` as it was by `qualify public-install`; the strict
  `X.Y.Z` grammar of the acceptance is gone. No released wheel changes
  verdict: every `se_harness-*.whl` on record is a plain `X.Y.Z`.
- `installer.plan_install` and `mutation_guard._configured_version` read
  `.engineering-harness.toml` through `utf-8-sig`, so a BOM no longer
  fails them; `workflow._revision_policy` already did.
- The three evidence writers of `workflow_compliance.py` fsync before they
  replace and use a randomized sibling name instead of a fixed `.tmp`.
- `workflow_compliance.authoring_ready` folds a lone `\r` like `\r\n`.
- `candidate_acceptance`'s environment removes `PYTHONPATH` instead of
  setting it to the empty string; under `-I` the two were equivalent.

## The `json.dumps` calls that stay

`candidate_acceptance.py:40` (`CONTRACT_SHA256`, default separators, the
recorded digest depends on them) and `:185` (a per-scenario output hash
with default separators); `cli.py:82` and `:788`, `preflight.py:636`,
`runtime_identity.py:372` (indent-2 renderings to stdout or to a string
without the trailing newline). None is a canonical byte form a digest or a
retained file depends on, and folding them into the two primitives would
change bytes the specification says must not move.

## Disclosures

1. `ECP-PRM-009` and `ECP-PRM-015` were read as `DEC-ECP-001` amended them:
   the package only. `repository_tools/json_bytes.py` re-exports nothing;
   `upgrade_rehearsal._environment` stays.
2. `release_build.canonical_json_bytes` stays as an alias of
   `recipe_json_bytes` because `scripts/replay_release_build.py`, a lane
   script outside this work order's scope, imports it by the old name.
   Removing the alias needs that script's one import line changed; a scope
   amendment or a later work order.
3. The duplication scan reads 4 blocks after this group: three pair an
   engine copy with a package copy (the layout registry, the standing
   deviations, the body parser) and belong to wave 3 (#378); one pairs
   `workflow_contract` with `workflow_result`, the restitution fields group
   C wires from the contract. `ECP-PRM-027` is read at group C's completion.
4. `tests/test_hash_bound_integrity.py` pinned the installer's lock-write
   line and `tests/test_release_build.py` the tools' serializer name; both
   pins moved with the code.
5. `se_harness/interpreter_safety.py` keeps its private digest.
   `SPEC-REB-015` rule 2 binds the loader modules to the standard library and
   `tests/test_interpreter_safety.py` refused the import of `integrity`; the
   first cut of the code commit crossed that line and `b72c9652` restores
   `hashlib`. The inventory test of `ECP-PRM-006` exempts that one module and
   says why. `ECP-PRM-006` is therefore met for every package module the
   barrier lets import the primitive.
6. Two rollback cases of `tests/test_standard_repository_lifecycle.py`
   patched `se_harness.installer.os.replace`; the replace now happens in
   `integrity.atomic_write_bytes`, so they patch `se_harness.integrity.os.replace`
   and still see every file restored after an interrupted apply.
7. `se_harness/preflight.py` was outside the work order's scope though
   `ECP-PRM-013` names the phase value it alone defines. The handoff check
   refused it (`WEX201`); the accountable engineering owner amended the scope
   on 2026-09-08 under DR-REMEDIATION-SCOPE and the work order carries the
   dated amendment. Nothing else was widened.
