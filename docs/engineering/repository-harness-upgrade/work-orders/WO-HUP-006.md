+++
id = "WO-HUP-006"
type = "work_order"
title = "Adopt exact public 0.7.0 as the standard root evaluator"
status = "draft"
owners = ["repository-owner", "engineering-owner", "quality-owner", "security-owner"]
created = "2026-08-27"
updated = "2026-08-27"

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
  "scripts/select_harness_work_order.py",
  "scripts/validate_engineering_artifacts.py",
  "tests/",
]

[relations]
implements = ["REQ-HUP-012", "REQ-HUP-013"]
specifications = ["SPEC-HUP-006"]
architecture = ["ARCH-HUP-004"]
verification = ["VER-HUP-006"]
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
  see the packet index for the count.
- Run the complete qualification `VER-HUP-006` names and retain the
  changed-surface ledger.
- Transition only this work order to `implemented` after every local gate
  passes, under explicit authority.

## Out of scope

Product source and templates; version metadata; `RLS`, `VREC`, `REL`
records; tags; publication, replay and Pages workflows; the `release/0.7`
line; branch policy; credentials; external policy; the RC-070 issues;
retiring the `accept-candidate` bootstrap exception.

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
  the governor statements only.
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
