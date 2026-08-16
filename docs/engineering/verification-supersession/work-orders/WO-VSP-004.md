+++
id = "WO-VSP-004"
type = "work_order"
title = "Supersede the stale aggregate-release verification candidate"
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

# Work Order: Supersede the stale aggregate-release verification candidate

## Objective and authorization

Retire ready `VREC-AGR-001` explicitly in favor of verified corrected candidate `VREC-PMI-001`, preserving both candidates and their evidence as immutable history while removing the stale record from the active assurance queue.

On 2026-08-16, immediately after authorizing the analogous `VREC-DST-006` cleanup, the accountable repository owner stated that `VREC-AGR-001` has the same issue and should be superseded by either `VREC-SEH-001` or `VREC-PMI-001`. Repository intent, requirements, specification, ADR, and prior verification evidence consistently identify `VREC-PMI-001` as the direct corrected candidate. This authorizes `WO-VSP-004`, selection of that documented direct successor, the exact VREC transition, retained evidence, and an honest `implemented` work-order state on `governance/graph-maintenance`. It does not authorize commit, push, pull-request creation, release, tag, publication, deployment, modification of the successor, or another lifecycle decision.

## In scope

- Confirm source `VREC-AGR-001` is `ready` and successor `VREC-PMI-001` is `verified` or `released`.
- Confirm the successor covers every source work order, including `WO-AGR-001`, and applicable verification contract `VER-AGR-001`.
- Confirm no active release record includes `VREC-AGR-001`.
- Transition only `VREC-AGR-001` from `ready` to `superseded`.
- Add one UTC `superseded_at`, non-empty `supersession_authorized_by = "repository-owner"`, and exactly one `superseded_by = ["VREC-PMI-001"]` relation.
- Add a decision note while preserving the source candidate, object format, clean-worktree assertion, capture timestamp, artifact snapshot, evidence paths, original work-order relation, and original verification-contract relation byte-for-byte.
- Retain exact transition evidence in `docs/engineering/verification-supersession/evidence/WO-VSP-004-verification.md`.

## Out of scope

Changing or deleting either candidate, any retained evidence, `VREC-PMI-001`, `VREC-SEH-001`, `WO-AGR-001`, another VREC, release contract or record, runtime source, tests beyond verification execution, managed policy, package metadata, version, tag, publication, deployment, pull-request state, or Git history.

This governance-only work order stops at `implemented`. Superseding the target VREC does not verify or release this work order.

## Authorized decision envelope

The implementation agent may choose concise evidence wording and verification commands. The successor choice is limited to documented direct corrected candidate `VREC-PMI-001`; it may not substitute the later release aggregate, alter captured source facts, infer another lifecycle decision, change release scope, or expand cleanup to another stale record.

## Constraints

Preserve both historical records and every captured source fact. Record only the authorized append-only lifecycle edge. Automation validates and displays the decision but never grants it.

## Expected change surface

- `docs/engineering/aggregate-release/verification-records/VREC-AGR-001.md`
- this bounded work order and its evidence
- the verification-supersession packet summary

## Required verification

Run start and review preflight, formal validation, doctor, focused supersession and inspection tests, supported-runtime regression suites, deterministic inspection and Explorer generation, source/successor status and coverage checks, active-release back-reference inspection, transition field-preservation review, protected-path inspection, and `git diff --check`.

## Evidence to record

Retain source and successor SHA-256 values, immutable metadata and relation comparisons, lineage, UTC transition time and authority, command results, warning classification, bounded diff, and residual authority limits.

## Implementation result

`VREC-AGR-001` is now explicitly `superseded` by verified corrected candidate `VREC-PMI-001`. The direct successor was selected because the governing packet names that exact edge and because it adds the corrective `WO-PMI-001` while preserving coverage of `WO-AGR-001` and `VER-AGR-001`. Later release aggregate `VREC-SEH-001` remains unchanged.

The source candidate, object format, worktree assertion, capture time, artifact snapshot, evidence path, and original relations remain unchanged, and no active release record references it. Formal validation, managed-integrity doctor, supported-runtime regression suites, start and review preflight, deterministic graph inspection, and diff hygiene pass. Exact results are retained in `docs/engineering/verification-supersession/evidence/WO-VSP-004-verification.md`. Commit, push, pull-request creation, release, publication, and merge remain separate decisions.

## Stop and escalate conditions

Stop if the source is no longer `ready`, the successor is not `verified` or `released`, coverage is incomplete, an active release record references the source, a captured source field or original relation would change, validation fails, or cleanup would require modifying a record other than `VREC-AGR-001`.

## Completion report format

Report the explicit successor edge, why the direct corrected candidate was selected, preserved provenance, verification results, retained evidence path, branch, and uncommitted state. Do not claim commit-bound verification, release, publication, push, or merge.
