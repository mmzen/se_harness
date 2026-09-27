# Define the change

## Read this when

A new change needs an outcome, limits or selection of existing artifacts.

## Before this action

Before selecting artifacts, read [ARTIFACTS.md#artifact-types](ARTIFACTS.md#artifact-types) and [DEFINITION_LINKS.md#links-between-definitions](DEFINITION_LINKS.md#links-between-definitions).

## 1. Define the change

**When:** A new change is requested, or existing definitions need to change.

**Inputs:** The requested outcome and any relevant existing formal artifacts.

**Output:** Proposed definitions and work orders (WO), validation results,
and unresolved decisions or amendment proposals for review.

**Steps:**

1. [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).
2. [Define the limits of the change](DEFINE_CHANGE.md#define-the-limits-of-the-change).
3. [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change).
4. [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions).
5. [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions).
6. [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified).
7. [Record risks (RISK) affecting the change](RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change).
8. [Record unresolved decisions (DEC)](RISKS_AND_DECISIONS.md#record-unresolved-decisions-dec).
9. [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements).

## Procedure

### Describe the intended outcome

**Inputs:** The change request and any clarifications already provided by
the requester.

**Output:**

- **Formal artifacts:** None created or modified.
- **Transient working material:** The confirmed intended-outcome statement and the
  requester's confirmation. This material is needed only for the current
  change-definition context. The agent SHALL retain it in the conversation
  or, at its discretion, in a temporary location outside the repository.
  It SHALL NOT be persisted in the repository. The agent chooses whether a
  temporary file is needed and, if so, its filename and format.

**Actions:**

1. Read the change request and existing clarifications.
2. Draft one statement describing the observable result for the intended
   human, agent, or system. Include the conditions under which it is needed.
3. Present the statement to the requester.
4. Ask the requester to resolve any missing information or competing
   interpretations that would change the outcome.
5. Revise the statement using the feedback. Repeat the exchange until the
   requester confirms the wording. Reuse an existing confirmation of the
   same wording.
6. Retain the confirmed statement and the confirmation as transient working
   material.

**Harness command:** None.

**Completion:** One intended-outcome statement is confirmed by the requester
and available for the following steps. This confirmation does not approve a
formal artifact or authorize implementation.

**Later use:** The statement guides scope definition in [Define the limits of the change](DEFINE_CHANGE.md#define-the-limits-of-the-change) and artifact
selection in [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change). It supplies the outcome for a missing intent (INT) drafted
in [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions) or an amendment proposed in [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions). Any lasting definition belongs
in those formal artifacts.

### Define the limits of the change

**Inputs:** The confirmed outcome from [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome) and the constraints supplied
by the requester.

**Output:**

- **Formal artifacts:** None created or modified.
- **Transient working material:** The confirmed scope statement and requester
  clarification. Retain these under the same conditions as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. List the behaviors, components, and interfaces included in the change.
2. List the adjacent behaviors, components, and interfaces excluded from it.
3. List the conditions the result must respect, such as compatibility or a
   named operating environment.
4. Use component names where exact file paths are not yet known.
5. Present these boundaries to the requester. Identify any unresolved boundary.
6. Revise the scope until the requester confirms it. Reuse an existing
   confirmation when the boundaries are unchanged.
7. Retain the confirmed scope as transient working material.

**Harness command:** None.

**Completion:** One scope statement defines what is included, what is
excluded, and which constraints apply. No unresolved boundary affects the
definitions to be drafted next.

**Later use:** The scope selects artifacts in [Identify the existing artifacts that apply to the change](DEFINE_CHANGE.md#identify-the-existing-artifacts-that-apply-to-the-change), limits definition work
in [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions), [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions), [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified), and supplies the work order (WO) boundaries in [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements).

### Identify the existing artifacts that apply to the change

**Inputs:** The confirmed outcome, scope limits, any artifact IDs supplied
in the request, and the existing formal records. Use
`docs/engineering/README.md` when locating a domain.

**Output:**

- **Formal artifacts:** None created or modified.
- **Transient working material:** A list of selected artifacts (the artifact
  inventory), a list of missing definitions, and the evaluator results.
  These are needed only for the current change-definition context. The agent
  SHALL retain them in the conversation or, at its discretion, in a temporary
  location outside the repository. They SHALL NOT be persisted in the
  repository. The agent chooses whether a temporary file is needed and, if
  so, its filename and format.

**Actions:**

1. Run the repository inspection command below.
2. If the request selects a work order (WO), run the selected-work command
   below. Read that work order (WO) and every file in the returned
   `context.reading_manifest`.
3. Otherwise, locate the artifacts named in the request. If none are named,
   use `docs/engineering/README.md` to locate the domain covering the function
   or component in the scope. Read its intents (INT), capabilities (CAP),
   and requirements (REQ). Record a missing domain if none covers the change.
4. Select the requirements (REQ) whose behavior the change would modify or
   reuse. Trace each one back to its capabilities (CAP) and intents (INT).
5. Read the specifications (SPEC), applicable architectures (ARCH), architecture
   decisions (ADR), verification contracts (VER), and work orders (WO) linked
   to those selected requirements (REQ). Use the declared relations listed
   in [Definition links](DEFINITION_LINKS.md#links-between-definitions). Keep unrelated work outside the selected scope.
6. Read decisions (DEC) and risks (RISK) that name the selected artifacts.
7. For each selected artifact, retain its name and code, such as Requirement
   (REQ), its ID, file path, current lifecycle state, and why it applies to the
   change. Keep this list as transient working material; do not create a
   repository inventory file.
8. Assign one treatment to each entry: `reuse`, `amend`, or `reference only`.
   Use `reuse` only when its existing meaning covers the change unchanged.
9. List missing definitions by type and purpose. Identify their intended domain.

**Harness commands:**

Repository inspection, used in action 1:

```text
harnessctl inspect REPO --json
```

Selected-work inspection, used in action 2. Replace `WO-ID` with the actual
work order (WO) ID:

```text
harnessctl check REPO --artifact WO-ID --json
```

Both commands are read-only. `inspect` does not select the change scope.
The checkpoint-free `check` reports lifecycle context without evaluating
checkpoint gates. Preserve its reported blockers and next action.

**Completion:** One inventory identifies the existing artifacts to reuse,
amend, or consult and the definitions that are missing. Ambiguous artifact
identities are resolved before dependent drafting.

**Later use:** The inventory controls creation in [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions), amendments in [Propose any needed amendments to existing definitions](AMEND_DEFINITIONS.md#propose-any-needed-amendments-to-existing-definitions),
and the verification, risk, decision, and work-order work in [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified), [Record risks (RISK) affecting the change](RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change), [Record unresolved decisions (DEC)](RISKS_AND_DECISIONS.md#record-unresolved-decisions-dec), [Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements](DRAFT_WORK_ORDERS.md#prepare-work-orders-wo-linking-the-definitions-scope-planned-work-and-verification-requirements).

## Read next when

Definitions are missing → [DRAFT_DEFINITIONS.md#procedure](DRAFT_DEFINITIONS.md#procedure). Meaning must change → [AMEND_DEFINITIONS.md#procedure](AMEND_DEFINITIONS.md#procedure). Scope is ready → [DRAFT_WORK_ORDERS.md#procedure](DRAFT_WORK_ORDERS.md#procedure).
