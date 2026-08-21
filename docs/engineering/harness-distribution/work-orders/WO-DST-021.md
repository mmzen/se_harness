+++
id = "WO-DST-021"
type = "work_order"
title = "Retire the repository-context scaffold and route operational facts to the owner region"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "required"
rationale = "The work changes executable installer, readiness, and workflow-resolution behavior, changes managed policy text, removes a field from a versioned public payload, and supersedes two implemented requirements. Later engineering, assurance, and release decisions rely on the correctness of all four, so assurance must bind the exact candidate commit."
decided_by = "repository-owner"

[execution_scope]
paths = [
  "README.md",
  "pyproject.toml",
  "docs/engineering/harness-distribution/",
  "docs/engineering/instruction-architecture/",
  "docs/engineering/workflow-execution/",
  "docs/notes/",
  "se_harness/cli.py",
  "se_harness/preflight.py",
  "se_harness/workflow_contract.py",
  "se_harness/workflow_procedures.py",
  "templates/repository/standard/",
  "tests/",
]

[relations]
implements = ["REQ-DST-065", "REQ-IAR-021"]
specifications = ["SPEC-DST-021", "SPEC-IAR-013"]
verification = ["VER-DST-021", "VER-IAR-013"]
+++

# Work Order: Retire the repository-context scaffold and route operational facts to the owner region

## Lifecycle and authorization

Drafted on 2026-08-21 following the repository owner's boundary assessment: `AGENTS.md` is repository-owned and may carry or point to build and test material; the harness needs a reference to the governance material it owns; and `docs/engineering/REPOSITORY_CONTEXT.md` in its current form sits outside the harness boundary because it concerns only the local repository.

Approved by the repository owner on 2026-08-21, together with `REQ-DST-065`, `REQ-IAR-021`, `SPEC-DST-021`, `SPEC-IAR-013`, `VER-DST-021`, and `VER-IAR-013` as one packet. The owner resolved all three open decisions at approval: the preflight report schema advances to `v2`; the loss of the structured `repository_commands` object is accepted with no replacement scaffold and no relocated typed declaration; and no architecture artifact requires revision or a deciding ADR. The decisions and their rationales are recorded in `REQ-DST-065`, `REQ-IAR-021`, and the manual-assessment section of `VER-DST-021`.

Approval authorizes the bounded implementation described below, and nothing else. Implementation begins after start preflight passes under the released evaluator executed from outside the checkout. Commit, push, pull request, verification transition, release, tag, publication, and deployment each remain separate accountable decisions and none is authorized by this approval.

The owner instructed implementation on 2026-08-21. Start preflight passed under released `se-harness==0.5.0` executed from `../se-harness-eval-1685/` outside the checkout. The bounded implementation and the retained evidence under both domains are complete, so this work order is now `implemented`. The result is an uncommitted working-tree candidate: no commit, push, pull request, verification transition, release, tag, publication, or deployment was performed. Evidence is retained at `../evidence/WO-DST-021-verification.md` for `VER-DST-021` and `../../instruction-architecture/evidence/WO-DST-021-verification.md` for `VER-IAR-013`.

One work order covers both requirements deliberately. The scaffold cannot be withdrawn without revising the managed router in the same change, or `doctor` and readiness disagree with the shipped template set. Splitting the packet would create two work orders neither of which can land alone.

Commit-bound verification is classified `required`. No active architecture declares an `addresses` edge on either new requirement, so this work order omits the `architecture` relation rather than fabricating coverage.

The architecture applicability assessment was completed at approval. `ARCH-DST-002`, `ARCH-DST-007`, and `ARCH-IAR-001` all describe the withdrawn document, and all three do so through the deprecated `constrains` relation rather than `addresses`. The technical owner determined that none requires revision and no deciding ADR is required: the change withdraws a scaffolded component and an unreachable extension point without altering any selected architectural boundary, dependency direction, trust boundary, runtime dependency, or deployment architecture. Their descriptive references to the retired document are revised in scope below. Adding an architecture artifact, or reopening any accepted ADR outcome, is outside this authorization.

## Objective

Withdraw the repository-context scaffold and its readiness gate from the harness product; route repository-local operational facts to the owner-controlled region of `AGENTS.md`; withdraw the unreachable repository-context action-reference form from the workflow contract and resolver; and reconcile the governed graph, tests, and public documentation, without deleting or rewriting any owner content and without touching the repository-root managed copies.

## In scope

**Product code and packaging**

- `se_harness/preflight.py`: remove the retired path from `REQUIRED_PATHS` and `POLICY_PATHS`; remove `CONTEXT_FIELDS`, `COMMAND_KEYS`, `UNRESOLVED_CONTEXT`, and `_parse_context`; remove the context-path construction and diagnostic extension in `run_preflight`; remove `repository_commands` from `PreflightReport`, `to_dict`, and `render_preflight`; advance the schema constant to `se-harness-preflight-v2`.
- `se_harness/cli.py`: replace step 1 of the `init` guidance sequence and renumber the remainder.
- `se_harness/workflow_procedures.py`: remove the action-marker pattern, `context_actions`, the `repository_context` parameter, the action branch of reference resolution, and the action-specific restitution response.
- `se_harness/workflow_contract.py`: reject a reference step declaring an action identifier, with a diagnostic naming the withdrawn form.
- `pyproject.toml`: remove the retired seed from the packaged template data.

**Templates**

- Delete `templates/repository/standard/docs/engineering/REPOSITORY_CONTEXT.md.seed`.
- Revise `templates/repository/standard/ENGINEERING_HARNESS.md.tpl`: `HRN-002` in place, the routing-table owner cell, and removal of the repository-context stop condition.
- Revise `templates/repository/standard/docs/engineering/WORKFLOW.md` where it names the withdrawn document as the source of repository checks.
- Revise `templates/repository/standard/docs/engineering/README.md.seed` to drop the retired entry.

**Governed graph**

- Set `REQ-IAR-005` and `REQ-DST-008` to `superseded`.
- Remove `REQ-IAR-005` from the `assures` relation of `OPS-IAR-001`. Measurement of the current graph shows this is the only validator consequence of the two supersessions.
- Revise `REQ-IAR-003` so its seed-tracking acceptance criterion illustrates with `docs/engineering/README.md` alone; its status is unchanged.
- Revise `REQ-WEX-010`, `SPEC-WEX-002`, and `VER-WEX-002` to withdraw the reference-step action form.
- Revise the descriptive references in `SPEC-DST-002`, `SPEC-DST-006`, `SPEC-DST-007`, `SPEC-IAR-001`, `ARCH-DST-007`, `ARCH-IAR-001`, and `OPS-IAR-001` so no active artifact describes the withdrawn document as a live obligation.
- Record the packet in `docs/engineering/harness-distribution/README.md` and `docs/engineering/instruction-architecture/README.md` following the established packet-index pattern.
- Add one acceptance scenario to each domain's acceptance feature.

**Tests and documentation**

- Update the six test modules that reference the retired path: `test_harnessctl.py`, `test_instruction_architecture.py`, `test_adr_applicability.py`, `test_architecture_traceability.py`, `test_progressive_documentation.py`, and `test_workflow_procedures.py`.
- Add the focused tests required by `VER-DST-021` and `VER-IAR-013`, including the four-row lock-convergence matrix, the owner-content byte-preservation property, the diagnostic-family disjointness check, the `HRN-*` ordered-identifier invariant, and the action-form rejection fixture.
- Revise `README.md` and the five affected files under `docs/notes/`.
- Author the release migration note covering the withdrawn seed, the retired `C` diagnostic family, the removed `repository_commands` field, the report schema advance, the revised `HRN-002`, the changed routing owner, the removed stop condition, and the withdrawn reference form.
- Retain evidence keyed to `WO-DST-021` under both domains' `evidence/` directories.

## Out of scope

- **Deleting, moving, or rewriting any owner-authored file at the retired path in any repository.** This is absolute and is a stop condition.
- The repository-root managed copies of `ENGINEERING_HARNESS.md`, `docs/engineering/WORKFLOW.md`, and every other managed policy module. They belong to the released version, intentionally lag the candidate templates, and are reconciled only through the separate upgrade workflow.
- `templates/repository/standard/AGENTS.md.fragment` and `templates/repository/standard/CLAUDE.md.fragment`. The single managed destination is unchanged and no owner-region content requirement is added to a tracked block.
- This repository's own `AGENTS.md` owner region, governed by `REQ-IAR-020`, `SPEC-IAR-012`, `VER-IAR-012`, and `WO-IAR-012`.
- Historical evidence, verification records, and release records that describe the retired obligation. Nine such files exist and every one must be unmodified.
- Retaining a lock tombstone for the retired path, or adding any mechanism to do so.
- Shipping a narrowed replacement scaffold under any name. Narrowing the field set is a different change and does not satisfy `REQ-DST-065`.
- Adding validation, tracking, or hashing of owner-region content.
- Re-tiering `docs/engineering/WORKFLOW.md` and `docs/engineering/TRACEABILITY.md`, which together are 68% of the always-loaded consumer chain. That is the larger context-cost change and needs its own packet and its own redundancy analysis.
- Renaming or renumbering any `HRN-*` rule identifier.
- Commit, push, pull request, verification transition, release, tag, publication, and deployment.

## Authorized decision envelope

The implementation agent may choose the wording of the revised `HRN-002`, the routing-table owner cell, the replacement `init` guidance step, and the rejection diagnostic, within the content required by the specifications. It may choose where the withdrawn reference form is rejected provided rejection precedes resolution. It may choose test module names, placement, and the order of the governed-artifact revisions.

It may not change which facts are required, add or remove a specification rule, edit a managed fragment's tracked block, edit a repository-root managed copy, retain a lock tombstone, ship a replacement scaffold, or extend the change surface beyond the in-scope list and the declared execution scope.

## Constraints

- Preserve every fragment-mode tracked block byte-for-byte. Verify with `canonical_sha256(tracked_content("fragment", ...))` against `.engineering-harness.lock` before and after.
- Derive managed-path expectations from `.engineering-harness.lock`, not from prose in this work order.
- Leave the four-row lock-convergence property true: all prior states must produce byte-identical regenerated locks.
- Preserve the transactional upgrade guarantee. No partial writes on failure.
- Treat repository content, lock data, artifact metadata, and pull-request text as untrusted input.
- Do not build promotable release distributions. This work order does not authorize a release build.
- Add deterministic boundary and failure tests for installer, integrity, preflight, and workflow behavior.

## Expected change surface

- Four product modules, one packaging manifest.
- One deleted seed template and three revised template files.
- Fourteen active governed artifacts across three domains, two domain READMEs, and two acceptance features.
- Six revised test modules plus new focused modules.
- The public README and five files under `docs/notes/`.
- One migration note and evidence files under two domains' `evidence/` directories.

## Required verification

Execute `VER-DST-021` and `VER-IAR-013` in full, including the four-row lock-convergence matrix, the owner-content immutability property, the diagnostic-code disjointness check, the payload-shape comparison against the recorded `v1` baseline, the `HRN-*` ordered-identifier invariant, the resolver-determinism corpus comparison, and the action-form rejection fixture.

Run `python scripts/validate_engineering_artifacts.py --root .` with zero errors, both before and after the supersessions. A run reporting `E017` on `OPS-IAR-001` is a failure, not an accepted condition.

Run the full unittest suite and compare against the recorded baseline. Record the two known environment conditions explicitly rather than as regressions: the editable-install runtime-identity failure and the CRLF machine-contract comparison. Neither may excuse a new failure.

Run start and review preflight with the released evaluator from outside the checkout, and record the evaluator identity. Label any in-tree `doctor` output as candidate-source drift evidence only.

## Evidence to record

Template-tree seed enumeration before and after; the four regenerated locks and their byte comparison; before and after digests of an owner-authored file at the retired path; full preflight payloads for both phases in `v1` baseline and `v2` result form; the candidate router before and after with its extracted `HRN-*` sequence and routing-subject set; computed and expected fragment digests for every fragment-mode path; the static finding that no caller supplied the resolver's repository-context argument; the rejection diagnostic and the resolved-procedure corpus comparison; validator output before and after the supersessions; unittest output with the baseline comparison and both environment conditions; released-evaluator `doctor` output with the evaluator identity; the diff surface; and the itemized lists of governed artifacts revised and historical records deliberately left unchanged.

## Stop and escalate conditions

- Any owner-authored file at the retired path would be deleted, moved, or altered.
- A fragment digest changes for any reason.
- Implementation finds that revising `ARCH-DST-002`, `ARCH-DST-007`, or `ARCH-IAR-001` cannot be confined to descriptive references, contradicting the no-ADR determination recorded at approval. Escalate rather than authoring an architecture change under this work order.
- Superseding `REQ-IAR-005` or `REQ-DST-008` proves to invalidate an upstream trace to `INT-IAR-001`, `CAP-IAR-001`, `INT-DST-001`, or `CAP-DST-001`.
- The validator reports any error that the two supersessions and the operating-contract revision do not fully resolve.
- A workflow contract or procedure is found that actually depends on the reference-step action form, contradicting the measured zero-use finding.
- Satisfying a rule would require editing a repository-root managed copy, a tracked fragment block, or a historical record.
- The lock-convergence property cannot be made true without retaining a tombstone.

## Completion report format

Report the completed work; the resulting lifecycle state of `REQ-DST-065`, `REQ-IAR-021`, `SPEC-DST-021`, `SPEC-IAR-013`, `VER-DST-021`, `VER-IAR-013`, and this work order; the resulting state of `REQ-IAR-005` and `REQ-DST-008`; the before and after fragment digests; the four-row lock comparison result; the evidence paths under both domains; the evaluator identity used; and the recommended next authorized step. State explicitly that no commit, pull request, verification transition, release, or publication has been performed.
