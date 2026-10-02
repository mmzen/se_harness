# Plugin integration

## Current public package: plugin 0.2.3

The [0.20.1 release package](../release-0-20-1/README.md) is published with
plugin 0.2.3 at `556d0faf83c32fd188409c5ba191552fad1522e1`.
VREC-PLG-027 verifies local package qualification.
[WO-RLS-029 evidence](../release-0-20-1/evidence/WO-RLS-029/README.md) records
the public file comparison, fresh installs, updates from 0.2.2, offline setup
and native-evidence applicability on both Windows CLIs. Current documentation
integration and final closeout remain separate steps. Repository adoption and
the plugin-owned minimal layout remain separate work.

The [0.2.2 public delivery report](../release-0-20-0/evidence/WO-PLG-031/README.md)
retains that version's observations unchanged.

## Approved next package: plugin 0.2.4

The [0.21.0 release package](../release-0-21-0/README.md) selects the merged
bootstrap, session activation and external-resource adapter. WO-RLS-031 updates
the source manifests and qualifies the final candidate. WO-RLS-032 requires
the public 0.21.0 wheel before marketplace assembly. WO-RLS-033 verifies actual
public fresh/update routes. The new package is not published. Codex Windows
desktop remains an unverified requirement, separate from native CLI evidence.

## Historical marketplace refresh for plugin 0.2.1

[WO-PLG-026](work-orders/WO-PLG-026.md) prepares plugin 0.2.1 with the unchanged
released evaluator 0.19.0. Its [local evidence](evidence/WO-PLG-026/README.md)
records Windows native qualification on Codex and Claude Code.
[WO-PLG-027](work-orders/WO-PLG-027.md) corrects current guidance.
[SPEC-PLG-023](specifications/SPEC-PLG-023.md) defines this delivery and
[VER-PLG-026](verification/VER-PLG-026.md) defines preparation acceptance.

VREC-PLG-023 verified preparation, integrated through PR #496. The separately
authorized public commit `86d75e56e28c0c34819c0079b41dc67075f58490` supplied
plugin 0.2.1 with evaluator 0.19.0. [WO-PLG-028](work-orders/WO-PLG-028.md)
retains the [publication and public-route evidence](evidence/WO-PLG-028/README.md)
under [VER-PLG-027](verification/VER-PLG-027.md). Fresh-install and update package
checks, startup and manual compaction passed on both hosts.
[WO-PLG-029](work-orders/WO-PLG-029.md) covers the approved publication-test
correction. VREC-PLG-024 verified public confirmation; PR #497 integrated the
current claims. The [delivery closeout](evidence/WO-PLG-028/delivery-closeout.md),
integrated through PR #498, records completion of all five declared surfaces.

The 0.2.1 receipt remains historical evidence; it does not establish 0.2.2 delivery.

## Replacement cleanup package

[WO-PLG-025](work-orders/WO-PLG-025.md) is implemented, completing the existing cleanup
with the required onboarding-test and documentation corrections. Its
[implementation evidence](evidence/WO-PLG-025/implementation.md) records passing
regression and handoff checks; assurance is a separate decision.
[VER-PLG-025](verification/VER-PLG-025.md) defines final acceptance, and
[SPEC-DST-029](../harness-distribution/specifications/SPEC-DST-029.md) describes
the plugin-first README presentation. Both definitions are approved.
WO-PLG-024 is rejected as replaced; its history and observations are preserved.

## Root cleanup and plugin ownership

[WO-PLG-024](work-orders/WO-PLG-024.md) adopts plugin ownership in this checkout,
removes the obsolete delegation configuration and corrects selected contributor
guidance. [VER-PLG-024](verification/VER-PLG-024.md) defines its bounded checks.
The verification contract remains approved historical input; the work order is
closed as replaced by WO-PLG-025. [Retained checks](evidence/WO-PLG-024/README.md)
describe the earlier onboarding failures and scope-recording blocker after the
owner-approved README repair. See
[contributor setup and restoration](../../notes/developing-se-harness.md#agent-skills-for-this-checkout).
This adoption does not change the published plugin or earlier assurance records.

## Initial marketplace publication

[WO-PLG-023](work-orders/WO-PLG-023.md) prepared the initial 0.1.0/0.18.0 delivery: the complete Codex and Claude
marketplaces, native installation evidence and provider submission drafts.
[SPEC-PLG-022](specifications/SPEC-PLG-022.md) defines the composition;
[VER-PLG-023](verification/VER-PLG-023.md) separates local acceptance from later
public Git observation. See the [publication procedure](../../notes/plugin-marketplace-publication.md).
Preparation does not establish a public catalog listing.

## Earlier connection work

The current plan applies the merged plugin and codebase KISS changes. The old
[umbrella PR #416](https://github.com/mmzen/se_harness/pull/416) is historical input,
not an implementation queue. The owner approved WO-PLG-022 completion and authorized
WO-PLG-009 and WO-PLG-016 on 2026-09-15. Both work orders are now implemented after the owner approved completion.
[VREC-PLG-017](verification-records/VREC-PLG-017.md) covers WO-PLG-009 and
[VREC-PLG-018](verification-records/VREC-PLG-018.md) covers WO-PLG-016; both
records are verified by the owner. Their implementations are merged in PRs #478 and #479. Start with the
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
This repository uses released 0.19.0 following WO-HUP-021. Plugin marketplace delivery is separate.

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
