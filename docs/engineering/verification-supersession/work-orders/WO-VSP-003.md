+++
id = "WO-VSP-003"
type = "work_order"
title = "Supersede the stale documentation verification candidate"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
implements = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007"]
specifications = ["SPEC-VSP-001"]
architecture = ["ARCH-VSP-001", "ADR-VSP-001"]
verification = ["VER-VSP-001"]
+++

# Work Order: Supersede the stale documentation verification candidate

## Objective and authorization

Retire ready `VREC-DST-006` explicitly in favor of verified aggregate `VREC-SEH-005`, preserving the earlier documentation candidate and evidence as immutable history while removing the stale record from the active assurance queue.

On 2026-08-16, after the preceding inspection and documentation work was merged, the accountable repository owner instructed `first create a branch, something like graph-maintenance, and change VREC-DST-006 to state superseded, by VREC-SEH-005`. That decision authorizes branch `governance/graph-maintenance`, this bounded governance work order, the exact VREC transition, retained evidence, and an honest `implemented` work-order state. It does not authorize commit, push, pull-request creation, modification of the successor or another record, release, tag, publication, or deployment.

## In scope

- Confirm source `VREC-DST-006` is `ready` and successor `VREC-SEH-005` is `verified` or `released`.
- Confirm the successor covers every source work order, including `WO-DOC-009`, and applicable verification contract `VER-DST-006`.
- Confirm no active release record includes `VREC-DST-006`.
- Transition only `VREC-DST-006` from `ready` to `superseded`.
- Add one UTC `superseded_at`, non-empty `supersession_authorized_by = "repository-owner"`, and exactly one `superseded_by = ["VREC-SEH-005"]` relation.
- Add a decision note while preserving the source candidate, object format, clean-worktree assertion, capture timestamp, artifact snapshot, evidence paths, original work-order relation, and original verification-contract relation byte-for-byte.
- Retain exact transition evidence in `docs/engineering/verification-supersession/evidence/WO-VSP-003-verification.md`.

## Out of scope

Changing or deleting either candidate, any retained evidence, `VREC-SEH-005`, `WO-DOC-009`, another VREC, a release contract or record, runtime source, tests beyond verification execution, managed policy, package metadata, version, tag, publication, deployment, pull-request state, or Git history.

This governance-only work order stops at `implemented`. Superseding the target VREC does not verify or release this work order.

## Authorized decision envelope

The implementation agent may choose concise evidence wording and verification commands. It may not select another successor, alter captured source facts, infer another lifecycle decision, change release scope, or expand cleanup to another stale record.

## Required verification

Run start and review preflight, formal validation, doctor, focused supersession and instruction-architecture tests, the complete supported-runtime suite, deterministic inspection and Explorer generation, source/successor status and coverage checks, active-release back-reference inspection, transition field-preservation review, protected-path inspection, and `git diff --check`.

## Evidence and completion

Retain source and successor SHA-256 values, immutable metadata and relation comparisons, lineage, UTC transition time and authority, command results, warning classification, bounded diff, and residual authority limits in the work-order evidence. After all checks pass, set this work order to `implemented` and stop for separate commit, push, and pull-request authority.

## Implementation result

`VREC-DST-006` is now explicitly `superseded` by verified aggregate `VREC-SEH-005`. The successor covers the source record's complete `WO-DOC-009` work set and its `VER-DST-006` contract, while the source candidate, object format, worktree assertion, capture time, artifact snapshot, evidence path, and original relations remain unchanged. No active release record references the source.

Formal validation, managed-integrity doctor, start and review preflight, supported-runtime tests, deterministic inspection and Explorer generation, transition-field preservation, active-release inspection, and diff hygiene pass. Exact results are retained in `docs/engineering/verification-supersession/evidence/WO-VSP-003-verification.md`. Commit, push, pull-request creation, release, publication, and merge remain separate decisions.

## Stop and escalate conditions

Stop if the source is no longer `ready`, the successor is not `verified` or `released`, coverage is incomplete, an active release record references the source, a captured source field or original relation would change, validation fails, or the cleanup would require modifying a record other than `VREC-DST-006`.

## Completion report format

Report the explicit successor edge, preserved provenance, verification results, retained evidence path, branch, and uncommitted state. Do not claim commit-bound verification, release, publication, push, or merge.
