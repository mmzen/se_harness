# Deliver the result

## Read this when

A delivery path is selected or its exact external action needs preparation, authority or readback.

## Before this action

Before any external action, read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and the repository instructions for that action. Read the exact selected candidate, verification or release record.

## 5. Deliver the result

**When:** Integration, release, publication, deployment, or another delivery
action is requested.

**Inputs:** The selected candidate, intended destination, delivery procedure,
existing action authority, and verified coverage when required by the selected
path and applicable gates.

**Output:** The exact requested delivery is completed and evidenced, or a
specific blocker or failure is reported. A release decision alone performs
no external action.

**Steps:**

1. [Select the delivery action](DELIVER_RESULT.md#select-the-delivery-action).
2. [Prepare the delivery package](DELIVER_RESULT.md#prepare-the-delivery-package).
3. [Obtain the release decision, when required](RELEASE.md#obtain-the-release-decision-when-required).
4. [Record the release decision, when required](RELEASE.md#record-the-release-decision-when-required).
5. [Confirm authority for the external action](DELIVER_RESULT.md#confirm-authority-for-the-external-action).
6. [Perform the authorized delivery](DELIVER_RESULT.md#perform-the-authorized-delivery).
7. [Confirm the delivery result](DELIVER_RESULT.md#confirm-the-delivery-result).

## Procedure

Publishing a branch and draft PR for human verification follows
[Publish the review package](PULL_REQUEST.md#publish-the-review-package).
Its declared `PROC-REVIEW-PUBLISH` path accepts a ready VREC and does not
authorize merge. The later integration path retains its verified-coverage
checks. Reuse the explicit publication grant from work approval while its
scope and destination still match.

### Select the delivery action

**Inputs:** The requested delivery, selected work or verification record,
candidate identity, and intended destination.

**Output:**

- **Formal artifacts:** None changed.
- **Transient working material:** One named action, its exact candidate or
  release identity, destination, selected procedure, and required authority.

**Actions:**

1. Inspect the selected work order (WO), verification record (VREC), or release
   record (RLS) with the command below.
2. Name the action: for example, create a pull request, merge, prepare a
   release, tag, publish, or deploy.
3. Identify the full candidate commit or immutable release identity.
4. Identify the exact target repository and ref, registry, or deployment environment.
5. Read the repository's instructions for that delivery action.
6. Select the matching procedure or a complete alternative declared by the
   evaluator. Resolve an ambiguous destination with the requester.

**Harness command:**

```text
harnessctl check REPO --artifact ARTIFACT-ID --json
```

Use a work order (WO), verification record (VREC), or release record (RLS)
as `ARTIFACT-ID`. Selection changes no lifecycle state.

**Completion:** One delivery action and target are explicit. Selecting a path
does not authorize or perform its external action.

**Later use:** [Prepare the delivery package](DELIVER_RESULT.md#prepare-the-delivery-package), [Obtain the release decision, when required](RELEASE.md#obtain-the-release-decision-when-required), [Record the release decision, when required](RELEASE.md#record-the-release-decision-when-required), [Confirm authority for the external action](DELIVER_RESULT.md#confirm-authority-for-the-external-action), [Perform the authorized delivery](DELIVER_RESULT.md#perform-the-authorized-delivery), [Confirm the delivery result](DELIVER_RESULT.md#confirm-the-delivery-result) prepare, authorize, perform, and confirm that action.

### Prepare the delivery package

**Inputs:** The selected delivery path, preparation authority and exact candidate.

**Output:** For release, a ready RLS and its generated evidence. For integration,
the proposed PR body or other inputs required by the repository delivery procedure.
Required durable evidence remains at its authorized location; other preparation
notes and proposed external content are transient.

**Actions:**

1. Confirm authority for the exact preparation operation. Reuse matching authority
   already supplied; obtain only a missing human decision.
2. Inspect existing records and outputs before preparing replacements.
3. For release, follow [Prepare a release record](RELEASE.md#prepare-a-release-record).
4. For a PR, follow [Prepare the integration package](PULL_REQUEST.md#prepare-the-integration-package).
5. For another integration action, use its repository procedure and named inputs.
6. Retain required build or delivery evidence at the authorized locations. Build
   only when the selected scope separately covers that build.

**Harness commands:** Use only the selected branch's commands. No generic
delivery-preparation command exists.

**Completion:** The selected package is prepared or its exact blocker is known.
Preparation performs no merge, publication, deployment or release decision.

**Later use:** A ready RLS goes to [Obtain the release decision](RELEASE.md#obtain-the-release-decision-when-required).
Other prepared delivery actions go to [Confirm authority for the external action](DELIVER_RESULT.md#confirm-authority-for-the-external-action).

### Confirm authority for the external action

**Inputs:** The exact action, immutable candidate or release identity,
destination, current gates, and any existing human authorization.

**Output:**

- **Formal artifacts:** None changed by the authority review.
- **Transient working material:** The matching authorization and current gate
  results, or the exact missing authority or control.
- **Retained evidence:** Any control or approval evidence required by the
  repository's delivery procedure remains at its specified location.

**Actions:**

1. Match the supplied authorization to the action, identity, and destination.
   A matching complete-release approval may cover all listed delivery actions;
   use [Complete-release authority](AUTHORITY.md#complete-release-authority).
   Compare the frozen plan digest and the actual decision, not just RLS status.
2. Obtain the exact missing human decision if no matching authorization exists.
3. Run the selected procedure's pre-action check with the command below.
4. Check required CI, repository protection, and destination controls using
   the delivery procedure's tools.
5. Read and check any additional controls required by the selected tool or
   provider before the external mutation. When using Verity Plane's `change`
   or `evidence` skill, read the installed `change` skill's
   `references/authority.md#external-actions`. It owns the provider's
   independent-enforcement requirement for the exact action and destination.
6. Stop the external mutation if authority, a required gate, or a required
   control is missing. Reuse valid existing authorization without a duplicate request.

**Harness command:**

```text
harnessctl check REPO --artifact ARTIFACT-ID --checkpoint pre-action --procedure PROCEDURE-ID --json
```

Use only the procedure selected by the evaluator or one of its declared
alternatives, such as `PROC-REVIEW-PUBLISH`, `PROC-REPOSITORY-INTEGRATION` or `PROC-EXTERNAL-ACTION`
when offered. Include any further change-set inputs required by that procedure.
This check does not authenticate a human decision or prove external controls.

The Verity Plane requirement comes from the installed `change` skill's
`references/authority.md#external-actions`. It applies when its `change` or
`evidence` skill is used; it is not a
new lifecycle gate defined by this document. Read the selected provider's
current requirements and report a missing control against that source.

**Completion:** The exact external action has matching authority and passing
required checks, or a specific blocker prevents it.

**Later use:** [Perform the authorized delivery](DELIVER_RESULT.md#perform-the-authorized-delivery) acts only while those inputs and conditions remain valid.

### Perform the authorized delivery

**Inputs:** The prepared delivery package, exact target, and current authority
and gate results from [Confirm authority for the external action](DELIVER_RESULT.md#confirm-authority-for-the-external-action).

**Output:**

- **External state:** Only the authorized repository, registry, tag, or
  deployment change, if the action succeeds.
- **Retained evidence:** The delivery tool's actual response and operation
  identity at the location required by the delivery procedure.
- **Transient working material:** Execution notes that are not required evidence.

**Actions:**

1. Recheck that the candidate, action, and destination still match the authority.
2. Invoke the repository's specified delivery tool for that exact operation.
3. Retain the returned operation ID, URL, version, commit, or other result identifier.
4. If the response is uncertain, inspect the destination before retrying.
   Continue only effects known not to have occurred.
5. For complete release delivery, continue every remaining listed action under
   the same matching authority. Recheck its prerequisites and public results.
   Keep successful stages; report failures or missing required observations as
   incomplete delivery. Promote moving release markers only after the plan's
   required delivery checks pass. A completed publication is not proof that all
   other outputs were delivered.

**Harness command:** None performs the external delivery. Use the project's
specified Git, hosting, package-registry, or deployment tools. No generic
harness merge, publish, or deploy command is implied.

**Completion:** The authorized operation has an observed tool result, or its
outcome is explicitly uncertain. Tool success alone does not replace destination checks.

**Later use:** [Confirm the delivery result](DELIVER_RESULT.md#confirm-the-delivery-result) confirms what actually happened at the target.

### Confirm the delivery result

**Inputs:** The delivery invocation, returned identifiers, target system,
and verification requirements for the delivery action.

**Output:**

- **Retained evidence:** The observed destination state and required delivery
  receipts or checks at the locations specified by the delivery procedure.
- **Formal artifacts:** No additional lifecycle transition is inferred from
  successful delivery. Change a record only through its own authorized procedure.
- **Transient working material:** The final report of completed effects,
  missing effects, failures, and the evaluator's current next action.

**Actions:**

1. Inspect the destination using its read-only tools.
2. Compare the observed commit, version, content identity, or deployment
   identity with the authorized target.
3. Run the delivery procedure's required post-action checks.
4. Retain the actual results, including partial effects or failures.
5. Inspect the selected formal record with `harnessctl`.
6. Report what completed, what did not, the evidence location, and the current
   next action. Do not infer production health from publication alone.

**Harness command:**

```text
harnessctl check REPO --artifact ARTIFACT-ID --json
```

Use destination-specific tools for the remote inspection. `harnessctl check`
reports formal lifecycle context; it does not inspect the remote target.

**Completion:** The delivery result is confirmed against the target, or its
specific failure or uncertainty is reported with observed effects preserved.

**Later use:** Retained delivery evidence supports subsequent release or
operating obligations. Further work requires its own applicable scope and authority.

## Read next when

Release preparation or decision is selected → [RELEASE.md#procedure](RELEASE.md#procedure). PR preparation/check is selected → [PULL_REQUEST.md#procedure](PULL_REQUEST.md#procedure). Report actual effects → [RESULTS.md#report-a-lifecycle-result](RESULTS.md#report-a-lifecycle-result).
