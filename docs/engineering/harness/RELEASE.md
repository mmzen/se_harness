# Prepare and decide a release

## Read this when

The evaluator selects release-record preparation or a decision on a ready release record.

## Before this action

Before preparing, read [WORK_AND_EVIDENCE.md#release-coverage](WORK_AND_EVIDENCE.md#release-coverage) and the selected REL/VREC records. Before a release decision, read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and [AUTHORITY.md#delegation-and-separation](AUTHORITY.md#delegation-and-separation).

## Procedure

### Prepare a release record

**Inputs:** The selected path, existing preparation authority, exact candidate,
and the release contract (REL) and eligible verified coverage required by that
path. Release-record preparation requires both.

**Output:**

- **Release path:** One release record (RLS) in `ready` and its generated
  evaluator evidence, when preparation is required and succeeds.
- **Retained files:** Required build or delivery evidence at the authorized
  locations. Builds occur only when separately covered by the selected scope.
- **Transient working material:** Preparation notes, proposed external content,
  and inspected write destinations.

**Actions:**

1. Confirm authority for the exact preparation operation. Obtain a missing
   human decision before writing; reuse matching authority already supplied.
2. Inspect existing records and outputs before creating replacements.
3. For release, select an active release contract (REL), version, domain,
   and unused release record (RLS) ID. Check local Git refs and existing
   version reservations before choosing the ID and version.
4. Select the final eligible verification record (VREC) for the candidate.
   Its work-order (WO) set must exactly cover the work being released.
5. Confirm all intended output paths and the clean working-tree condition
   required by release preparation.
6. Run the release preparation command. Inspect its written record, evidence,
   candidate identity, and `ready` state.
7. Retain the new release record (RLS) and evidence in an authorized governance
   commit after the candidate they describe.

**Harness commands:**

For release preparation:

```text
harnessctl prepare-release REPO --id RLS-ID --release-contract REL-ID --verification-record VREC-ID --work-order WO-ID --version VERSION --owner ACTOR --domain DOMAIN --json
harnessctl check REPO --artifact RLS-ID --json
```

Use the actual preparation actor for `--owner`. Preparation does not record
a future verification or release decision. Preserve the generated record and
its bound evidence without changing the recorded evidence bytes.

Repeat `--work-order` for every released work order (WO). This evaluator requires one final verification record (VREC) covering the complete
release. Earlier records remain supporting evidence. If that coverage is
missing, return to verification instead of inventing or relabelling it.

Add `--tag TAG` only for an explicitly selected tag value; this records the
value and does not create a Git tag. `prepare-release` writes after its checks;
it has no `--dry-run` or `--apply` option.

**Completion:** The required delivery inputs are prepared, or a precise
preparation blocker is known. Preparation performs no merge, publication,
deployment, or release decision.

**Later use:** A ready release record (RLS) proceeds to [Obtain the release decision, when required](RELEASE.md#obtain-the-release-decision-when-required). 

### Obtain the release decision, when required

**Inputs:** The ready release record (RLS), release contract (REL), candidate,
verified coverage, version, and accountable human's release authority.

**Output:**

- **Formal artifacts:** None changed by review or the gate check.
- **Transient working material:** The human's exact release or rejection
  decision, including the reason for rejection.

**Actions:**

1. Present the candidate, included work, verification coverage, version,
   constraints, rollback conditions, and required release evidence.
2. Run the transition gate check for the intended target state.
3. Obtain the accountable human's decision on the selected release record
   (RLS). Reuse a matching decision already supplied.
4. Retain a rejection reason when applicable.

**Harness command:**

```text
harnessctl check REPO --artifact RLS-ID --checkpoint transition --target TARGET --json
```

Use `released` or `rejected` for `TARGET`, according to the proposed decision.
The evaluator determines legality. A passed check does not supply approval.

**Completion:** The release decision is explicit, or remains pending.

**Later use:** [Record the release decision, when required](RELEASE.md#record-the-release-decision-when-required) records that decision. It does not extend to publication
or deployment unless the exact external action is separately authorized.

### Record the release decision, when required

**Inputs:** The human's exact decision and unchanged release inputs.

**Output:**

- **Formal artifacts:** Only the selected release record (RLS) receives the
  permitted state and lifecycle-history entry.
- **Retained files:** The updated release record (RLS), retained through
  authorized Git actions.
- **Transient working material:** The applied result and current next action.

**Actions:**

1. Compare the current release inputs with the human's reviewed inputs.
2. Preview the selected transition.
3. Apply the same command when its gates pass and effects match the decision.
4. Inspect the release record (RLS) and report the actual resulting state.

**Harness commands:**

```text
harnessctl transition REPO --set RLS-ID=TARGET --decision RLS-ID=ACTOR --json
harnessctl transition REPO --set RLS-ID=TARGET --decision RLS-ID=ACTOR --apply --json
harnessctl check REPO --artifact RLS-ID --json
```

For rejection, add `--reason "RLS-ID=Rejection reason"` to both transition
commands. Related verification records (VREC) and work orders (WO) are not
transitioned automatically.

**Completion:** The release decision is recorded or explicitly refused.
No Git tag, publication, or deployment has been performed by this transition.

**Later use:** A released record may support [Confirm authority for the external action](DELIVER_RESULT.md#confirm-authority-for-the-external-action)'s external-action checks.
Rejection follows the evaluator's remediation procedure.

## Read next when

An authorized external action is selected → [DELIVER_RESULT.md#confirm-authority-for-the-external-action](DELIVER_RESULT.md#confirm-authority-for-the-external-action). Verification coverage is missing → [VERIFY_OUTCOME.md#procedure](VERIFY_OUTCOME.md#procedure).
