# WO-HBI-005 implementation and verification evidence

Work-order-keyed evidence for `WO-HBI-005` (repository issue #207, complexity
audit P0-1). Retained under `VER-HBI-001`, third amendment. Every reading below
was taken on 2026-08-28 on Linux (CPython 3.12.13, Git 2.52.0) from the
implementation branch `governance/hbi-005-fresh-consumer-doctor`, whose base is
the governance commit `03a3e22` (amendments accepted, `WO-HBI-005` approved and
started). Windows figures come from the hosted lanes and are recorded in
section 9 once the pull request has run them.

## 1. Changed paths

| Path | Change |
| --- | --- |
| `se_harness/hash_bound_classes.json` | `governance-migration-protocol` removed; `implementation_sha256` added to `unbound_digest_fields` with a reason that matches `_REASON` |
| `templates/repository/standard/gitattributes.fragment` | the comment line and three `governance_migration` rules removed; the `evaluator-evidence` rule and its comment remain |
| `se_harness/hash_bound.py` | `_class_declared`: "pattern matches no tracked path" fails only a `repository`-region class; an empty `template`-region class passes with `vacuously declared <class>: 0 tracked paths` in the detail. `_attribute_effective`, `_mode_consistent`, resolution, mode determination and every digest comparison unchanged |
| `tests/test_hash_bound_integrity.py` | `SPECIFIED_CLASSES` and `SYNTHETIC_FILES` reduced to the two-class declaration; a synthetic `repository`-region class (`owner-notes`, `notes/*.txt`) introduced; 13 cases retargeted; `test_candidate_fragment_promotion_of_repository_patterns_is_pinned` deleted; 7 cases added (see section 4) |
| `tests/test_public_onboarding.py` | `FreshConsumerDoctorTests`: `init`, `git init`, `add -A`, commit, `doctor`, on `core.autocrlf=false` and `=true` |
| `tests/test_standard_repository_lifecycle.py` | `test_evaluator_evidence_bytes_are_portable_across_git_checkouts` retargeted: shipped and freshly installed fragment are the two-line form; the root managed block keeps the released 0.7.1 six-line block; the owner region keeps its three rules (scope amendment of 2026-08-28) |
| `docs/notes/harness-installation-and-upgrades.md` | one subsection on the managed `.gitattributes` block changing at the next release |
| `docs/engineering/hash-bound-integrity/work-orders/WO-HBI-005.md` | dated scope amendment |
| this file | new |

Not changed, as the approval envelope requires: every root managed file
(`doctor` reads `managed:.gitattributes: unchanged`), every
`se_harness/governance_migration*` source and fixture, the owner-controlled
region of the root `.gitattributes`, and every recorded digest.

## 2. Before: the defect, reproduced

Public `se-harness==0.7.1` installed from the index into a venv outside the
checkout, run with `-I`:

```text
harnessctl init consumer --project-name fresh
cd consumer && git init && git add -A && git commit -m init
harnessctl doctor consumer            # exit 1
FAIL hash-bound-class-declared: evaluator-evidence: pattern docs/engineering/**/evidence/*.json matches no tracked path; governance-migration-protocol: pattern se_harness/governance_migration*.py matches no tracked path; governance-migration-protocol: pattern se_harness/governance_migration_contract.json matches no tracked path (+1 more)
FAIL hash-bound-attribute-effective: governance-migration-protocol: pattern se_harness/governance_migration*.py is declared in template; requires the repository region; governance-migration-protocol: pattern se_harness/governance_migration_contract.json is declared in template; requires the repository region; governance-migration-protocol: pattern tests/fixtures/governance_migration/*.json is declared in template; requires the repository region
```

The in-tree code at the base commit reproduces the same two lines
(`hash_bound.py` and `hash_bound_classes.json` are byte-identical between
`v0.7.1` and the base).

## 3. After: fresh consumer, candidate code

`PYTHONPATH=<checkout> python -m se_harness init`, then `git init`, `add -A`,
commit, `doctor`, once per checkout configuration:

| `core.autocrlf` | exit | checks | hash-bound lines |
| --- | --- | --- | --- |
| `false` | 0 | 143 PASS, 0 FAIL | `PASS hash-bound-class-declared: 2 classes cover 1 tracked paths; 10 digest fields declared out of scope; vacuously declared evaluator-evidence: 0 tracked paths` / `PASS hash-bound-attribute-effective: 1 raw classes effective for 0 tracked paths` / `PASS hash-bound-mode-consistent: one mode per class: evaluator-evidence=raw, standard-lock=utf8-text-lf-v1` |
| `true` | 0 | 143 PASS, 0 FAIL | identical three lines |

The one covered tracked path is `.engineering-harness.lock` (`standard-lock`).

## 4. Tests

`python -m unittest tests.test_hash_bound_integrity tests.test_public_onboarding tests.test_standard_repository_lifecycle`: OK.

Added (VER-HBI-001 rows in parentheses):

- `FreshConsumerDoctorTests.test_init_commit_doctor_exits_zero_on_an_lf_checkout` and `..._on_a_crlf_checkout` (fresh consumer)
- `FailClosedTests.test_empty_template_class_is_vacuously_declared` and `test_empty_template_class_still_requires_its_attribute_rule` (vacuous class)
- `AttributeEffectivenessTests.test_repository_class_present_only_in_the_managed_block_is_ineffective`, rewritten on the synthetic class so its pattern does match tracked paths, and `test_repository_class_in_owner_content_is_effective` (misplaced class; issue #207 acceptance criterion 3)
- `TemplateParityTests.test_shipped_surface_names_no_candidate_only_path` and `test_the_canonical_fragment_carries_only_template_region_rules` (portability; SPEC-HBI-001 rule 10)
- `InventoryReconciliationTests.test_the_harness_data_digest_is_declared_out_of_scope_not_bound`

Retargeted: `test_untracked_declared_path_fails_closed` (now a `repository`-region
class covering nothing), `test_declares_exactly_the_specified_classes`,
`test_known_paths_resolve_to_exactly_one_class`, `test_ordering_independence`,
`test_declared_bindings_are_actually_recorded_somewhere`,
`test_template_class_present_only_in_owner_content_is_ineffective`,
`ModeArbitrationTests` (two cases), and the synthetic fixture set. Deleted:
`test_candidate_fragment_promotion_of_repository_patterns_is_pinned`, whose
pinned divergence no longer exists.

Full suite, `python scripts/run_tests.py`: 965 tests, 2 failures, 4 skipped.
A control at the base commit `03a3e22` and at `origin/main` reads the same two
failures, `test_artifact_authoring_policy...test_repository_dry_run_report_is_retained_and_matches_a_fresh_run`
and `test_release_build...test_declared_mode_set_is_what_a_posix_export_already_carries`;
neither touches a path this work order changed and both are outside its scope.
Before the scope amendment the suite read 3 failures; the third was the
lifecycle test named in section 1.

## 5. Released evaluator readings

Exact public `se-harness==0.7.1`, installed outside the checkout, run with `-I`:

| Command | Result |
| --- | --- |
| `doctor .` | 0 FAIL; `PASS managed:.gitattributes: unchanged`; the three hash-bound checks PASS (`3 classes cover 71 tracked paths`) — the released evaluator still carries the retired class and finds its paths tracked here |
| `validate .` | 1054 artifacts, 0 errors, 471 warnings |
| `preflight . --work-order WO-HBI-005 --phase start` | PASS |
| `check . --artifact WO-HBI-005 --checkpoint handoff` | section 8 |

Candidate `doctor .` on this checkout: the three hash-bound checks PASS
(`2 classes cover 64 tracked paths`); the candidate-versus-released
`distribution:*` skew lines are boundary evidence, as `AGENTS.md` describes.

Other required checks: `python scripts/validate_release_distributions.py --root .`
PASS (4 records); `python -m se_harness --help` exit 0.

## 6. Premise checks the work order named as stop conditions

- No product code path resolves `governance-migration-protocol`:
  `governance_migration.py` and `governance_migration_contract.py` hash with
  `sha256_bytes`, never through `hash_bound.resolve_mode`; `grep` finds the
  class id nowhere under `se_harness/` but the declaration itself.
- No digest comparison outcome changed: the suite's mode-arbitration and
  compare cases pass unchanged for the remaining two classes; the three
  retained evidence digests still verify (`test_predecessor_bootstrap_retirement`).
- The vacuous case cannot pass a missing rule:
  `test_empty_template_class_still_requires_its_attribute_rule` fails
  `hash-bound-attribute-effective` naming `evaluator-evidence` and
  `requires the template region`.
- This repository's own `doctor` keeps passing under both the released evaluator
  and the candidate.

## 7. Disclosures

1. The `unbound_digest_fields` reason is validated by `_REASON`
   (`^[A-Za-z0-9 ;,.()_-]+$`). The wording first tried carried an apostrophe and
   made every hash-bound check fail with `invalid unbound digest reason`; the
   committed wording conforms. Recorded in the work order.
2. One file outside the original execution scope had to change,
   `tests/test_standard_repository_lifecycle.py`; execution stopped and the
   owner amended the scope on 2026-08-28 before it was edited.
3. Windows readings are not local: this host is Linux. The `core.autocrlf=true`
   cases stand in for a Windows checkout locally; the hosted Windows lanes are
   the Windows criterion and are recorded in section 9.
4. The two suite failures of section 4 pre-exist on `origin/main`.
5. The root `.gitattributes` managed block and the owner region are untouched;
   the divergence between the candidate fragment (two lines) and the root
   managed block (six lines, released 0.7.1) is asserted by the retargeted
   lifecycle test rather than hidden.
6. `.github/workflows/`, `candidate_acceptance.py` and the `governance_migration`
   files are untouched, as the work order excludes them.

## 8. Handoff checkpoint binding

The released 0.7.1 evaluator's `check` at the handoff checkpoint binds this
evidence to the formal snapshot of the working tree at the candidate:

artifact: WO-HBI-005
checkpoint: handoff
formal_snapshot_sha256: 5f84095c72f5c2b39d627fce0c8ed1dfd8fac7d065f0a0a943a708f808ca6588

The first run, before these lines existed, was blocked only by
`QGP-G4I-EVIDENCE` (no keyed evidence for this snapshot); every other
`QG-G4-IMPLEMENTATION-EVIDENCE` predicate passed with the nine changed paths
declared and completeness asserted. The rerun result follows.

Rerun: outcome `completed`, compliance `pass`, all eight
`QG-G4-IMPLEMENTATION-EVIDENCE` predicates `pass`;
`result_sha256 adeb6b46107626ec885938944c3f9c61f57aea1bdd9ba2a1a421ac4b49c64924`.

## 9. Hosted lanes

First push (`03a3e22` base, implementation commit): the `candidate-source` job
and the candidate qualification replay failed on
`test_repository_dry_run_report_is_retained_and_matches_a_fresh_run`, the
string-form pin that had kept `main` red since #231 and that this work
order's `REQ-HBI-003`/`REQ-HBI-004` also tripped; the Windows legs were
skipped. The owner chose to fix `main` first: `WO-AUT-003` (#237, verified as
`VREC-AUT-003`) retargeted the pin, and `origin/main` was merged into this
branch as `7e317e5`.

At `7e317e5`, all thirteen checks pass: `candidate-evidence.yml` run
`33165010486` (candidate source, candidate package, deterministic integration
package, governance migration on Linux and Windows, integration package
verified on Linux and Windows, retained), `publication-rehearsal.yml` run
`33165010647` (record selection, candidate replay, release-record replay),
`validate` run `33165010478`, governor transition assessment run
`33165010485`. The Windows integration-package and governance-migration legs
are the Windows criterion of `VER-HBI-001`'s fresh-consumer row: the hosted
suite includes `FreshConsumerDoctorTests` on both `core.autocrlf` settings.
### 8.1 Re-binding after merging `main`

`origin/main` (with #237, `WO-AUT-003`) was merged into this branch as
`7e317e5` before completion, so the formal snapshot changed. Re-bound:

artifact: WO-HBI-005
checkpoint: handoff
formal_snapshot_sha256: 70f30a7230d10c52df4aace063d683757751f26d748a7829384921f26a6685a3

Rerun after merge: rerun completed pass adeb6b46107626ec885938944c3f9c61f57aea1bdd9ba2a1a421ac4b49c64924

