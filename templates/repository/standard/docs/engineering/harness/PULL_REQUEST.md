# Prepare and check a pull request

## Read this when

The selected delivery action is preparing or checking an exact governed pull request.

## Before this action

Read the selected work orders and the repository PR procedure. Before an external PR write, read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action).

## Procedure

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
