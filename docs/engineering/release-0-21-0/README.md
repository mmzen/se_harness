# Release 0.21.0 delivery

Human mmzen approved the package and required commit-bound verification.
RLS-SEH-031 is released; evaluator 0.21.0 is published. VREC-PLG-030 verifies
plugin 0.2.4 qualification, and the separately authorized marketplace update is
public at `7e366438165a40a14783bac650a2887e7ec8bc75`. WO-RLS-033 is in progress.
This repository continues to use released evaluator 0.20.1.

[Current observations](evidence/WO-RLS-033/README.md) retain public package/setup
results and the outstanding native, documentation and marker conditions.

| Stage | Work order | Verification |
| --- | --- | --- |
| Final evaluator candidate, pinned build, aggregate verification and RLS | [WO-RLS-031](work-orders/WO-RLS-031.md) | [VER-RLS-030](verification/VER-RLS-030.md) |
| Plugin 0.2.4 assembly and native qualification after public evaluator release | [WO-RLS-032](work-orders/WO-RLS-032.md) | [VER-RLS-031](verification/VER-RLS-031.md) and existing VER-IAR-021 |
| Public fresh/update routes, current documentation and delivery closeout | [WO-RLS-033](work-orders/WO-RLS-033.md) | [VER-RLS-032](verification/VER-RLS-032.md) |

[REL-SEH-033](release/REL-SEH-033.md) selects the exact release work set, final
verification sequence and five delivery surfaces. Reuse accepted definitions and
existing tools; no new product requirement, framework or approval artifact is added.

## Historical preparation inputs

- Proposed evaluator: 0.21.0. Proposed plugin: 0.2.4, after public maintenance 0.2.3.
- Preparation base: f5f7c77c6eadfd7d6f1c68e136f1f7cc29cfc0a5.
- Confirmed assurance: required commit-bound verification for all three work orders.
- Review envelope: ordinary release-review branch push/draft PR and read-only
  existing build/replay workflow dispatches under WO-RLS-031.
- Human verification of the final candidate, exact RLS decision, merges, protected
  provider approval, marketplace publication and marker changes remain distinct.
- Existing evaluator publication and repository-adoption requests are retained.

## Qualification limits

Claude exact-release native qualification and Codex Windows desktop remain unverified. DEC-RLS-002 accepts these gaps for WO-RLS-032 only; public-route native assessment under WO-RLS-033 remains pending.
DEC-RLS-001 records the earlier evaluator-release desktop deviation. Neither
decision establishes missing native evidence or changes the repository selection.

## Current observations

Independent public marketplace readback matches all 69 qualified files. Fresh
installation and updates from 0.2.3 match all 29 installed files on both Windows
CLIs. Offline setup and exact evaluator identity checks pass on all four routes.
Overall delivery remains incomplete while native public-route assessment,
documentation verification/integration/readback and separately authorized release
marker observations remain outstanding. Published package bytes and historical
release evidence are unchanged.
