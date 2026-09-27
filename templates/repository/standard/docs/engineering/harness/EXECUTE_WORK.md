# Execute the work

## Read this when

The evaluator selects work start, implementation or completion under matching authority.

## Before this action

Read the selected work order and governing artifacts returned by the evaluator. Before using its execution grant, read [AUTHORITY.md#authority-from-work-approval](AUTHORITY.md#authority-from-work-approval). For a scope finding, read [RESULTS.md#if-a-procedure-is-blocked](RESULTS.md#if-a-procedure-is-blocked).

## 3. Execute the work

**When:** A selected work order (WO) is approved and ready to start, or its
authorized execution is already in progress.

**Inputs:** The selected work orders (WO), governing artifacts, approved scope,
verification contracts (VER), and required reading manifest.

**Output:** Implemented work within the approved scope, retained evidence,
and work orders (WO) with completion recorded when the required checks pass.

**Steps:**

1. [Establish the execution context](EXECUTE_WORK.md#establish-the-execution-context).
2. [Start the selected work](EXECUTE_WORK.md#start-the-selected-work).
3. [Implement the approved scope](EXECUTE_WORK.md#implement-the-approved-scope).
4. [Retain the implementation evidence](EXECUTE_WORK.md#retain-the-implementation-evidence).
5. [Record implementation completion](EXECUTE_WORK.md#record-implementation-completion).

## Procedure

### Establish the execution context

**Inputs:** The selected work order (WO) ID and its recorded approval.

**Output:**

- **Formal artifacts:** None changed.
- **Transient working material:** The current execution scope, reading list,
  applicable procedure, and trusted Git base for the complete change set.

**Actions:**

1. Inspect the selected work order (WO).
2. Read every file in `context.reading_manifest`.
3. Read the approved behavior, permitted paths, decision limits, stop
   conditions, verification contracts (VER), and required repository checks.
4. Identify the complete change baseline required by the selected procedure.
   Retain its full commit ID as `BASE`. Do not choose a newer base merely to
   exclude earlier changes from the checks.
5. Compare the planned work with the recorded approval. Return changed scope
   to definition and authorization before executing it.

**Harness command:**

```text
harnessctl check REPO --artifact WO-ID --json
```

**Completion:** The executor has an explicit approved scope and the inputs
required by the selected procedure. Missing baseline or scope information
is reported before dependent work.

**Later use:** [Start the selected work](EXECUTE_WORK.md#start-the-selected-work), [Implement the approved scope](EXECUTE_WORK.md#implement-the-approved-scope), [Retain the implementation evidence](EXECUTE_WORK.md#retain-the-implementation-evidence), [Record implementation completion](EXECUTE_WORK.md#record-implementation-completion) use this scope, baseline, and verification plan.

### Start the selected work

**Inputs:** The approved work order (WO), actual executor identity, and
current execution context.

**Output:**

- **Formal artifacts:** The selected work order (WO) becomes `in_progress`
  with a lifecycle-history entry when start succeeds.
- **Transient working material:** Start-check and transition results.

**Actions:**

1. If the work order (WO) is already `in_progress`, inspect the recorded start
   and resume unapplied work. Do not replay the start transition.
2. Otherwise, run start preflight under the existing approval.
3. Preview the transition to `in_progress` using the actual executor identity.
4. Apply the same transition only when preflight and the preview pass.
5. Inspect the resulting state.

**Harness commands:**

```text
harnessctl preflight REPO --work-order WO-ID --phase start --json
harnessctl transition REPO --set WO-ID=in_progress --decision WO-ID=ACTOR --json
harnessctl transition REPO --set WO-ID=in_progress --decision WO-ID=ACTOR --apply --json
harnessctl check REPO --artifact WO-ID --json
```

**Completion:** The selected work order (WO) is `in_progress`, or its start
is blocked with an explicit reason. Existing approval covers a permitted
start; no duplicate human start decision is required.

**Later use:** [Implement the approved scope](EXECUTE_WORK.md#implement-the-approved-scope) performs the authorized implementation.

### Implement the approved scope

**Inputs:** The work order (WO) in `in_progress`, approved definitions,
permitted paths, and baseline from [Establish the execution context](EXECUTE_WORK.md#establish-the-execution-context).

**Output:**

- **Repository files:** The code, tests, documentation, or configuration
  changes authorized by the work order (WO).
- **Formal artifacts:** No lifecycle transition in this step. Artifact content
  changes require the authority and procedure applicable to those records.
- **Transient working material:** Implementation notes and unresolved findings.

**Actions:**

1. Inspect the files and behavior to be changed.
2. Compare the complete actual and planned path set with the approved scope.
3. Run the scope check below with every actual and planned path.
4. Make the changes allowed by the work order (WO).
5. Run local checks as needed to guide the implementation. Keep failures
   available for the evidence record.
6. Review the diff against the accepted definitions. Apply
   [Review of implemented changes](../ARTIFACT_AUTHORING.md#review-of-implemented-changes).
7. Resolve in-scope defects. Stop affected work when a finding requires changed
   requirements, paths, or authority.

**Harness commands:**

Repeat `--changed-path PATH` for the complete set, including planned new files:

```text
harnessctl check REPO --artifact WO-ID --checkpoint scope --changed-path PATH --changes-complete --json
```

This declaration is checked evidence, not independent proof of completeness.
When the selected procedure requires a `pre-action` check, use its returned
command with the complete change-set inputs. For Git-derived actual changes:

```text
harnessctl check REPO --artifact WO-ID --checkpoint pre-action --from-git BASE --json
```

Use the repository's editing, build, and test tools for implementation.
`harnessctl` does not implement the change.

**Completion:** The approved behavior is implemented within scope, or the
remaining work and blocker are explicit. No completion state is inferred yet.

**Later use:** [Retain the implementation evidence](EXECUTE_WORK.md#retain-the-implementation-evidence) checks the result and retains its evidence.

### Retain the implementation evidence

**Inputs:** The implemented changes, verification contracts (VER), required
repository checks, and work-order evidence locations.

**Output:**

- **Retained evidence files:** Actual check results, review findings, their
  resolution, and Git-derived handoff evidence at authorized evidence paths.
- **Formal artifacts:** Evidence references may be added where the work order
  (WO) requires them. No lifecycle state changes here.
- **Transient working material:** A summary of remaining evidence gaps.

**Actions:**

1. Run every required check using its specified inputs and environment.
2. Retain the command arguments, working directory, runtime identity, exit
   status, output, and relevant file paths or digests.
3. Preserve failed results alongside later corrections and successful reruns.
4. Retain the material diff-review findings and their resolution.
5. Confirm that all required evidence files exist at the locations named by
   the work order (WO) or verification contract (VER).
6. Run review preflight.
7. Run the Git-derived handoff check with the trusted `BASE` from [Establish the execution context](EXECUTE_WORK.md#establish-the-execution-context).
8. Inspect its written evidence and reported findings. Correct in-scope gaps
   and rerun affected checks.

**Harness commands:**

```text
harnessctl preflight REPO --work-order WO-ID --phase review --json
harnessctl check REPO --artifact WO-ID --checkpoint handoff --from-git BASE --json
```

For ordinary files listed in the work order’s `evidence_paths`, confirm that
each file exists inside the repository and contains the required evidence.
These files do not need a machine header. Use the supported evidence command
for generated packets; do not edit their evaluator-owned binding fields.

The Git-derived handoff command writes retained evidence. Confirm its output
paths are covered by the approved preparation scope. If the evaluator calls
for creating or rebinding the handoff evidence packet, use:

```text
harnessctl evidence REPO --artifact WO-ID --checkpoint handoff --json
```

This command also writes a file. It does not run tests or make an unsupported
claim true. Rerun the required handoff check after correcting the evidence gap.

**Completion:** Required implementation checks pass and the actual evidence
is retained, or the exact missing or failed checks remain visible.

**Later use:** [Record implementation completion](EXECUTE_WORK.md#record-implementation-completion) requires passing handoff results. Verification later
assesses these retained files; they are not disposable planning notes.

### Record implementation completion

**Inputs:** Completed work, passing handoff checks, retained evidence, and
the unchanged approved execution scope.

**Output:**

- **Formal artifacts:** The selected work order (WO) becomes `implemented`
  with the actual executor recorded in its lifecycle history.
- **Transient working material:** The completion report and current next step.

**Actions:**

1. Confirm that the work and required evidence are complete.
2. Preview the completion transition using the executor's own identity.
3. Apply the same transition when the preview passes.
4. Inspect the resulting work order (WO).
5. Report the completed behavior, checks, limitations, and evaluator's next
   action. Preserve failures if completion was refused.

Use the passing handoff result from the preceding step. A passing completion
preview does not replace the handoff check. If the implementation, governing
artifacts, or required evidence changed after handoff, rerun the affected
checks before applying completion. If `harnessctl` refuses the retained
handoff evidence, follow its reported corrective step.

**Harness commands:**

```text
harnessctl transition REPO --set WO-ID=implemented --decision WO-ID=ACTOR --json
harnessctl transition REPO --set WO-ID=implemented --decision WO-ID=ACTOR --apply --json
harnessctl check REPO --artifact WO-ID --json
```

**Completion:** The work order (WO) is `implemented`, or its completion is
blocked. Completion does not verify, release, or deliver the result.

**Later use:** Work requiring commit-bound verification proceeds to
“Verify the outcome.” An implemented work order (WO) classified `not_required`
needs no new verification record (VREC); follow its actual next action and
any separately authorized delivery instruction.

## Read next when

The evaluator selects verification preparation → [VERIFY_OUTCOME.md#prepare-the-verification-record](VERIFY_OUTCOME.md#prepare-the-verification-record). At handoff → [RESULTS.md#report-a-lifecycle-result](RESULTS.md#report-a-lifecycle-result).
