+++
id = "WO-HUP-010"
type = "work_order"
title = "Adopt exact public 0.10.0 as the standard root, the simple way"
status = "in_progress"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "docs/engineering/QUALITY_GATES.json", "docs/engineering/QUALITY_GATES.md", "docs/engineering/WORKFLOW.md", "docs/engineering/repository-harness-upgrade/", "docs/notes/developing-se-harness.md", "pyproject.toml", "se_harness/__init__.py", "tests/"]

[relations]
implements = ["REQ-HUP-020", "REQ-HUP-021"]
specifications = ["SPEC-HUP-010"]
architecture = ["ARCH-HUP-008"]
verification = ["VER-HUP-010"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T10:40:51Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-HUP-010', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared simple upgrade from an isolated 0.10.0 wheel-file install outside the checkout, the owner statements, the candidate move to 0.11.0, the identity-aware test change and the retained evidence, inside the declared execution scope. It authorizes no verification record, no release, no publication and no change to the guard. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-29T10:40:58Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-08-29, 'Approve and start WO-HUP-010'. Start preflight PASS with no diagnostics over the approval commit 294b4ad carrying unmoved main 47f67de, run with the governing exact public 0.9.0 evaluator outside the checkout. Bounded to the declared execution scope; the applying runtime is exact public 0.10.0 installed from the digest-verified PyPI wheel file into an isolated environment outside the checkout. This start authorizes no verification record, no release and no publication."
+++

# Work Order: Adopt exact public 0.10.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. It follows `WO-HUP-009` (0.9.0) and is the
acceptance in the wild that `REL-SEH-021`'s observation window names.

Commit-bound verification is `required`: the root this work order writes is
what every later gate runs under.

## Objective

Use exact public 0.10.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-019` binds, to replace the 0.9.0 standard root with
one evidence-bound 0.10.0 root by the simple upgrade — one command, no
packet — and prove the complete graph and the repository suite under the
new root, without changing product, release, publication, deployment,
maintenance or external state.

## In scope

- Prove the installed 0.10.0 identity (version, payload digest, archive
  pair equal to the published wheel) from the isolated environment;
  `SPEC-HUP-010` rules 1 and 2. Rehearsed on 2026-08-29 on a throwaway
  clone of `main` at `47f67de`: wheel `se_harness-0.10.0-py3-none-any.whl`
  `e2f8077264ee2c8ad39d6ac33f726030627f0f70de5579e80bcc159d971f93c3`,
  payload `723c98ecf21a853441ead771956af7aed6564fcffb97389c0468b9376214235d`.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict` (rule 3). Measured: 61 files, 6
  `update`, 55 unchanged.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured: replay 61 unchanged;
  prior lock `fb61f1fe…`, prior `tool_version 0.9.0`.
- Update owner content only where it must state the new governor: the
  `se-harness==0.9.0` instruction in `AGENTS.md`'s owner region, and the
  candidate/root statements in `docs/notes/developing-se-harness.md`
  (rule 8).
- Move the candidate to `0.11.0` (`pyproject.toml`, `se_harness/__init__.py`,
  the README install example); no scenario, no legacy-contract entry
  (rule 7). Measured: with the candidate left at 0.10.0, `evaluator_facts
  derive` raises `PRE008`; at 0.11.0 it yields the 0.10.0 to 0.11.0 pair.
- Replace pinned root and candidate assumptions in `tests/` with
  identity-aware assertions, each named in the evidence (rule 9). The
  rehearsal compared the full suite on the moved root against a control on
  the unmoved root at the same commit: 1117 tests each; exactly three names
  differ, all in the direction of the move — two
  `test_ci_pipeline.PredecessorDerivationTests` (`PRE008`, the candidate
  version) and
  `test_instruction_architecture…test_owner_region_directs_the_evaluator_outside_the_checkout`
  (the owner region). The test edit is the `0.10.0` literal added to the
  forbidden version set for repository-owned workflows.
- Run the complete `VER-HUP-010` qualification and the suite, and retain the
  evidence; hand off with the pull request's lanes green — under this
  root's own `scope` gate, which must stay green through completion.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
`release/0.10` line; credentials; the published 0.10.0 itself, which does
not move; the workstation-only suite failures the control also reads; any
change to the guard when it refuses.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted; the order of readings.

## Constraints

- The applying runtime is exact public 0.10.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal by
  the guard is a stop, not a thing to bypass.
- No `customized` or `conflict` action may be waived; a `null` archive pair
  is a stop.
- The complete graph must pass exact 0.10.0 directly after apply.
- Candidate template bytes must remain unchanged.

## Expected change surface

The 6 reviewed `update` paths and the installer-owned lock; `AGENTS.md`'s
owner region and `docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; `tests/test_ci_pipeline.py`; this
packet, the domain index, the transaction JSON and the evidence packet.

## Required verification

Execute `VER-HUP-010` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-010/` and
`WO-HUP-010-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, a `null` archive pair, a partial transaction, a failed replay, a
failed graph, a suite whose failure set differs from the control, an
unexplained warning, a product or release byte moved beyond the version
identity, a test that cannot assert the released root without weakening the
candidate-template assertion, or a need for authority beyond the approved
stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
