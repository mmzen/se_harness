+++
id = "WO-HUP-015"
type = "work_order"
title = "Adopt exact public 0.14.0 as the standard root, the simple way"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "security-owner"]
created = "2026-09-02"
updated = "2026-09-02"

[assurance]
commit_bound_verification = "required"
rationale = "Every later gate, decision and release runs under the evaluator this transaction installs; the moved root, the candidate identity and the test assumptions are trusted engineering state."
decided_by = "repository-owner"

[execution_scope]
paths = [".engineering-harness.lock", ".engineering-harness.toml", ".github/workflows/engineering-harness.yml", "AGENTS.md", "ENGINEERING_HARNESS.md", "README.md", "pyproject.toml", "se_harness/__init__.py", "tests/", "docs/notes/developing-se-harness.md", "docs/engineering/repository-harness-upgrade/README.md", "docs/engineering/repository-harness-upgrade/evidence/", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-029.md", "docs/engineering/repository-harness-upgrade/requirements/REQ-HUP-030.md", "docs/engineering/repository-harness-upgrade/specifications/SPEC-HUP-015.md", "docs/engineering/repository-harness-upgrade/architecture/ARCH-HUP-012.md", "docs/engineering/repository-harness-upgrade/verification/VER-HUP-015.md"]

[relations]
implements = ["REQ-HUP-029", "REQ-HUP-030"]
specifications = ["SPEC-HUP-015"]
architecture = ["ARCH-HUP-012"]
verification = ["VER-HUP-015"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-02T11:42:30Z"
decided_by = "engineering-owner"
reason = "Approved by the accountable engineering owner on 2026-09-02 by selecting the presented option 'Approve, start, complete on green, prepare and verify the VREC', as a decision distinct from the approval of its definitions in the same transaction. Authorizes start preflight and then only the declared scope: the simple upgrade transaction from the isolated 0.14.0 environment, the owner statements naming the new governor, the candidate move to 0.15.0, the identity-aware test assertion the rehearsal names, this packet, the domain index, the transaction JSON and the evidence packet; and authorizes marking the work order implemented once the declared evidence is green. It authorizes no product byte beyond the version identity, no template, no verification record, no release and no publication; the pull request's merge remains the owner's decision. Start preflight has not been run."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-09-02T11:43:04Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's explicit start decision of 2026-09-02, made by selecting the presented option 'Approve, start, complete on green, prepare and verify the VREC'. Start preflight PASS with no diagnostics over the approval commit 90baabc carrying unmoved main 25c0ef9, run with the governing exact public 0.13.0 evaluator outside the checkout on this Windows checkout; the reading manifest (INT-HUP-002, CAP-HUP-002, the five definitions of this packet and this work order) was read. Bounded to the declared execution scope. This start authorizes no verification record, no release and no publication."

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-09-02T12:01:12Z"
decided_by = "engineering-owner"
reason = "Marked implemented by the accountable engineering owner on 2026-09-02 under DR-WO-COMPLETE, under the decision made by selecting the presented option 'Approve, start, complete on green, prepare and verify the VREC', which authorized this transition once the declared evidence was green, on the handoff check reading Completed over the Git-derived change set at 454696b, self-bound at result 2b4386978089, produced by the exact public 0.14.0 evaluator that this transaction installed as the root, outside the checkout, on this Windows checkout. The root lock reads 0.14.0 by version, payload 25034dc7 and the archive pair of the wheel RLS-SEH-023 binds; 46 managed files, 3 updated, replay unchanged; nothing left the managed set; exact 0.14.0 validate 1254 artifacts 0 errors 69 warnings 0 advisories, doctor 0 FAIL, released-root 113/113, the Explorer identical twice, review preflight PASS, derive 0.14.0 to 0.15.0; the full-scale suite at its one baseline name with the one identity-aware edit named in the packet; the prior-lock digest deviation of rule 4 explained in the packet as the rehearsal clone's CRLF working tree; all lanes of pull request #317 pass at 3aa09ca and at 454696b including the governor-transition assessment of the real root move. This authorizes no verification record, no release and no publication."
+++

# Work Order: Adopt exact public 0.14.0 as the standard root, the simple way

## Lifecycle

This work order requires the accountable owners' approval before start
preflight or any declared work. Its authoritative state, and the timestamp
and reason of every decision taken on it, are the front matter and
`[[lifecycle_events]]` above. Commit-bound verification is `required`.

Its scope names no `verification-records/` directory: the gate admits this
work order's own records by construction on both sides of the move
(`ECP-ADM-001`).

## Objective

Use exact public 0.14.0, installed outside the checkout from the wheel file
whose digest `RLS-SEH-023` binds, to replace the 0.13.0 standard root with
one evidence-bound 0.14.0 root by the simple upgrade, one command and no
packet, and prove the complete graph and the repository suite under the
new root, without changing product, release, publication, deployment,
maintenance or external state. This adoption has no public observation of
its own: the 0.14.0 evaluator behaves as 0.13.0 does.

## In scope

- Prove the installed 0.14.0 identity from the isolated environment;
  `SPEC-HUP-015` rules 1 and 2. Rehearsed on 2026-09-02 on a throwaway
  clone of `main` at `25c0ef9`: wheel `70d438b5…`, payload
  `25034dc7…`.
- Review the plan (rules 3 and 6). Measured: 46 files, 3 `update`, 43
  unchanged; nothing leaves the managed set.
- Apply with `harnessctl upgrade . --apply --evidence-output
  docs/engineering/repository-harness-upgrade/evidence/WO-HUP-015-evaluator-upgrade.json`;
  require the no-op replay (rules 4 and 5). Measured: replay 46 unchanged;
  prior lock `9dfec5b4645774ed…`, prior `tool_version 0.13.0`.
- Update owner content only where it must state the new governor (rule 9).
- Move the candidate to `0.15.0` (rule 8).
- Replace the one pinned root assumption in `tests/` with an identity-aware
  assertion (rule 10): `tests/test_instruction_architecture.py`, the
  managed count of root 0.14.0.
- Run the complete `VER-HUP-015` qualification and the suite, and retain
  the evidence; hand off with the pull request's lanes green.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`
and `REL` records; tags, publication, replay and Pages workflows; the
published 0.14.0 itself; credentials; the workstation-only suite error the
control also reads.

## Authorized decision envelope

The name of the external environment; the wording of the owner-content
statements; the order of readings.

## Constraints

- The applying runtime is exact public 0.14.0 outside the checkout, in
  isolated mode, installed from the digest-verified wheel file; a refusal
  by the guard is a stop, not a thing to bypass.
- No `customized`, `conflict` or unexpected `remove` action may be waived;
  a `null` archive pair is a stop.
- The complete graph must pass exact 0.14.0 directly after apply.
- Candidate template bytes must remain unchanged.

## Expected change surface

The 3 reviewed `update` paths and the installer-owned lock; `AGENTS.md`'s
owner region and `docs/notes/developing-se-harness.md`; `pyproject.toml`,
`se_harness/__init__.py`, `README.md`; one test module; this packet, the
domain index, the transaction JSON and the evidence packet.

## Required verification

Execute `VER-HUP-015` in full; repository-required checks; the pull
request's lanes green; the handoff check over the Git-derived change set.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-015/` and
`WO-HUP-015-evaluator-upgrade.json`.

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
