# Authorize the work

## Read this when

The proposed package needs validation, review or a human authorization decision.

## Before this action

For reviewing each definition, use its selected [Type checklist](DRAFT_DEFINITIONS.md#type-checklists). Before review, read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and [AUTHORITY.md#delegation-and-separation](AUTHORITY.md#delegation-and-separation). Before approving work, read [WORK_AND_EVIDENCE.md#assurance-classification](WORK_AND_EVIDENCE.md#assurance-classification). For an open or deferred decision, read [RISKS_AND_DECISIONS.md#blocking-decisions](RISKS_AND_DECISIONS.md#blocking-decisions).

## 2. Authorize the work

**When:** The proposed definitions and work orders (WO) are ready for review.

**Inputs:** The proposed artifacts, their validation results, and unresolved
decisions (DEC) or amendment proposals.

**Output:** Explicit decisions on the selected definitions and work orders
(WO), recorded through permitted transitions. Work orders (WO) may become
`approved`; approval does not start execution.

**Steps:**

1. [Assess the proposed artifact package](AUTHORIZE_WORK.md#assess-the-proposed-artifact-package).
2. [Resolve approval blockers](AUTHORIZE_WORK.md#resolve-approval-blockers).
3. [Obtain the human's decision](AUTHORIZE_WORK.md#obtain-the-humans-decision).
4. [Apply the selected transitions](AUTHORIZE_WORK.md#apply-the-selected-transitions).
5. [Confirm the authorization result](AUTHORIZE_WORK.md#confirm-the-authorization-result).

## Procedure

### Assess the proposed artifact package

**Inputs:** The selected work order (WO) IDs, proposed definitions, validation
results, and existing decision records (DEC).

**Output:**

- **Formal artifacts:** None created or modified.
- **Transient working material:** A review list identifying the selected
  artifacts, their states, applicable checks, and reported blockers.

**Actions:**

1. Run validation for the repository.
2. Inspect each selected work order (WO) with the command below.
3. Read the work order (WO) and its returned reading manifest.
4. Review the governing definitions against the relevant checklists in
   `docs/engineering/ARTIFACT_AUTHORING.md`.
5. Check that the proposed work has defined scope, verification coverage,
   assurance classification, and accountable humans for the required decisions.
6. List the blockers affecting the selected package. Keep unrelated findings
   separate.

**Harness commands:**

```text
harnessctl validate REPO --json
harnessctl check REPO --artifact WO-ID --json
harnessctl check REPO --artifact WO-ID --checkpoint transition --target approved --json
```

Read the result of each required check. A `pass` satisfies that check only;
it does not approve the artifacts or authorize implementation. If a required
check returns `fail` or `not_assessable`, report its identifier and stated
reason, then follow “If a procedure is blocked.” Do not proceed with the
affected approval.

The last command evaluates work-order approval gates. A checkpoint-free
`check` only reports lifecycle context. Definition artifacts cannot be selected
with `check`; their transition gates are evaluated by the previews in [Apply the selected transitions](AUTHORIZE_WORK.md#apply-the-selected-transitions).

Before proposing a definition for approval, resolve its template placeholders.
If it contains an `Open decisions` section, confirm that no unresolved decision
remains before setting that section to `None`. Do not remove an unresolved
question merely to make validation pass.

**Completion:** The selected package has an explicit list of review findings
and approval blockers. No approval is inferred from these checks.

**Later use:** [Resolve approval blockers](AUTHORIZE_WORK.md#resolve-approval-blockers) resolves the blockers. [Obtain the human's decision](AUTHORIZE_WORK.md#obtain-the-humans-decision) presents the package for a
human decision.

### Resolve approval blockers

**Inputs:** The findings from [Assess the proposed artifact package](AUTHORIZE_WORK.md#assess-the-proposed-artifact-package) and the affected draft artifacts or
pending decisions (DEC).

**Output:**

- **Formal artifacts:** Corrected drafts within the proposed scope. Where an
  actual human decision is supplied, the selected decision (DEC) receives its
  disposition. A paired risk (RISK) may change through that same operation.
- **Transient working material:** The resolution of each finding and any
  remaining dependency requiring an amendment or another human decision.

**Actions:**

1. Correct incomplete or inconsistent draft content within the requested scope.
2. Return an accepted-definition change to the amendment procedure in
   “Define the change.” Do not edit accepted authority to clear a check.
3. For a blocking decision (DEC), inspect its current question and options.
4. Obtain the accountable human's exact answer if it has not already been given.
5. Preview that disposition with the command below.
6. Apply the same command with `--apply` only if its inputs match the actual
   decision and the preview passes.
7. Read back the decision (DEC) and any paired risk (RISK).
8. Rerun the checks affected by the corrections. Preserve unresolved blockers.

**Harness commands:**

```text
harnessctl check REPO --artifact DEC-ID --json
harnessctl decide REPO --artifact DEC-ID --option OPTION-ID --decision ACTOR --reason "Exact decision reason" --json
```

Use a declared option ID. Add `--revisit "Trigger"` for acceptance of a
deviation. A risk-mitigation option also requires `--mitigated-by WO-ID` for
each selected mitigating work order (WO). For a risk-avoidance option, use
`--avoided-by ARTIFACT-ID` when naming a separate architecture decision (ADR)
or decision (DEC). Review the returned operation before applying it.

ACTOR is the actual human who made the decision. If that human acts under an
existing owner label, first resolve their authority under
[Decision rights](AUTHORITY.md#decision-rights), then add
`--authority-owner OWNER` to both preview and apply. For example, a human
named `mmzen` acting under `engineering-owner` uses
`--decision mmzen --authority-owner engineering-owner`. Do not put the owner
label in place of the human. Neither string authenticates the decision.
OWNER must be non-blank printable text of at most 128 characters and match
an eligible owner exactly. An unrelated label refuses without writing.

For an explicitly authorized deferral, use this preview instead:

```text
harnessctl decide REPO --artifact DEC-ID --defer --scope ARTIFACT-ID:FROM-TO --revisit "Trigger" --decision ACTOR --reason "Exact decision reason" --json
```

Repeat `--scope` for each permitted transition. For an explicitly authorized
withdrawal, replace the option or deferral arguments with `--withdraw`.
Apply a passing preview by repeating the exact command with `--apply`.
Then inspect the decision (DEC) again and rerun validation:

```text
harnessctl check REPO --artifact DEC-ID --json
harnessctl validate REPO --json
```

If proposing a departure from a `SHOULD` rule, record the rule ID, reason,
impact, accountable human or agent, and compensating evidence. Present these
with the affected review finding. Recording the departure does not authorize
an action or waive a required check.

**Completion:** Each blocker is resolved or assigned an explicit outstanding
decision. A deferral clears only its recorded transition scope.

**Later use:** [Obtain the human's decision](AUTHORIZE_WORK.md#obtain-the-humans-decision) receives the corrected package. Unresolved blockers
remain visible and prevent the affected approval.

### Obtain the human's decision

**Inputs:** The reviewed package, current findings, and any decision already
supplied for the same artifact contents and target states.

**Output:**

- **Formal artifacts:** Pending assurance fields in selected draft work orders
  completed from the human's confirmed classification. No lifecycle state
  changes in this step.
- **Transient working material:** The human's approval, rejection, or request
  for revision, bound to exact artifact IDs, reviewed contents, and authority.

**Actions:**

1. Present one concise request for the coherent package using the decision
   card below. Identify the selected artifacts and proposed state for each.
2. Present the scope, verification obligations, proposed assurance classification,
   its rationale, and unresolved findings.
3. Identify the human accountable for each requested decision.
4. Retain a SHA-256 digest of each reviewed definition's complete file bytes.
5. Obtain an explicit approval, rejection, or request for revision. Work-order
   approval must include confirmation of the assurance classification. Record that
   confirmation in the work order's `[assurance]` fields before the approval
   preview. A rejection needs a reason. Reuse an existing decision while its
   reviewed inputs match.
6. If revision is requested, return the affected drafts to [Resolve approval blockers](AUTHORIZE_WORK.md#resolve-approval-blockers). Do not
   interpret a request for revision as a terminal rejection.

**Harness command:** None. A command result cannot supply the human decision.

**Decision card:**

- **Approval requested:** Name the decision and useful outcome in ordinary
  language. Use "Approve implementation" for local implementation authority.
  For PR-based work, use "Approve implementation and review publication" and
  describe the bounded grant from [Review publication authority](AUTHORITY.md#review-publication-authority).
  Verification acceptance and merge remain separate decisions.
- **Why:** State the problem this change solves.
- **What changes:** Summarize the bounded changes, including supporting work.
- **What success looks like:** State the observable result and required checks.
- **Important limit:** State material uncertainty or an unresolved boundary,
  when one exists. Do not hide it behind a passing coverage report.
- **Your approval permits:** State the exact permitted actions and any
  separate acceptance or external-action decision relevant to this request.
- **Review details:** Link the exact definitions, work orders and verification
  contracts, their proposed states and their reviewed revisions.

Offer "Approve implementation" and "Request changes" when implementation is
the decision. When the described grant includes review publication, offer
"Approve implementation and review publication" instead. Name the repository,
source branch, target branch, draft PR and later verification-decision push
in "Your approval permits." The human need not type artifact IDs or CLI commands. Bind the
answer to the displayed package and permission. Reuse an actual prior decision
while its reviewed inputs still match; do not ask for the same authority again.

**Completion:** Each selected artifact has an explicit human decision or
remains pending. Pending artifacts are not included in an approval transaction.

**Later use:** [Apply the selected transitions](AUTHORIZE_WORK.md#apply-the-selected-transitions) applies only the transitions named by these decisions.

### Apply the selected transitions

**Inputs:** The exact artifact IDs, target states, accountable human identities,
reviewed file digests, decisions from [Obtain the human's decision](AUTHORIZE_WORK.md#obtain-the-humans-decision), and clarification answers from
[Define the change](DEFINE_CHANGE.md#procedure) that must be retained in the transition reason.

**Output:**

- **Formal artifacts:** Only explicitly selected definitions and work orders
  (WO) receive the applied state and lifecycle-history entries.
- **Transient working material:** The preview and apply results, including
  any refused transition.

**Actions:**

1. Confirm that the reviewed artifact contents still match the human decision.
2. Select only the named transitions. Approve governing definitions before
   dependent work, or use one explicitly selected packet for mutually
   dependent definitions when the evaluator permits it.
3. Preview the transition command below.
4. Compare every selected ID, target state, actor, and reported effect with
   the human decision. Resolve failed gates before proceeding.
5. Recheck reviewed definition digests immediately before applying.
6. Repeat the passing command with `--apply`. Do not add related artifacts
   that the human did not select.

**Harness commands:**

```text
harnessctl transition REPO --set ARTIFACT-ID=TARGET --decision ARTIFACT-ID=ACTOR --json
harnessctl transition REPO --set ARTIFACT-ID=TARGET --decision ARTIFACT-ID=ACTOR --apply --json
```

For each clarification below the formal-decision threshold, add
`--reason "ARTIFACT-ID=Question and confirmed answer"` to both the preview
and apply command. Use the actual question and answer. When one artifact
has several such answers, combine them into one reason value for that ID.
Keep each complete `ID=TEXT` value as one argument. Confirm the saved reason
in the resulting lifecycle entry before discarding the working notes.

For approval, `TARGET` is `approved`. For rejection, use `rejected` and add
`--reason "ARTIFACT-ID=Rejection reason"` to both commands. Rejection is
terminal. For a packet, repeat `--set` and `--decision` for every explicitly
selected artifact. Preview and apply must contain the same assignments.

**Completion:** The evaluator reports the actual applied transitions, or the
specific refusal. A successful preview alone changes nothing.

**Later use:** [Confirm the authorization result](AUTHORIZE_WORK.md#confirm-the-authorization-result) confirms the resulting authority and readiness.

### Confirm the authorization result

**Inputs:** The applied transition result and selected artifact files.

**Output:**

- **Formal artifacts:** None changed by readback.
- **Transient working material:** The authorization handoff, stating actual
  states, execution readiness, remaining blockers, and the evaluator's next step.

**Actions:**

1. Read the selected artifact states and new lifecycle-history entries.
2. Inspect each selected work order (WO) with `check`.
3. For an approved work order (WO), run start preflight to assess readiness.
4. Report the approved scope and any remaining start blockers. Report rejected
   or pending work separately.

**Harness commands:**

```text
harnessctl check REPO --artifact WO-ID --json
harnessctl preflight REPO --work-order WO-ID --phase start --json
```

Use the preflight command only for work proposed to start. It changes no state.
Read definition states from the files and transition result; do not call
`check` with definition IDs.

**Completion:** Actual authorization and start readiness are known. An approved
work order (WO) remains `approved` until the start transition is applied.

**Later use:** [Execute the work](EXECUTE_WORK.md#procedure) uses the recorded approval. It does not
request the same execution authority again while the scope and conditions match.

## Read next when

The evaluator selects execution → [EXECUTE_WORK.md#procedure](EXECUTE_WORK.md#procedure). A blocker remains → [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked).
