+++
id = "WO-HUP-009"
type = "work_order"
title = "Adopt exact public 0.9.0 as the standard root, the simple way"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/repository-harness-upgrade/", "docs/notes/developing-se-harness.md", "pyproject.toml", "se_harness/__init__.py", "tests/"]

[relations]
implements = ["REQ-HUP-018", "REQ-HUP-019"]
specifications = ["SPEC-HUP-009"]
architecture = ["ARCH-HUP-007"]
verification = ["VER-HUP-009"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T06:37:22Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'i approve the artifact packet and you can start WO-HUP-009', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared simple upgrade from an isolated 0.9.0 wheel-file install outside the checkout, the owner statements, the candidate move to 0.10.0, the identity-aware test changes and the retained evidence, inside the declared execution scope. It authorizes no verification record, no release, no publication and no change to the guard. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T06:37:42Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'you can start WO-HUP-009'. Start preflight PASS with no diagnostics over the approval commit 420d74d carrying unmoved main 7291602, run with the governing exact public 0.8.0 evaluator outside the checkout. Bounded to the declared execution scope; the applying runtime is exact public 0.9.0 installed from the digest-verified PyPI wheel file into an isolated environment outside the checkout. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-29T07:23:02Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-08-29 under DR-WO-COMPLETE, 'Mark WO-HUP-009 implemented', on the handoff check reading Completed over the Git-derived change set of 22 paths, formal snapshot eb25d0239c9ac6945c95552b8ca17fd7bab3a5316c770c47127f78af902f1875, result d91dd8c0, no scope amendment. The root moved from exact public 0.8.0 to exact public 0.9.0 by one upgrade --apply from a wheel-file install outside the checkout whose digest c4b56175 equals the wheel RLS-SEH-018 binds; lock records that archive pair and payload e74ad2ae; plan 5 update, replay 61 unchanged. Readings under the 0.9.0 root, isolated mode: validate PASS at 1096 artifacts, 0 errors, 475 maintenance warnings; doctor 0 FAIL; released-root 143/143; dashboard content deterministic; derive 0.9.0 to 0.10.0. Candidate: full suite 1117 tests failing nothing a same-commit control on the unmoved root does not. All thirteen pull-request lanes pass on #253 at 5957139 and 10e1994 including the governor transition assessment of the real transition and 0.9.0's unconditional scope gate. Two product observations outside this work order are disclosed in the packet: the Windows backslash refusal (issue #254) and the line-ending-dependent formal snapshot. This authorizes no further act."
+++

# Work Order: Adopt exact public 0.9.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It follows `WO-HUP-008` (0.8.0) and is the
acceptance in the wild of `RLS-SEH-018`.

Commit-bound verification is `required`: the root this work order writes is
what every later gate runs under.

## Objective

Use exact public 0.9.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-018` binds, to replace the 0.8.0 standard root with one
evidence-bound 0.9.0 root by the simple upgrade — one command, no packet —
and prove the complete graph and the repository suite under the new root,
without changing product, release, publication, deployment, maintenance or
external state.

## In scope

- Prove the installed 0.9.0 identity (version, payload digest, archive pair
  equal to the published wheel) from the isolated environment;
  `SPEC-HUP-009` rules 1 and 2. Rehearsed on 2026-08-29 on a throwaway
  clone of `main` at `7291602`: wheel `se_harness-0.9.0-py3-none-any.whl`
  `c4b5617585a3cb908a3b3c14b97e1039824ca731b8acce0251888d095927f364`,
  payload `e74ad2ae73d7298ebf2ae5125f84068c5f011d96d7c6bb75a105ff45895348f7`.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict` (rule 3). Measured: 61 files, 5
  `update`, 56 unchanged.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured: replay 61 unchanged;
  prior lock `174db6dc…`, prior `tool_version 0.8.0`.
- Update owner content only where it must state the new governor: the
  `se-harness==0.8.0` instruction in `AGENTS.md`'s owner region, and the
  candidate/root statements in `docs/notes/developing-se-harness.md`
  (rule 8).
- Move the candidate to `0.10.0` (`pyproject.toml`, `se_harness/__init__.py`,
  the README install example); no scenario, no legacy-contract entry
  (rule 7). Measured: with the candidate left at 0.9.0, `evaluator_facts
  derive` raises `PRE008`; at 0.10.0 it yields the 0.9.0 to 0.10.0 pair.
- Replace pinned root and candidate assumptions in `tests/` with
  identity-aware assertions, each named in the evidence (rule 9). The
  rehearsal compared the full suite on the moved root against a control on
  the unmoved root at the same commit: 1117 tests each; exactly four names
  differ, all in the direction of the move — three
  `test_ci_pipeline.PredecessorDerivationTests` (`PRE008`, the candidate
  version) and
  `test_instruction_architecture…test_owner_region_directs_the_evaluator_outside_the_checkout`
  (the owner region). The test edits are the `0.9.0` literal added to the
  forbidden version set for repository-owned workflows and the version-bump
  fixture that bumped to a literal `0.9.0`.
- Run the complete `VER-HUP-009` qualification and the suite, and retain the
  evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
`release/0.9` line; credentials; the published 0.9.0 itself, which does not
move; the workstation-only suite failures the control also reads; any change
to the guard when it refuses.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted; the order of readings.

## Constraints

- The applying runtime is exact public 0.9.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal by
  the guard is a stop, not a thing to bypass.
- No `customized` or `conflict` action may be waived; a `null` archive pair
  is a stop.
- The complete graph must pass exact 0.9.0 directly after apply.
- Candidate template bytes must remain unchanged.

## Expected change surface

The 5 reviewed `update` paths and the installer-owned lock; `AGENTS.md`'s
owner region and `docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; `tests/test_ci_pipeline.py`; this
packet, the domain index, the transaction JSON and the evidence.

## Required verification

Execute `VER-HUP-009` in full; repository-required checks; the pull
request's lanes green; the handoff check over the complete changed-path set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-009-verification.md`
and `WO-HUP-009-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, a `null` archive pair, a partial transaction, a failed replay, a
failed graph, a suite whose failure set differs from the control, an
unexplained warning, a product or release byte moved beyond the version
identity, a test that cannot assert the released root without weakening the
candidate-template assertion, or a need for authority beyond the approved
stage.

## Completion report format

The evidence file, the changed-path ledger, the handoff `check` restitution;
the completion decision is the engineering owner's.
