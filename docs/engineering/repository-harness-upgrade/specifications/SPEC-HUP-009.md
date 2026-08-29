+++
id = "SPEC-HUP-009"
type = "specification"
title = "Standard-root adoption contract for released 0.9.0, the simple way"
status = "approved"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"
[relations]
specifies = ["REQ-HUP-018", "REQ-HUP-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T06:37:01Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-29 by the accountable owner, 'i approve the artifact packet', for the adoption of exact public 0.9.0 (RLS-SEH-018, released and published 2026-08-28) as the standard root the simple way: one command from an isolated wheel-file install outside the checkout whose digest equals the record's bound wheel, no packet, candidate moved to 0.10.0 in the same change. Measured before this transition over branch state 7b6f3e1 carrying unmoved main 7291602: validate PASS at 0 errors under the governing 0.8.0 root and under public 0.9.0; rehearsal on a throwaway clone: plan 61 files, 5 update, 56 unchanged, no customization or conflict; 0.9.0 doctor 0 FAIL and released-root 143/143 after apply; the full suite on the moved root differs from the same-commit control by four tests, all resolved by owner content, the candidate version and two test edits."
+++

# Specification: Standard-root adoption contract for released 0.9.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.8.0 to exact public 0.9.0, and what must be true afterwards.
It follows `SPEC-HUP-008` (0.8.0) rule for rule; the only changes are the
identities, the smaller plan, and a pass condition for the suite that is
stated against a same-commit control rather than as "green", because the
workstation baseline is red for reasons the root does not touch.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.9.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard (`RID006`, `RID007`, `RID024`)
   and is not to be worked around.
2. Prove identity by version, installed-payload digest and archive pair
   (`SPEC-REB-012` rule 1): the wheel file's SHA-256 must equal the digest
   `RLS-SEH-018` binds before it is installed, and the lock's
   `archive_sha256` must equal it after apply. A `null` pair is a stop.
   Measured on 2026-08-29: wheel
   `c4b5617585a3cb908a3b3c14b97e1039824ca731b8acce0251888d095927f364`,
   installed payload
   `e74ad2ae73d7298ebf2ae5125f84068c5f011d96d7c6bb75a105ff45895348f7`.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path outside
   the managed set stops for amendment. Measured on 2026-08-29 against `main`
   at `7291602`: 61 files, 5 `update`, 56 unchanged, 0 `add`. The five:
   `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`,
   `ENGINEERING_HARNESS.md`, `docs/engineering/WORKFLOW.json`,
   `docs/engineering/WORKFLOW.md`.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-evaluator-upgrade.json`
   (repository-relative) as the transaction document the
   governor-transition lane requires: exactly one under
   `docs/engineering/**/evidence/`, prior lock
   `174db6dc47a4dbd12d6d695d05bfd2ef44366f788de21a19f714f344043f9770` and
   prior `tool_version 0.8.0`, target identity equal to the new lock.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged.
6. Directly after apply, exact 0.9.0 must pass `validate` (0 errors),
   `doctor` (0 FAIL), `qualify released-root`, `inspect`, a `dashboard`
   whose content is identical across two runs (only `generation-summary.json`
   may differ), and this work order's review preflight. The root copies of
   the five updated files must equal the candidate templates under
   `templates/repository/standard/` modulo the installer's substitutions
   and line endings.
7. Move the candidate to `0.10.0` in `pyproject.toml`, `se_harness/__init__.py`
   and the README install example. No scenario is written (`WO-ECP-010`) and
   `LEGACY_ACCEPTANCE_CONTRACT_SHA256` gains no entry.
8. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its 6000-byte bound) and
   `docs/notes/developing-se-harness.md`. Candidate template bytes under
   `templates/` do not move.
9. Replace pinned root and candidate assumptions in `tests/` with
   identity-aware assertions, each file named in the evidence with the
   assumption it carried. Measured on the rehearsal: the two test edits
   are both in `tests/test_ci_pipeline.py` — `0.9.0` added to the forbidden
   version-literal set asserted over the repository-owned workflows, and the
   version-bump fixture bumping past the lock's root version instead of to a
   literal `0.9.0`; every other divergence from the control is resolved by
   rules 7 and 8.
10. Run the complete `VER-HUP-009` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane assessing the
    real root transition (base 0.8.0 lock `174db6dc…` to the 0.9.0 lock,
    exactly one transaction document, the released `RLS-SEH-018` supplying
    the wheel).
11. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan path outside the managed set, a `customized` or
`conflict` action, a `null` archive pair, a failed replay, a failed graph, a
suite whose failure set differs from the control, or an unexplained warning
stops the work order; the branch is abandoned or amended under the owner's
decision, never patched around.
