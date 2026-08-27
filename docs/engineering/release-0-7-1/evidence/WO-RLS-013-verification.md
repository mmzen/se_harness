# WO-RLS-013 implementation evidence

artifact: WO-RLS-013
checkpoint: handoff
formal_snapshot_sha256: 0865550524c75e5bbd2a61d86fa0b19951dea16bb5bb5ec727f21631ecd70fe5

Retained by the implementation actor on 2026-08-27. This file is evidence. It
does not complete, verify, or release the work order.

## Evaluators

- Governing: released `se-harness 0.6.0` installed outside the checkout from
  the exact wheel `2a952eb6ff4ea137d0904c3c9a6f19c88482bfbaa18a9766e5ad4d4a6fef62f7`
  (`C:\Users\mathi\se-harness-eval`, invoked with `-I`).
- Public 0.7.0 outside the checkout (`C:\Users\mathi\se-harness-eval-070`),
  as a second reading only.
- Candidate: this checkout, branch `governance/release-0-7-1-packet` off
  `main` at `f605e58`.

## What was built

- **Version identity**: `pyproject.toml`, `se_harness/__init__.py` and the
  README install line moved to `0.7.1`.
- **Governance-migration scenario**:
  `tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.1.json` written
  by `python -m repository_tools.predecessor_facts write-scenario` from the
  0.7.0 pair (sha256 `b45bf951608fe1db8f40b30feca2b40704b7ee1d825809dea868b4a7ab60cccd`,
  3862 bytes); the 0.7.0 pair retired, because `derive` selects exactly one
  scenario from the root and the candidate version.
- **Scenario writer** (`repository_tools/predecessor_facts.py`, scope
  amendment of 2026-08-27): `_retarget` recomputes
  `simulated_publication_sha256` from the adopted proposal and the successor
  version, the identity the adopt stage checks (`MIG413`). Before the fix the
  writer copied the template's digest and the new scenario failed the
  rehearsal; the fix was first written under the rejected `WO-HUP-006` and
  never reached `main`. `repository_tools` is not in the packaged surface.
- **Developer note**: `docs/notes/developing-se-harness.md` states the candidate
  version 0.7.1, which `test_progressive_documentation` pins to `__version__`.
- **Tests**: `tests/test_ci_pipeline.py` pins the recomputed publication
  digest and follows the candidate version; `tests/test_governance_migration.py`
  points at the new scenario.
- **Governance**: this domain's README, `REL-SEH-018`, `WO-RLS-013` (approved,
  started, scope amended), the `docs/engineering/README.md` domain line.

## Commands and results

| Command | Evaluator | Result |
| --- | --- | --- |
| `harnessctl preflight . --work-order WO-RLS-013 --phase start` | released 0.6.0 | `PASS` (recorded in the start transition) |
| `harnessctl preflight . --work-order WO-RLS-013 --phase review` | released 0.6.0 | `PASS` |
| `harnessctl validate .` | released 0.6.0 | PASS, 978 artifacts, 0 errors, 53 pre-existing warnings |
| `harnessctl validate .` | public 0.7.0, outside the checkout | PASS, 978 artifacts, 0 errors |
| `harnessctl doctor .` | released 0.6.0 | 0 FAIL |
| `python -m repository_tools.predecessor_facts derive --repository .` | candidate | version 0.6.0, wheel `2a952eb6`, candidate_version 0.7.1, scenario `candidate-0.6.0-to-0.7.1.json` |
| `python scripts/validate_release_distributions.py --root .` | candidate | PASS (3 distribution-bearing records) |
| `python scripts/check_portable_release_surface.py --repository .` | candidate | PASS |
| `git diff --check` | git | clean |
| `python -m unittest` over `test_ci_pipeline`, `test_governance_migration`, `test_release_qualification`, `test_standard_repository_lifecycle` | candidate | OK, 72 tests (the migration rehearsal 0.6.0 to 0.7.1 inside `test_governance_migration` reads pass, complete, compatible, deterministic) |
| `python scripts/run_tests.py --workers 8 --scale full` | candidate, Windows 11, CPython 3.14 | OK, 983 tests, 24 skipped (Windows-only guards), 0 failures |
| `py -3.11 scripts/run_tests.py --workers 4 --scale full` | candidate, Windows 11, CPython 3.11 | OK, 983 tests, 24 skipped (Windows-only guards), 0 failures |
| `harnessctl release-unit . --from v0.7.0 --to HEAD --exempt <the six contract commits> --contract REL-SEH-018 --json` | candidate | traces `WO-REB-027` and `WO-RLS-013`; incomplete only because `WO-RLS-013` is `in_progress` at this reading; no `E-CIP-001` finding; the contract's other three members are reached only through exempted merge commits (deviation 2) |
| `harnessctl check . --artifact WO-RLS-013 --checkpoint handoff --changed-path ... --changes-complete --json` | released 0.6.0 and candidate | Completed on both over the fourteen paths; before this file existed the only non-pass predicate was QGP-G4I-EVIDENCE; formal snapshot above |
| `qualify complete-candidate --candidate-commit <candidate>` | candidate | at candidate 11b5a8c30b12e192aaa54542424d9574bc1e7a0b, run with python -s (a first run with user site-packages enabled failed CC001 on RID009, not on the candidate): passed, CC001 bound to the checkout, CC002 HEAD and tracked tree match, CC003 978 artifacts 0 errors, CC004 target unchanged; independence candidate-controlled |
| Build of record, WSL Ubuntu, `python -m repository_tools.release_build replay --commit <candidate> --version 0.7.1` | pinned linux/amd64 producer | at candidate 11b5a8c, WSL Ubuntu 24.04 with Docker Desktop integration, output under /tmp: state exact, two byte-identical producer runs; wheel se_harness-0.7.1-py3-none-any.whl 25a65a3934c681ea2bf56be020cad834e79bfc9729eb385ab97be0e1fa7bbc8b, sdist se_harness-0.7.1.tar.gz b834549869628aa29526c65d9272f3aef1b0bb3a94c99d61cbc197d547fb3590; to be compared with the hosted candidate-mode replay at the pull-request head |
| Hosted | pull request #199 at 11b5a8c | all fourteen lanes pass (Engineering Harness, Candidate Evidence, Publication Rehearsal, Governor Transition Assessment; Publication Rehearsal run 33093001090); the candidate-mode replay ran on the merge-preview commit 385d357, so its digests are not the candidate's; the comparison of record is the release-candidate-replay dispatch at the bound commit |

## Deviations from the work order, recorded for the completion decision

1. **Scope amendment.** `repository_tools/predecessor_facts.py` was added to
   the execution scope during execution on the owner's answer of 2026-08-27
   (recorded in the work order). The frozen unit's packaged bytes are
   untouched.
2. **The release-unit derivation reads two of the five members.** The
   derivation traces work orders from first-parent trailers; `WO-REB-024`,
   `WO-REB-025` and `WO-REB-026` reached `main` through merge commits without
   a trailer, which the contract exempts by name. The contract's five-member
   allow-list is the authority (`REL-SEH-018` names no `candidate_commit`, so
   `QGP-G5P-RELEASE-UNIT` is unmeasured); the derivation is recorded, not
   enforced, as for `REL-SEH-017`. The command reports no `E-CIP-001` finding.
   The `[release_unit].untraced_exemptions` table in the contract is read by
   nobody today; the six exemptions are passed as `--exempt` flags, and the
   developer note's claim that the contract carries them is a gap owed.

## Deviation acceptances

Recorded on 2026-08-27 from the owner's interactive answer 'Accept both',
before the completion decision.

| Deviation | Owner answer |
| --- | --- |
| 1 - scope amendment for the scenario writer | Accept (answered during execution). |
| 2 - derivation traces two of five members; exemptions passed as flags | Accept; the unread `untraced_exemptions` table is a gap owed. |

## Complete changed-path set

```
README.md
docs/engineering/README.md
docs/engineering/release-0-7-1/README.md
docs/engineering/release-0-7-1/evidence/WO-RLS-013-verification.md
docs/engineering/release-0-7-1/release/REL-SEH-018.md
docs/engineering/release-0-7-1/work-orders/WO-RLS-013.md
docs/notes/developing-se-harness.md
pyproject.toml
repository_tools/predecessor_facts.py
se_harness/__init__.py
tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.0.json
tests/fixtures/governance_migration/candidate-0.6.0-to-0.7.1.json
tests/test_ci_pipeline.py
tests/test_governance_migration.py
```

## Not done

- The completion transition; `VREC-SEH-015`; `RLS-SEH-016`; the tag, the
  publication and the adoption.
