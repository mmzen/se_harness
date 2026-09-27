# Proposed release coverage — SE Harness 0.19.0

Draft review material. No release or verification decision is recorded here.

Baseline: `v0.18.0` (`353da23881fdf045a52322a313c1e67341f7a9b1`).
Reviewed merged head: `fbc47dfdcff2b355ee973acb5be09bcdf7cefe78`.
The final release candidate will also contain the approved WO-RLS-025 work.

| Work order | Included change | Existing verified evidence |
| --- | --- | --- |
| [WO-DOC-016](../harness-distribution/work-orders/WO-DOC-016.md) | Refresh the public README for published plugin onboarding | [VREC-DOC-008](../harness-distribution/verification-records/VREC-DOC-008.md) |
| [WO-ECP-039](../execution-control-plane/work-orders/WO-ECP-039.md) | Correct the plugin-owned upgrade rehearsal assertion | [VREC-ECP-041](../execution-control-plane/verification-records/VREC-ECP-041.md) |
| [WO-HUP-019](../repository-harness-upgrade/work-orders/WO-HUP-019.md) | Upgrade the repository evaluator from 0.17.0 to 0.18.0 | [VREC-HUP-018](../repository-harness-upgrade/verification-records/VREC-HUP-018.md) |
| [WO-HUP-020](../repository-harness-upgrade/work-orders/WO-HUP-020.md) | Support plugin ownership in the existing CI assessor | [VREC-ECP-041](../execution-control-plane/verification-records/VREC-ECP-041.md), [VREC-HUP-019](../repository-harness-upgrade/verification-records/VREC-HUP-019.md) |
| [WO-IAR-013](../instruction-architecture/work-orders/WO-IAR-013.md) | Split the agent instructions and preserve their meaning | [VREC-IAR-012](../instruction-architecture/verification-records/VREC-IAR-012.md) |
| [WO-IAR-014](../instruction-architecture/work-orders/WO-IAR-014.md) | Implement evaluator discovery and safe installer migration | [VREC-IAR-012](../instruction-architecture/verification-records/VREC-IAR-012.md) |
| [WO-IAR-015](../instruction-architecture/work-orders/WO-IAR-015.md) | Deliver current instructions at startup and after compaction | [VREC-IAR-011](../instruction-architecture/verification-records/VREC-IAR-011.md) |
| [WO-IAR-016](../instruction-architecture/work-orders/WO-IAR-016.md) | Package the approved startup and compaction instruction delivery | [VREC-IAR-012](../instruction-architecture/verification-records/VREC-IAR-012.md) |
| [WO-IAR-017](../instruction-architecture/work-orders/WO-IAR-017.md) | Align regression coverage with the approved instruction evolution | [VREC-IAR-009](../instruction-architecture/verification-records/VREC-IAR-009.md) |
| [WO-IAR-018](../instruction-architecture/work-orders/WO-IAR-018.md) | Cover the preserved governance package in PR 489 | Governance transport; assurance classified `not_required`. |
| [WO-IAR-019](../instruction-architecture/work-orders/WO-IAR-019.md) | Exercise guarded instruction retirement in the upgrade rehearsal | [VREC-IAR-010](../instruction-architecture/verification-records/VREC-IAR-010.md) |
| [WO-PLG-023](../plugin-integration/work-orders/WO-PLG-023.md) | Prepare Verity Plane marketplace publication | [VREC-PLG-019](../plugin-integration/verification-records/VREC-PLG-019.md), [VREC-PLG-020](../plugin-integration/verification-records/VREC-PLG-020.md) |
| [WO-PLG-025](../plugin-integration/work-orders/WO-PLG-025.md) | Complete repository cleanup and align onboarding checks | [VREC-ECP-041](../execution-control-plane/verification-records/VREC-ECP-041.md), [VREC-HUP-019](../repository-harness-upgrade/verification-records/VREC-HUP-019.md), [VREC-PLG-022](../plugin-integration/verification-records/VREC-PLG-022.md) |
| [WO-RLS-025](work-orders/WO-RLS-025.md) | Final qualification, reproducible checker build and plugin 0.2.0 inputs. | Proposed; no result yet. |

## Membership review

The released `release-unit` command found WO-ECP-039, WO-HUP-019,
WO-HUP-020, WO-PLG-023, WO-PLG-025 and WO-RLS-024. Review of the Git delta
and formal records adds WO-DOC-016 and WO-IAR-013 through WO-IAR-019.
WO-RLS-024 is excluded because RLS-SEH-027 already released it.
Rejected WO-PLG-024 is excluded; its completed successor is WO-PLG-025.

The five untraced first-parent commits are the merges of PRs #483, #484, #485,
#486 and #489. PR #483 carries WO-DOC-016; PR #489 carries the IAR work above.
PRs #484–486 are owner README/value-proposition edits. They are present in the
source tree, but this table does not invent a work-order or historical approval
for them. Inspect their final content as part of distribution review; do not
add retrospective trailers, exemptions or formal authority.

## Final verification

The linked records describe different historical candidates. They are inputs
to the final integration assessment, not proof that this release candidate has
already been verified. Collect the union of each selected WO's declared VERs
and capture one final aggregate VREC after implementation and checks complete.
Include WO-IAR-018 without changing its approved assurance classification.

## Packaging finding

At the merged head, both native manifests still declare 0.1.0. The production
assembly plan omits `scripts/inject_instructions.py` and both host hook files.
WO-RLS-025 proposes the three plan additions and plugin version 0.2.0.
No assembly plan or manifest has been changed during proposal drafting.
