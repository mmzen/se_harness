```toml
artifact = "WO-HUP-017"
checkpoint = "handoff"
formal_snapshot_sha256 = "920fcf53b02e1dd178bbc105a4d7b3489449d0c23e1144ac250f8e276b0fbcfc"
rebound_at = "2026-09-07T12:19:27Z"
```

# WO-HUP-017 handoff evidence

Retained by `harnessctl evidence`; body content is owner-authored.

## Outcome

The standard root is exact public 0.16.0: lock schema 3, `tool_version
0.16.0`, archive `a969d6ab…` equal to the wheel `RLS-SEH-025` binds,
payload `51712fcf…`, written by the simple upgrade from the isolated
wheel-file environment in one atomic transaction (48 managed files, 6
updated, the 8 retired script copies removed through the leaving-set rule,
replay 40 unchanged; forty lock entries, none under `scripts/`). This is the
first adoption in which files left the managed set. The candidate moved to
0.17.0. The 0.16.0 gate reads this graph with the same numbers the 0.15.0
gate read: 0 errors, 73 warnings, 0 advisories; the Explorer generates
identically twice. The three release workflows, the owner region,
`SPEC-IAR-012` and twelve test modules that read the root copies now read
the evaluator, as `SPEC-DST-025` bound this work order to do. The in-tree
`doctor` reports no `lock-extra` finding any more, and `WO-TCM-011` may
start after this merges.

## Evaluators

- Predecessor (approval, start): released `se-harness 0.15.0` outside the
  checkout (`C:/Users/hok/se-harness-eval-0150`), installed from the wheel
  file whose digest equals `RLS-SEH-024`.
- Governor from the transaction onward: released `se-harness 0.16.0`
  outside the checkout (`C:/Users/hok/se-harness-eval-0160`), installed
  from the wheel file downloaded from PyPI and verified against
  `RLS-SEH-025` before install; every later reading, this packet and the
  handoff check included.
- Candidate: this checkout, an LF clone (`core.autocrlf=input`) of `main`
  at `6dd288d7`, branch `governance/hup-017-adopt-0-16-0`; the transaction
  commit is `4d160466`; `pyproject.toml` reads 0.17.0 after `HUP-ADP-011`.
  The LF clone was chosen so the transaction document's prior lock digest
  is the committed blob's, `f617ff0b…`, and no line-ending deviation has to
  be recorded.

## Readings (VER-HUP-017)

| Reading | Evaluator / platform | Result |
| --- | --- | --- |
| wheel SHA-256 before install | workstation | `a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae`, equal to `RLS-SEH-025`'s distribution table (`HUP-ADP-002`) |
| `upgrade .` plan | exact 0.16.0 | 48 files, 6 `update` (`.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`, `ARTIFACT_AUTHORING.md`, `DECISION.template.md`, `SPECIFICATION.template.md`), 8 `remove` (the eight retired copies), 34 unchanged, no `add`/`adopt`/`customized`/`conflict`; equal to the rehearsal (`HUP-ADP-004`, `HUP-ADP-005`) |
| `upgrade . --apply --evidence-output …` | exact 0.16.0 | transaction complete; `WO-HUP-017-evaluator-upgrade.json` retained: prior lock `f617ff0b21265a57…` (the committed 0.15.0 LF blob), prior `tool_version 0.15.0`, target 0.16.0 with archive `a969d6ab…` and payload `51712fcf…`, fourteen plan actions, postconditions `lock_matches_target`, `no_op_replay`, no external action, no product release (`HUP-ADP-006`, `HUP-ADP-007`) |
| `upgrade .` replay | exact 0.16.0 | 40 files, 40 unchanged (`HUP-ADP-008`) |
| lock | exact 0.16.0 | `tool_version 0.16.0`, archive pair recorded, forty entries, none under `scripts/`; the eight copies gone from the tree (`HUP-ADP-008`) |
| root copies vs candidate templates | workstation | `ARTIFACT_AUTHORING.md`, `DECISION.template.md` and `SPECIFICATION.template.md` byte-equal to `templates/repository/standard/`; `.github/workflows/engineering-harness.yml` and `ENGINEERING_HARNESS.md` equal their templates with the version and project name substituted; `.engineering-harness.toml` reads `tool_version = "0.16.0"` |
| `validate --advisories` | exact 0.16.0 | 1,351 artifacts, 0 errors, 73 warnings (44 `W013`, 15 `W015`, 14 `W014`, all pre-existing), 0 advisories (`HUP-ADP-009`) |
| `doctor` | exact 0.16.0 | 97 PASS, 0 FAIL, 44 `W013` location warnings on historical records (`HUP-ADP-009`) |
| `qualify released-root .` | exact 0.16.0 | PASS; `RR001` runtime matches the target root lock, `RR002` 97/97 managed checks, `RR003` artifacts 1,351 errors 0 warnings 73, `RR004` target state unchanged (`HUP-ADP-009`) |
| `inspect` | exact 0.16.0 | exit 0; 1,351 artifacts, 4,944 relations (`HUP-ADP-009`) |
| `dashboard` twice | exact 0.16.0 | 1,608 resources, resource digest `f766c3c0e1062ccb…` over the 1,606 outside the generation summary and manifest, identical across both runs (`HUP-ADP-010`) |
| review preflight `--work-order WO-HUP-017` | exact 0.16.0 | PASS (`HUP-ADP-009`) |
| `identity --role released-evaluator` | exact 0.16.0, Windows | `passed: true`, no diagnostic, with the evaluator environment as `--expected-root`, this checkout as `--checkout-root`, the wheel and payload digests declared and isolated Python required (`HUP-ADP-001`, `HUP-ADP-002`) |
| `evaluator_facts derive` | candidate | `PRE008` with the candidate still at 0.16.0 (rehearsal, 2026-09-07); the 0.16.0 to 0.17.0 pair after `HUP-ADP-011`: `candidate_version 0.17.0`, `version 0.16.0`, payload `51712fcf…` |
| `PYTHONUTF8=1 python scripts/run_tests.py --scale full` | candidate, Windows 11 (CPython 3.13.3) | section below (`HUP-ADP-017`) |

### The Windows suite

All three runs on this Windows 11 workstation (CPython 3.13.3, 8 workers,
LF checkouts):

| Run | Root | Result |
| --- | --- | --- |
| moved root, this branch at `8d42ab20`, after `HUP-ADP-011` to `HUP-ADP-016` (detached worktree) | exact 0.16.0 | 1,265 tests, 1 error, 26 skipped |
| same-commit control (the release branch at `3caa77e8`, whose `tests/` bytes equal `main` at `6dd288d7`) | exact 0.15.0 | 1,265 tests, 1 error, 26 skipped |
| rehearsal clone at `5df10aa9`, moved root, candidate 0.17.0, no edit | exact 0.16.0 | 1,198 collected (six modules failed to import), 5 failures, 22 errors, 25 skipped |

The one error is the same name on both roots,
`test_artifact_authoring.IdentifierAllocationTests.test_allocation_refuses_outside_a_checkout_and_an_explicit_id_on_any_ref`,
the workstation baseline error every release reading of this cycle also
carries (a Windows `PermissionError` on a read-only temporary Git object
during teardown). The 26 skips are the Windows-only guards; the Linux lane
skips none. The rehearsal's 27 failing names, every one a read of a removed
root copy or of an owner sentence naming the eight, are the names
`SPEC-HUP-017` `HUP-ADP-016` lists; after the edits the failure set is the
control's, `HUP-ADP-017` satisfied.

## Identity-aware edits and switched consumers (HUP-ADP-011 to HUP-ADP-016)

- `pyproject.toml`, `se_harness/__init__.py`: 0.17.0.
- `AGENTS.md` owner region: the Graph command is `python -m se_harness
  validate .`; the eight-scripts bullet now states that no file under
  `scripts/` is managed since the 0.16.0 root; every file in `scripts/` is
  repository-owned; the candidate-source paragraph names
  `se_harness/engine/`; the evaluator instruction reads
  `se-harness==0.16.0` (`DST-ENG-015`, `HUP-ADP-012`).
- `docs/notes/developing-se-harness.md`: the identity paragraph names the
  0.17.0 candidate and the 0.16.0 root; the repository-structure block and
  the engine paragraph state that the root copies left with this work
  order; the development-check command is the evaluator's `validate`; the
  "Advancing the root evaluator" paragraph states 0.16.0 adopted by this
  work order from the wheel `RLS-SEH-025` binds, with `WO-HUP-016` joining
  the list of earlier adoptions (`HUP-ADP-013`).
- `SPEC-IAR-012`: a dated amendment record states that rules 6 and 8's
  eight `scripts/` paths and the 28-path count no longer hold under a
  0.16.0 root, the managed set being 33 paths (`DST-ENG-015`, `HUP-ADP-013`).
- `.github/workflows/release-qualification.yml` and
  `.github/workflows/release-candidate-replay.yml`: the graph is validated
  by `python -m se_harness validate .`, one line each, nothing else
  changed (`DST-ENG-016`, `HUP-ADP-014`).
- `.github/workflows/pages-publication.yml`: the Explorer is generated by
  the proven released evaluator's `dashboard` over the generation snapshot,
  the form `SPEC-DPG-001` rule 8 admits; one command replaced, nothing else
  changed (`DST-ENG-016`, `HUP-ADP-015`).
- `tests/root_identity_support.py` (new): `root_manages_scripts`,
  `evaluator_scripts_dir`, `root_copy` and `committed_copies`, each keyed
  on the lock.
- `tests/test_revision_provenance.py`, `test_artifact_catalog.py`,
  `test_artifact_authoring.py`, `test_architecture_traceability.py`,
  `test_adr_applicability.py`: `SCRIPTS` is `evaluator_scripts_dir()`; the
  first had pointed at `templates/repository/standard/scripts`, a directory
  `WO-DST-024` removed, and imported through another module's `sys.path`
  entry. `test_artifact_authoring.py` compares the root registry only when
  the lock names it.
- `tests/test_validation_taxonomy.py`, `test_predecessor_bootstrap_retirement.py`,
  `test_inspection.py`, `test_dashboard_webui.py`,
  `test_dashboard_publication.py`: the root copy is read only when the lock
  names it; otherwise the engine copy, or the copy's absence is asserted.
- `tests/test_instruction_architecture.py`: `managed_count_by_root` gains
  `"0.16.0": 33`; the `scripts/` sentence and the eight-count assertions
  are keyed on the root; the required owner fact is the new Graph command.
- `tests/test_release_build.py`, `test_release_orchestration.py`,
  `test_dashboard_publication.py`: the workflow assertions read the
  evaluator commands and assert the root-script invocations are gone.
- `ARCH-HUP-012` was amended by record on the packet branch, after the
  requirements were approved and before the start preflight, so that it
  addresses `REQ-HUP-033` and `REQ-HUP-034` and conforms to `SPEC-HUP-017`;
  without it the review preflight reported `W021`, as for `WO-HUP-016`. An
  approved architecture may not address a draft requirement (`E016`), which
  is why the amendment could not ride the draft packet.

## Material non-effects

No product byte under `se_harness/` beyond `__init__.py`'s version; no
candidate template byte under `templates/`; no release, tag, publication,
Pages or maintenance-line change; the published 0.16.0 did not move.
`RLS-SEH-025` and `VREC-SEH-025` are unchanged. No decision artifact was
raised. `WO-TCM-011` was not started.

## Hosted lanes

At the edits head `8d42ab20` (pull-request event of PR #371), three of four
lanes green before the evidence existed:

- Governor Transition Assessment 34120536918: plan phase
  `transition_required: true`, base `6dd288d7` under 0.15.0 with canonical
  lock `f617ff0b…`, target 0.16.0 with archive `a969d6ab…`, payload
  `51712fcf…` and canonical lock `69d0fb9f…`; exactly one transaction
  document, this work order's `WO-HUP-017-evaluator-upgrade.json`
  (`0efc6451…`), and the trusted release `RLS-SEH-025` (tag `v0.16.0`)
  supplying the wheel; the exact target evaluator assessed the moved root
  and the assessment made no checkout change (`HUP-ADP-019`).
- SE Harness Candidate Evidence 34120536991: source and package evidence,
  governance migration on Linux and Windows, the integration package built
  and verified on both platforms; upgrade rehearsal 0.16.0 to 0.17.0.
- Publication Rehearsal 34120537144: candidate and release-record modes
  both PASS, the release-record leg exercising the switched
  `release-qualification.yml` with `RLS-SEH-025` selected (`HUP-ADP-014`).
- Engineering Harness 34120536823: the lane installed `se-harness==0.16.0`
  from the transaction's lock and ran the 0.16.0 gate; it stopped at the
  handoff step on `QGP-G4I-EVIDENCE`, no readable evidence for this work
  order yet, the expected reading before this packet existed.

The evidence head, the completion head and the record head are checked the
same way before each act and recorded in this section as they complete.

## Disclosures

1. The packet's first draft of `SPEC-HUP-017` used the 0.15.0 root's
   specification shape and drew twenty specification advisories under the
   candidate validator, which the repository's corpus test
   (`test_reader_first_specifications`) refuses; the specification was
   rewritten in the reader-first shape with identified rules before
   approval, and the packet drew no advisory under either validator.
2. The Pages workflow's switch to `harnessctl dashboard` is exercised end to
   end only by the next release's publication; its unit tests and the
   unchanged packaging steps are the evidence available now.
