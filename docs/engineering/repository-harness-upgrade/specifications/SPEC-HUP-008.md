+++
id = "SPEC-HUP-008"
type = "specification"
title = "Standard-root adoption contract for released 0.8.0, the simple way"
status = "draft"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-28"
updated = "2026-08-28"
[relations]
specifies = ["REQ-HUP-016", "REQ-HUP-017"]
+++

# Specification: Standard-root adoption contract for released 0.8.0, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.7.1 to exact public 0.8.0, and what must be true afterwards.
It follows `SPEC-HUP-007` (0.7.1) rule for rule, with the changes that
adoption's aftermath taught: the wheel-file install that records the archive
pair, and the tests that must stop declaring a divergence that no longer
exists.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.8.0` was installed from the wheel file
   downloaded from PyPI, with `python -I -m se_harness`. A runtime resolving
   inside the checkout is refused by the guard (`RID006`, `RID007`, `RID024`)
   and is not to be worked around.
2. Prove identity by version, installed-payload digest and archive pair
   (`SPEC-REB-012` rule 1): the wheel file's SHA-256 must equal the digest
   `RLS-SEH-017` binds before it is installed, and the lock's
   `archive_sha256` must equal it after apply. A `null` pair is a stop: it is
   the condition that blocked `prepare-release` under the 0.7.1 root.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path outside
   the managed set stops for amendment. Measured on 2026-08-28 against `main`
   at `2628627`: 61 files, 9 `update`, 52 unchanged, 0 `add`.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output
   docs/engineering/repository-harness-upgrade/evidence/WO-HUP-008-evaluator-upgrade.json`
   (the path is repository-relative; an absolute path is refused) as the
   transaction document the governor-transition lane requires.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged.
6. Directly after apply, exact 0.8.0 must pass `validate` (0 errors),
   `doctor` (0 FAIL), `qualify released-root`, `inspect`, a `dashboard`
   whose content is identical across two runs (only `generation-summary.json`'s
   timestamp and elapsed time may differ), and this work order's review
   preflight.
7. Move the candidate to `0.9.0` in `pyproject.toml`, `se_harness/__init__.py`
   and the README install example. No scenario is written (`WO-ECP-010`) and
   `LEGACY_ACCEPTANCE_CONTRACT_SHA256` gains no entry: 0.8.0 carries
   `qualify candidate-package`, the typed branch of the candidate-package job.
8. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its 6000-byte bound) and
   `docs/notes/developing-se-harness.md`. Candidate template bytes under
   `templates/` do not move.
9. Replace pinned root and candidate assumptions in `tests/` with
   identity-aware assertions, each file named in the evidence with the
   assumption it carried. Where a test declared a released-0.7.1-versus-
   candidate divergence, the identity-aware form asserts the divergence when
   the root is 0.7.1 and byte-identity when the root is 0.8.0 or later, so
   the candidate templates are still asserted in both states. The retained
   stage-machine files and the owner-region `.gitattributes` rules of issue
   #210 are not deleted here; their deletion is the separate follow-up work
   order that this adoption unblocks.
10. Run the complete `VER-HUP-008` qualification and the suite; all
    pull-request lanes must pass, the governor-transition lane now assessing
    a real root transition (base 0.7.1 lock `6739fef0…` to the 0.8.0 lock,
    exactly one transaction document, the released `RLS-SEH-017` supplying
    the wheel).
11. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan path outside the managed set, a `customized` or
`conflict` action, a `null` archive pair, a failed replay, a failed graph or
suite, or an unexplained warning stops the work order; the branch is
abandoned or amended under the owner's decision, never patched around.
