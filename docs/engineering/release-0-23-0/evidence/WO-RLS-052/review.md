# Proposal: ground drafting in confirmed inputs

**Approve WO-RLS-052 and required verification**, with its exact linked release
membership amendment and inclusion in review publication through PR #544.
Product instructions and accepted REL-SEH-036 remain **unchanged**.

## Diagnosis

The last Claude run received the relevant rules. It displayed the required
assessment table but treated its own interpretation as supplied evidence. It
also counted a read as a write. See [R23-NATIVE-007/008](../WO-RLS-046/candidate-32f2834e-claude-assessment.json).
Storage, authentication and instruction delivery worked in that trial.

There is a competing pull in the task: it requests an artifact, while the
canonical procedure requires confirmed inputs first. These are not conflicting
permissions: the request also limits writing to supported content. The observed
failure is applying that distinction. We cannot establish the model's internal
cause or guarantee a wording-only fix from one trace.

## Exact proposal

1. Apply the already required requester-confirmation step before drafting.
   Reuse a matching confirmation; ask only when it is absent.
2. Replace the fact/source assertion with a short source passage that directly
   answers each required checklist item. Interpretations and proposed limits
   stay unconfirmed. Existing code proves behavior, not an unstated user need.
3. Keep the success condition separate from its baseline. Review the saved
   content against the same assessment; derive write counts from receipts.

This is one shared instruction file: **1607 → 1588 words**.
Read the [exact diff](hosted-drafts.patch) or [full proposed file](hosted-drafts-proposed.txt).
Repeated routing text is removed. No new tool, call, runtime, repository file or
lifecycle gate is required for native authoring. Required content remains owned
by the canonical type checklist. The confirmation step already exists in
released DEFINE_CHANGE.md; this proposal makes its use explicit.

The change is still a hypothesis. A quote can be irrelevant or misinterpreted.
Independent semantic review remains necessary; a matching phrase is not a pass.
The positive case must show that sufficiently specified work proceeds without
unnecessary questions. No correctness, time or context improvement is claimed.

## Alternatives and limits

Repeating this candidate is forbidden by the current qualification contract.
Another longer reminder is poorly supported by the repeated failures. Changing
the model or replacing semantic judgment with a new runtime control would need
a different proposal and qualification basis. This bounded replacement tests a
more concrete evidence rule while reducing duplication. If it fails, preserve
the result and review the approach; do not automatically add another instruction.

## Qualification

Keep VER-HAG-008 / VER-RLS-040, model, request, fixture and permissions unchanged.
After exact package checks, run one fresh Claude EFF-04A2 diagnostic. Stop on
failure. Only a pass permits the Codex diagnostic and positive sequence. Review
the actual source support and effects; do not feed this assessment or expected
missing answers to the native agent. Retain failures and independent readbacks.
Source/package checks and separate desktop evidence remain required.

## Authority and amendment

The [work order](../../work-orders/WO-RLS-052.md) reuses accepted REQ-HAG-014,
SPEC-HAG-008, VER-HAG-008 and VER-RLS-040. Their criteria are not changed.
WO-RLS-051 authorized different exact bytes and remains in progress. The user's
continuation request permits this preparation; the new implementation requires
review of this concrete package.

The selected evaluator cannot amend accepted definitions generically. Request
explicit manual activation of the [one-line REL-SEH-036 revision](REL-SEH-036.patch)
adding only WO-RLS-052, with preserved accepted bytes and lifecycle history.
The [binding](review-binding.json) records all reviewed digests.

Approval includes this work and later separately given verification decisions in
review pushes to codex/release-0-23-0, PR #544, mmzen/se_harness:main. Human
verification, merge, complete-release approval, desktop omission, adoption and
host updates remain separate. Existing failed results remain failed.

## Preparation checks

Released 0.22.1 validation: **2,008 artifacts, zero errors**, 63 existing
warnings and no advisories. All 16 planned paths are covered, with no invalid
declaration. WO-RLS-052 remains `draft`; its checkpoint-free result is
`PROC-FOCUS-SELECTED / STEP-FOCUS-SELECTED`, with
`harnessctl check REPO --artifact WO-RLS-052`. This supplies no implementation
approval. Commands and outputs are in [proposal-checks.zip](proposal-checks.zip).

The first template-creation attempt could not perform its atomic move in the
Windows sandbox. Its destination was confirmed absent; the same released
command succeeded in the permitted host context. An initial GitHub read could
not connect from the sandbox; the host read confirmed the expected PR and head.
All 17 executed checks on that preceding evidence head passed; two release-only
legs were skipped. The proposal head has its own CI after publication.
No product edit, accepted-definition amendment or native rerun occurred.
