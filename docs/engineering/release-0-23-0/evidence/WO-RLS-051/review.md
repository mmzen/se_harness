# Proposal: assess inputs before drafting

**Approve WO-RLS-051 and required verification**, including its exact linked
release-membership amendment and review publication in existing PR #544.
The product edit and accepted release amendment are **unapplied**.

## Problem and proposed change

The previous Claude diagnostic saved one draft and declared it complete despite
missing required inputs. It also added unsupported claims and reported proposed
scope limits differently from the saved artifact. The
[independent assessment](../WO-RLS-046/candidate-74feac07-claude-assessment.json)
preserves R23-NATIVE-005/006. Authentication, tools and storage succeeded.

The guide already says to check inputs. It does not require an observable
assessment before drafting. The next hypothesis makes that assessment explicit:

1. Before creating or editing a draft, show each required input with its supplied
   fact/source, or mark it missing and state the question.
2. Ask about missing required inputs and stop dependent writing. Existing partial
   drafts may remain saved. The agent must not fill gaps with assumptions.
3. After saving, update the same assessment against the saved content and use
   that result in the report and final reply. Mark proposed limits in both.

Only the shared hosted-drafts instruction file changes. Read the
[exact diff](hosted-drafts.patch) or [full proposed file](hosted-drafts-proposed.txt).
Length: **1532 → 1607 words**. The small increase pays for
an explicit source-to-input check. There is no new tool, dependency, parser,
service, mandatory repository file or lifecycle gate. Existing source content
and a matching assessment are reused; duplicate reads and reports are unnecessary.
The type checklist remains the canonical owner of required content.

This remains an instruction hypothesis. The table can itself contain unsupported
claims, so table presence is not a pass. Independent semantic review remains
required. No measured correctness, speed or context improvement is claimed.

## Qualification after approval

Build and test the exact candidate packages, then run one fresh Claude diagnostic
under unchanged VER-HAG-008 / VER-RLS-040. Keep the same request, source fixture,
model, permissions and pass criteria. Do not supply test-specific answers.
Stop further native tests on failure. Only a pass permits the remaining required
Codex and positive cases. Source/package checks and separate desktop evidence
remain required. Use the existing aggregate commit-bound verification.

## Scope and authority

The [work order](../../work-orders/WO-RLS-051.md) selects REQ-HAG-014,
SPEC-HAG-008, VER-HAG-008 and VER-RLS-040 unchanged. Its evidence scope includes
the fixed evaluator outputs and later aggregate verification in this release
domain. These destinations are checked before writing.

WO-RLS-050 approved different exact bytes. Your "Ok go" confirms this new approach;
this request is for its concrete work order and release-membership amendment.
The evaluator lacks a generic amendment command. The requested explicit manual
amendment adds **only WO-RLS-051** to REL-SEH-036's gates, preserving and linking
the accepted file and all lifecycle history. Review its
[one-line diff](REL-SEH-036.patch) and [exact digests](review-binding.json).

Approval includes this work in review pushes to codex/release-0-23-0 and PR #544
targeting mmzen/se_harness:main, including a later separately given verification
decision. Human verification, merge, complete-release approval, desktop omission,
adoption and host changes remain separate. Earlier failures stay failed.

## Preparation checks

Released 0.22.1 validation: **2,007 artifacts, zero errors**, 63 existing
warnings and no advisories. All 16 planned paths are covered, with no invalid
declaration. WO-RLS-051 remains `draft`; its checkpoint-free result is
`PROC-FOCUS-SELECTED / STEP-FOCUS-SELECTED`, with
`harnessctl check REPO --artifact WO-RLS-051`. This supplies no implementation
approval. Commands and outputs are in [proposal-checks.zip](proposal-checks.zip).

The initial GitHub read could not connect from the sandbox. The same read
succeeded in the permitted host context and confirmed the expected draft PR
and head. All 17 executed checks on that preceding head passed; two release
legs were skipped. This proposal head has its own CI after publication.
No product implementation, accepted-definition edit or native rerun occurred.
