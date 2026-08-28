# WO-ECP-011 implementation evidence

artifact: WO-ECP-011
checkpoint: handoff
formal_snapshot_sha256: f4f0748a085c357235190d0575093508842eba8ffcafaffa7a356eee6ee88fb6

Retained by the implementation actor on 2026-08-28. This file is evidence. It
does not complete, verify, or release the work order.

## Outcome

The governance-migration stage machine that `WO-ECP-010` retired and kept
dead is deleted; nothing of it ships in the candidate wheel, nothing under
`se_harness/` names it, the owner region of `.gitattributes` no longer pins
it, and the portable-surface check forbids its members in the wheel and in
the active repository surface. Issue #210's second acceptance criterion is
proven without exemption:
`test_no_json_under_se_harness_embeds_a_digest_of_a_python_module` now scans
every `se_harness/*.json`.

## Evaluators

- Governing: released `se-harness 0.8.0` (the root since `WO-HUP-008`,
  `main` at `6573bd8`), installed outside the checkout from the
  digest-verified wheel, invoked with `-I`.
- Candidate: this checkout, branch `governance/ecp-011-delete-stage-machine`
  off `main` at `6573bd8`; suite run with candidate source.

## What was deleted

- `se_harness/governance_migration.py` (38,123 bytes),
  `se_harness/governance_migration_contract.py` (22,941),
  `se_harness/governance_migration_contract.json` (5,206, the last JSON under
  `se_harness/` embedding a digest of a Python module), and
  `tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json`
  (3,476) with its now-empty directory.
- `governance_migration_contract.json` from `pyproject.toml`'s package data.
- The three owner-region `.gitattributes` rules
  (`se_harness/governance_migration*.py`,
  `se_harness/governance_migration_contract.json`,
  `tests/fixtures/governance_migration/*.json`) and the comment that
  explained their retention.
- The boundary `se_harness.governance_migration.runtime_probe` from
  `se_harness/interpreter_safety.json`'s registry. One rule boundary
  remains, `se_harness.runtime_identity.installed_interpreter`.

## What `WO-ECP-010` called "no importer, no test", corrected

`WO-ECP-010`'s disclosure recorded the retained module as having no
subcommand, no importer under `se_harness/` and no test. The first two were
true and still are. The third held for `tests/` by module name only:
`tests/test_interpreter_safety.py` imported `governance_migration` for the
`MIG2xx` refusal map (`test_the_migration_refusal_map_covers_exactly_the_declared_cases`,
`test_migration_retains_mig205_for_the_link_and_junction_refusals`) and its
boundary inventory named the module. Both tests go with the module (the
`EPS` cases they mapped are still declared and still exercised by the corpus
conformance tests; only the `MIG` code mapping ceased to exist), the
inventory lists the one remaining boundary, and
`test_declaration_rejects_an_unsorted_boundary_registry` inserts a synthetic
out-of-order entry instead of reversing a one-element list. The registry
was also named by `ARCH-REB-010`'s identity-boundary list; amended by date,
decision unchanged.

## Test assumptions replaced

| Module | Assumption carried | Now |
| --- | --- | --- |
| `tests/test_upgrade_rehearsal.py` | `RETAINED_UNTIL_ROOT_ADVANCES` exist; contract JSON exempt from the digest scan; owner rules present and say why | `DELETED_WITH_THE_ROOT_ADVANCE` absent, directory gone; no exemption; `.gitattributes` names nothing of the stage machine; the surface check joins the retired members to both forbidden sets |
| `tests/test_hash_bound_integrity.py` | `test_the_harness_data_digest_is_declared_out_of_scope_not_bound` read the deleted contract to show an `implementation_sha256` adapter | the declaration assertions stand on their own; the contract read is gone. The pattern-specificity and synthetic-attributes tests keep the pattern strings as data |
| `tests/test_standard_repository_lifecycle.py` | owner region carries the three rules | present under a 0.7.1 root, absent otherwise (reads the lock) |
| `tests/test_interpreter_safety.py` | see above | one rule boundary; two `MIG` tests removed; unsorted-registry test rewritten |

## Portable surface

- `scripts/check_portable_release_surface.py`: `RETIRED_MIGRATION_MEMBERS`
  is retained as the named set and joined into `FORBIDDEN_MEMBERS` (wheel)
  and `FORBIDDEN_ACTIVE_PATHS` (repository); the "neither required nor
  forbidden" comment is replaced.
- `--repository .`: `portable release surface: PASS`.
- Candidate wheel built from this tree (`pip wheel --no-deps`,
  `se_harness-0.9.0-py3-none-any.whl`): 107 members, none naming
  `governance_migration`; `--wheel`: `portable release surface: PASS`.

## Notes

The work order provided for correcting notes that still described the
retention. Read in full, the notes that name the stage machine
(`evaluator-migration-rehearsal.md`, `harness-installation-and-upgrades.md`,
`ci-pipeline.md`, `developing-se-harness.md`, the two 2026-08 audit notes)
describe its retirement, the `WO-HBI-005` fragment change or the
`governance-migration` lane name, all still true; none states that the files
are retained. No note was changed.

## Readings under the 0.8.0 root, isolated mode, over the complete change set

- `validate .`: PASS; structure E0/W0, governance E0/W0, policy E0/W0,
  maintenance E0/W473.
- `doctor .`: 0 FAIL — the deletion that released 0.7.1 refused
  (`hash-bound-class-declared … matches no tracked path`, `WO-ECP-010`
  disclosure 1) is accepted by 0.8.0, which declares no
  `governance-migration-protocol` class.
- No live reference remains: a scan of every `.py`, `.json`, `.toml`, `.yml`
  and `.gitattributes` outside `docs/` for `governance_migration` finds only
  the forbidden-member set, the deleted-path assertions and the pattern
  strings used as test data.

## Suite

`python scripts/run_tests.py --scale full` with candidate source against the
0.8.0 root (CPython 3.12, this workstation): 1009 tests (1011 before, the two
`MIG` tests gone with the module), 1 failure, 4 skips — the failure is
`test_release_build…test_declared_mode_set_is_what_a_posix_export_already_carries`,
the workstation file-mode condition that passes hosted, unchanged from before
this work order. Rehearsed identically on a throwaway export of `main`
before approval.


## Handoff check

`harnessctl check . --artifact WO-ECP-011 --checkpoint handoff --changed-path … --changes-complete` with released 0.8.0 outside the checkout: Completed over the 15 paths below; before this file carried the formal snapshot the only non-pass predicate was QGP-G4I-EVIDENCE. The work order's own file changes only through its recorded lifecycle transitions and is not a declared change (as under `WO-ECP-010`).

## Complete changed-path set

Every path this work order changed since `main` at `6573bd8`, packet index and evidence included:

```
docs/engineering/execution-control-plane/evidence/WO-ECP-011/WO-ECP-011-verification.md
docs/engineering/execution-control-plane/README.md
docs/engineering/released-evaluator-boundary/architecture/ARCH-REB-010.md
.gitattributes
pyproject.toml
scripts/check_portable_release_surface.py
se_harness/governance_migration_contract.json
se_harness/governance_migration_contract.py
se_harness/governance_migration.py
se_harness/interpreter_safety.json
tests/fixtures/governance_migration/synthetic-n-minus-1-to-n.json
tests/test_hash_bound_integrity.py
tests/test_interpreter_safety.py
tests/test_standard_repository_lifecycle.py
tests/test_upgrade_rehearsal.py
```

## Hosted lanes

Pull request #245 at `d2d7a49`: all 13 lanes pass, including the candidate-evidence lane that builds the wheel and runs `check_portable_release_surface.py` hosted, the governance-migration (upgrade-rehearsal) legs on Linux and Windows, and the governor transition assessment (no root change).
