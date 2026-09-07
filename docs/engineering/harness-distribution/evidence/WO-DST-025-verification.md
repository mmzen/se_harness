# WO-DST-025 verification evidence

Retained under `VER-DST-026` for the removal of the inert keys from the
installed configuration. Measurements were taken on Windows 11 at candidate
revision `5e02039` plus the working tree of branch
`packet/dst-025-configuration-surface`, whose base is `main` at `5e02039`. The
governing evaluator is released 0.16.0 in `C:/Users/mathi/se-harness-eval-0160`,
run with `-I` from outside the checkout. The consumer scenarios ran in
`C:/Users/mathi/dst025-scenarios`, outside the checkout, from an ephemeral
non-promotable candidate wheel `se_harness-0.17.0-py3-none-any.whl`
(`sha256:9e12ed80...63f`, built on Windows and not a build of record) installed
in its own virtual environment.

## Authorization

- 2026-09-07: the owner instructed "remove all unused configuration items".
- 2026-09-07: the owner disposed `DEC-DST-001` by selecting the presented
  option "Remove it (Recommended)", which put `schema_version` in the set to
  remove.
- 2026-09-07: the owner approved `REQ-DST-071`, `SPEC-DST-026`, `VER-DST-026`
  and `WO-DST-025` and started the work order by selecting the presented
  option "Approve and start immediately".

## Reader inventory

The twelve keys released 0.16.0 wrote, each against the code that reads it.
A search for each name across `se_harness/`, `templates/`, `.github/` and
`scripts/` is the measurement; the reading module is the file that consumes the
parsed value.

| Key | Table | Reader | Effect of the value |
| --- | --- | --- | --- |
| `tool_version` | `[harness]` | `se_harness/mutation_guard.py` | absent is `MG001`; disagreeing with the lock is `MG003` |
| `installed_at` | `[harness]` | `se_harness/installer.py` | carried across an upgrade so the date is not reset |
| `project_name` | `[harness]` | `se_harness/installer.py` | carried across an upgrade so the name is not reset |
| `required_for_verified_work` | `[revision_provenance]` | `se_harness/engine/validate_engineering_artifacts.py` | `E010` for a verified work order with no covering record |
| `required_for_release` | `[revision_provenance]` | `se_harness/workflow.py` | closes the release transition at `QGS-EDGE` |
| `schema_version` | `[harness]` | none | none; audit item P2-10 |
| `artifact_root` | `[harness]` | none | none; the layout is a constant |
| `dashboard_output` | `[harness]` | none | none; the output root is a constant |
| `require_full_commit` | `[revision_provenance]` | none | none |
| `require_clean_worktree` | `[revision_provenance]` | none | none |
| `verification_record_status` | `[revision_provenance]` | none | none |
| `release_record_status` | `[revision_provenance]` | none | none |

Occurrence counts after the change, over `se_harness/`, `templates/`,
`.github/` and `scripts/`: `schema_version` 0, `dashboard_output` 0,
`require_full_commit` 0, `verification_record_status` 0,
`release_record_status` 0, `require_clean_worktree` 5, `artifact_root` 47. The
two non-zero counts are name collisions, not readers, and the inspection below
records why.

## Inspections

`se_harness/provenance.py` defines `require_clean_worktree(repository_root)`
and calls it unconditionally before `capture-verification` and
`prepare-release`. The clean-worktree rule is the command's own, always in
force; the configuration key of the same name was never consulted, which is
exactly why it read as a live setting to an owner (DST-CFG-007, DST-CFG-013).

`artifact_root` survives as a derived projection, not a setting.
`se_harness/engine/generate_harness_dashboard.py:1946` writes the value of its
own `artifact_root` argument into the snapshot's repository block, and
`se_harness/engine/inspect_engineering_artifacts.py:572` reads it back out of
that snapshot. `DEFAULT_ARTIFACT_ROOT` and `DEFAULT_OUTPUT_ROOT` are module
constants. `validate_engineering_artifacts.validate_canonical_layout` returns
no findings at all when the artifact root is not
`<repository>/docs/engineering`, so a configurable root would have switched the
canonical-layout gate off silently. That is the reason the key is removed
rather than wired up.

The two provenance loaders,
`validate_engineering_artifacts.load_revision_policy` and
`workflow._revision_policy`, read only `required_for_verified_work` and
`required_for_release`, and both default them to `false` when the table or the
file is missing. `mutation_guard._configured_version` reads only
`[harness] tool_version`. No reader of a removed key exists (DST-CFG-013).

`SPEC-REV-001` and `REQ-SHB-009` are amended by record, prose only
(DST-CFG-006). `SPEC-REV-001`'s compatibility sentence no longer promises
configuration schema 2 and now names the lock as the recorder of the schema and
the tool version. `REQ-SHB-009`'s acceptance example named
`require_clean_worktree`; it now names `required_for_release`, a key the
harness does read, and the reconciliation behaviour it illustrates is
unchanged. Each carries an `## Amendment record` entry dated 2026-09-07 under
this work order. Neither statement, rule identifier, relation, verification
method nor status moves.

## Rendered configuration, before and after

Before, as released 0.16.0 wrote it into a fresh repository (twelve keys in
two tables):

```toml
[harness]
schema_version = 2
tool_version = "0.16.0"
installed_at = "2026-09-07"
project_name = "Consumer"
artifact_root = "docs/engineering"
dashboard_output = "target/harness-dashboard"

[revision_provenance]
require_full_commit = true
require_clean_worktree = true
required_for_verified_work = true
required_for_release = true
verification_record_status = "ready"
release_record_status = "ready"
```

After, as the candidate writes it (five keys in two tables):

```toml
[harness]
tool_version = "0.17.0"
installed_at = "2026-09-07"
project_name = "Consumer"

[revision_provenance]
required_for_verified_work = true
required_for_release = true
```

The template diff is seven deletions and no insertions
(`templates/repository/standard/.engineering-harness.toml.tpl`, 7 deletions).

## Scenario A, consumer install

`init` into an empty directory, then `doctor`, `validate`, `dashboard`, all
from the wheel's virtual environment.

| Step | Result |
| --- | --- |
| `init` | exit 0; 41 files, 0 unchanged; "installed se-harness 0.17.0" |
| rendered configuration | five keys, `project_name = "Scenario A"` |
| `doctor` | exit 0; 0 `FAIL` lines |
| `validate` | exit 0; `Artifacts: 0 \| Errors: 0 \| Warnings: 0 \| Advisories: 0` |
| `dashboard` | exit 0; `Output: target/harness-dashboard` |

The dashboard still writes `target/harness-dashboard` with no key telling it
to, which is the removal's point.

## Scenario B, consumer upgrade

A repository initialized by released 0.16.0 from
`C:/Users/mathi/se-harness-eval-0160`, then upgraded by the candidate.

| Step | Result |
| --- | --- |
| key count before | 12 keys in 2 tables |
| `upgrade` plan | `update .engineering-harness.toml`; summary 40 files, 37 unchanged |
| `upgrade --apply` | exit 0; updated the configuration, the managed workflow and `ENGINEERING_HARNESS.md`; "upgraded managed files to se-harness 0.17.0" |
| key count after | 5 keys in 2 tables |
| retired names remaining | none |
| `doctor` after | exit 0; 97 `PASS`, no `FAIL` |
| `project_name` | `Consumer`, unchanged |
| `installed_at` | `2026-09-07`, unchanged |

The plan classified the unmodified configuration as `update`, the existing
managed-mode safe rewrite, with no new installer code (DST-CFG-008,
DST-CFG-009).

## Scenario C, customized configuration

The same fixture with one line appended to the configuration
(`artifact_root = "docs/elsewhere"`, an owner reinstating a removed key by
hand).

| Step | Result |
| --- | --- |
| `upgrade` plan | `customized .engineering-harness.toml` |
| `upgrade --apply` | exit 1; "customized files require manual review; no files were written: `.engineering-harness.toml`" |
| configuration bytes | `e6dbbd19...103` before and after, identical |
| lock bytes | `fc8d83db...79a` before and after, identical |

The refusal names the path and writes nothing, including the two files the same
plan would otherwise have updated (DST-CFG-010).

## Tests

`tests/test_configuration_surface.py`, new, five cases:

| Case | Rules |
| --- | --- |
| `test_installed_configuration_declares_only_keys_a_reader_uses` | DST-CFG-001, DST-CFG-002, DST-CFG-012, DST-CFG-013 |
| `test_the_retired_keys_are_declared_nowhere` | DST-CFG-003, DST-CFG-004, DST-CFG-005 |
| `test_the_retired_keys_change_no_behaviour` | DST-CFG-007, DST-CFG-011 |
| `test_upgrade_removes_the_retired_keys_and_preserves_owner_values` | DST-CFG-008, DST-CFG-009 |
| `test_upgrade_refuses_a_customized_configuration` | DST-CFG-010 |

The key-set case asserts the tables and their keys exactly, and asserts that
each key's name occurs in the source file named beside it, so a key that loses
its reader fails the test as loudly as a key that appears without one.

The tolerance case writes the whole 0.16.0 twelve-key shape into an installed
target, rebinds the lock to those bytes, and reads the two provenance loaders
again: the values are the ones the surviving keys declare, and the only failing
installation check is `distribution:.engineering-harness.toml`, "differs from
distribution template". The lock still calls the file unchanged; the drift is
against the newer template, and `upgrade --apply` is what closes it. That is
the same reading this repository's own root shows and is not a defect.

`tests/test_harnessctl.py`, changed: the assertion that a fresh installation
carries `schema_version = 2` is retired to an `assertNotIn`, with a comment
naming DST-CFG-005 and pointing at the new module.

Test files changed: `tests/test_configuration_surface.py` (new),
`tests/test_harnessctl.py` (one assertion). No other test file is touched.

## Governing readings

| Reading | Command | Result |
| --- | --- | --- |
| artifact graph, governing | released 0.16.0 `-I -m se_harness validate .` | `Artifacts: 1357 \| Errors: 0 \| Warnings: 73 \| Advisories: 0` |
| release distributions | `python scripts/validate_release_distributions.py --root .` | PASS, 13 distribution-bearing records |
| local suite, Windows control | `python -m unittest discover -s tests -p "test_*.py"` | `Ran 1270 tests`, 1 failure and 1 error, both known Windows-only controls; 26 skips |
| candidate suite, hosted lane, the record | `SE Harness Candidate Evidence` on pull request #373 at `e2da416` | `Ran 1270 tests in 47.552s (134 classes, 4 workers)`, `OK (skipped=4)`; run 34154160252 |
| managed harness lane | `Engineering Harness` on pull request #373 | success; the lane read the live body's `Harness-Work-Order: WO-DST-025` |
| governor transition | `Governor Transition Assessment` on pull request #373 | success |
| publication rehearsal | `Publication Rehearsal` on pull request #373 | success |

The hosted lane is the record and it is green. Its 1,270 tests are `main`'s
1,265 plus this work order's five, and its four skips are the same four `main`
skips at run 34123580408; the local Windows control skips 26 because that host
cannot make symbolic links. The candidate-evidence workflow also rehearsed the
real predecessor-to-successor upgrade twice on both Linux and Windows, from
released 0.16.0 to the candidate wheel, which is the same path as scenario B,
and exercised a disposable standard repository with the reduced configuration:
`Artifacts: 0 | Errors: 0 | Warnings: 0 | Advisories: 0` and a dashboard
written to `target/harness-dashboard`.

The two local failures are the controls this repository already carries on
Windows and are unrelated to this work:
`test_instruction_architecture.OwnerInstructionRegionTests.test_owner_region_stays_within_the_size_bound`
fails as "6024 not less than 6000" because the worktree copy of `AGENTS.md` is
CRLF, a file this work order does not touch, and
`test_artifact_authoring` raises `PermissionError: [WinError 5]` from
`shutil.rmtree` on a temporary `.git` directory. Both reproduce on `main`
before the change. All 26 skips are host-capability guards: unprivileged
symbolic links, hostile portable filenames, and POSIX virtual-environment
launchers. None of them hides a configuration or template-parity assertion.

## Root configuration and lock

`git diff main -- .engineering-harness.toml .engineering-harness.lock` is
empty: both are byte-identical to `main` (DST-CFG-014). The in-tree
`doctor` still reports `PASS config`, `PASS managed:.engineering-harness.toml`
and `FAIL distribution:.engineering-harness.toml`, beside the same distribution
readings for `ENGINEERING_HARNESS.md` and the managed workflow. That is the
candidate-versus-released skew this checkout already carried, since the root
belongs to released 0.16.0 while the templates are candidate 0.17.0.

## Carried obligation

`SPEC-DST-026` DST-CFG-015 binds the root-adoption work order of the release
that carries this change: it takes the reduced configuration into this
repository's root and records the new lock digest. Nothing in this work order
may do it.

## Review preflight and checkpoints

All three run with released 0.16.0 from outside the checkout, with the change
set taken from `--from-git main`.

| Command | Result |
| --- | --- |
| `preflight . --work-order WO-DST-025 --phase review` | PASS; work order `in_progress`; commit-bound verification required, decided by `repository-owner` |
| `check . --artifact WO-DST-025 --checkpoint scope --from-git main` | `QGP-G4I-SCOPE` pass, `QGP-G4I-COMPLETE` pass, `QGP-G4I-PATHS` pass; twelve changed paths, all inside `[execution_scope]` |
| `check . --artifact WO-DST-025 --checkpoint handoff --from-git main` | all nine gates pass: `STATUS`, `GRAPH`, `INTEGRITY`, `SCOPE`, `COMPLETE`, `PATHS`, `PREFLIGHT`, `EVIDENCE`, `DECISION` |

The handoff checkpoint first read `QGP-G4I-EVIDENCE: not_assessable`.
`harnessctl evidence . --artifact WO-DST-025 --checkpoint handoff` wrote the
packet at `evidence/WO-DST-025/` bound to formal snapshot
`89405e1472eb322d10a6df2f4cdc1f28a767480bf668dcbcb281524cc939df63`, and the
second run passed. Both `WO-DST-025-handoff.md` and `handoff.json` are
committed, so the hosted lane reads the packet rather than `E012`.

The decision the handoff checkpoint names is the owner's:
`engineering-owner` decides under `DR-WO-COMPLETE` whether the authorized
implementation and evidence are complete, with `implemented`, `continue` or
`reject` permitted. Nothing in this evidence exercises it.
