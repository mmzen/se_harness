+++
id = "WO-HUP-014"
type = "work_order"
title = "Adopt exact public 0.13.0 as the standard root, the simple way"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "scripts/generate_harness_dashboard.py", "scripts/harness_explorer/index.template.html", "pyproject.toml", "se_harness/__init__.py", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-027.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-028.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-014.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-011.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-014.md"]

[relations]
implements = ["REQ-HUP-027", "REQ-HUP-028"]
specifications = ["SPEC-HUP-014"]
architecture = ["ARCH-HUP-011"]
verification = ["VER-HUP-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T08:31:12Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-02 by selecting the presented option 'Approve, start, complete on green', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the simple upgrade transaction from the isolated 0.13.0 environment, the owner statements naming the new governor, the candidate move to 0.14.0, the identity-aware test assertions in the two modules the rehearsal names, this packet, the domain index, the transaction JSON and the evidence packet; and authorizes marking the work order implemented once the declared evidence is green. It authorizes no product byte beyond the version identity, no template, no verification record, no release and no publication; the pull request's merge remains the owner's decision. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-02T08:31:56Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-09-02, made by selecting the presented option 'Approve, start, complete on green'. Start preflight PASS with no diagnostics over the approval commit d768e23 carrying unmoved main 09aa69f, run with the governing exact public 0.12.0 evaluator outside the checkout, on this Windows checkout; every file of the reading manifest was read. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-02T08:46:26Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-09-02 under DR-WO-COMPLETE, under the decision made by selecting the presented option 'Approve, start, complete on green', which authorized this transition once the declared evidence was green, on the handoff check reading Completed over the Git-derived change set at a2f4677, self-bound in one run at result 60e03c50, produced by the exact public 0.13.0 evaluator that this transaction installed as the root, outside the checkout, on this Windows checkout. The root lock reads 0.13.0 by version, payload 9b4cdb5f and the archive pair of the wheel RLS-SEH-022 binds; 46 managed files, 5 updated, replay unchanged; nothing left the managed set; exact 0.13.0 validate 1241 artifacts 0 errors 67 warnings 0 advisories, doctor 0 FAIL, released-root 113/113, the designed Explorer identical twice with no remote origin, review preflight PASS, derive 0.13.0 to 0.14.0; the full-scale suite at its one baseline name with the identity-aware edits named in the packet; all thirteen lanes of pull request #314 pass at a2f4677 including the governor-transition assessment of the real root move. This authorizes no verification record, no release and no publication."
+++

# Work Order: Adopt exact public 0.13.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the gate admits this
work order's own records by construction on both sides of the move
(`ECP-ADM-001`).

## Objective

Use exact public 0.13.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-022` binds, to replace the 0.12.0 standard root with
one evidence-bound 0.13.0 root by the simple upgrade, one command and no
packet, and prove the complete graph and the repository suite under the
new root, without changing product, release, publication, deployment,
maintenance or external state. After the merge, the Pages deployment
regenerates the public demonstration from the new root, which is the
observation `REL-SEH-024` names.

## In scope

- Prove the installed 0.13.0 identity (version, payload digest, archive
  pair equal to the published wheel) from the isolated environment;
  `SPEC-HUP-014` rules 1 and 2. Rehearsed on 2026-09-02 on a throwaway
  clone of `main` at `09aa69f`: wheel `se_harness-0.13.0-py3-none-any.whl`
  `1bbf3b747b7ebbb07fd3fd975e87e3c11049e7a6a8e1377e3d35099f4fe862ae`,
  payload `9b4cdb5f2148683f3ceaad868e64b1b4ebefbadcac49cf4cd1feccd954540bfe`.
- Review the plan against the installer's managed set: `add` or `update`
  only, no `customized`, no `conflict`, no unexpected `remove` (rules 3
  and 6). Measured: 46 files, 5 `update`, 41 unchanged; nothing leaves the
  managed set.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-014-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured at rehearsal: replay
  46 unchanged; prior lock `4d8f9d37a91132cd…`, prior `tool_version
  0.12.0`.
- Update owner content only where it must state the new governor: the
  `se-harness==0.12.0` instruction in `AGENTS.md`'s owner region, and the
  candidate/root statements in `docs/notes/developing-se-harness.md`
  (rule 9).
- Move the candidate to `0.14.0` (`pyproject.toml`,
  `se_harness/__init__.py`, the README install example); the derivation
  reports `PRE008` otherwise (rule 8).
- Replace pinned root and candidate assumptions in `tests/` with
  identity-aware assertions, each named in the evidence (rule 10); the
  rehearsal names two modules: `tests/test_instruction_architecture.py`
  (the managed count of root 0.13.0) and `tests/test_dashboard_webui.py`
  (eight tests that asserted the 0.12.0 page against the root copy of the
  Explorer template, guarded by the root's version).
- Run the complete `VER-HUP-014` qualification and the suite, and retain
  the evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
published 0.13.0 itself, which does not move; credentials; the
workstation-only suite error the control also reads.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; which assertion form replaces each pinned test assumption,
provided the released-root identity and the candidate templates are both
still asserted; the order of readings.

## Constraints

- The applying runtime is exact public 0.13.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal
  by the guard is a stop, not a thing to bypass.
- No `customized`, `conflict` or unexpected `remove` action may be waived;
  a `null` archive pair is a stop.
- The complete graph must pass exact 0.13.0 directly after apply.
- Candidate template bytes must remain unchanged.

## Expected change surface

The 5 reviewed `update` paths and the installer-owned lock; `AGENTS.md`'s
owner region and `docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; the test modules the evidence
names; this packet, the domain index, the transaction JSON and the
evidence packet.

## Required verification

Execute `VER-HUP-014` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-014/` and
`WO-HUP-014-evaluator-upgrade.json`.

## Stop and escalate conditions

A guard refusal, a plan path outside the managed set, customization,
conflict, an unexpected removal, a `null` archive pair, a partial
transaction, a failed replay, a failed graph, a suite whose failure set
differs from the control beyond the names the evidence explains, an
unexplained warning, a product or release byte moved beyond the version
identity, or a need for authority beyond the approved stage.

## Completion report format

The evidence packet, the changed-path ledger, the handoff `check`
restitution; the completion decision is the engineering owner's.
