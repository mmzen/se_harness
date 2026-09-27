# Record a selected state change

## Read this when

The evaluator or explicit human decision selects a separate definition or work-order state change.

## Before this action

Read [AUTHORITY.md#decision-rights](AUTHORITY.md#decision-rights) and [AUTHORITY.md#delegation-and-separation](AUTHORITY.md#delegation-and-separation) before applying a decision. Read the exact artifacts and matching evidence; linked records do not change automatically.

## Procedure

### Complete a selected definition

**Inputs:** An approved definition, its completion evidence, and the exact
decision from the human authorized for that definition.

**Output:**

- **Formal artifact:** The selected definition becomes `implemented` with a
  lifecycle-history entry if the permitted transition succeeds.
- **Transient working material:** The preview, apply result, and readback.

**Actions:**

1. Read the selected definition and its current state.
2. Confirm that its content and evidence match the human's completion decision.
3. If completion is already recorded, report that state; do not replay it.
4. Preview the exact transition below.
5. Inspect every target, actor, gate result, and reported effect.
6. Apply the same transition only when it matches the decision and passes.
7. Read the artifact and new history entry. Preserve any refusal.

**Harness commands:**

```text
harnessctl transition REPO --set DEFINITION-ID=implemented --decision DEFINITION-ID=HUMAN --json
harnessctl transition REPO --set DEFINITION-ID=implemented --decision DEFINITION-ID=HUMAN --apply --json
```

The selected release does not accept definition IDs in `check`. The transition
preview supplies the legality and gate result. Do not change a definition's
state by hand to make it selectable.

**Completion:** Completion is recorded on that definition, or the exact
refusal is known. Linked work orders keep their states.

**Later use:** Select a related work order by its actual ID and use its current
`check` result. A completed definition does not select or start all linked work.

### Record work-order verification or release

**Inputs:** The explicitly selected work order, its current state, exact
human decision, and eligible verification or release coverage.

**Output:**

- **Formal artifact:** Only the selected work order receives the requested
  state and lifecycle-history entry if the transition succeeds.
- **Transient working material:** Coverage references and evaluator results.

**Actions:**

1. Inspect the work order with `check`.
2. Confirm the human selected a work-order transition, rather than only a
   decision on a related verification or release record.
3. Choose `verified` or `released` only as specified by that decision.
4. Inspect the supporting verification or release records. Do not infer their
   eligibility from a shared branch, commit message, or dashboard.
5. Preview the exact transition. The evaluator determines the permitted edge
   and coverage requirements.
6. Apply the same transition only if it matches the decision and passes.
7. Inspect the work order again.

**Harness commands:**

```text
harnessctl check REPO --artifact WO-ID --json
harnessctl transition REPO --set WO-ID=TARGET --decision WO-ID=HUMAN --json
harnessctl transition REPO --set WO-ID=TARGET --decision WO-ID=HUMAN --apply --json
harnessctl check REPO --artifact WO-ID --json
```

Here `TARGET` is the selected `verified` or `released` state. A work order's
verification requires eligible verification-record coverage. Its release
requires coverage by a released release record. These commands do not make
those supporting decisions or perform an external action.

**Completion:** The explicitly requested work-order state is recorded, or its
refusal is reported. Related records remain unchanged.

**Later use:** Follow the returned next action. Do not infer a work-order
transition merely because a VREC was verified or an RLS was released.

## Read next when

Obtain current context for supported records → [CONTINUE.md#procedure](CONTINUE.md#procedure). Report actual state → [RESULTS.md#report-a-lifecycle-result](RESULTS.md#report-a-lifecycle-result).
