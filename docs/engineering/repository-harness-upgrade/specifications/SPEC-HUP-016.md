+++
id = "SPEC-HUP-016"
type = "specification"
title = "Standard-root adoption contract for released 0.15.0, the simple way"
status = "approved"
owners = ["technical-owner", "engineering-owner"]
created = "2026-09-05"
updated = "2026-09-05"

[relations]
specifies = ["REQ-HUP-031", "REQ-HUP-032"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-05T08:35:42Z"
decided_by = "technical-owner"
reason = "Approved by the accountable repository owner on 2026-09-05 with the instruction 'i appprove' (approve), after reviewing PR #352 (REQ-HUP-031, REQ-HUP-032, SPEC-HUP-016, VER-HUP-016, WO-HUP-016) and the rehearsal of the 0.15.0 root adoption on a throwaway clone of main at e4192ed."
+++

# Specification: Standard-root adoption contract for released 0.15.0, the simple way

## Purpose

Fix the exact procedure, identities and readings by which this repository
moves its standard root from exact public 0.14.0 to exact public 0.15.0
with one `harnessctl upgrade --apply` from an isolated wheel-file install,
and by which the move is proven. The figures below were measured on
2026-09-05 on a throwaway clone of `main` at `e4192ed` created with
`core.autocrlf=false`; the real transaction is compared with them.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.15.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard and is not to be worked
   around.
2. Prove identity by version, installed-payload digest and archive pair:
   the wheel file's SHA-256 must equal the digest `RLS-SEH-024` binds
   before it is installed, and the lock's `archive_sha256` must equal it
   after apply. A `null` pair is a stop. Measured on 2026-09-05: wheel
   `eb09343f65a52ecc7511aacbe7f4cc546cfe4bf28eeed62cf3ff2bccf838d947`,
   installed payload
   `11e4ad03da90093dc1f4bd1ac7fed746c157162187019d7b6feb37873d3a237e`.
3. Review the plan: every path must be `add`, `update` or `adopt` inside
   the managed set the installer declares; no `customized`, no `conflict`;
   a path outside the managed set stops for amendment. Measured against
   `main` at `e4192ed`: 48 files, 19 `update`, 1 `add`, 1 `adopt`, 27
   unchanged, 0 `remove`. The updates: `.engineering-harness.toml`,
   `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`,
   `docs/engineering/ARTIFACT_AUTHORING.md`, `DECISION_RIGHTS.md`,
   `QUALITY_GATES.json`, `QUALITY_GATES.md`, `TRACEABILITY.md`,
   `WORKFLOW.json`, `WORKFLOW.md`, the templates `CAPABILITY`, `INTENT`,
   `REQUIREMENT` and the templates `README.md`, and the five managed
   scripts `artifact_layout_registry.py`, `generate_harness_dashboard.py`,
   `harness_explorer/index.template.html`,
   `inspect_engineering_artifacts.py`,
   `validate_engineering_artifacts.py`. The add:
   `docs/engineering/templates/DECISION.template.md`. The adopt: this
   repository's own `GLOSSARY.md` at the root, which the installer records
   as a seed and never rewrites; its bytes do not change.
4. Apply with `harnessctl upgrade . --apply` and nothing else. Retain
   `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-016-evaluator-upgrade.json`
   as the transaction document the governor-transition lane requires:
   exactly one under `docs/engineering/**/evidence/`, prior `tool_version
   0.14.0`, prior lock digest equal to the committed 0.14.0 lock (measured
   `0425fccf0578c52f…` on the LF clone), target identity equal to the new
   lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged. Measured: `48 files, 48 unchanged`.
6. No file leaves the managed set (measured). An unexpected `remove` is a
   stop for review, not a waiver.
7. Directly after apply, exact 0.15.0 must pass `validate` (0 errors, 0
   advisories), `doctor` (0 FAIL), `qualify released-root`, `inspect`, a
   `dashboard` whose resource digests are identical across two runs, and
   this work order's review preflight. Measured: 1,310 artifacts, 0 errors,
   71 warnings (42 `W013`, 15 `W015`, 14 `W014`, every one pre-existing), 0
   advisories; `doctor` 116 PASS, 0 FAIL; `RR001` to `RR004` PASS;
   `inspect` exit 0; 1,557 Explorer resources with one digest across both
   runs, the generation summary alone carrying a timestamp. The root copies
   of the 19 updated files and the added template must equal the candidate
   templates modulo the installer's substitutions and line endings.
8. Move the candidate to `0.16.0` in `pyproject.toml` and
   `se_harness/__init__.py`; the README no longer pins a version in its
   install lines. With root and candidate both at 0.15.0 the derivation
   reports `PRE008` (measured); with the candidate at 0.16.0 it yields the
   0.15.0 to 0.16.0 pair (measured).
9. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (the evaluator instruction reads
   `se-harness==0.15.0`) and `docs/notes/developing-se-harness.md` (the
   candidate/root identity paragraph and the root-advance paragraph).
   Candidate template bytes under `templates/` do not move.
10. Replace pinned root and candidate assumptions in `tests/` with
    identity-aware assertions, each file named in the evidence. Measured by
    the rehearsal's suite comparison on the moved root with the candidate
    at 0.16.0: two modules carry a pin. `tests/test_instruction_architecture.py`
    declares the managed count per root (`managed_count_by_root`) and needs
    `"0.15.0": 41`, the 40 managed files of 0.14.0 plus
    `DECISION.template.md`; its owner-region test reads rule 9's
    `se-harness==0.15.0`. `tests/test_validation_taxonomy.py` pins three
    predicate rows of the root `QUALITY_GATES.md` without the
    `QGP-G*-DECISION` predicates 0.15.0 adds, and its equality branch on a
    root carrying `decision_gate_clear` must compare canonical and root
    copies directly. The developer-note test of
    `tests/test_progressive_documentation.py` reads the owner content of
    rule 9 (`0.16.0` named). The rehearsal also failed
    `tests/test_dashboard_webui.py`'s source-URL assertion, because the
    throwaway clone's remote is a local path and not the GitHub origin; that
    is a rehearsal artefact, not a pin, and the real checkout is expected to
    pass it. No other name differs from the same-commit control beyond the
    workstation-only baseline error.
11. This work order's execution scope names no `verification-records/`
    directory; the gate admits the work order's own records by
    construction on both sides of the move (`ECP-ADM-001`).
12. Run the complete `VER-HUP-016` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing
    the real root transition (base 0.14.0 lock to the 0.15.0 lock, exactly
    one transaction document, the released `RLS-SEH-024` supplying the
    wheel) and the managed lane green through completion and the record
    heads.
13. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan outside the measured shape, a `null` archive pair,
a failed replay, a failed reading of rule 7 or a suite whose failure set
differs from the control beyond rule 10's names stops the work order
before any commit; the branch is amended or abandoned under the owner's
decision. The transaction itself is atomic: a failed write or
postcondition restores the pre-write snapshot.

## Explicitly unspecified decisions

The name of the external environment; the wording of the owner-content
statements; the order in which the readings are taken; the exact
identity-aware form of each test edit.
