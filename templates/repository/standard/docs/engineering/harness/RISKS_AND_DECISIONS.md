# Record risks and decisions

## Read this when

A risk or unresolved formal question affects the selected change.

## Before this action

Before writing, read [Links for decisions and risks](RISKS_AND_DECISIONS.md#links-for-decisions-and-risks), [Blocking decisions](RISKS_AND_DECISIONS.md#blocking-decisions) and [Raised risks](RISKS_AND_DECISIONS.md#raised-risks). Apply [../ARTIFACT_AUTHORING.md#risk](../ARTIFACT_AUTHORING.md#risk) or [../ARTIFACT_AUTHORING.md#decision](../ARTIFACT_AUTHORING.md#decision) for the selected record.

## Procedure

### Record risks (RISK) affecting the change

**Inputs:** The outcome, scope, selected definitions, verification coverage,
and existing risks (RISK) found in [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change).

**Output:**

- **Formal artifacts:** New risks (RISK) in `raised` for threats not already
  covered. A paired decision (DEC) in `open` for each risk created with
  `--with-decision`. None created where existing records cover the threats.
- **Transient working material:** The selection of reused risks (RISK),
  review notes, generated IDs and paths, and links awaiting new work order
  (WO) IDs. If no risks are identified, retain that result with the reviewed
  scope. Retain this material under the same conditions as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. Identify what could go wrong within the selected change scope.
2. Check whether an existing risk (RISK) already records each threat and its
   follow-up. Reference that record instead of creating a duplicate.
3. For each new risk (RISK), describe the threat and why it matters.
4. Identify its follow-up owner.
5. Specify the owner's next action.
6. Identify the formal artifacts threatened by it.
7. Determine whether an unresolved decision must block those artifacts.
8. Preview the risk (RISK) with the command below. Inspect the proposed
   content, affected IDs, and destination paths.
9. Run the same command with the same arguments, removing only `--dry-run`.
10. Read every written file reported by the command. Retain its ID and path
    for the review handoff.

**Harness command:**

Replace the quoted text and `OWNER` with the risk description and identified
owner. Repeat `--threatens ARTIFACT-ID` for each threatened artifact. Omit that
option if no affected formal artifact exists yet:

```text
harnessctl raise-risk REPO --domain DOMAIN --title "Risk title" --description "What could go wrong and why it matters" --action "Next follow-up action" --owner OWNER --threatens ARTIFACT-ID --dry-run --json
```

Add `--with-decision` only if action 7 identifies a decision (DEC) that must
block the named artifacts. Use the same option in both preview and creation.
A risk (RISK) alone does not block work.

**Completion:** Identified risks (RISK) have formal records with an owner and
next action. If none were identified, retain `None identified` with the
reviewed scope as transient working material.

**Later use:** Review any paired decision (DEC) in [Record unresolved decisions (DEC)](RISKS_AND_DECISIONS.md#record-unresolved-decisions-dec). [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements) uses the
risks (RISK) to define work and stop conditions and adds links that depend on
new work order (WO) IDs.

### Record unresolved decisions (DEC)

**Inputs:** Unresolved questions from [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome), [Define the limits of the change](DEFINE_CHANGE.md#define-the-limits-of-the-change), [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change), [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions), [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions), [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified), [Record risks (RISK) affecting the change](RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change) and existing decisions (DEC),
including any paired records created in [Record risks (RISK) affecting the change](RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change).

**Output:**

- **Formal artifacts:** New or completed decisions (DEC) in `open` for
  unresolved questions requiring a record. None if existing records are
  sufficient or no formal question remains. Resolved decisions (DEC) and
  earlier dispositions remain unchanged.
- **Transient working material:** Clarifications, selected decision (DEC) IDs,
  and links awaiting new work order (WO) IDs. Retain these under the same
  conditions as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. Collect unresolved questions affecting the selected scope.
2. Check whether each question already has a decision (DEC). Reuse that record
   rather than creating a duplicate.
3. For a new question, determine whether it blocks an artifact transition,
   concerns more than one artifact, or must remain recorded after approval.
4. If none of those conditions applies, resolve the clarification with the
   requester. Use the answer to complete the affected draft. Retain the
   question, answer, and affected artifact ID as transient working material
   for the later approval transition. That transition MUST preserve the
   answer in its `reason`; the working notes remain transient.
5. Otherwise, create a decision (DEC) with the commands below.
6. Complete `kind`, `question`, `raised_by`, and `owners` in each new record.
7. Define at least two `[[options]]` with distinct IDs and labels.
8. Set `recommendation` to one option ID. Explain the recommendation and the
   consequences of each option in the body.
9. Set `[relations].concerns` to every artifact the question is about.
10. Set `[relations].blocks` to the artifacts whose transitions must wait for
    the answer. Include every blocked ID in `concerns`. Use only existing IDs.
11. For `kind = "deviation"`, set `against` to an existing `SPEC-ID#RULE-ID`.
    Record the fact preventing compliance in `observed`. Choose options from
    `amend`, `supersede`, `accept`, and `stop`; include `stop`.
12. Apply `## decision` → `### Checklist` in
    `docs/engineering/ARTIFACT_AUTHORING.md`, including for paired records
    created in [Record risks (RISK) affecting the change](RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change). Leave `[disposition]` unwritten.

**Harness commands:**

For each missing decision (DEC), run the creation sequence from [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions).
Inspect the preview before creation; replace `DEC-ID` with its `allocated_id`:

```text
harnessctl create-artifact REPO --domain DOMAIN --type decision --dry-run --json
harnessctl create-artifact REPO --domain DOMAIN --type decision --id DEC-ID --json
```

Recording a question does not answer it. Do not run `harnessctl decide` as
part of this step.

**Completion:** Each unresolved question requiring a formal record has a
decision (DEC), with options, a recommendation, and the affected artifacts.
If no questions remain, retain `None` as transient working material.

**Later use:** [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements) links newly created work orders (WO) where needed and
presents unresolved decisions (DEC) for review. The authorization process
handles decisions that block approval.

## Read next when

A recorded question needs a human disposition → [AUTHORIZE_WORK.md#resolve-approval-blockers](AUTHORIZE_WORK.md#resolve-approval-blockers). The package is ready for review → [AUTHORIZE_WORK.md#procedure](AUTHORIZE_WORK.md#procedure).
## Links for decisions and risks

| Source → target | Relation | Meaning and coverage |
| --- | --- | --- |
| Decision (DEC) → any artifact type | `concerns` | Names every artifact the question is about. |
| Decision (DEC) → Requirement (REQ), Specification (SPEC), Verification contract (VER), Architecture (ARCH), Architecture decision (ADR), or Work order (WO) | `blocks` | Names artifacts whose transitions the decision (DEC) blocks. Each must also appear in `concerns`. |
| Decision (DEC) → Requirement (REQ), Specification (SPEC), Verification contract (VER), Architecture (ARCH), Architecture decision (ADR), or Work order (WO) | `produces` | A decision (DEC) in `decided` names artifacts its answer created or amended, when applicable. |
| Risk (RISK) → any artifact type | `threatens` | Names the artifacts the risk (RISK) could damage. |
| Risk (RISK) → Work order (WO) | `mitigated_by` | Names the work orders (WO) reducing a risk (RISK) in `mitigating` or `mitigated`. The decision operation writes this link. |
| Risk (RISK) → Architecture decision (ADR) or Decision (DEC) | `avoided_by` | Names the single architecture decision (ADR) or decision (DEC) that removes a risk (RISK) in `avoided`. The decision operation writes this link. |

A decision (DEC) records a question that needs an answer or a proposed deviation.
An architecture decision (ADR) records a settled design choice. They serve different purposes.

A risk (RISK) does not block work by itself. When a blocking decision (DEC)
is requested, that decision (DEC) concerns the risk (RISK). The `blocks` set
of the decision (DEC) matches the `threatens` set of the risk (RISK).

## Blocking decisions

A decision (DEC) in `open` blocks every transition
of the artifacts in its `blocks` relation. A decision (DEC) in `deferred`
blocks transitions outside its recorded permitted scope.

For example, a decision (DEC) names work order (WO) `WO-EXAMPLE-001` in both
`concerns` and `blocks`. It is deferred with the scope
`WO-EXAMPLE-001:approved-in_progress`. This deferral
allows the work order (WO) to move from `approved` to `in_progress` if all
other checks pass. It still blocks moving that work order (WO) from
`in_progress` to `implemented`. The deferral also records when the decision
(DEC) must be revisited. Deferral does not itself start the work.

An accepted deviation is a decision (DEC) with `kind = "deviation"`,
`status = "decided"`, and `disposition.option = "accept"`.
It records permission to depart from one identified specification (SPEC)
rule; “accepted” is not a separate lifecycle state for the decision (DEC).

That deviation remains applicable to the affected specification (SPEC),
work orders (WO), and their verification records (VREC) and release records
(RLS) until a later decision (DEC) against the same rule reaches
`status = "decided"` with `disposition.option` set to `amend` or
`supersede`. The disposition is written through `harnessctl decide`, not
by editing the metadata by hand.

## Raised risks

A risk (RISK) in `raised` may have no paired decision
(DEC). Recording that risk alone does not block work. Use
`raise-risk --with-decision` when creating a risk that needs a paired blocking
decision.

A raised risk MUST NOT have more than one paired decision in `open` or
`deferred`. When that decision exists, it names the risk in `concerns`, and
its `blocks` set MUST equal the risk's `threatens` set. Disposing the paired
decision applies its recorded effect to the risk in the same operation.
The blocked artifacts change state only through their own transitions.
