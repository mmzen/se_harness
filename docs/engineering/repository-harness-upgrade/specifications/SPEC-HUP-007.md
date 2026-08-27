+++
id = "SPEC-HUP-007"
type = "specification"
title = "Standard-root adoption contract for released 0.7.1, the simple way"
status = "approved"
owners = ["technical-owner", "engineering-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"
[relations]
specifies = ["REQ-HUP-014", "REQ-HUP-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T17:43:24Z"
decided_by = "technical-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'Approve and start', for the adoption of exact public 0.7.1 as the standard root the simple way (REQ-REB-027, REQ-REB-028 shipped by RLS-SEH-016): one command from an isolated index install outside the checkout, no packet, candidate moved to 0.8.0 with its scenario in the same change. Successor to the rejected WO-HUP-006. Measured before this transition over branch state 12e9e36 carrying unmoved main 23d5781: validate PASS at 986 artifacts, 0 errors under both the governing 0.6.0 root and public 0.7.1; doctor 0 FAIL; upgrade plan 61 files, 43 add or update, 18 unchanged."
+++

# Specification: Standard-root adoption contract for released 0.7.1, the simple way

## Purpose

Bound the one transaction that moves this repository's standard root from
exact public 0.6.0 to exact public 0.7.1, and what must be true afterwards.
It replaces `SPEC-HUP-006` (0.7.0, packet-bound, never completed) for this
adoption; `SPEC-HUP-006` stays as history.

## Rules

1. Execute the evaluator only from an isolated environment outside the
   checkout in which `se-harness==0.7.1` was installed from the index, with
   `python -I -m se_harness`. A runtime resolving inside the checkout is
   refused by the guard (`RID006`, `RID007`, `RID024`) and is not to be
   worked around.
2. Prove identity by version and installed-payload digest only
   (`SPEC-REB-012` rule 1); the archive pair is `null` for an index install
   and that is not a finding.
3. Review the plan: every path must be `add` or `update` inside the managed
   set the installer declares; no `customized`, no `conflict`; a path outside
   the managed set stops for amendment.
4. Apply with `harnessctl upgrade . --apply` and nothing else: no
   `--work-order`, no packet, no declaration. Retain `--evidence-output`
   under this domain's `evidence/` as the transaction document.
5. Require an atomic write and the no-op replay: a second `upgrade .` reads
   every file unchanged.
6. Directly after apply, exact 0.7.1 must pass `validate` (0 errors),
   `doctor` (0 FAIL), `qualify released-root`, `inspect`, a deterministic
   `dashboard`, and this work order's review preflight.
7. Move the candidate to `0.8.0` in `pyproject.toml`, `se_harness/__init__.py`
   and the README install example, and write
   `tests/fixtures/governance_migration/candidate-0.7.1-to-0.8.0.json` with
   the canonical writer from the 0.7.1 pair; the 0.7.1 pair is retained as
   the previous candidate. `LEGACY_ACCEPTANCE_CONTRACT_SHA256` gains the
   `0.7.1` entry, measured from the installed evaluator.
8. Adjust owner content only where it must state the new governor
   truthfully: `AGENTS.md`'s owner region (within its 6000-byte bound) and
   `docs/notes/developing-se-harness.md`. Candidate template bytes under
   `templates/` do not move.
9. Replace pinned 0.6.0 root assumptions in `tests/` with released-root
   identity-aware assertions, each file named in the evidence with the
   assumption it carried; the candidate templates are still asserted.
10. Run the complete `VER-HUP-007` qualification and the suites on CPython
    3.14 and 3.11; all pull-request lanes must pass, the candidate-package
    job now taking the typed `qualify candidate-package` branch under the
    0.7.1 verifier (`SPEC-REB-012` rule 6).
11. Stop before commit, push, pull request, merge, verification, release or
    publication of anything beyond this work order's own commits; each of
    those is a separate decision.

## Error and recovery

A guard refusal, a plan path outside the managed set, a `customized` or
`conflict` action, a failed replay, a failed graph or suite, or an
unexplained warning stops the work order; the branch is abandoned or amended
under the owner's decision, never patched around.
