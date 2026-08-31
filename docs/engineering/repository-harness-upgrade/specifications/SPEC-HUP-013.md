+++
id = "SPEC-HUP-013"
type = "specification"
title = "Standard-root adoption contract for released 0.12.0, the simple way"
status = "draft"
owners = ["technical-owner", "security-owner"]
created = "2026-08-31"
updated = "2026-08-31"

[relations]
specifies = ["REQ-HUP-025", "REQ-HUP-026"]
+++

# Specification: Standard-root adoption contract for released 0.12.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.11.0 to exact public 0.12.0, and what must be true
afterwards. It follows `SPEC-HUP-011` rule for rule; the changes are the
identities, the plan, and two retirements the new root makes real: nothing
leaves the managed set this time (and the installer's own `remove` action,
`WO-DST-022`, would handle it if it did), and the gate's own numbers change
(advisories apart, `W024` retired).

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.12.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard and is not to be worked
   around.
2. Prove identity by version, installed-payload digest and archive pair:
   the wheel file's SHA-256 must equal the digest `RLS-SEH-021` binds
   before it is installed, and the lock's `archive_sha256` must equal it
   after apply. A `null` pair is a stop. Measured on 2026-08-31: wheel
   `639edbeed4bdca7c9e21a5eb2afc3b9fc993ddb3f66177eec962f1646a545811`,
   installed payload
   `0df83ce9c9bb6d456f3244f517031753daee740bb22180a492f835d25831ee0d`.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path
   outside the managed set stops for amendment. Measured on 2026-08-31
   against `main` at `63889f7`: 46 files, 8 `update`, 38 unchanged, 0
   `add`, 0 `remove`. The eight: `.engineering-harness.toml`,
   `.github/workflows/engineering-harness.yml`, `ENGINEERING_HARNESS.md`,
   `docs/engineering/DECISION_RIGHTS.md`, `docs/engineering/WORKFLOW.json`,
   `docs/engineering/WORKFLOW.md`,
   `docs/engineering/templates/WORK_ORDER.template.md`,
   `scripts/validate_engineering_artifacts.py`.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-013-evaluator-upgrade.json`
   (repository-relative) as the transaction document the
   governor-transition lane requires: exactly one under
   `docs/engineering/**/evidence/`, prior lock `e3f7039416fdec4f` (full
   digest in the document) and prior `tool_version 0.11.0`, target identity
   equal to the new lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged.
6. No file leaves the managed set: the 0.11.0 lock's 46 entries and the
   0.12.0 plan name the same paths (measured). A leaving file would be a
   plan `remove` executed by the installer itself (`WO-DST-022`); an
   unexpected `remove` is a stop for review, not a waiver.
7. Directly after apply, exact 0.12.0 must pass `validate` (0 errors, 0
   advisories in the default count), `doctor` (0 FAIL), `qualify
   released-root`, `inspect`, a `dashboard` whose content is identical
   across two runs, and this work order's review preflight. The root
   copies of the eight updated files must equal the candidate templates
   modulo the installer's substitutions and line endings.
8. Move the candidate to `0.13.0` in `pyproject.toml`,
   `se_harness/__init__.py` and the README install example. No scenario
   and no legacy table exist to update (`WO-ECP-010`, `WO-REB-031`).
9. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its byte bound — the
   evaluator instruction reads `se-harness==0.12.0`, and the pull-request
   trap states the live-body lane the 0.12.0 root installs) and
   `docs/notes/developing-se-harness.md`. Candidate template bytes under
   `templates/` do not move.
10. Replace pinned root and candidate assumptions in `tests/` with
    identity-aware assertions, each file named in the evidence with the
    assumption it carried. Measured by the rehearsal's suite comparison:
    `tests/test_instruction_architecture.py` (the managed count of root
    0.12.0 is 40; the operational-fact pin moves from the stored-payload
    sentence to the live-body sentence) and the two owner-content files of
    rule 9; no other name differs from the same-commit control.
11. This work order's execution scope names no `verification-records/`
    directory; the gate admits the work order's own records by
    construction on both sides of the move (`ECP-ADM-001`).
12. Run the complete `VER-HUP-013` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing
    the real root transition (base 0.11.0 lock to the 0.12.0 lock, exactly
    one transaction document, the released `RLS-SEH-021` supplying the
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
