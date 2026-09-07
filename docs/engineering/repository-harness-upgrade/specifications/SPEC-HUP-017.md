+++
id = "SPEC-HUP-017"
type = "specification"
title = "Standard-root adoption contract for released 0.16.0, the simple way, with the retired scripts leaving"
status = "draft"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-07"
updated = "2026-09-07"

[relations]
specifies = ["REQ-HUP-033", "REQ-HUP-034"]
+++

# Specification: Standard-root adoption contract for released 0.16.0, the simple way, with the retired scripts leaving

## Purpose

Fix the exact procedure, identities and readings by which this repository
moves its standard root from exact public 0.15.0 to exact public 0.16.0
with one `harnessctl upgrade --apply` from an isolated wheel-file install,
by which the eight retired script copies leave, by which the last consumers
of those copies are switched to the evaluator, and by which the move is
proven. The figures below were measured on 2026-09-07 on a throwaway clone
of `main` at `5df10aa9` created with `core.autocrlf=input`; the real
transaction is compared with them.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.16.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard and is not to be worked
   around.
2. Prove identity by version, installed-payload digest and archive pair:
   the wheel file's SHA-256 must equal the digest `RLS-SEH-025` binds
   before it is installed, and the lock's `archive_sha256` must equal it
   after apply. A `null` pair is a stop. Measured on 2026-09-07: wheel
   `a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae`,
   installed payload
   `51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c`.
3. Review the plan: every path must be `update` inside the managed set or
   `remove` of one of the eight retired copies `SPEC-DST-025` names; no
   `add`, `adopt`, `customized` or `conflict`; any other path stops for
   amendment. Measured against `main` at `5df10aa9`: 48 files, 6 `update`,
   8 `remove`, 34 unchanged. The updates: `.engineering-harness.toml`,
   `.github/workflows/engineering-harness.yml` (its `SE_HARNESS_VERSION`
   alone), `ENGINEERING_HARNESS.md`, `docs/engineering/ARTIFACT_AUTHORING.md`,
   `docs/engineering/templates/DECISION.template.md` and
   `docs/engineering/templates/SPECIFICATION.template.md`. The removes:
   `scripts/validate_engineering_artifacts.py`,
   `scripts/generate_harness_dashboard.py`,
   `scripts/inspect_engineering_artifacts.py`,
   `scripts/select_harness_work_order.py`,
   `scripts/artifact_layout_registry.py`,
   `scripts/check_engineering_harness.sh`,
   `scripts/check_engineering_harness.ps1` and
   `scripts/harness_explorer/index.template.html`, each byte-identical to
   its lock entry, under the leaving-set rule (`DST-ENG-011`).
4. Apply with `harnessctl upgrade . --apply` and nothing else. Retain
   `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-017-evaluator-upgrade.json`
   as the transaction document the governor-transition lane requires:
   exactly one under `docs/engineering/**/evidence/`, prior `tool_version
   0.15.0`, prior lock digest equal to the committed 0.15.0 lock (measured
   `f617ff0b21265a57…` on the LF clone, equal to the blob), target identity
   equal to the new lock, the fourteen plan actions recorded.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every remaining file unchanged. Measured: `40 files, 40 unchanged`.
6. Exactly the eight retired copies leave the managed set and the lock, and
   nothing else does; the written lock carries forty entries and no
   `scripts/` path (`DST-ENG-013`, measured). A `remove` outside the eight
   is a stop for review, not a waiver.
7. Directly after apply, exact 0.16.0 must pass `validate` (0 errors, 0
   advisories), `doctor` (0 FAIL), `qualify released-root`, `inspect`, a
   `dashboard` whose resource digests are identical across two runs, and
   this work order's review preflight. Measured: 1,346 artifacts, 0 errors,
   73 warnings (44 `W013`, 15 `W015`, 14 `W014`, every one pre-existing and
   equal to the 0.15.0 reading of the same commit), 0 advisories; `doctor`
   97 PASS, 0 FAIL (the 116 of 0.15.0 less the nineteen checks the eight
   copies carried); `RR001` to `RR004` PASS with 97/97 managed checks;
   `inspect` exit 0; 1,603 Explorer resources, the 1,601 outside the
   generation summary and manifest carrying one digest across both runs.
   The root copies of the six updated files must equal the candidate
   templates modulo the installer's substitutions and line endings.
8. Move the candidate to `0.17.0` in `pyproject.toml` and
   `se_harness/__init__.py`. With root and candidate both at 0.16.0 the
   derivation reports `PRE008` (measured); with the candidate at 0.17.0 it
   yields the 0.16.0 to 0.17.0 pair (measured).
9. Adjust owner content only where it must state the new governor
   truthfully, and where `DST-ENG-015` binds this work order: in
   `AGENTS.md`'s owner region the Graph command becomes the evaluator's
   `validate`, the eight-scripts bullet and the "remaining files in
   `scripts/`" sentence state that no `scripts/` path is managed since the
   0.16.0 root and that every file there is repository-owned, the
   candidate-source paragraph names `se_harness/engine/` as the home of the
   evaluator's scripts, and the evaluator instruction reads
   `se-harness==0.16.0`; `docs/notes/developing-se-harness.md` follows in
   its identity paragraph, its repository-structure block, its
   development-environment command and its root-advance paragraph;
   `SPEC-IAR-012` receives a dated amendment record stating that rules 6
   and 8's eight `scripts/` paths and the managed-path count no longer hold
   under a 0.16.0 root. Candidate template bytes under `templates/` do not
   move.
10. Replace pinned root assumptions in `tests/` with identity-aware
    assertions keyed on whether the lock names a `scripts/` path, each file
    named in the evidence. Measured by the rehearsal's suite on the moved
    root with the candidate at 0.17.0 and no edit: 1,198 tests collected
    (six modules failed to import), 5 failures, 22 errors, 25 skips, against
    the control's 1,265 tests, 1 error, 26 skips. The names:
    `tests/test_revision_provenance.py`, `tests/test_artifact_catalog.py`,
    `tests/test_artifact_authoring.py`,
    `tests/test_architecture_traceability.py` and
    `tests/test_adr_applicability.py` put the root `scripts/` directory on
    `sys.path` to import the layout registry or the Explorer generator, and
    `tests/test_cli_shape.py` and `tests/test_artifact_authoring_policy.py`
    fail with them; they must import the evaluator's engine copies when the
    lock names no `scripts/` path. `tests/test_validation_taxonomy.py`
    reads the root validator's source; `tests/test_predecessor_bootstrap_retirement.py`
    reads the root validator, generator and Explorer template;
    `tests/test_inspection.py` compares the root inspector with its lock
    digest; `tests/test_dashboard_webui.py` reads the root Explorer template
    in twelve tests; `tests/test_dashboard_publication.py` binds the notice
    boundary to both templates: each reads the root copy only when the lock
    names it and otherwise the engine copy, or asserts that the canonical
    template is the only committed Explorer source.
    `tests/test_instruction_architecture.py` declares
    `managed_count_by_root` and needs `"0.16.0": 33`, the 41 of 0.15.0 less
    the eight; its `scripts/` sentence and eight-count assertions apply only
    to a root that manages scripts; its required owner facts read rule 9's
    Graph command and `se-harness==0.16.0`.
    `tests/test_progressive_documentation.py` reads rule 9's note (`0.17.0`
    named). `tests/test_release_build.py`,
    `tests/test_release_orchestration.py` and
    `tests/test_dashboard_publication.py` pin the three workflows' script
    invocations and must read rule 11's evaluator commands. No other name
    differs from the control beyond the workstation-only baseline error.
11. Switch the three repository-owned workflows `DST-ENG-016` names from
    root scripts to evaluator commands, changing nothing else in them:
    `.github/workflows/release-qualification.yml` and
    `.github/workflows/release-candidate-replay.yml` validate the graph with
    `python -m se_harness validate .` from the checkout they already run
    the candidate from, in place of
    `python scripts/validate_engineering_artifacts.py --root .`;
    `.github/workflows/pages-publication.yml` generates the Explorer with
    the released evaluator it has already acquired and proven,
    `"$RUNNER_TEMP/evaluator-env/bin/python" -I -m se_harness dashboard`
    over the generation snapshot with `--output` to the staging directory,
    in place of the snapshot's `scripts/generate_harness_dashboard.py`; this
    is the `harnessctl dashboard` form `SPEC-DPG-001` rule 8 admits, and the
    generator is the one the governance commit's lock names, as rule 7
    intends.
12. This work order's execution scope names no `verification-records/`
    directory; the gate admits the work order's own records by
    construction on both sides of the move (`ECP-ADM-001`).
13. Run the complete `VER-HUP-017` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing
    the real root transition (base 0.15.0 lock to the 0.16.0 lock, exactly
    one transaction document, the released `RLS-SEH-025` supplying the
    wheel) and the managed lane green through completion and the record
    heads.
14. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan outside the measured shape, a `customized` retired
copy, a `null` archive pair, a failed replay, a failed reading of rule 7 or
a suite whose failure set differs from the control beyond rule 10's names
stops the work order before any commit; the branch is amended or abandoned
under the owner's decision. The transaction itself is atomic: a failed write
or postcondition restores the pre-write snapshot.

## Explicitly unspecified decisions

The name of the external environment; the wording of the owner-content
statements and the amendment record; the order in which the readings are
taken; the exact identity-aware form of each test edit.
