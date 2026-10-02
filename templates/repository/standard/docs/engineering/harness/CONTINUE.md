# Continue selected work

## Read this when

An existing artifact is selected, including recovery after compaction.

## Before this action

Recover the exact repository, artifact IDs, pending action and existing authority. Obtain the current result; read the selected step and its returned prerequisites before acting. A prior summary does not establish current state.

## Procedure

### Continue selected work

**Inputs:** An exact existing artifact ID, its current record, any existing
authority, and the latest evaluator result when one is available.

**Output:**

- **Formal artifacts:** None created or changed by selecting the continuation.
- **Transient working material:** The current result and the matching procedure
  file and heading. No new decision or scope is inferred.

**Actions:**

1. Read the selected artifact's type and current state. Do not treat a prior
   conversation summary as current state.
2. For a work order, verification record, release record, or decision, obtain
   its current result with `check`.
3. For a definition, use its recorded state and the explicitly requested human
   decision. A permitted transition preview evaluates that decision. The
   selected release does not accept definition IDs in `check`.
4. For a risk, read its record and any paired decision. Use [Record risks](RISKS_AND_DECISIONS.md#record-risks-risk-affecting-the-change) for
   creation and [Resolve approval blockers](AUTHORIZE_WORK.md#resolve-approval-blockers) for a requested decision disposition.
   Do not infer a work-order stop from an unpaired risk alone.
5. Read the result's selected procedure and its exact next typed step. Use the
   index below to find the accompanying human instructions.
6. Resume the unapplied step under existing authority. Completed operations and
   terminal records are not invitations to replay earlier transitions.
7. If a returned command is unsupported by the exact selected release, report
   that contract/version mismatch. Do not repair it by inventing another next
   action, changing record state, or running candidate source.

**Harness command:**

```text
harnessctl check REPO --artifact ARTIFACT-ID --json
```

Use only the supported types named in action 2. The following is an index of
the released procedure IDs, not an independent rule for selecting one:

| Returned procedure ID | Instruction destination |
| --- | --- |
| `PROC-WO-START` | [EXECUTE_WORK.md#start-the-selected-work](EXECUTE_WORK.md#start-the-selected-work) |
| `PROC-WO-IMPLEMENT` | [EXECUTE_WORK.md#retain-the-implementation-evidence](EXECUTE_WORK.md#retain-the-implementation-evidence) |
| `PROC-WO-PREPARE-VREC` | [VERIFY_OUTCOME.md#prepare-the-verification-record](VERIFY_OUTCOME.md#prepare-the-verification-record) |
| `PROC-FOCUS-SELECTED` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `PROC-FOCUS-RELATED` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `PROC-VREC-DECIDE` | [VERIFY_OUTCOME.md#obtain-the-humans-verification-decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision) |
| `PROC-REVIEW-PUBLISH` | [PULL_REQUEST.md#publish-the-review-package](PULL_REQUEST.md#publish-the-review-package) |
| `PROC-VREC-REJECT` | [VERIFY_OUTCOME.md#record-the-verification-decision](VERIFY_OUTCOME.md#record-the-verification-decision) |
| `PROC-VREC-SUPERSEDE` | [VERIFY_OUTCOME.md#record-the-verification-decision](VERIFY_OUTCOME.md#record-the-verification-decision) |
| `PROC-DELIVERY-SELECT` | [DELIVER_RESULT.md#select-the-delivery-action](DELIVER_RESULT.md#select-the-delivery-action) |
| `PROC-REPOSITORY-INTEGRATION` | [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action) |
| `PROC-PREPARE-RELEASE` | [RELEASE.md#prepare-a-release-record](RELEASE.md#prepare-a-release-record) |
| `PROC-RLS-DECIDE` | [RELEASE.md#obtain-the-release-decision-when-required](RELEASE.md#obtain-the-release-decision-when-required) |
| `PROC-RLS-REJECT` | [RELEASE.md#record-the-release-decision-when-required](RELEASE.md#record-the-release-decision-when-required) |
| `PROC-EXTERNAL-ACTION` | [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action) |
| `PROC-REMEDIATE` | [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked) |
| `PROC-DEFINITION-COMPLETE` | [RECORD_STATE.md#complete-a-selected-definition](RECORD_STATE.md#complete-a-selected-definition) |
| `PROC-DEFINITION-WORK` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `PROC-DEC-DISPOSE` | [AUTHORIZE_WORK.md#resolve-approval-blockers](AUTHORIZE_WORK.md#resolve-approval-blockers) |

The returned typed step determines where to enter each referenced procedure.
Do not restart the whole procedure when earlier steps are already complete.
Preserve any exact decision request or command supplied by the evaluator.

**Completion:** One current next step or one exact blocker is reported for the
selected scope. Completed and historical records remain unchanged.

**Later use:** Perform the selected step with its inputs and authority, then
report its actual result under “Report a lifecycle result.”

## Returned typed steps

This index is rendered from the evaluator's versioned instruction catalogue. It
maps selected identifiers; it does not select an action or authorize its execution.

| Returned step | Instruction destination |
| --- | --- |
| `STEP-WO-START-PREFLIGHT` | [EXECUTE_WORK.md#establish-the-execution-context](EXECUTE_WORK.md#establish-the-execution-context) |
| `STEP-WO-START-PREVIEW` | [EXECUTE_WORK.md#start-the-selected-work](EXECUTE_WORK.md#start-the-selected-work) |
| `STEP-WO-START-APPLY` | [EXECUTE_WORK.md#start-the-selected-work](EXECUTE_WORK.md#start-the-selected-work) |
| `STEP-WO-START-FINAL-FOCUS` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `STEP-WO-IMPLEMENT-CHECK` | [EXECUTE_WORK.md#retain-the-implementation-evidence](EXECUTE_WORK.md#retain-the-implementation-evidence) |
| `STEP-WO-IMPLEMENT-PREVIEW` | [EXECUTE_WORK.md#record-implementation-completion](EXECUTE_WORK.md#record-implementation-completion) |
| `STEP-WO-IMPLEMENT-APPLY` | [EXECUTE_WORK.md#record-implementation-completion](EXECUTE_WORK.md#record-implementation-completion) |
| `STEP-WO-PREPARE-VREC-CAPTURE` | [VERIFY_OUTCOME.md#prepare-the-verification-record](VERIFY_OUTCOME.md#prepare-the-verification-record) |
| `STEP-FOCUS-SELECTED` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `STEP-FOCUS-RELATED` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `STEP-VREC-DECIDE` | [VERIFY_OUTCOME.md#obtain-the-humans-verification-decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision) |
| `STEP-REVIEW-PUBLISH` | [PULL_REQUEST.md#publish-the-review-package](PULL_REQUEST.md#publish-the-review-package) |
| `STEP-VREC-REJECT` | [VERIFY_OUTCOME.md#record-the-verification-decision](VERIFY_OUTCOME.md#record-the-verification-decision) |
| `STEP-VREC-SUPERSEDE` | [VERIFY_OUTCOME.md#record-the-verification-decision](VERIFY_OUTCOME.md#record-the-verification-decision) |
| `STEP-DELIVERY-SELECT` | [DELIVER_RESULT.md#select-the-delivery-action](DELIVER_RESULT.md#select-the-delivery-action) |
| `STEP-REPOSITORY-INTEGRATION` | [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action) |
| `STEP-PREPARE-RELEASE` | [RELEASE.md#prepare-a-release-record](RELEASE.md#prepare-a-release-record) |
| `STEP-RLS-DECIDE` | [RELEASE.md#obtain-the-release-decision-when-required](RELEASE.md#obtain-the-release-decision-when-required) |
| `STEP-RLS-REJECT` | [RELEASE.md#record-the-release-decision-when-required](RELEASE.md#record-the-release-decision-when-required) |
| `STEP-EXTERNAL-ACTION` | [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action) |
| `STEP-REMEDIATE-FOCUS` | [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked) |
| `STEP-DEFINITION-COMPLETE` | [RECORD_STATE.md#complete-a-selected-definition](RECORD_STATE.md#complete-a-selected-definition) |
| `STEP-DEFINITION-WORK` | [CONTINUE.md#continue-selected-work](CONTINUE.md#continue-selected-work) |
| `STEP-DEC-DISPOSE` | [AUTHORIZE_WORK.md#resolve-approval-blockers](AUTHORIZE_WORK.md#resolve-approval-blockers) |

## Read next when

Use the returned procedure/step destination in [Continue selected work](CONTINUE.md#continue-selected-work). For a blocker or unknown identifier → [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked).
