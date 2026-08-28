# WO-ECP-010 implementation and verification evidence

Work-order-keyed evidence for `WO-ECP-010` (`REQ-ECP-012`, `SPEC-ECP-007`
`ECP-PRD-008`; repository issue #210). Retained under `VER-ECP-007`, the rows
that name `REQ-ECP-012` and `ECP-PRD-008`. Readings taken on 2026-08-28 on
Linux (CPython 3.12.13, Git 2.52.0) from branch
`governance/ecp-010-upgrade-rehearsal-packet`, based on `main` at `4b1eee9`
plus the packet, approval and start commits (`621ed3a`, `2a8dc58`). Windows
figures come from the hosted lanes, section 9.

## 1. Changed paths

| Path | Change |
| --- | --- |
| `repository_tools/upgrade_rehearsal.py` | new, 230 lines: exports the committed tree, runs predecessor `doctor` (pass), successor `upgrade` plan and `upgrade --apply --evidence-output`, successor `doctor` (pass) and `validate` (no error but `E012` on ready records), predecessor `doctor` (must fail), asserts the schema-3 lock names the successor's version and installed-payload digest; `semantic_sha256` is the canonical `utf8-text-lf-v1` digest of the resulting lock; standard library only, no `se_harness` import, evaluators run with `-I` under a credential-stripped environment |
| `repository_tools/evaluator_facts.py` | `predecessor_facts.py` renamed and trimmed: `derive` keeps the root, released-record and candidate-version facts and `LEGACY_ACCEPTANCE_CONTRACT_SHA256`; the scenario coupling (`PRE009` to `PRE012`, `load_scenario`, `_retarget`, `write-scenario`) is gone; `PredecessorFactsError`/`PredecessorFacts` retained as names |
| `.github/workflows/candidate-evidence.yml` | `candidate-source` derives through `evaluator_facts` and exports no scenario outputs; the `governance-migration` job keeps both platforms, the exact wheels, the two runs and the cross-platform digest comparison, and runs `repository_tools.upgrade_rehearsal` |
| `tests/test_governance_migration.py`, three of the four `tests/fixtures/governance_migration/` scenarios, `repository_tools/predecessor_facts.py` | deleted |
| `se_harness/governance_migration.py`, `_contract.py`, `_contract.json`, `tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json` | **retained, dead** (section 6, item 1): no subcommand, no importer, no test; their deletion is deferred by the owner's amendment until the root advances past 0.7.1 |
| `se_harness/cli.py` | `rehearse-migration` and its handler and imports removed |
| `scripts/check_portable_release_surface.py` | the three migration members are no longer required (neither forbidden until the follow-up deletes them); `rehearse-migration` forbidden on the CLI surface |
| `.gitattributes` | the three owner-region `governance_migration*` rules are retained with a dated rationale (section 6, item 1) |
| `REQ-REB-016`, `REQ-REB-017`, `SPEC-REB-008` | dated retirement amendments in the form `WO-REB-028` used |
| `REQ-REB-029`, `SPEC-REB-013`, the REB index | dated amendments naming the upgrade rehearsal as the one retained mechanism |
| `docs/notes/evaluator-migration-rehearsal.md` | rewritten for the upgrade rehearsal |
| `developing-se-harness.md`, `ci-pipeline.md`, `harnessctl-reference.md`, `release-qualification-roles.md`, `harness-dashboard-publication.md` | corrected where they named the retired command, scenario or module |
| `tests/test_upgrade_rehearsal.py` | new, 17 cases (section 4) |
| `tests/test_ci_pipeline.py`, `test_standard_repository_lifecycle.py`, `test_predecessor_bootstrap_retirement.py`, `test_hash_bound_integrity.py`, `test_interpreter_safety.py`, `test_release_orchestration.py`, `test_release_qualification.py` | retargeted |

Not changed: `mutation_guard`, the installer, the lock format,
`recovery_rehearsal.py`, `accept-candidate`, `qualify`, `validate_governor_transition.py`,
`se_harness/interpreter_safety.py` and `.json` (section 6, item 2), `repository_tools/interpreter_safety.py` (#220),
any root managed file, any historical record.

## 2. The real rehearsal, run here

Exact public `se-harness==0.7.1` (the released root) as predecessor, a
non-editable install of this tree as successor, `python -m
repository_tools.upgrade_rehearsal --repository .`, twice:

| Reading | Value |
| --- | --- |
| result | `PASS (0.7.1 -> 0.8.0)`, about 8 s per run |
| steps | `predecessor-doctor-before` pass (exit 0); `successor-upgrade-plan` pass; `successor-upgrade-apply` pass; `successor-doctor-after` pass (exit 0); `successor-validate-after` 1,061 artifacts, 2 errors both tolerated (`E012` on `VREC-REB-026` and `VREC-REB-027`, both `ready` on `main`); `predecessor-doctor-after` pass = exit 1 as required |
| resulting lock | schema 3, `tool_version 0.8.0`, evaluator `0.8.0` with the successor's installed-payload digest, equal to the transaction evidence's `target.payload_sha256` |
| `semantic_sha256` | `de31d822df254e969d3940e91a1407a788ff8a0bb1f73fc33f0dab4deeb622ce`, identical across the two runs |
| operational checkout | untouched (`git status` clean; its lock still names 0.7.1) |

The predecessor's `doctor` fails afterwards on the nine `distribution:*`
managed files that now differ from 0.7.1's templates; the lock itself is
judged by the rehearsal's own assertion, not by that failure.

## 3. Acceptance criteria of issue #210

| Criterion | Reading |
| --- | --- |
| The Linux and Windows lanes execute the successor's `installer.apply_changes` against a lock written by the predecessor and fail unless the lock ends at schema 3 naming the successor | the lane runs `upgrade --apply` (the installer's own transaction) on both platforms; the rehearsal asserts schema 3, version and payload, and `test_the_lock_must_end_at_schema_three_naming_the_successor` proves each of the three refusals |
| No JSON file in `se_harness/` embeds a digest of a Python module | **deferred with the deletion**: `governance_migration_contract.json`, the one file that does, is retained dead until the root advances (section 6, item 1); `test_no_json_under_se_harness_embeds_a_digest_of_a_python_module` proves no other `se_harness/*.json` does and carries the exemption the follow-up removes |
| Per-release preparation needs no hand-authored migration scenario | `test_a_version_bump_needs_no_scenario`: a `pyproject.toml` bump alone derives and the CLI exits 0 |

## 4. Tests

`tests/test_upgrade_rehearsal.py` (17): the passing handover binding the
resulting lock and leaving the operational repository untouched; the
predecessor must own the root before and not after; the successor's `doctor`
must pass; only `E012` on ready records is tolerated (`E010` fails);
the lock must be schema 3 naming the successor's version and payload (three
refusals); same version is no handover; the exported lock must belong to the
predecessor; the output must be empty and outside the repository; the export
is the committed tree, not the working tree; the canonical digest ignores
newline form; credential variables never reach the evaluators; and the
retired-surface cases (no module digest in a `se_harness/` JSON, the stage
machine gone and its names reserved, the retained owner rules say why, the
lane runs the rehearsal twice per platform with the cross-platform compare).
The evaluator invocations are answered by a fake that mutates the throwaway
lock the way the installer does; Git runs for real.

Full suite `python scripts/run_tests.py`: 1,009 tests, 1 failure, 4 skipped;
the failure is the known `test_release_build…declared_mode_set…` file-mode
artefact of this Linux checkout, which fails identically at `main` here and
passes on the hosted runner.

## 5. Released evaluator readings

Exact public `se-harness==0.7.1` outside the checkout, run with `-I`:
`validate` 1,061 artifacts, 0 errors, 471 warnings; `doctor` 0 FAIL;
`preflight --work-order WO-ECP-010 --phase review` PASS;
`check --checkpoint handoff` in section 8.
Repository-required: `validate_release_distributions.py` PASS (4 records);
`python -m se_harness --help` exit 0; `check_portable_release_surface.py --repository .` PASS.
An explicitly non-promotable ephemeral wheel built outside the checkout from a
clean tree passes the portable-surface check and carries no
`governance_migration` member.

## 6. Disclosures

1. **The stage machine is retired but not yet deleted.** With the deletions
   staged, the released 0.7.1 evaluator that governs this root failed
   `hash-bound-class-declared` (`governance-migration-protocol: pattern
   se_harness/governance_migration*.py matches no tracked path`) and with it
   the review preflight and `QGP-G4I-PREFLIGHT`: 0.7.1 still ships the
   `repository`-region class that `WO-HBI-005` removed from the candidate,
   and refuses any tree where a pattern matches nothing. An earlier "0 FAIL"
   reading was taken before the deletions were staged and was wrong. On the
   implementer's escalation the owner chose to land the rehearsal now and
   delete after the root advances ("Land the rehearsal now, delete after the
   root advances"), recorded as a dated amendment in the work order. So
   `se_harness/governance_migration.py`, `governance_migration_contract.py`,
   `governance_migration_contract.json` and one fixture stay tracked, dead:
   no subcommand, no importer under `se_harness/`, no test; the owner-region
   `.gitattributes` rules stay with them; the portable-surface check neither
   requires nor forbids the members; the wheel carries the dead module for one
   release. `test_the_stage_machine_is_retired_dead_and_its_names_are_reserved`
   pins that state and names the four files the follow-up deletes. Issue
   #210's second acceptance criterion is met for every JSON but the retained
   contract and closes with that follow-up.
2. **`se_harness/interpreter_safety.py` and `.json` are not deleted.** The
   work order named them because the retired module was their only product
   caller; `ARCH-REB-010` and a 1,400-line conformance suite bind both loader
   copies to that architecture, and amending it is outside scope. With the
   module retained (item 1) the registry is unchanged. #220 tracks the copy.
3. The rehearsal tolerates exactly one validator error, `E012` on a `ready`
   record, and reports each tolerated line; `main` carries two ready records
   today (`VREC-REB-026`, `VREC-REB-027`), so the lane's runs tolerate two.
   The tolerance is by code and message, never by count.
4. The predecessor's `doctor` after the upgrade fails on distribution skew,
   which is evidence that 0.7.1 no longer owns the root but not a check of
   the lock; the lock assertion is separate and explicit.
5. The deleted `write-scenario` had reproduced the committed scenarios byte
   for byte; that property has no successor because there is nothing to
   author. `LEGACY_ACCEPTANCE_CONTRACT_SHA256` stays the one fact the lock
   cannot supply.
6. `WO-ECP-007` was narrowed in the packet commit; its remaining evictions
   are untouched here.
7. A stale `build/` directory in this checkout made the first ephemeral wheel
   carry stale files; a clean rebuild passes the portable-surface check. The
   hosted lane builds from a Git export and is not exposed to it.
8. Windows readings are the hosted lanes'.
9. The first hosted run failed `candidate-package` on the portable-surface
   script's help inspection, which still invoked `harnessctl rehearse-migration
   --help`; the local check had only been run in `--wheel` mode. The
   invocation was removed (commit after `4da6a9f`), the `--harnessctl` mode
   now passes locally against the successor environment, and the formal
   snapshot the handoff binds is unchanged by a script edit.

## 7. Handoff checkpoint binding

artifact: WO-ECP-010
checkpoint: handoff
formal_snapshot_sha256: 3ee7a5307a70842ee5c19a4ca97f06aa91bb6b1afd77ef41a8863d35dc7dce57

Rerun: completed pass d1544bd18226e2a3569b1052bb6b9a1312ce8c138be44e8f86a828aaee1bd9e2

## 8. Hosted lanes

Recorded in a later commit once the pull request has run them.
