+++
id = "WO-IAR-012"
type = "work_order"
title = "Carry local operational facts in the owner instruction region"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes the always-available instruction surface that later engineering decisions rely on, including which paths are hash-locked; an incorrect managed-path boundary would lead an agent to break managed integrity, so assurance must bind the exact candidate commit."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "AGENTS.md",
  "docs/engineering/instruction-architecture/",
  "tests/test_instruction_architecture.py",
]

[relations]
implements = ["REQ-IAR-020"]
specifications = ["SPEC-IAR-012"]
verification = ["VER-IAR-012"]
+++

# Work Order: Carry local operational facts in the owner instruction region

## Lifecycle and authorization

Drafted on 2026-08-21 alongside `REQ-IAR-020`, `SPEC-IAR-012`, and `VER-IAR-012`, following the repository owner's instruction to record this change before making it. Approved by the repository owner on 2026-08-21 together with those three artifacts and with the `WO-DST-021` packet.

Approval authorizes the bounded implementation described below and nothing else. Implementation begins after start preflight passes under the released evaluator executed from outside the checkout. Commit, push, pull request, verification transition, and release remain separate accountable decisions.

This work order and `WO-DST-021` are independent and may be implemented in either order. The revised rule 3 of `SPEC-IAR-012` states the `REPOSITORY_CONTEXT.md` pointer by content rather than by harness status, which is correct both before and after `WO-DST-021` retires the scaffold, so neither work order blocks the other.

Commit-bound verification is classified `required`. No active architecture addresses `REQ-IAR-020`, so this work order omits the `architecture` relation rather than fabricating coverage. The technical owner accepted that applicability assessment at approval on 2026-08-21: revising an owner-controlled instruction region alters no architectural boundary, and the accountable no-ADR rationale is that the work adds no component, dependency, or trust boundary.

An uncommitted revision of the `AGENTS.md` owner region already existed in the worktree at approval, made before this packet was drafted. It is not implementation of this work order and confers no authority. It did not satisfy the revised rule 3 of `SPEC-IAR-012`: it described `docs/engineering/REPOSITORY_CONTEXT.md` as preflight-required and harness-seeded, which rule 3 and the `REQ-IAR-020` boundary behavior prohibit. Correcting that sentence was part of implementation, and the uncommitted state was reviewed against every rule rather than assumed compliant.

The owner instructed implementation on 2026-08-21. Start preflight passed under released `se-harness==0.5.0` executed from `../se-harness-eval-1685/` outside the checkout. That pre-existing sentence was replaced with a statement by content, and rules 1, 2, and 4 through 13 were reviewed against the whole region and found already satisfied. The bounded implementation and the retained evidence at `../evidence/WO-IAR-012-verification.md` are complete, so this work order is now `implemented`. The result is an uncommitted working-tree candidate: no commit, push, pull request, verification transition, or release was performed.

## Objective

Revise the owner-controlled region of the repository-root `AGENTS.md` so it carries the operational entry point, the authoritative managed-path boundary with its candidate-source counterpart, and the known pull-request and evaluator failure conditions, while withdrawing restatements of obligations that governed requirements already own and leaving the managed fragment byte-exact.

## In scope

- Rewrite the owner-controlled region of `AGENTS.md` to satisfy rules 1 through 13 of `SPEC-IAR-012`.
- Add focused tests covering managed-block digest invariance, lock-derived managed and owner-editable path agreement, required content presence, the withdrawn-restatement negative assertions, and the region size bound.
- Add one instruction-architecture acceptance scenario to `docs/engineering/instruction-architecture/acceptance/instruction-architecture.feature`.
- Record the `IAR-012` packet in `docs/engineering/instruction-architecture/README.md` following the established packet-index pattern.
- Retain evidence keyed to `WO-IAR-012` under this domain's `evidence/` directory.

## Out of scope

- The managed fragment inside the `se-harness` markers, `CLAUDE.md`, `ENGINEERING_HARNESS.md`, and every managed policy module.
- `templates/repository/standard/AGENTS.md.fragment`, `templates/repository/standard/CLAUDE.md.fragment`, and any other packaged template or portable SE Harness behavior. The product-level concerns identified by the same analysis — the undefined "before engineering work" trigger, the absent operational tier in the shipped fragment, and the single-line `CLAUDE.md` adapter — are deliberately excluded and need their own packet.
- `docs/engineering/REPOSITORY_CONTEXT.md`, the repository-level `docs/engineering/README.md`, and any other seed or managed file. Retiring the repository-context scaffold is out of scope here but is not infeasible: `WO-DST-021` owns it, under `REQ-DST-065` and `REQ-IAR-021`, and covers the six couplings that put it beyond this work order — `se_harness.preflight.REQUIRED_PATHS` and `POLICY_PATHS`, the `_parse_context` reader and its `C` diagnostic family, the lock's `seed` entry and the `doctor` presence check, the managed router's authority model and routing table, `harnessctl init` step 1, and the managed stop condition on incomplete repository context. This work order changes none of them. It lifts the operational content an agent needs into the owner region, leaves the file itself untouched, and states its pointer by content rather than by harness status, so the owner region stays correct whether `WO-DST-021` lands before or after it.
- Relocating the managed block above the owner sections. Permitted by the installer and preserved across upgrades, but not authorized here.
- Any formatter or linter gate, CLI change, machine-readable output, or `.engineering-harness.lock` edit.
- Commit, push, pull request, verification transition, release, tag, publication, and deployment.

## Authorized decision envelope

The implementation agent may choose section order, headings, wording, and whether paths appear inline or as lists, and may select the test module and test names. It may not change which facts are required, add or remove a rule, alter the managed block, or extend the change surface beyond the in-scope list.

## Constraints

- Reproduce the managed block byte-for-byte, including both markers. Verify with `canonical_sha256(tracked_content("fragment", ...))` against `.engineering-harness.lock` before and after the edit.
- Derive the managed-path list from `.engineering-harness.lock` rather than from this work order or any prose.
- Keep the owner region under 6,000 bytes.
- Add no obligation that waives formal artifact authority, approved work-order scope, required evidence, or accountable verification and release decisions.
- Do not build any release distribution.

## Expected change surface

- The owner region of the repository-root `AGENTS.md`.
- One test module under `tests/`, extending the existing instruction-architecture coverage.
- The instruction-architecture acceptance feature and domain README.
- One evidence file under this domain's `evidence/` directory.

## Required verification

Execute `VER-IAR-012` in full: the automated matrix, the lock-agreement and idempotence invariants, `python scripts/validate_engineering_artifacts.py --root .` with zero errors, the full unittest suite compared against the recorded baseline, and the retained existing instruction-route test. Record the `RID018` environment condition explicitly rather than reporting it as a regression. Run start and review preflight with the released evaluator from outside the checkout.

## Evidence to record

Computed and expected fragment digests before and after the edit; the lock-derived managed and owner-editable path sets; validator output; unittest output with the baseline comparison and the environment condition; the diff surface; preflight output for both phases; and the evaluator identity used.

## Stop and escalate conditions

- The fragment digest changes for any reason.
- The technical owner rejects the reuse of `INT-IAR-001` and `CAP-IAR-001`, which invalidates the upstream trace.
- A required fact cannot be stated without exceeding the size bound or duplicating managed policy.
- `.engineering-harness.lock` and the intended path list disagree in a way that suggests the lock itself is wrong.
- Satisfying a rule would require changing an out-of-scope file.

## Completion report format

Report the completed work, the resulting lifecycle state of `REQ-IAR-020`, `SPEC-IAR-012`, `VER-IAR-012`, and this work order, the before and after fragment digests, the evidence path, and the recommended next authorized step. State explicitly that no commit, pull request, verification transition, or release has been performed.
