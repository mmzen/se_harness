+++
id = "SPEC-HUP-010"
type = "specification"
title = "Standard-root adoption contract for released 0.10.0, the simple way"
status = "draft"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
specifies = ["REQ-HUP-020", "REQ-HUP-021"]
+++

# Specification: Standard-root adoption contract for released 0.10.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.9.0 to exact public 0.10.0, and what must be true afterwards.
It follows `SPEC-HUP-009` (0.9.0) rule for rule; the changes are the
identities, the plan, and the fact that this root's own evaluator can now
run every checkpoint on the Windows checkout, so no reading needs a Linux
environment.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.10.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard (`RID006`, `RID007`, `RID024`)
   and is not to be worked around.
2. Prove identity by version, installed-payload digest and archive pair
   (`SPEC-REB-012` rule 1): the wheel file's SHA-256 must equal the digest
   `RLS-SEH-019` binds before it is installed, and the lock's
   `archive_sha256` must equal it after apply. A `null` pair is a stop.
   Measured on 2026-08-29: wheel
   `e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3`,
   installed payload
   `723c98ecf21a853441ead771956af7aed6564fcffb97389c0468b9376214235d`.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path outside
   the managed set stops for amendment. Measured on 2026-08-29 against `main`
   at `47f67de`: 61 files, 6 `update`, 55 unchanged, 0 `add`. The six:
   `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`,
   `ENGINEERING_HARNESS.md`, `docs/engineering/QUALITY_GATES.json`,
   `docs/engineering/QUALITY_GATES.md`, `docs/engineering/WORKFLOW.md`.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010-evaluator-upgrade.json`
   (repository-relative) as the transaction document the
   governor-transition lane requires: exactly one under
   `docs/engineering/**/evidence/`, prior lock
   `fb61f1fee6a6d796` (full digest in the document) and prior
   `tool_version 0.9.0`, target identity equal to the new lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged.
6. Directly after apply, exact 0.10.0 must pass `validate` (0 errors),
   `doctor` (0 FAIL), `qualify released-root`, `inspect`, a `dashboard`
   whose content is identical across two runs (only `generation-summary.json`
   may differ), and this work order's review preflight. The root copies of
   the six updated files must equal the candidate templates modulo the
   installer's substitutions and line endings.
7. Move the candidate to `0.11.0` in `pyproject.toml`, `se_harness/__init__.py`
   and the README install example. No scenario is written (`WO-ECP-010`) and
   `LEGACY_ACCEPTANCE_CONTRACT_SHA256` gains no entry.
8. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its 6000-byte bound) and
   `docs/notes/developing-se-harness.md`. Candidate template bytes under
   `templates/` do not move.
9. Replace pinned root and candidate assumptions in `tests/` with
   identity-aware assertions, each file named in the evidence with the
   assumption it carried. Measured on the rehearsal: the only test edit is
   `0.10.0` added to the forbidden version-literal set that
   `tests/test_ci_pipeline.py` asserts over the repository-owned workflows;
   every other divergence from the control is resolved by rules 7 and 8.
10. Run the complete `VER-HUP-010` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing the
    real root transition (base 0.9.0 lock to the 0.10.0 lock, exactly one
    transaction document, the released `RLS-SEH-019` supplying the wheel)
    and the managed lane running, for the first time on this repository,
    the state-independent `scope` gate of 0.10.0 — which must stay green
    through the completion transition (`VER-ECP-009` scenario 6).
11. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan path outside the managed set, a `customized` or
`conflict` action, a `null` archive pair, a failed replay, a failed graph, a
suite whose failure set differs from the control, or an unexplained warning
stops the work order; the branch is abandoned or amended under the owner's
decision, never patched around.
