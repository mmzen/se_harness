# Draft work orders

## Read this when

Definitions, work scope and verification requirements are ready for work planning.

## Before this action

Read [WORK_AND_EVIDENCE.md#links-from-work-orders-wo](WORK_AND_EVIDENCE.md#links-from-work-orders-wo), [WORK_AND_EVIDENCE.md#complete-work-scope](WORK_AND_EVIDENCE.md#complete-work-scope) and [WORK_AND_EVIDENCE.md#assurance-classification](WORK_AND_EVIDENCE.md#assurance-classification). Apply [../ARTIFACT_AUTHORING.md#design-simplicity](../ARTIFACT_AUTHORING.md#design-simplicity) and [../ARTIFACT_AUTHORING.md#work_order](../ARTIFACT_AUTHORING.md#work_order).

## Procedure

### Prepare work orders (WO) linking the definitions, scope, planned work, and verification requirements

**Inputs:** The outcome, scope, artifact inventory, definition drafts,
amendment proposals, verification contracts (VER), risks (RISK), and
unresolved decisions (DEC).

**Output:**

- **Formal artifacts:** New or completed work orders (WO) in `draft`.
  Applicable risks (RISK) and open decisions (DEC) updated with the actual
  work order (WO) links. Lifecycle states and dispositions are preserved.
  Approved work orders (WO) remain unchanged; proposed scope changes require
  review.
- **Transient working material:** The review handoff and evaluator results.
  Retain these under the same conditions as [Describe the intended outcome](DEFINE_CHANGE.md#describe-the-intended-outcome).

**Actions:**

1. Divide the planned work into bounded units that can each be authorized and
   verified. Assign each unit its governing definitions and scope.
2. Select an existing work order (WO) in `draft` for a unit only if its scope
   matches. Otherwise, create a new work order (WO) with the commands below.
3. Complete each draft using the field table below.
4. Check that every selected requirement (REQ) has the specification (SPEC)
   and verification contract (VER) coverage defined in [Complete work scope](WORK_AND_EVIDENCE.md#complete-work-scope).
5. Apply `## work_order` → `### Checklist` in
   `docs/engineering/ARTIFACT_AUTHORING.md`.
6. Add the new work order (WO) IDs to applicable `threatens` relations in risks
   (RISK) and `concerns` or `blocks` relations in open decisions (DEC). Keep
   every blocked ID in `concerns`. Preserve any required pairing between the
   risk (RISK) and decision (DEC).
7. If the planned change needs a missing release or operating contract,
   use [Prepare a release or operating contract](DRAFT_DEFINITIONS.md#prepare-a-release-or-operating-contract) now that the work
   order IDs exist. Include its draft in the proposed package.
8. Run the validation command below.
9. Correct findings within the proposed drafts. Rerun validation after edits.
   Report unrelated findings separately. Retain findings that need a decision
   or an accepted-definition amendment as unresolved dependencies.
10. Run the selected-work check below for each proposed work order (WO).
11. Present the outcome, scope, artifact IDs and paths, validation results,
    unresolved decisions (DEC), and unapplied amendments. Include the
    evaluator's reported next action for each selected work order (WO).

| Field or section | Content |
| --- | --- |
| `Objective` | The outcome this work order (WO) will deliver. |
| `In scope` / `Out of scope` | The boundaries from [Define the limits of the change](DEFINE_CHANGE.md#define-the-limits-of-the-change) assigned to this work order (WO). |
| `Constraints` | The conditions from [Define the limits of the change](DEFINE_CHANGE.md#define-the-limits-of-the-change) that apply to this work. |
| `Expected change surface` | The planned changes by file or component. |
| `[execution_scope].paths` | Exact repository-relative files or component directories ending in `/`. Use forward slashes; no wildcards, absolute paths, or `..`. |
| `Authorized decision envelope` | What the implementer may decide and what requires another accountable decision. |
| `Required verification` / `Evidence to record` | The checks and retained outputs defined in [Define how the result will be verified](DRAFT_DEFINITIONS.md#define-how-the-result-will-be-verified). |
| `Stop and escalate conditions` | The conditions that require pausing this work. |
| `Completion report format` | The required report of completed behavior, checks, limitations, and next accountable decision. |
| `[assurance]` | `commit_bound_verification`, its `rationale`, and `decided_by`. Apply the classification rules in [Assurance classification](WORK_AND_EVIDENCE.md#assurance-classification). Record the human who confirmed the classification; an agent may propose it and record that human's decision. |
| `[relations]` | `implements` → requirements (REQ); `specifications` → specifications (SPEC); `verification` → verification contracts (VER); `architecture` → applicable architectures (ARCH) and required architecture decisions (ADR). |

If the assurance classification has not been confirmed, present it as a
proposal in the review handoff. Report the missing decision. Do not fill
`decided_by` with the draft author's name or an example identity to satisfy
validation. The human may confirm the classification while reviewing the
work order; record that decision before previewing approval.

**Harness commands:**

For each new work order (WO), run the creation sequence from [Draft any missing definitions](DRAFT_DEFINITIONS.md#draft-any-missing-definitions).
Inspect the preview before creation; replace `WO-ID` with its `allocated_id`:

```text
harnessctl create-artifact REPO --domain DOMAIN --type work_order --dry-run --json
harnessctl create-artifact REPO --domain DOMAIN --type work_order --id WO-ID --json
```

Validate the formal artifacts after completing the drafts and links:

```text
harnessctl validate REPO --json
```

Inspect each proposed work order (WO) using its actual ID:

```text
harnessctl check REPO --artifact WO-ID --json
```

Validation does not approve the change. The checkpoint-free `check` reports
lifecycle context without evaluating checkpoint gates.

**Completion:** Draft work orders (WO) are presented for review with their
governing artifacts and evaluator results. Every unresolved dependency is
identified. Preparation does not approve or start execution.

**Later use:** The authorization process reviews this artifact package,
resolves approval blockers, and applies permitted lifecycle transitions.
Only the formal artifacts carry lasting definitions and work authority;
transient working material is not persisted in the repository.

## Read next when

A proposed package is ready → [AUTHORIZE_WORK.md#procedure](AUTHORIZE_WORK.md#procedure).
