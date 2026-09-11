# Bring the verified plugin stack into main

**Updated 11 September 2026: approval packet merged; baseline amendment proposed.**

## Current status and required correction

PR #450 is now merged at `fc1f087371b100d5fda7a1f254ee00ebde8cbadf`.
The approved delegation exists on main. The remaining prerequisite is approval
of the [baseline amendment](../engineering/plugin-integration/evidence/WO-PLG-018/base-amendment.md),
which pins that new main commit for execution in a new PR. Its 3,177 imported
paths, five source heads and verification obligations match the original plan.
The WO and VER remain approved under their existing terms; implementation has
not started, and this amendment is not yet approved.

### Earlier refusal and correction

The operator approved VER-PLG-018 and WO-PLG-018, including execution delegation.
The released evaluator recorded both approvals. Its start preview then refused
with **WEX-ECP-022**: WO-PLG-018 has no delegation class at `origin/main`.
The work order remains **approved**; no integration has started.

[DR-015](../engineering/DECISION_RIGHTS.md#governed-delegated-execution) reads
delegation from the PR base, not its branch. The proposal below missed this
prerequisite: passing CI and approving a new branch-only work order do not make
its delegated start legal. The earlier WO-PLG-017 route worked because main
already contained that work order's delegation through #447.

The corrected delivery sequence is:

1. Deliver **PR #450 as the approval packet only**, after its checks pass and
   the operator separately chooses to merge it. This establishes delegation
   on main; it delivers no plugin implementation and claims no verification.
2. Prepare a reviewed amendment naming the resulting main commit and a new
   implementation PR. Recheck the pinned source heads and import plan. Keep the
   original plan and its approval intact as history; the approved packet requires
   another review when its base changes.
3. After that amendment is approved and the exact-head gate passes, use delegated
   start, assembly, acceptance, completion and ready VREC preparation. Assurance
   of the assembled candidate and its final merge stay separate decisions.

The [start-block receipt](../engineering/plugin-integration/evidence/WO-PLG-018/start-block.json)
retains the refused command and the unchanged state. No base override, manual
start, policy edit or merge was used to bypass the refusal. This correction is a
delivery proposal, not an amendment to the approved WO, VER or frozen plan.

Use one integration PR under **WO-PLG-018**. Import the existing commits, prove
that their files and decisions survived, then let the operator merge the result.
Keep the four implementation work orders and their verification history intact.

## Why a separate integration scope

The current stack is `#446 → #449 → #445 → #444 → main`. Each arrow is a PR's
target branch. Merging children into parents combines several work orders,
while the harness checks each PR against just one work order's scope.
The combined diff therefore needs an explicit scope of its own.

There is also a current failure on [#444](https://github.com/mmzen/se_harness/pull/444).
Its [validation run](https://github.com/mmzen/se_harness/actions/runs/34579932796/job/103200884887)
compared the checkout against base `9bc323a7` and rejected a WO-PLG-017 evidence
path with WEX201. Local checks of #444's own branch diff passed; they did not
prove that hosted comparison. The failed run remains evidence, not a waived gate.

## What will be integrated

| Work | Source PR | Assurance already recorded |
| --- | --- | --- |
| Change skill — WO-PLG-010 | [#444](https://github.com/mmzen/se_harness/pull/444) | VREC-PLG-007 verified |
| Evidence skill — WO-PLG-011 | [#445](https://github.com/mmzen/se_harness/pull/445), repaired by #449 | VREC-PLG-010 verified |
| Windows evidence repair — WO-PLG-017 | [#449](https://github.com/mmzen/se_harness/pull/449) | VREC-PLG-010 verified |
| Orientation and briefing — WO-PLG-012 | [#446](https://github.com/mmzen/se_harness/pull/446) | VREC-PLG-009 verified |

The [pinned plan](../engineering/plugin-integration/evidence/WO-PLG-018/plan.json)
records full source commits, base `c0451b76`, and all **3,177 imported paths**
with their exact Git blob IDs and file modes. Every path maps to an existing
implementation scope. A Git tree preview found no conflicts; it did not assemble
an implementation branch or authorize work.

## Original workflow (blocked by the prerequisite above)

1. **Approve the packet.** Review [WO-PLG-018](../engineering/plugin-integration/work-orders/WO-PLG-018.md)
   and [VER-PLG-018](../engineering/plugin-integration/verification/VER-PLG-018.md).
   Both are draft. Proposed execution delegation covers start, completion and
   single-work-order verification-record preparation under the existing gates.
2. **Assemble in this PR after start.** From the pinned main baseline, preserve
   the approved packet and merge the exact #446 head, then the exact #444 head.
   #446 already contains the #445, #448 and #449 source histories. Use merge
   commits, preserving every candidate hash. Any conflict or changed input stops
   assembly for a reviewed amendment.
3. **Prove the combination.** A small new checker compares imported files with
   the approved manifest, verifies ancestry and record preservation, and rejects
   unexpected changes. Run the existing source, package, Windows/Linux upgrade
   and integration-package checks on the assembled result. The hosted scope
   check must use this PR's actual base and `Harness-Work-Order: WO-PLG-018`.
4. **Record integration assurance.** Complete WO-PLG-018 only after its checks
   pass. Prepare VREC-PLG-011 for a clean committed integration candidate, retain
   it in a later commit, and request the operator's verification. Existing VRECs
   keep their candidates and decisions; the new record covers the combination.
5. **Operator merges to main.** Recheck the final PR head and current base after
   the verification decision. The operator then makes a separate merge decision
   and uses a merge commit. Close the old PRs only after their source commits are
   confirmed as ancestors of main. No release is part of this work.

## Boundaries that keep this small

Imported code, tests, evidence, work orders and existing VRECs are frozen.
New edits are limited to this packet, its checker, integration evidence and the
new VREC. No plugin behavior, managed policy, CI configuration, version, or old
scope changes are proposed. VREC-PLG-008 remains ready and unchanged; superseding
it would be a separate assurance decision.

The preview contains **9,955 archive entries** against the existing 10,000 limit.
Count the final tree including new evidence and governance. Keep new traces in
one indexed archive; do not raise the limit or repack old evidence in this work.

## What happens to the old PRs

| PR | Proposed disposition after main contains its exact source head |
| --- | --- |
| #444, #445, #446, #449 | Close as delivered through the integration PR; retain review and failure history. |
| #448 | Close too. Its approval commit is already included through #449. |

This adds one bounded work order and one integration verification contract.
It avoids expanding the original work orders or pretending that separate
candidate verifications prove the final combined tree. Existing component
evidence is reused where bytes are unchanged; new evidence proves composition.
