# Plugin integration

## Remaining work

The current plan applies the merged plugin and codebase KISS changes. The old
[umbrella PR #416](https://github.com/mmzen/se_harness/pull/416) is historical input,
not an implementation queue. The owner approved WO-PLG-022 completion and authorized
WO-PLG-009 and WO-PLG-016 on 2026-09-15. Both work orders are now implemented after the owner approved completion.
[VREC-PLG-017](verification-records/VREC-PLG-017.md) covers WO-PLG-009 and
[VREC-PLG-018](verification-records/VREC-PLG-018.md) covers WO-PLG-016; both
records are verified by the owner. Integration remains pending in PRs #478 and #479. Start with the
[local installation guide](../../notes/plugin-installation-guide.md), then see
[connection evidence](evidence/WO-PLG-009/README.md) and
[host walkthrough evidence](evidence/WO-PLG-016/README.md). Helpers remain deferred.

| Order | Work order | Result |
| --- | --- | --- |
| 1 | [WO-PLG-009](work-orders/WO-PLG-009.md) | Connect and maintain projects using existing setup/installer operations. Absorbs old WO-PLG-013. |
| 2 | [WO-PLG-016](work-orders/WO-PLG-016.md) | One installation guide and practical checks of claimed host use. Absorbs old WO-PLG-015. |
| Deferred | [WO-PLG-014](work-orders/WO-PLG-014.md) | Helpers only after a concrete need is identified; not required for installation. |

[The amendment and full disposition](../../notes/plugin-backlog-kiss-2026-09-14.md)
explain what was kept and removed. [WO-PLG-022](work-orders/WO-PLG-022.md) governs
this definition cleanup; [its evidence](evidence/WO-PLG-022/README.md) records the checks.

## Current implementation baseline

WO-PLG-001 through 008, 010 through 012, and 017 through 021 are implemented on
main. The decisive simplifications are [SPEC-PLG-021](specifications/SPEC-PLG-021.md)
and the [codebase KISS work](../harness-simplification/README.md). They supply
disposable skill replacement, one repairable environment, explicit checks,
proportionate evidence and one execution route. Optional helpers are not a prerequisite.

Merged source is not automatically a published plugin or an adopted evaluator.
This repository still uses released 0.17.0 until an explicit release/adoption action.

## Historical records

Earlier work orders, decisions, verification records and evidence remain under
their existing paths with their recorded lifecycle states and tested candidates.
Their old hooks, ownership transactions and qualification matrices describe those
past deliveries, not additional acceptance conditions for the remaining work.
The specification applicability tables define the changed behavior prospectively.

- [Initial definition delivery plan](../../notes/plugin-definition-delivery-2026-09-08.md)
- [Ownership migration](../../notes/plugin-ownership-migration-2026-09-12.md)
- [Accepted plugin simplification](specifications/SPEC-PLG-021.md)
- [Plugin simplification evidence](evidence/WO-PLG-021/implementation/README.md)
