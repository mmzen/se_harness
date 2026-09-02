+++
id = "SPEC-HUP-015"
type = "specification"
title = "Standard-root adoption contract for released 0.14.0, the simple way"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
specifies = ["REQ-HUP-029", "REQ-HUP-030"]
+++

# Specification: Standard-root adoption contract for released 0.14.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.13.0 to exact public 0.14.0, and what must be true
afterwards. It follows `SPEC-HUP-014` rule for rule; only the identities
and the plan change, and the new root carries no behavioural novelty.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.14.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard and is not to be worked
   around.
2. Prove identity by version, installed-payload digest and archive pair:
   the wheel file's SHA-256 must equal the digest `RLS-SEH-023` binds
   before it is installed, and the lock's `archive_sha256` must equal it
   after apply. A `null` pair is a stop. Measured on 2026-09-02: wheel
   `70d438b501d374fec06f41e25571f674b3cd1f43178389e6e06b0269c92f4856`,
   installed payload
   `25034dc72a6be582ebef3c6b9a733c6ab9b6dcd879b9fda162d4d3e131a04306`.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path
   outside the managed set stops for amendment. Measured on 2026-09-02
   against `main` at `25c0ef9`: 46 files, 3 `update`, 43 unchanged, 0
   `add`, 0 `remove`. The three: `.engineering-harness.toml`,
   `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`.
4. Apply with `harnessctl upgrade . --apply` and nothing else. Retain
   `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-015-evaluator-upgrade.json`
   as the transaction document the governor-transition lane requires:
   exactly one under `docs/engineering/**/evidence/`, prior lock
   `9dfec5b4645774ed` (full digest in the document) and prior `tool_version
   0.13.0`, target identity equal to the new lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged. Measured: `46 files, 46 unchanged`.
6. No file leaves the managed set (measured). An unexpected `remove` is a
   stop for review, not a waiver.
7. Directly after apply, exact 0.14.0 must pass `validate` (0 errors, 0
   advisories), `doctor` (0 FAIL), `qualify released-root`, `inspect`, a
   `dashboard` whose content is identical across two runs, and this work
   order's review preflight. The root copies of the three updated files
   must equal the candidate templates modulo the installer's substitutions
   and line endings.
8. Move the candidate to `0.15.0` in `pyproject.toml`,
   `se_harness/__init__.py` and the README install example; with root and
   candidate both at 0.14.0 the derivation reports `PRE008` (measured).
9. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (the evaluator instruction reads
   `se-harness==0.14.0`) and `docs/notes/developing-se-harness.md` (the
   candidate/root identity paragraph and the root-advance paragraph).
   Candidate template bytes under `templates/` do not move.
10. Replace pinned root and candidate assumptions in `tests/` with
    identity-aware assertions, each file named in the evidence. Measured by
    the rehearsal's suite comparison on the moved root with the candidate
    at 0.15.0: one module carries a pin,
    `tests/test_instruction_architecture.py` (the managed count of root
    0.14.0 is 40; the owner region names `se-harness==0.14.0`); the
    dashboard tests' root-version guard of `WO-HUP-014` already admits any
    root of 0.13.0 or later. The developer note's evaluator-and-candidate
    test reads the owner content of rule 9. No other name differs from the
    same-commit control beyond the workstation-only baseline error.
11. This work order's execution scope names no `verification-records/`
    directory; the gate admits the work order's own records by
    construction on both sides of the move (`ECP-ADM-001`).
12. Run the complete `VER-HUP-015` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing
    the real root transition (base 0.13.0 lock to the 0.14.0 lock, exactly
    one transaction document, the released `RLS-SEH-023` supplying the
    wheel) and the managed lane green through completion and the record
    heads.
13. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan path outside the managed set, a `customized` or
`conflict` action, an unexpected `remove`, a `null` archive pair, a failed
replay, a failed graph, a suite whose failure set differs from the control
beyond the names rule 10 records, or an unexplained warning stops the work
order; the branch is abandoned or amended under the owner's decision, never
patched around.
