+++
id = "WO-SHB-003"
type = "work_order"
title = "Record assurance for the self-hosting upgrade candidate"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-SHB-007", "REQ-SHB-008", "REQ-SHB-009"]
specifications = ["SPEC-SHB-002"]
architecture = ["ARCH-SHB-002", "ADR-SHB-002"]
verification = ["VER-SHB-002"]
+++

# Work Order: Record assurance for the self-hosting upgrade candidate

## Objective and authorization

Record the accountable assurance decision for `VREC-SHB-001` after its exact candidate, retained evidence, ready-record commit, and hosted three-plane CI results became reviewable on merged pull request 40.

On 2026-08-15, the accountable repository owner explicitly instructed `ok i validate the verification record`. The transition was deliberately withheld until the ready record had been committed unchanged and the hosted checks had passed. After the metadata-only PR-body repair made all three planes green without changing the candidate or VREC, the owner reported `merged`. Together, those human decisions authorize only the `VREC-SHB-001` transition from `ready` to `verified`, its decision note, this governance-only work order and evidence, one bounded commit, normal branch publication, and a reviewable pull request. Automation records and validates the decision; it does not grant assurance or release authority.

## In scope

- Confirm candidate `94ef1ac10420d79c61aa43c916d2a1bae15d650a` and ready-record commit `a3f708f658326e60aa4592fc09336a9f84b90b54` exist and are ancestors of merged commit `a89f67f`.
- Confirm the ready record still covers only `WO-SHB-002` under `VER-SHB-002` and retains its captured provenance unchanged.
- Review the retained implementation and commit-bound acceptance evidence, deterministic replay hashes, PR 40 selection repair, and final hosted three-plane results.
- Transition only `VREC-SHB-001` from `ready` to `verified` and add the explicit human-decision note.
- Retain this work order and its evidence with the transition in one governance-only commit and route it through a separate pull request.

## Out of scope

Changing the candidate commit, object format, worktree state, capture timestamp, artifact snapshot, evidence path, work-order relation, verification-contract relation, implementation source, tests, workflows, governor controls, package metadata, version, or historical commits; reconciling or promoting the governor; transitioning another VREC or work order; preparing or approving a release record; merging the governance pull request; tagging; publishing; deploying; force pushing; or rewriting history.

This governance-only work order stops at `implemented`. The target VREC's verified state does not recursively verify this work order or add it to the verified payload.

## Required verification

Run formal artifact validation, managed-integrity doctor, start and review preflight, focused self-hosting tests, the complete unit suite, deterministic Explorer generation, candidate/ready/merge ancestry checks, ready/verified record hash and captured-field preservation checks, protected-path inspection, `git diff --check`, and final diff-scope review. Confirm the governance commit contains only this work order, its evidence, and the bounded VREC transition.

## Evidence and completion

Retain the reviewed lineage, exact hashes, CI run and repair facts, commands, results, transition integrity, authority limits, deviations, and residual risks in `docs/engineering/self-hosting-boundary/evidence/WO-SHB-003-verification.md`. After all checks pass, mark this work order `implemented`, commit the three bounded files, push normally, and open a pull request declaring `Harness-Work-Order: WO-SHB-003` with LF line endings.

## Stop and escalate conditions

Stop if the ready record differs from commit `a3f708f658326e60aa4592fc09336a9f84b90b54`, candidate or ready-record ancestry is invalid, final hosted checks are not green, captured provenance would change, validation fails, or the action would affect anything other than `VREC-SHB-001` and this governance pair.

## Implementation result

`VREC-SHB-001` is now `verified` through the repository owner's accountable decision. Candidate commit, object format, clean worktree state, capture timestamp, artifact snapshot, evidence path, work-order relation, and verification-contract relation remain unchanged. The exact candidate and ready-record commits are ancestors of merged pull request 40, whose final three-plane checks passed after an LF-only PR-body repair that did not change repository content.

Formal validation, candidate-source doctor and preflights, focused self-hosting tests, the complete suite, deterministic Explorer generation, ancestry, transition diff, record hashes, protected paths, and diff hygiene pass. The selected 0.2.1 released-governor executable predictably reports the newer Explorer asset as distribution drift when asked to interpret the post-0.2.1 work order; that cross-version observation is retained but is not misrepresented as candidate-semantic assessment. Exact results and remaining authority boundaries are retained in `docs/engineering/self-hosting-boundary/evidence/WO-SHB-003-verification.md`.
