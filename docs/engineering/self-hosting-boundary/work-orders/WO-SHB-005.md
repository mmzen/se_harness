+++
id = "WO-SHB-005"
type = "work_order"
title = "Record assurance for the governor 0.3.0 promotion candidate"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-SHB-005", "REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
specifications = ["SPEC-SHB-001", "SPEC-SHB-002"]
architecture = ["ARCH-SHB-001", "ADR-SHB-001", "ARCH-SHB-002", "ADR-SHB-002"]
verification = ["VER-SHB-001", "VER-SHB-002"]
+++

# Work Order: Record assurance for the governor 0.3.0 promotion candidate

## Objective and authorization

Record the accountable assurance decision for `VREC-SHB-002` after its exact candidate, retained evidence, committed ready record, and hosted three-plane CI results became reviewable on pull request 44.

On 2026-08-15, after all released-governor, candidate-source, and candidate-package checks passed, the accountable repository owner explicitly instructed `ok CI, I validate the validation record, it can be committed and pushed`. That human decision authorizes only the transition of `VREC-SHB-002` from `ready` to `verified`, its decision note, this governance-only work order and evidence, one bounded governance commit, and a normal push to the existing pull request. Automation records and validates the decision; it does not grant assurance or merge authority.

## In scope

- Confirm candidate `7726d7686dfe7a01452c53f21871a78569cf3ac4` precedes ready-record commit `e0ac4e8b1018e909cc6fedaaa6ead430d2445d2f` and both are selected by pull request 44.
- Confirm the ready-record blob is `a304d44f45b44a2ed596c4dd6bc2876a2ff99acf` and still covers only `WO-SHB-004` under `VER-SHB-001` and `VER-SHB-002`.
- Confirm both hosted workflow runs completed the released-governor, candidate-source, and candidate-package planes successfully.
- Transition only `VREC-SHB-002` from `ready` to `verified` and add the accountable decision note.
- Retain this work order and its evidence with the transition in one governance-only commit and push it normally to pull request 44.

## Out of scope

Changing the candidate commit, object format, worktree state, capture timestamp, artifact snapshot, evidence path, work-order or verification-contract relations, implementation source, tests, workflow, descriptor, lock, package, version, historical commit, or ready-record commit; transitioning another artifact; preparing a release record; merging pull request 44; tagging; publishing; deploying; force pushing; or rewriting history.

This governance-only work order stops at `implemented`. The target VREC's verified state does not recursively verify this work order or add it to a product release payload.

## Required verification

Run formal artifact validation, exact published 0.3.0 doctor, review preflight, candidate and ready-record ancestry checks, ready-versus-verified captured-field preservation checks, hosted-check inspection, `git diff --check`, and final diff-scope review. Confirm the governance commit contains only this work order, its evidence, and the bounded VREC transition.

## Evidence and completion

Retain the reviewed lineage, exact hashes, hosted run and job results, transition integrity, authority limits, deviations, and residual risks in `docs/engineering/self-hosting-boundary/evidence/WO-SHB-005-verification.md`. After all checks pass, keep this work order `implemented`, commit the three bounded files, and push normally to the existing branch.

## Stop and escalate conditions

Stop if the ready record differs from commit `e0ac4e8b1018e909cc6fedaaa6ead430d2445d2f`, candidate ancestry is invalid, any required hosted plane is not successful, captured provenance would change, validation fails, or the action would affect anything other than `VREC-SHB-002` and this governance pair.

## Implementation result

`VREC-SHB-002` is now `verified` through the repository owner's accountable decision. Candidate commit, object format, clean worktree state, capture timestamp, artifact snapshot, evidence path, work-order relation, and both verification-contract relations remain unchanged. Candidate `7726d7686dfe7a01452c53f21871a78569cf3ac4` is the parent lineage of ready-record commit `e0ac4e8b1018e909cc6fedaaa6ead430d2445d2f`; pull request 44 selected that ready-record commit before the assurance transition.

Formal validation, exact published 0.3.0 doctor, review preflight, ancestry, ready-blob identity, captured-field preservation, hosted-check inspection, and diff hygiene pass. Exact results and remaining merge authority are retained in `docs/engineering/self-hosting-boundary/evidence/WO-SHB-005-verification.md`.
