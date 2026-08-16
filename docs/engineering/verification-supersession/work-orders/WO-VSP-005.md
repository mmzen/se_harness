+++
id = "WO-VSP-005"
type = "work_order"
title = "Publish the aggregate stale-verification cleanup"
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

# Work Order: Publish the aggregate stale-verification cleanup

## Objective and authorization

Carry the two independently authorized and implemented stale-record transitions from `WO-VSP-003` and `WO-VSP-004` through one clean candidate, one accurately scoped pull request, and one later aggregate ready verification record.

On 2026-08-16, after the inspection-semantics correction merged and the graph-maintenance transaction was restored, the repository owner instructed `ok let's finish the current supersession transaction`. That instruction authorizes this bounded publication envelope, refreshed evidence, the candidate commit, normal branch push, one pull request declaring `WO-VSP-005`, and preparation of one aggregate `ready` VREC covering `WO-VSP-003`, `WO-VSP-004`, and `WO-VSP-005`. It does not authorize transition of that VREC to `verified`, merge, release, tagging, publication, deployment, another supersession, or Phase 2 operating-contract activation.

## In scope

- Preserve the exact `VREC-DST-006 -> VREC-SEH-005` decision authorized by `WO-VSP-003`.
- Preserve the exact `VREC-AGR-001 -> VREC-PMI-001` decision authorized by `WO-VSP-004`.
- Refresh retained evidence after rebasing onto merged `IAR-010` without changing either supersession decision.
- Carry both completed work orders, their evidence, the two source-record transitions, and the packet index in one clean candidate commit.
- Use this work order as the single PR-level scope declaration required by CI.
- After the clean candidate exists, prepare one aggregate ready VREC containing all three work orders, `VER-VSP-001`, and evidence keyed to every work order.

## Out of scope

Changing either successor; changing a captured candidate, snapshot, evidence path, original relation, transition time, or transition authorizer; adding another supersession; disposing draft release or operating contracts; modifying runtime behavior; changing managed controls; release, tagging, package publication, deployment, VREC assurance transition, or merge.

## Authorized decision envelope

The implementation agent may choose the concise PR summary, commit message, refreshed deterministic output locations, and aggregate VREC ID consistent with the repository sequence. It may not alter the two decisions, combine their historical source records, infer assurance, or treat the publication envelope as release-bearing work.

## Required verification

Run formal validation, doctor, review preflight for all three work orders, complete supported-runtime regression, focused revision-provenance/dashboard/inspection tests, deterministic inspection and Explorer generation, immutable-field and successor-coverage comparison, active-release back-reference inspection, protected-path inspection, and diff hygiene.

## Evidence and result

Evidence is retained in `docs/engineering/verification-supersession/evidence/WO-VSP-005-verification.md`. Both original work orders remain honestly `implemented`; this work order is also `implemented` because the bounded candidate preparation and evidence are complete. Commit-bound assurance remains a later human decision over the aggregate ready record.

## Stop and escalate conditions

Stop if either source is no longer `superseded`, either successor becomes ineligible, coverage is lost, an active release references a source, captured provenance changes, the diff includes another lifecycle decision, validation fails, or one PR cannot accurately declare this complete scope.
