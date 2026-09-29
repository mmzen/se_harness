# Release membership and assurance coverage

REL-SEH-031 selects the following 16 work orders and 10 distinct verification
contracts. Historical verification applies only at its recorded candidate.
The final aggregate VREC must cover every member and contract at one clean C.
WO-PLG-030 and WO-PLG-031 are downstream delivery work, excluded from this
pre-publication candidate because they require its public evaluator wheel.

| Work order | Required verification | Historical assurance |
| --- | --- | --- |
| [WO-HUP-021](../repository-harness-upgrade/work-orders/WO-HUP-021.md) | VER-HUP-021 | VREC-HUP-021 |
| [WO-HUP-023](../repository-harness-upgrade/work-orders/WO-HUP-023.md) | VER-HUP-021 | VREC-HUP-021 |
| [WO-KIS-016](../harness-simplification/work-orders/WO-KIS-016.md) | VER-KIS-009 | VREC-KIS-016 |
| [WO-IAR-020](../instruction-architecture/work-orders/WO-IAR-020.md) | VER-IAR-016 | VREC-IAR-015 |
| [WO-IAR-021](../instruction-architecture/work-orders/WO-IAR-021.md) | VER-IAR-015 | VREC-IAR-013 |
| [WO-IAR-022](../instruction-architecture/work-orders/WO-IAR-022.md) | VER-IAR-017 | VREC-IAR-014 |
| [WO-IAR-023](../instruction-architecture/work-orders/WO-IAR-023.md) | VER-IAR-015 | VREC-IAR-013 |
| [WO-IAR-024](../instruction-architecture/work-orders/WO-IAR-024.md) | VER-IAR-017 | VREC-IAR-014 |
| [WO-IAR-025](../instruction-architecture/work-orders/WO-IAR-025.md) | VER-IAR-017 | VREC-IAR-014 |
| [WO-RLO-010](../release-orchestration/work-orders/WO-RLO-010.md) | VER-RLO-007 | VREC-RLO-010 |
| [WO-RLO-011](../release-orchestration/work-orders/WO-RLO-011.md) | VER-RLO-008 | VREC-RLO-011 |
| [WO-PLG-026](../plugin-integration/work-orders/WO-PLG-026.md) | VER-PLG-026 | VREC-PLG-023 |
| [WO-PLG-027](../plugin-integration/work-orders/WO-PLG-027.md) | VER-PLG-026 | VREC-PLG-023 |
| [WO-PLG-028](../plugin-integration/work-orders/WO-PLG-028.md) | VER-PLG-027 | VREC-PLG-024 |
| [WO-PLG-029](../plugin-integration/work-orders/WO-PLG-029.md) | VER-PLG-027 | VREC-PLG-024 |
| [WO-RLS-026](../release-0-20-0/work-orders/WO-RLS-026.md) | VER-RLS-026 | New aggregate preparation |

The historical evidence review compares all directly bound evidence Git blobs
with the original verified candidates and checks evaluator sidecar digests.
Current source/package/upgrade CI and the pinned build replay supplement those
bounded observations; they do not rewrite them. Native qualification for the
new 0.2.2 archives belongs to VER-PLG-028 after evaluator publication.
