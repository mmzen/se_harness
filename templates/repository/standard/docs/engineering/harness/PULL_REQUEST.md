# Prepare and check a pull request

## Read this when

The selected delivery action is preparing or checking an exact governed pull request.

## Before this action

Read the selected work orders and the repository PR procedure. Before an external PR write, read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action).

## Procedure

### Publish the review package

**Inputs:** Implemented PR-based work, its exact captured candidate, ready VREC,
retained evidence, trusted comparison base, and the matching
[review-publication grant](AUTHORITY.md#review-publication-authority).

**Output:** A confirmed draft PR containing the review package, or a precise
publication blocker. The VREC stays `ready`; no verification or merge occurs.
Keep working observations in conversation or temporary storage outside the
repository unless the verification contract requires durable evidence.

**Actions:**

1. Inspect the selected ready VREC and reuse its candidate and bound evidence.
   Commit the generated record and its required preparation evidence. Record
   the review head separately from the candidate: the later commit contains
   the record prepared from that candidate. Confirm that intervening changes
   contain only the expected preparation material, not new implementation or
   changed bound evidence.
2. Confirm the actual publication grant and its repository, source branch,
   target branch and selected work. Obtain only missing authority. Resolve the
   exact full head commit for this write and compare its complete content with
   the grant. A passing check or ordinary implementation approval is insufficient.
3. Use [Check a governed pull request](PULL_REQUEST.md#check-a-governed-pull-request)
   for the complete work-order set, body and change set. Keep the work-order
   declaration, state "verification pending", and link the captured candidate,
   ready record, assessment and evidence. Report actual CI status; a pending
   or skipped check is not a pass.
4. Run the review-publication check below, then
   [confirm external-action authority and provider controls](DELIVER_RESULT.md#confirm-authority-for-the-external-action).
   Use this ready-record route, not the verified integration route.
5. With the repository's Git and hosting tools, push the exact review head and
   create the draft PR. Reuse or update a matching existing draft PR. Do not
   force-push, duplicate a PR, merge or mark it ready for merge.
6. Read back the PR URL, head repository, source and target branches, full head
   commit and draft status. Confirm that the selected record and evidence are
   readable at that head by the intended owner. Use immutable remote links.
   A local file or successful write response alone does not establish this.
7. If publication fails or the response is uncertain, inspect the remote before
   retrying. Report a missing grant, inaccessible package or mismatched head
   as a blocker. Do not request verification until the exact PR is confirmed.

**Harness commands:**

```text
harnessctl check REPO --artifact VREC-ID --json
harnessctl check REPO --artifact VREC-ID --checkpoint pre-action --procedure PROC-REVIEW-PUBLISH --json
```

The evaluator must declare this alternative for the selected ready record.
The command evaluates local prerequisites; it neither publishes the PR nor
proves remote visibility or authenticates a human grant. Use the normal
`pr-body` and `check-pr` commands below for PR preparation and scope.

**Completion:** The exact remote draft PR and its review content are confirmed,
or the publication blocker is known. Required verification evidence must still
pass before acceptance is offered.

**Later use:** Present the [verification request](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision)
with the PR URL and remote evidence links. Local-only work does not use this
PR procedure. If the human requests corrections, keep the PR in draft and the
decision pending; assess eligible work and recapture or refresh changed inputs.

### Publish the verification decision

**Inputs:** The human's recorded verification decision, unchanged candidate and
bound evidence, confirmed review PR, and the existing publication grant.

**Output:** One final decision commit pushed to the same PR, with its remote
decision confirmed. Merge remains the human's choice.

**Actions:**

1. Apply and read back the selected decision through
   [Record the verification decision](VERIFY_OUTCOME.md#record-the-verification-decision).
   Inspect an existing event before retrying an uncertain transition.
2. Compare the working changes with the published review head. The final commit
   MUST contain only the selected VREC's state and lifecycle-history update.
   An aggregate decision may update the selected VRECs together. Preserve their
   captured candidate, evidence digests and governing links. Stop for assessment
   if implementation, evidence, other artifacts or the destination changed.
3. Commit that decision update. Use the current integration pre-action check,
   complete PR scope check and provider controls for the full final head.
   Reuse the explicit grant covering this decision-only push; do not request
   another push/PR approval while its bounds still match.
4. Push the final commit to the same source branch. Confirm the remote head and
   the recorded verification before marking the PR ready. Update its review
   summary under the existing grant, preserving the original candidate identity.
5. Report required CI against the final PR head. Marking the PR ready does not
   establish that its checks pass or authorize the agent to merge. The human
   may merge when the required checks and protections permit it.

**Harness command:**

```text
harnessctl check REPO --artifact VREC-ID --checkpoint pre-action --procedure PROC-REPOSITORY-INTEGRATION --json
```

Use this procedure only when the evaluator declares it for the verified record.
The Git and hosting tools perform the authorized writes.

**Completion:** The verified decision is remote as the final commit, or it is
recorded locally with publication still blocked. In the latter case, do not
reapply the decision or mark the PR ready; inspect the remote and retry only
missing effects. This commit records acceptance of the earlier candidate.
It does not require a new VREC merely to verify the recording of that decision.

**Later use:** The human may select merge. A later implementation or evidence
change needs reassessment and applicable work and verification procedures;
the old decision must not be applied to changed inputs.

### Check a governed pull request

**Inputs:** The exact pull request or proposed body, complete selected
work-order set, checked-out PR candidate, trusted comparison base, and existing
authority for any PR creation or update.

**Output:**

- **Formal artifacts:** No lifecycle transition.
- **Pull-request content:** A proposed or authorized updated body with one
  exact work-order declaration and the actual verification summary.
- **Retained evidence:** Check results and any handoff evidence written by
  `check-pr` at the work orders' authorized evidence locations.
- **Transient working files:** The event JSON used as command input, stored
  outside the repository. Retain a durable copy only if a governing evidence
  requirement explicitly calls for it.

**Actions:**

1. Identify the complete set of work orders covering the PR diff. Use the
   selected released PR checker's eligibility result. Do not reset a later
   state to fit the checker.
2. For one work order, generate its body with `pr-body` and review the result.
3. For several work orders, prepare one body with the combined scope and
   verification summary. Use exactly one plural declaration; do not concatenate
   several generated singular declarations.
4. Preserve one standalone declaration with no Markdown bullet or indentation:

   ```text
   Harness-Work-Order: WO-AAA-001
   ```

   Or, for several distinct work orders:

   ```text
   Harness-Work-Orders: WO-AAA-001, WO-BBB-002
   ```

5. Publish or update the body only under the exact existing PR authority.
6. For an existing PR, obtain its current body from the hosting service. Do not
   use an earlier workflow-event snapshot after the body has changed.
7. Write a temporary JSON object with `pull_request.body` containing that exact
   body. Use a JSON writer so quotes and newlines are encoded correctly.
8. Resolve the PR's comparison base to a trusted commit available locally.
   Use that commit as `BASE`, and the temporary JSON path as `EVENT`.
9. Run `check-pr`. It checks the complete diff against the union of the selected
   scopes and runs the applicable checks for those work orders.
10. Resolve reported gaps within existing authority. If the live body changes,
    obtain it again and rerun the check. A body-only correction needs no dummy
    source commit or push.

**Harness commands:**

For one work order:

```text
harnessctl pr-body REPO --artifact WO-ID --json
```

For the proposed or current body and complete PR scope:

```text
harnessctl check-pr REPO --event EVENT --from-git BASE --json
```

`pr-body` returns text; it does not create or update a PR. `check-pr` may write
handoff evidence for selected work in progress; its destinations must be
authorized. Neither command approves or merges the PR. A generated
`Harness-Restitution` digest refers to one work order. Omit that field for a
combined PR; do not copy a single-work-order digest into a combined result.

**Completion:** The result describes the exact body and complete compared
change set. A changed body, candidate, or base requires a new check.

**Later use:** Use the current result with the selected integration procedure
and its external-action authority. Required CI still applies. Repository
exception support is described in [EXCEPTIONS.md#availability](EXCEPTIONS.md#availability).

## Read next when

The exact external action is authorized → [DELIVER_RESULT.md#perform-the-authorized-delivery](DELIVER_RESULT.md#perform-the-authorized-delivery). Report checks → [RESULTS.md#report-a-lifecycle-result](RESULTS.md#report-a-lifecycle-result).


## Prepare the integration package

**Inputs:** The selected work orders, exact candidate, preparation authority and
repository PR procedure.

**Output:** A proposed PR body and required check results. Proposed external
content is transient until an authorized write. No RLS is created for integration.

**Actions:** Confirm matching preparation authority and inspect existing outputs.
Prepare the repository's required content and checks. Generate the work-order
declaration with `pr-body`; follow [Check a governed pull request](PULL_REQUEST.md#check-a-governed-pull-request)
for combined scope and live-body handling. Retain required evidence at its
authorized locations. Body generation does not create or update a PR.

**Harness command:**

```text
harnessctl pr-body REPO --artifact WO-ID --json
```

**Completion:** The proposed body and required inputs are ready, or the precise
preparation blocker is reported.

**Later use:** [Confirm authority for the external action](DELIVER_RESULT.md#confirm-authority-for-the-external-action)
before creating, updating or merging the PR.
