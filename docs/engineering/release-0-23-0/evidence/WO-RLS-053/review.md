# Proposal: fit the complete native test input

**Approve WO-RLS-053 and required verification**, including its exact one-line
release-membership amendment. This changes two existing test instruction files.
The implementation and accepted release contract are still unchanged.

## Problem and proposed change

Both missing-input diagnostics now pass. The positive case does not start:
its complete input exceeds 64 KiB. The launcher correctly refuses it without
truncation. This is an input-assembly blocker, not a new Claude content failure.
See the [current results](../WO-RLS-045/qualification-progress-05c629dd.md).

- Shorten `native-tools.md` from **8,684 to 5,303 bytes** (39%). Keep typed
  operations, file discovery, permissions and evidence handling visible.
- Put the original raw-request, lifecycle and encoding paragraphs in the
  **existing** `native-execution-tools.md`, unchanged. Link them before use.
  They are not needed for ordinary typed drafting. Its original check capability
  instructions are unchanged and still required when choosing a planned check.
- Remove duplicated authoring/report policy in favor of the already delivered
  plugin reference. No new file, tool, dependency or ordinary drafting read.

Review the exact [main-guide diff](native-tools.patch),
[execution-guide diff](native-execution-tools.patch), or complete proposed
[main guide](native-tools-proposed.txt) and [execution guide](native-execution-tools-proposed.txt).
Keep every original source file, selected canonical section and plugin reference.
Keep the 65,536-byte limit, task, model, permissions and content criteria.

## Offline checks

The unchanged launcher's input-assembly statements were executed through its
size/credential guard, with all subsequent provider/capture code excluded.
No provider or service was contacted. Both variants use equal-length paths for
each host under this ordinary workspace. They include all nine selected sections,
all six initial references and every original fixture file with matching digests.

| Host | Current guide | Proposed guide | Remaining bytes |
| --- | ---: | ---: | ---: |
| Claude | 67,481 — refused | 64,100 — fits | 1,436 |
| Codex | 68,251 — refused | 64,870 — fits | 666 |

The first draft fit Claude but exceeded Codex by 77 bytes; its result is retained.
An intervening shell quoting error prevented one offline rerun from starting; no
inputs or provider were affected. The final measured proposal passes both hosts.
The [measurements](offline-budget.json) retain paths, source identities and limits;
the [first attempt](offline-budget-first-attempt.json) remains visible.
The [check script](offline-budget.py) retains the host-specific assembly method;
its original fixture/package inputs are the preceding qualification evidence.

This is deliberately a size result only. Codex has limited headroom. Reassemble
the exact future launch inputs before contacting either provider; longer paths
or changed selection data may still fail. No unusually short-path workaround or
claim about all Windows paths. Native behavior and duration remain unproven.

## Instruction coverage and simplicity review

| Existing duty | Proposed location |
| --- | --- |
| One helper call, original permission boundary, new outputs inside work | Main guide introduction |
| Exact mutation fields, no automatic retries, no hosted dry-run, decoded created revision | Main guide: Draft mutations; full typed table retained |
| Exact revision reads and forbidden mutation-only fields | Main guide: Read one revision |
| Status/identity, section selectors, bounded file reads, JSON/base64 and truncated-read recovery | Main guide: Reads and discovery |
| Unknown-heading handling, known-path reuse, entry prerequisites | Main guide: Reads and discovery |
| Available test assertion, execution authority and evidence fields | Existing execution guide, required before planning/executing checks |
| Raw schemas, test-copy flags, handoff encoding | Original paragraphs copied unchanged to execution guide; explicit reading trigger |
| Uncertain effects and original operation-key recovery | Main guide: Draft mutations; existing plugin recovery rule unchanged |
| Observation snapshots, failed reads, incomplete capture, exact JSON record paths and original evidence | Main guide: Report evidence |
| Agent-selected operations, inspect template before editing, failed-call retention, content review and truthful final report | Already delivered hosted-drafts: Author and submit / Report and recover; explicit reference in main guide |

The main guide plus execution guide is smaller overall, not merely relocated.
The move reuses an existing staged file and adds no normal drafting call. A raw
operation may require reading its detail, as the explicit route indicates. The
first shortened guide still exceeded Codex's limit; further editing made it fit.
Changing launcher serialization or increasing the limit would add code/scope or
change the accepted contract; neither is needed for this measured proposal.

## Approval and qualification

The [work order](../../work-orders/WO-RLS-053.md) reuses REQ-HAG-014,
SPEC-HAG-008, VER-HAG-008 and VER-RLS-040 without changing them. WO-RLS-052
does not cover these test-guide files. The selected evaluator cannot generically
amend an accepted definition, so approval also needs to authorize the exact
[REL-SEH-036 amendment](REL-SEH-036.patch): add only WO-RLS-053 to release gates,
preserving its [accepted bytes](REL-SEH-036-accepted-before.txt) and history.
[Exact reviewed digests](review-binding.json) bind these proposed files.

After approval: apply the two reviewed edits, run existing input/source/package
checks, measure actual launch inputs, and run a fresh Claude diagnostic first.
Only a pass permits the required Codex diagnostic and positive sequence. Previous
passes remain bound to their old candidate; no automatic reuse. Full native,
lifecycle/delivery, walkthrough/restore and separate desktop checks remain required.

Approval includes required commit-bound verification and bounded review pushes
to PR #544 (codex/release-0-23-0 → main), including later separately supplied
verification decisions. Human verification, merge, complete release, desktop
omission, adoption and host updates remain separate.

## Preparation status

Released 0.22.1 validation: **2,009 artifacts, zero errors**, 63 existing
warnings and no advisories. All 24 planned paths are covered with no invalid
declaration. [Exact commands/results](proposal-checks.zip) are retained.

WO-RLS-053 remains `draft`. Its checkpoint-free result is
`PROC-FOCUS-SELECTED / STEP-FOCUS-SELECTED`, with
`harnessctl check REPO --artifact WO-RLS-053`; this supplies no approval.
All 17 executed CI checks on the preceding evidence head passed; two release-only
checks were skipped. The proposal head has its own CI after publication.
No source instruction edit, accepted-definition amendment, lifecycle transition
or native rerun occurred.
