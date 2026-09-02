+++
id = "SPEC-HUP-014"
type = "specification"
title = "Standard-root adoption contract for released 0.13.0, the simple way"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[relations]
specifies = ["REQ-HUP-027", "REQ-HUP-028"]
+++

# Specification: Standard-root adoption contract for released 0.13.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.12.0 to exact public 0.13.0, and what must be true
afterwards. It follows `SPEC-HUP-013` rule for rule; the changes are the
identities, the plan, and the one visible novelty of the new root: the
designed self-contained Explorer replaces the 0.12.0 page in this
repository's own generated dashboard.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.13.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard and is not to be worked
   around.
2. Prove identity by version, installed-payload digest and archive pair:
   the wheel file's SHA-256 must equal the digest `RLS-SEH-022` binds
   before it is installed, and the lock's `archive_sha256` must equal it
   after apply. A `null` pair is a stop. Measured on 2026-09-02: wheel
   `1bbf3b747b7ebbb07fd3fd975e87e3c11049e7a6a8e1377e3d35099f4fe862ae`,
   installed payload
   `9b4cdb5f2148683f3ceaad868e64b1b4ebefbadcac49cf4cd1feccd954540bfe`.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path
   outside the managed set stops for amendment. Measured on 2026-09-02
   against `main` at `09aa69f`: 46 files, 5 `update`, 41 unchanged, 0
   `add`, 0 `remove`. The five: `.engineering-harness.toml`,
   `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`,
   `scripts/generate_harness_dashboard.py`,
   `scripts/harness_explorer/index.template.html`.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-014-evaluator-upgrade.json`
   (repository-relative) as the transaction document the
   governor-transition lane requires: exactly one under
   `docs/engineering/**/evidence/`, prior lock `4d8f9d37a91132cd` (full
   digest in the document) and prior `tool_version 0.12.0`, target identity
   equal to the new lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged. Measured: `46 files, 46 unchanged`.
6. No file leaves the managed set: the 0.12.0 lock's 46 entries and the
   0.13.0 plan name the same paths (measured). An unexpected `remove` is a
   stop for review, not a waiver.
7. Directly after apply, exact 0.13.0 must pass `validate` (0 errors, 0
   advisories), `doctor` (0 FAIL), `qualify released-root`, `inspect`, a
   `dashboard` whose content is identical across two runs and whose page
   names no remote origin, and this work order's review preflight. The root
   copies of the five updated files must equal the candidate templates
   modulo the installer's substitutions and line endings (measured: the two
   scripts equal modulo line endings).
8. Move the candidate to `0.14.0` in `pyproject.toml`,
   `se_harness/__init__.py` and the README install example; with root and
   candidate both at 0.13.0 the derivation reports `PRE008` (measured). No
   scenario and no legacy table exist to update.
9. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its byte bound: the
   evaluator instruction reads `se-harness==0.13.0`) and
   `docs/notes/developing-se-harness.md` (the candidate/root identity
   paragraph and the root-advance paragraph). Candidate template bytes
   under `templates/` do not move.
10. Replace pinned root and candidate assumptions in `tests/` with
    identity-aware assertions, each file named in the evidence with the
    assumption it carried. Measured by the rehearsal's suite comparison on
    the moved root with the candidate at 0.14.0, two modules carry pins:
    `tests/test_instruction_architecture.py` (the managed count of root
    0.13.0 is 40; the owner region names `se-harness==0.13.0`) and
    `tests/test_dashboard_webui.py` (eight tests assert the previous page's
    markers against the root copy of the Explorer template; under a root of
    0.13.0 or later the root copy equals the canonical designed template
    modulo line endings, and the previous markers apply only to an older
    root). The developer note's evaluator-and-candidate test reads the
    owner content of rule 9. No other name differs from the same-commit
    control beyond the workstation-only baseline error.
11. This work order's execution scope names no `verification-records/`
    directory; the gate admits the work order's own records by
    construction on both sides of the move (`ECP-ADM-001`).
12. Run the complete `VER-HUP-014` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing
    the real root transition (base 0.12.0 lock to the 0.13.0 lock, exactly
    one transaction document, the released `RLS-SEH-022` supplying the
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
