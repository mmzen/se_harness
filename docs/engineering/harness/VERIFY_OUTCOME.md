# Verify the outcome

## Read this when

The evaluator selects verification preparation, review or a verification decision.

## Before this action

For preparation, read [WORK_AND_EVIDENCE.md#verification-coverage](WORK_AND_EVIDENCE.md#verification-coverage). For a decision, read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and [AUTHORITY.md#delegation-and-separation](AUTHORITY.md#delegation-and-separation). For supersession only, also read [WORK_AND_EVIDENCE.md#successor-coverage](WORK_AND_EVIDENCE.md#successor-coverage). Read the exact candidate and retained evidence required by the selected contract.

## 4. Verify the outcome

**When:** Implemented work and its evidence are ready for assessment, or an
existing verification record (VREC) awaits a decision.

**Inputs:** The exact candidate, selected work orders (WO), accepted
definitions, verification contracts (VER), and retained evidence.

**Output:** Required verification records (VREC) prepared and decided for the
exact candidate, or explicit findings that prevent verification.

**Steps:**

1. [Establish the verification scope](VERIFY_OUTCOME.md#establish-the-verification-scope).
2. [Assess the verification evidence](VERIFY_OUTCOME.md#assess-the-verification-evidence).
3. [Prepare the verification record](VERIFY_OUTCOME.md#prepare-the-verification-record).
4. [Obtain the human's verification decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision).
5. [Record the verification decision](VERIFY_OUTCOME.md#record-the-verification-decision).

## Procedure

### Establish the verification scope

**Inputs:** The implemented work orders (WO), candidate commit, verification
contracts (VER), and any existing verification records (VREC).

**Output:**

- **Formal artifacts:** None changed.
- **Transient working material:** The selected work-order (WO) set, full
  candidate commit ID, contract IDs, evidence paths, and applicable procedure.

**Actions:**

1. Inspect the selected work order (WO) or existing verification record (VREC).
2. Read its governing definitions, verification contracts (VER), and evidence.
3. Confirm the exact set of work orders (WO) being assessed.
4. Confirm the complete set of verification contracts (VER) declared by them.
5. Identify the full candidate commit and the retained evidence files.
6. Check whether the selected procedure requires a new verification record
   (VREC), an existing-record decision, or no new record.
7. If no new record is required, report that result and follow the returned
   next step. Do not claim a verification decision that has not occurred.

**Harness commands:**

Use the command matching the selected record:

```text
harnessctl check REPO --artifact WO-ID --json
harnessctl check REPO --artifact VREC-ID --json
```

**Completion:** The exact candidate and verification scope are selected, and
the need for a new record is known.

**Later use:** [Assess the verification evidence](VERIFY_OUTCOME.md#assess-the-verification-evidence), [Prepare the verification record](VERIFY_OUTCOME.md#prepare-the-verification-record), [Obtain the human's verification decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision), [Record the verification decision](VERIFY_OUTCOME.md#record-the-verification-decision) use these exact inputs. Changed candidate or evidence
inputs require reassessment before reusing a decision.

### Assess the verification evidence

**Inputs:** The selected candidate, accepted definitions, verification
contracts (VER), and retained implementation evidence.

**Output:**

- **Retained evidence files:** A requirement-by-requirement assessment with
  actual check results and unresolved gaps at the specified evidence locations.
- **Formal artifacts:** No verification decision or lifecycle transition.
- **Transient working material:** Review notes not required as retained evidence.

**Actions:**

1. Compare the candidate's observed behavior with each acceptance criterion.
2. Map every required check to its actual evidence file and pass condition.
3. Confirm that the evidence applies to the selected candidate and environment.
4. Run missing checks using the verification contract's (VER) commands or
   manual procedure. Retain their actual results.
5. Record each criterion as passed, failed, or not assessed, with its reason.
6. Retain material findings and their resolution with the verification evidence.
7. For a defect requiring implementation changes, identify a work order that
   covers the correction and is eligible for execution. Follow the recovery
   rules under “If a procedure is blocked.” A completed work order does not
   become executable again because verification found a defect.
8. After the authorized correction, establish the new candidate identity and
   reassess the affected criteria against evidence for that candidate.

**Harness command:** None for the substantive assessment. Use the check
commands and manual assessments defined in the verification contracts (VER).
Harness validation alone does not prove the required behavior.

**Completion:** Every required criterion has evidence or a visible gap.
Failures and missing checks are not reported as passes.

**Later use:** [Prepare the verification record](VERIFY_OUTCOME.md#prepare-the-verification-record) binds the retained evidence to a verification record
(VREC). [Obtain the human's verification decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision) uses it for the human's assessment.

### Prepare the verification record

**Inputs:** The exact candidate, selected work orders (WO), their verification
contracts (VER), retained evidence, and existing preparation authority.

**Output:**

- **Formal artifacts:** One new verification record (VREC) in `ready` when
  capture is required and succeeds. Related work-order (WO) states do not change.
- **Retained files:** The generated evaluator evidence and candidate snapshot
  or export required by the capture procedure.
- **Transient working material:** The capture result and inspected output paths.

**Actions:**

1. If a suitable verification record (VREC) already exists, inspect it and
   continue to [Obtain the human's verification decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision). Do not duplicate an interrupted successful capture.
2. Confirm preparation authority under every selected work order's (WO)
   approval. Reuse it while the scope and inputs match.
3. Select an unused `VREC-ID` after checking the repository's local Git refs.
4. Confirm the domain and actual record and evidence destinations. Keep all
   generated writes within the authorized preparation scope.
5. Establish a clean committed candidate using authorized local Git actions.
   Retain its full commit ID. Do not discard unrelated changes to obtain it.
6. Run the capture command with each selected work order (WO), every declared
   verification contract (VER), and each retained evidence file.
7. Read the generated record and evaluator evidence. Confirm the candidate
   commit, selected IDs, evidence digests, and `ready` state.
8. Retain generated records and evidence in a later authorized governance
   commit. Preserve the earlier candidate commit that the record assesses.

**Harness commands:**

```text
harnessctl capture-verification REPO --id VREC-ID --work-order WO-ID --verification VER-ID --evidence EVIDENCE-PATH --owner ACTOR --domain DOMAIN --json
harnessctl check REPO --artifact VREC-ID --json
```

Use the actual preparation actor for `--owner`. Preparation does not record
a future verification or release decision. Preserve the generated record and
its bound evidence without changing the recorded evidence bytes.

Repeat `--work-order`, `--verification`, and `--evidence` for every selected
input. `EVIDENCE-PATH` is a repository-relative file, not a directory or an
index whose links will be followed automatically. Capture writes immediately
after its checks; it has no `--dry-run` or `--apply` option.

If an unchanged rebase leaves an earlier ready record bound to the old
candidate, use [Refresh verification after an unchanged rebase](VERIFY_OUTCOME.md#refresh-verification-after-an-unchanged-rebase).
A verified source or changed relevant inputs cannot use that shortcut.

If preserving local edits requires the supported committed-candidate route,
use `--candidate-commit COMMIT` with `--test-command EXECUTABLE ARGUMENTS`.
Put `--test-command` last. That route tests the named commit in a temporary
checkout; use its actual results and returned record, not results from the
uncommitted edits.

**Completion:** A ready verification record (VREC) binds the selected candidate
and evidence, or capture reports a specific refusal. Preparation is not verification.

**Later use:** [Obtain the human's verification decision](VERIFY_OUTCOME.md#obtain-the-humans-verification-decision) presents the exact record and evidence for the human decision.

### Obtain the human's verification decision

**Inputs:** The ready verification record (VREC), candidate commit, evidence
digests, assessment results, and accountable human's verification authority.

**Output:**

- **Formal artifacts:** None changed by the discussion or read-only gate check.
- **Transient working material:** The human's exact verification, rejection,
  or supersession decision and reason where required.

**Actions:**

1. Present the record, full candidate commit, evidence, and unresolved findings.
2. For verification or rejection, evaluate the proposed target with the
   command below. Supersession gates are evaluated with the selected successor
   in [Record the verification decision](VERIFY_OUTCOME.md#record-the-verification-decision)'s transition preview.
3. Obtain the accountable human's decision on that exact verification record
   (VREC). Preserve the required independence from implementation.
4. Reuse a previous decision only while its record, candidate, evidence digests,
   authority, and current gates still match.
5. For rejection, retain the reason. For supersession, identify the exact
   eligible successor verification record (VREC).

**Harness command:**

```text
harnessctl check REPO --artifact VREC-ID --checkpoint transition --target TARGET --json
```

Use `verified` or `rejected` for `TARGET`. The evaluator determines whether
that edge is legal. Supersession needs the successor input accepted by
`transition --reason`, which this check command does not accept.
A passed check is not the human decision.

**Completion:** The exact verification decision is known, or the record remains
pending. No implementation actor infers acceptance from their own passing tests.

**Later use:** [Record the verification decision](VERIFY_OUTCOME.md#record-the-verification-decision) records only the selected decision.

### Record the verification decision

**Inputs:** The exact human decision, ready verification record (VREC), and
unchanged candidate and evidence inputs.

**Output:**

- **Formal artifacts:** Only the selected verification record (VREC) receives
  its permitted state and lifecycle-history entry.
- **Retained files:** The updated record is retained through authorized Git
  actions. Historical candidate and evidence facts are preserved.
- **Transient working material:** The observed decision result and next action.

**Actions:**

1. Recheck that the selected inputs still match the human decision.
2. Preview the exact transition.
3. Apply the same command when its gates pass and effects match the decision.
4. Inspect the verification record (VREC) and resulting workflow context.
5. Report its actual state, any blocker, and the evaluator's next action.

**Harness commands:**

```text
harnessctl transition REPO --set VREC-ID=TARGET --decision VREC-ID=ACTOR --json
harnessctl transition REPO --set VREC-ID=TARGET --decision VREC-ID=ACTOR --apply --json
harnessctl check REPO --artifact VREC-ID --json
```

For supersession, select a successor verification record that is already
`verified` or `released` and preserves the old record’s work-order coverage.
Use the transition preview to assess that selection.

For `rejected`, add `--reason "VREC-ID=Rejection reason"` to preview and apply.
For `superseded`, add `--reason "VREC-ID=SUCCESSOR-VREC-ID"` to both. Preserve
the old record; do not rewrite its candidate or evidence to match a new result.

**Completion:** The selected verification record (VREC) has the recorded
decision. Referenced work orders (WO) and release records (RLS) remain unchanged.

**Later use:** Eligible verified coverage supports the selected delivery path.
A rejection or supersession follows the evaluator's remediation or selection
procedure; it does not authorize new implementation scope.

### Refresh verification after an unchanged rebase

**Inputs:** An existing verification record in `ready`, a new clean committed
candidate, the unchanged work/contract/evidence selection, and preparation
authority under each selected work order's approval.

**Output:**

- **Formal artifact:** One new verification record in `ready`, with
  `refreshed_from` naming the original record, if the comparison passes.
- **Retained evidence:** New evaluator provenance for the new record. The
  original record and its evidence remain intact.
- **Transient working material:** The selected IDs, comparison result, and
  any refusal. No new test result is claimed.

**Actions:**

1. Read the original record and confirm it is `ready`. A verified record is
   not a valid refresh source.
2. Select the new candidate commit. Confirm the worktree is clean.
3. Select an unused new VREC ID after checking the local Git refs, as in the
   verification-record preparation procedure.
4. Read the original work-order, verification-contract, and evidence selections.
   The command reuses them; do not substitute a different selection.
5. Run the refresh command below using the actual preparation actor.
6. Inspect the result. The evaluator compares relevant Git tree entries,
   including governing files, execution scope, harness inputs, and evidence.
7. If relevant inputs changed, return to fresh tests and verification capture.
   Do not edit evidence or reduce scope to force the comparison to pass.
8. Read the new record and confirm its candidate, selections, provenance, and
   `refreshed_from`. Confirm the original record remains unchanged.

**Harness commands:**

```text
harnessctl check REPO --artifact OLD-VREC-ID --json
harnessctl refresh-verification REPO --from OLD-VREC-ID --id NEW-VREC-ID --owner ACTOR --domain DOMAIN --json
harnessctl check REPO --artifact NEW-VREC-ID --json
```

Refresh writes after its checks. It has no `--dry-run` or `--apply` option.
It reruns no tests and verifies neither record. Equality of relevant Git
entries is assessed by the evaluator, not inferred from the word “rebase.”

**Completion:** A new ready record binds the new candidate, or a refusal names
the changed or invalid inputs. The original record's state is unchanged.

**Later use:** Return to the human verification decision in “Verify the outcome.”
If the original ready record should be superseded, use its own explicitly
selected supersession procedure after an eligible successor exists.

## Read next when

The result selects delivery → [DELIVER_RESULT.md#select-the-delivery-action](DELIVER_RESULT.md#select-the-delivery-action). A separate work-order state change is selected → [RECORD_STATE.md#record-work-order-verification-or-release](RECORD_STATE.md#record-work-order-verification-or-release).
