+++
id = "WO-HUP-011"
type = "work_order"
title = "Adopt exact public 0.11.0 as the standard root, the simple way"
status = "approved"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-08-29"
updated = "2026-08-29"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", ".agents/skills/", ".claude/skills/", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "docs/engineering/WORKFLOW.json", "docs/engineering/WORKFLOW.md", "docs/engineering/templates/WORK_ORDER.template.md", "scripts/validate_engineering_artifacts.py", "pyproject.toml", "se_harness/__init__.py", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-022.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-023.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-011.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-009.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-011.md"]

[relations]
implements = ["REQ-HUP-022", "REQ-HUP-023"]
specifications = ["SPEC-HUP-011"]
architecture = ["ARCH-HUP-009"]
verification = ["VER-HUP-011"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-29T16:44:38Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-08-29 with the words 'Approve and start WO-HUP-011', as a decision distinct from the approval of its definitions seconds earlier. Authorizes start preflight and then only the declared scope: the simple upgrade transaction from the isolated 0.11.0 environment, the explicit removal of the fifteen retired skill files, the owner statements naming the new governor, the candidate move to 0.12.0, the identity-aware test assertions, this packet, the domain index, the transaction JSON and the evidence packet. It authorizes no product byte beyond the version identity, no template, no verification record, no release and no publication. Start preflight has not been run."
+++

# Work Order: Adopt exact public 0.11.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the 0.11.0 gate that
the moved root installs admits this work order's own record by construction
(`ECP-ADM-001`), and the record head of its pull request is `VER-ECP-012`'s
hosted demonstration (`SPEC-HUP-011` rule 11). Until the root moves, the
managed lane on this branch is the released 0.10.0 gate, which also admits
the work order's own file and packet directory.

## Objective

Use exact public 0.11.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-020` binds, to replace the 0.10.0 standard root with
one evidence-bound 0.11.0 root by the simple upgrade — one command, no
packet — remove the fifteen files the previous lock managed and the new
plan omits, and prove the complete graph and the repository suite under the
new root, without changing product, release, publication, deployment,
maintenance or external state.

## In scope

- Prove the installed 0.11.0 identity (version, payload digest, archive
  pair equal to the published wheel) from the isolated environment;
  `SPEC-HUP-011` rules 1 and 2. Rehearsed on 2026-08-29 on a throwaway
  clone of `main` at `896f8fa`: wheel `se_harness-0.11.0-py3-none-any.whl`
  `ba26ab7be14321cdc26b69d59e2b894d544c3e7b529227de1f24ad9cd8f935c0`,
  payload `71b4b5b694111a42785328f4b742f40e5654d7d4c67d88b9939a6c80213dd016`.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict` (rule 3). Measured: 46 files, 9
  `update`, 37 unchanged.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-011-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured: replay 46 unchanged;
  prior lock `aeb73cc7…`, prior `tool_version 0.10.0`.
- Remove the fifteen retired skill files the installer leaves behind
  (rule 6; issue #271), recorded as a deviation from `ECP-SKL-004`'s
  expectation.
- Update owner content only where it must state the new governor: the
  `se-harness==0.10.0` instruction in `AGENTS.md`'s owner region, and the
  candidate/root statements in `docs/notes/developing-se-harness.md`
  (rule 9).
- Move the candidate to `0.12.0` (`pyproject.toml`, `se_harness/__init__.py`,
  the README install example); no scenario, no legacy-contract entry
  (rule 8).
- Replace pinned root and candidate assumptions in `tests/` with
  identity-aware assertions, each named in the evidence (rule 10); the
  rehearsal's suite comparison against a same-commit control on the 0.10.0
  root is recorded in the evidence with every differing name and its
  cause.
- Run the complete `VER-HUP-011` qualification and the suite, and retain the
  evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
`release/0.11` line; credentials; the published 0.11.0 itself, which does
not move; the workstation-only suite failures the control also reads; any
change to the guard when it refuses; the installer's missing `remove`
action (issue #271, a later work order).

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted; the order of readings.

## Constraints

- The applying runtime is exact public 0.11.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal by
  the guard is a stop, not a thing to bypass.
- No `customized` or `conflict` action may be waived; a `null` archive pair
  is a stop.
- The complete graph must pass exact 0.11.0 directly after apply.
- Candidate template bytes must remain unchanged.

## Expected change surface

The 9 reviewed `update` paths and the installer-owned lock; 15 deletions
under `.agents/skills/` and `.claude/skills/`; `AGENTS.md`'s owner region
and `docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; the test modules the evidence names;
this packet, the domain index, the transaction JSON and the evidence packet.

## Required verification

Execute `VER-HUP-011` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-011/` and
`WO-HUP-011-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, a `null` archive pair, a partial transaction, a failed replay, a
failed graph, a suite whose failure set differs from the control beyond the
names the evidence explains, an unexplained warning, a product or release
byte moved beyond the version identity, a test that cannot assert the
released root without weakening the candidate-template assertion, or a
need for authority beyond the approved stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
