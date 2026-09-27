# Propose amendments

## Read this when

A selected definition needs changed meaning.

## Before this action

Read the selected definition and [DEFINITION_LINKS.md#links-between-definitions](DEFINITION_LINKS.md#links-between-definitions) to identify affected records. For draft edits, use [../ARTIFACT_AUTHORING.md#design-simplicity](../ARTIFACT_AUTHORING.md#design-simplicity) and the selected [Type checklist](DRAFT_DEFINITIONS.md#type-checklists).

## Procedure

### Propose any needed amendments to existing definitions

**Inputs:** The artifacts marked `amend` in [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change) and the confirmed outcome
and scope.

**Output:**

- **Formal artifacts:** Updated content in existing definition drafts where
  amendments are needed. Artifact IDs and lifecycle metadata are preserved.
  No accepted definition is modified.
- **Transient working material:** The amendment proposals and their effects
  on linked artifacts, or `None needed`. Retain these under the same
  conditions as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. Read each definition marked `amend`.
2. Identify the exact section or rule requiring a change.
3. Write its proposed replacement text.
4. Record the artifact ID, path, current state, existing text, proposed text,
   and reason for the change in the amendment proposal.
5. List the linked artifacts whose meaning or checks would be affected.
6. If the definition is in `draft`, apply the content edit. Apply its type's
   checklist in `docs/engineering/ARTIFACT_AUTHORING.md`.
7. If the definition is accepted, keep the replacement in transient working
   material for review. Identify the exact accepted version by its artifact
   ID, recorded state, and SHA-256 digest of its complete file bytes. Describe
   the proposed linked revision. Do not change the accepted record or its state.
8. Retain unresolved questions for [Record unresolved decisions (DEC)](RISKS_AND_DECISIONS.md#record-unresolved-decisions-dec).

**Harness command:** None for proposing replacement text or editing draft
content. No accepted-definition transition is performed here.

**Completion:** Each definition needing amendment has an explicit proposed
change and impact description. Existing drafts reflect the proposed edits.
Accepted definitions remain unchanged. If none need amendment, record
`None needed` in the transient working material.

**Later use:** The proposals inform verification planning in [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified) and the
review of work orders (WO) in [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements). Dependent work cannot treat proposed
replacement text as accepted authority.

**Accepted-definition amendment boundary:** An amendment MUST create a linked
revision and preserve the accepted version. The new revision MUST identify
the exact accepted version it replaces. Its proposed changes and effects on
linked work MUST be reviewed before approval. It MUST NOT govern work before
the required human decision and supported activation have been recorded.
Earlier work and evidence keep their original definition references.

This release has no supported command and relation for creating
and activating this linked definition revision. Keep the proposal transient
and report that precise missing capability. Stop dependent authorization or
execution until a released procedure can record the revision link, its human
decision, and its effect on selected work. Do not edit the accepted file, add
an invented relation, or treat an unrelated new draft as its replacement.


## Read next when

A missing supported revision mechanism blocks dependent work → [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked). A draft is ready for review → [AUTHORIZE_WORK.md#procedure](AUTHORIZE_WORK.md#procedure).
