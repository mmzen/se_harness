+++
id = "WO-HUP-006"
type = "work_order"
title = "Adopt exact public 0.7.0 as the standard root evaluator"
status = "rejected"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

rejected_at = "2026-08-27T15:15:07Z"
rejected_by = "repository-owner"
rejection_reason = "Rejected by the repository owner on 2026-08-27 after the transaction was executed on branch governance/hup-006-adopt-0-7-0 (pull request #196, closed unmerged): 0.7.0's managed engineering-harness workflow installs the evaluator from the index and then runs qualify released-root, which requires the installed evaluator's PEP 610 archive digest to equal the lock's, so the managed lane fails with RID022 for every index install and no in-scope change can clear it; the candidate-package lane also rejects the 0.7.0 verifier's typed result. The owner's direction supersedes the adoption model itself: the wheel-digest requirement (MG004) and the separately approved evaluator-upgrade work-order packet (MG007) are too restrictive and are to be removed, so the root stays at exact public 0.6.0 until a release carries the simplified upgrade and can be adopted the simple way. The packet's definitions stay approved as history; nothing on main moved: root, lock, product bytes, release records and tags are untouched."
[assurance]
commit_bound_verification = "required"
rationale = "Every later root lifecycle action and managed CI gate depends on the exact public evaluator, schema-3 lock and complete-graph validation this transaction establishes."
decided_by = "repository-owner"

[evaluator_upgrade]
schema = "se-harness-evaluator-upgrade-v1"
scope = "standard-root-only"
prior_lock_sha256 = "978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e"
target_version = "0.7.0"
target_payload_sha256 = "26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9"
target_archive_name = "se_harness-0.7.0-py3-none-any.whl"
target_archive_sha256 = "e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3"
publication = "immutable"
authorized_by = "repository-owner"

[execution_scope]
paths = [
  ".agents/skills/",
  ".claude/skills/",
  ".engineering-harness.lock",
  ".engineering-harness.toml",
  ".gitattributes",
  ".github/workflows/engineering-harness.yml",
  "AGENTS.md",
  "CLAUDE.md",
  "ENGINEERING_HARNESS.md",
  "docs/engineering/ARTIFACT_AUTHORING.md",
  "docs/engineering/DECISION_RIGHTS.md",
  "docs/engineering/OPERATING_CARD.md",
  "docs/engineering/QUALITY_GATES.json",
  "docs/engineering/QUALITY_GATES.md",
  "docs/engineering/TECHNICAL_COMMUNICATION.md",
  "docs/engineering/WORKFLOW.json",
  "docs/engineering/WORKFLOW.md",
  "docs/engineering/templates/",
  "docs/engineering/repository-harness-upgrade/",
  "docs/notes/developing-se-harness.md",
  "pyproject.toml",
  "scripts/select_harness_work_order.py",
  "scripts/validate_engineering_artifacts.py",
  "se_harness/__init__.py",
  "tests/",
]

[relations]
implements = ["REQ-HUP-012", "REQ-HUP-013"]
specifications = ["SPEC-HUP-006"]
architecture = ["ARCH-HUP-004"]
verification = ["VER-HUP-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-27T14:37:56Z"
decided_by = "repository-owner"
reason = "Approved on 2026-08-27 by the accountable owner, 'i approve the packet, you can start WO-HUP-006', after the rehearsal of the transaction in a throwaway worktree and the owner's decision to move the candidate to development version 0.8.0 inside the work order. Adopts exact public 0.7.0 (wheel e8f4fdc9ad60879a3fa4627c063fa7bb9513e2bd109c47258cf7f7aa6ecf27f3, payload 26c11ec5e2363c3c0a9a416e69a3faa8bdf2d7a046710075bdeb661dd1003ee9) from the 0.6.0 lock 978cebb7824b7928d95ed43897b0f848441cc4ab7403a0cdd08a55a77df2b79e through one reviewed standard-root transaction of 43 add or update paths, no customization. Approval authorizes start preflight and then only the declared work inside the execution scope; the transaction, completion, verification, pull request and merge are separate acts."

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-27T14:38:01Z"
decided_by = "engineering-owner"
reason = "Started on the engineering owner's decision of 2026-08-27; start preflight PASS with the exact public 0.6.0 evaluator outside the checkout on branch governance/hup-006-adopt-0-7-0 off main 7284743. The transaction runs next from the isolated 0.7.0 environment; commit, push, pull request, verification and merge remain separate acts."

[[lifecycle_events]]
from = "in_progress"
to = "rejected"
decided_at = "2026-08-27T15:15:07Z"
decided_by = "repository-owner"
reason = "Rejected by the repository owner on 2026-08-27 after the transaction was executed on branch governance/hup-006-adopt-0-7-0 (pull request #196, closed unmerged): 0.7.0's managed engineering-harness workflow installs the evaluator from the index and then runs qualify released-root, which requires the installed evaluator's PEP 610 archive digest to equal the lock's, so the managed lane fails with RID022 for every index install and no in-scope change can clear it; the candidate-package lane also rejects the 0.7.0 verifier's typed result. The owner's direction supersedes the adoption model itself: the wheel-digest requirement (MG004) and the separately approved evaluator-upgrade work-order packet (MG007) are too restrictive and are to be removed, so the root stays at exact public 0.6.0 until a release carries the simplified upgrade and can be adopted the simple way. The packet's definitions stay approved as history; nothing on main moved: root, lock, product bytes, release records and tags are untouched."
+++

# Work Order: Adopt exact public 0.7.0 as the standard root evaluator

## Lifecycle

Approval authorizes only the scope below. Start, completion, commit-bound
verification, the pull request and the merge are separate accountable acts.
The transaction itself runs only after this work order is `in_progress`.

## Objective

Use exact public 0.7.0, installed outside the checkout from the wheel
`RLS-SEH-015` binds, to replace the 0.6.0 standard root with one
evidence-bound 0.7.0 root candidate — without changing product, release,
publication, deployment, maintenance or external state.

## In scope

- Prove the public wheel and installed-payload identity
  (`e8f4fdc9…`, `26c11ec5…`) from the isolated environment.
- Review the 0.7.0 plan against `SPEC-HUP-006`'s reviewed managed plan: the
  same 43 add or update paths, no `customized`, no `conflict`.
- Apply the plan with this work order and the canonical evidence output;
  require the no-op replay.
- Update owner content only where it must state the new governor truthfully:
  the `se-harness==0.6.0` instruction in `AGENTS.md`'s owner region and the
  root-evaluator statements in `docs/notes/developing-se-harness.md`.
- Replace pinned 0.6.0 root assumptions in `tests/` with released-root
  identity-aware assertions, each file named in the evidence with the
  assumption it carried. Measured before approval in a throwaway worktree:
  eleven tests in six modules.
- Move the candidate to the next development version, `0.8.0`, in
  `pyproject.toml` and `se_harness/__init__.py`, and write the migration
  scenario `tests/fixtures/governance_migration/candidate-0.7.0-to-0.8.0.json`
  with the canonical writer (`repository_tools.predecessor_facts
  write-scenario`). Reason, measured in the rehearsal: with the root and the
  candidate both at 0.7.0, `predecessor_facts derive` raises `PRE008` (no
  predecessor pair), which is the second step of the candidate-evidence
  lane's first job, so every pull request's lane would be red after
  adoption. The candidate version and the scenario move together (release
  sequences note). `README.md`'s public install example stays `0.7.0`: it
  names the published version, not the candidate.
- Remove the repository-owned `.gitattributes` rules that 0.7.0's managed
  block now carries (the three `governance_migration` LF rules), keeping the
  other owner rules; the rules stay effective through the managed block.
- Run the complete qualification `VER-HUP-006` names and retain the
  changed-surface ledger.
- Transition only this work order to `implemented` after every local gate
  passes, under explicit authority.

## Out of scope

Product source and templates other than the version identity; `RLS`, `VREC`,
`REL` records; tags; publication, replay and Pages workflows; the
`release/0.7` line; branch policy; credentials; external policy; the RC-070
issues; retiring the `accept-candidate` bootstrap exception; the published
0.7.0 itself, which does not move.

## Authorized decision envelope

The name of the external environment; the exact wording of the two
owner-content statements; which assertion form replaces each pinned test
assumption, provided the released-root identity and the candidate templates
are both still asserted.

## Constraints

- The applying runtime must be the exact identity in `[evaluator_upgrade]`.
- A plan path outside the reviewed set stops for amendment.
- No `customized` or `conflict` action may be waived.
- The complete graph must pass exact 0.7.0 directly after apply.
- Candidate template bytes must remain unchanged; the repository-owned
  `.gitattributes` rules outside the managed block must stay effective.

## Expected change surface

- The 43 reviewed add or update paths and the installer-owned lock.
- `AGENTS.md`'s owner region and `docs/notes/developing-se-harness.md`, for
  the governor statements only; the owner region's managed-path list grows
  from 30 to 55 entries.
- `.gitattributes` owner content, for the three duplicated rules only.
- `pyproject.toml`, `se_harness/__init__.py` and the new scenario file, for
  the 0.8.0 development version.
- The test files named in the evidence, for root assumptions only.
- This packet, the HUP index, the canonical transaction JSON and the
  human-readable evidence.

## Required verification

Execute `VER-HUP-006` in full; repository-required checks; the pull request's
lanes green; handoff check.

## Evidence to record

`docs/engineering/repository-harness-upgrade/evidence/WO-HUP-006-verification.md`
and `WO-HUP-006-evaluator-upgrade.json`.

## Stop and escalate conditions

Wrong identity, prior-lock mismatch, plan drift, customization, conflict, a
partial transaction, an evidence collision, a failed graph or suite, an
unexplained warning, a product or release byte moved, or a need for
authority beyond the approved stage.

## Completion report format

The `harnessctl check . --artifact WO-HUP-006 --checkpoint handoff` schema-2
block verbatim with the complete changed-path set, and its `result_sha256`.
