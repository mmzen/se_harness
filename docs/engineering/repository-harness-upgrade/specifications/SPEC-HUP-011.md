+++
id = "SPEC-HUP-011"
type = "specification"
title = "Standard-root adoption contract for released 0.11.0, the simple way"
status = "draft"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
specifies = ["REQ-HUP-022", "REQ-HUP-023"]
+++

# Specification: Standard-root adoption contract for released 0.11.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.10.0 to exact public 0.11.0, and what must be true
afterwards. It follows `SPEC-HUP-010` rule for rule; the changes are the
identities, the plan, the explicit removal of the files 0.11.0 no longer
ships (issue #271), and the retirement of the interim records-directory
scoping rule.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.11.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard (`RID006`, `RID007`, `RID024`)
   and is not to be worked around.
2. Prove identity by version, installed-payload digest and archive pair
   (`SPEC-REB-012` rule 1): the wheel file's SHA-256 must equal the digest
   `RLS-SEH-020` binds before it is installed, and the lock's
   `archive_sha256` must equal it after apply. A `null` pair is a stop.
   Measured on 2026-08-29: wheel
   `ba26ab7be14321cdc26b69d59e2b894d544c3e7b529227de1f24ad9cd8f935c0`,
   installed payload
   `71b4b5b694111a42785328f4b742f40e5654d7d4c67d88b9939a6c80213dd016`.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path outside
   the managed set stops for amendment. Measured on 2026-08-29 against `main`
   at `896f8fa`: 46 files, 9 `update`, 37 unchanged, 0 `add`. The nine:
   `.agents/skills/harness-orient/SKILL.md`,
   `.agents/skills/harness-orient/scripts/orient.py`,
   `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`,
   `ENGINEERING_HARNESS.md`, `docs/engineering/WORKFLOW.json`,
   `docs/engineering/WORKFLOW.md`,
   `docs/engineering/templates/WORK_ORDER.template.md`,
   `scripts/validate_engineering_artifacts.py`.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-011-evaluator-upgrade.json`
   (repository-relative) as the transaction document the
   governor-transition lane requires: exactly one under
   `docs/engineering/**/evidence/`, prior lock `aeb73cc732474289` (full
   digest in the document) and prior `tool_version 0.10.0`, target identity
   equal to the new lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged.
6. Remove, in the same work order and as its own act, the fifteen files the
   0.10.0 lock managed and the 0.11.0 plan does not name:
   `.agents/skills/{harness-draft-change,harness-execute-work-order,harness-prepare-assurance}/**`
   (twelve files) and `.claude/skills/{same three}/SKILL.md`. The installer
   plans no `remove` (issue #271); the removal is recorded as a deviation
   from `SPEC-ECP-007` `ECP-SKL-004`'s expectation, not waived.
7. Directly after apply and removal, exact 0.11.0 must pass `validate`
   (0 errors), `doctor` (0 FAIL), `qualify released-root`, `inspect`, a
   `dashboard` whose content is identical across two runs (only
   `generation-summary.json` may differ), and this work order's review
   preflight. The root copies of the nine updated files must equal the
   candidate templates modulo the installer's substitutions and line
   endings.
8. Move the candidate to `0.12.0` in `pyproject.toml`,
   `se_harness/__init__.py` and the README install example. No scenario is
   written (`WO-ECP-010`) and `LEGACY_ACCEPTANCE_CONTRACT_SHA256` gains no
   entry.
9. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its 6000-byte bound) and
   `docs/notes/developing-se-harness.md`. Candidate template bytes under
   `templates/` do not move.
10. Replace pinned root and candidate assumptions in `tests/` with
    identity-aware assertions, each file named in the evidence with the
    assumption it carried; the tests that declared the 0.10.0 root's
    divergences from the candidate template (the validator's three-block
    deletion, the work-order template's delegation table, the `scope`
    checkpoint paragraphs) take their equality branch on the 0.11.0 root
    and must keep the declared-divergence branch for an older root.
11. This work order's execution scope names no `verification-records/`
    directory: the 0.11.0 gate admits the work order's own records by
    construction (`ECP-ADM-001`), and the record heads of its pull request
    are `VER-ECP-012`'s hosted demonstration.
12. Run the complete `VER-HUP-011` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing the
    real root transition (base 0.10.0 lock to the 0.11.0 lock, exactly one
    transaction document, the released `RLS-SEH-020` supplying the wheel)
    and the managed lane green through completion and the record heads.
13. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan path outside the managed set, a `customized` or
`conflict` action, a `null` archive pair, a failed replay, a failed graph, a
suite whose failure set differs from the control, or an unexplained warning
stops the work order; the branch is abandoned or amended under the owner's
decision, never patched around.
