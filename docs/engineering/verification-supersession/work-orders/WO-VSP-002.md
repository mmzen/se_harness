+++
id = "WO-VSP-002"
type = "work_order"
title = "Supersede the stale dashboard verification candidate"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-13"
updated = "2026-08-13"

[relations]
implements = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007"]
specifications = ["SPEC-VSP-001"]
architecture = ["ARCH-VSP-001", "ADR-VSP-001"]
verification = ["VER-VSP-001"]
+++

# Work Order: Supersede the stale dashboard verification candidate

## Objective and authorization

Retire ready `VREC-DST-007` explicitly in favor of verified `VREC-DST-008`, preserving the earlier candidate and evidence as immutable history while removing it from the active assurance queue.

After `VREC-DST-008` was separately retained and transitioned to verified, the accountable repository owner explicitly instructed `ok for WO-DST-007 supersession then so the graph is clean` on 2026-08-13. In context, this authorizes supersession of `VREC-DST-007`—not the unchanged implemented work order `WO-DST-007`—plus this separate governance work order and evidence, one bounded supersession commit, an accurate PR summary update, and a normal push to existing PR 35. Automation records and validates the decision but does not infer it.

## In scope

- Confirm source `VREC-DST-007` is `ready` and successor `VREC-DST-008` is `verified`.
- Confirm the successor's `verifies_work_order` set covers every work order in the source.
- Confirm no active ready or released release record includes `VREC-DST-007`.
- Transition only `VREC-DST-007` from `ready` to `superseded`.
- Add one UTC `superseded_at`, non-empty `supersession_authorized_by = "repository-owner"`, and exactly one `superseded_by = ["VREC-DST-008"]` relation.
- Add a decision note while preserving the source candidate, object format, clean worktree state, capture timestamp, artifact snapshot, evidence paths, original work-order relation, and original verification-contract relation byte-for-byte.
- Retain exact transition evidence and push the bounded governance commit to PR 35.

## Out of scope

Changing or deleting either candidate, evidence file, snapshot, original VREC relation, `VREC-DST-008`, `WO-DST-007`, `WO-DOC-011`, `WO-DST-008`, another VREC, any release record, implementation source, dashboard behavior, managed policy, tests, package metadata, version, tag, publication, deployment, pull-request merge, force push, or Git history.

This governance-only work order stops at `implemented`. Superseding the target VREC does not verify or release this work order.

## Required verification

Run formal validation, doctor, start and review preflight, focused supersession and dashboard tests, the complete suite, deterministic Explorer generation, source/successor status and coverage checks, active-release back-reference inspection, transition-diff and hash review, protected-path inspection, PR checks, and `git diff --check`. Confirm the final governance diff contains only `VREC-DST-007`, this work order, and its retained evidence.

## Evidence and completion

Retain exact source and successor hashes, relation sets, lineage, transition timestamp and authority, commands, results, warning classification, bounded diff, and residual authority limits in `docs/engineering/verification-supersession/evidence/WO-VSP-002-verification.md`. After all checks pass, mark this work order `implemented`, commit the three bounded files, push normally to PR 35, and report the explicit historical edge.

## Stop and escalate conditions

Stop if the source is no longer ready, the successor is not verified or released, coverage is incomplete, an active release record references the source, any captured source field or original relation would change, validation fails, or cleanup would require modifying any record other than `VREC-DST-007`.

## Implementation result

`VREC-DST-007` is now explicitly `superseded` by verified `VREC-DST-008`. The transition records the repository owner's authority and UTC decision time while preserving every captured source field and original relation. The successor covers the source's complete `WO-DST-007` work set, no active release record references the source, and the explicit declared edge appears in the deterministic Explorer snapshot.

Formal validation, managed-integrity doctor, start and review preflight, focused supersession and dashboard tests, the complete suite, two deterministic Explorer generations, active-release inspection, transition hash and field-preservation checks, protected-path inspection, and diff hygiene pass. The targeted stale-ready `W-REV-004` observation for `VREC-DST-007` is removed; the unrelated historical `VREC-AGR-001` observation and classified legacy advisories remain. Exact results are retained in `docs/engineering/verification-supersession/evidence/WO-VSP-002-verification.md`.
