+++
id = "WO-VSP-006"
type = "work_order"
title = "Supersede three stale workflow-execution verification candidates"
status = "implemented"
owners = ["engineering-owner", "assurance-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[assurance]
commit_bound_verification = "not_required"
rationale = "This governance-only work records already authorized assurance dispositions and changes no executable behavior, managed policy, release scope, or external state."
decided_by = "assurance-owner"

[execution_scope]
paths = ["docs/engineering/workflow-execution/verification-records/VREC-WEX-001.md", "docs/engineering/workflow-execution/verification-records/VREC-WEX-002.md", "docs/engineering/workflow-execution/verification-records/VREC-WEX-003.md", "docs/engineering/verification-supersession/work-orders/WO-VSP-006.md", "docs/engineering/verification-supersession/evidence/WO-VSP-006-verification.md"]

[relations]
implements = ["REQ-VSP-001", "REQ-VSP-002", "REQ-VSP-003", "REQ-VSP-004", "REQ-VSP-005", "REQ-VSP-006", "REQ-VSP-007"]
specifications = ["SPEC-VSP-001"]
architecture = ["ARCH-VSP-001", "ADR-VSP-001"]
verification = ["VER-VSP-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T14:08:27Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "approved"
to = "in_progress"
decided_at = "2026-08-21T14:08:27Z"
decided_by = "engineering-owner"

[[lifecycle_events]]
from = "in_progress"
to = "implemented"
decided_at = "2026-08-21T14:16:08Z"
decided_by = "engineering-owner"
+++

# Work Order: Supersede three stale workflow-execution verification candidates

## Lifecycle

On 2026-08-21, after preliminary 0.6.0 inspection identified three stale ready WEX records, the accountable owner separately authorized the assurance owner to review and explicitly disposition `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003`. That instruction approves this governance-only work order and authorizes only the three named ready-to-superseded decisions after eligibility, coverage, provenance, and active-release checks pass.

The instruction does not authorize an operational candidate commit, aggregate VREC preparation or transition, RLS preparation or transition, tag, publication, deployment, root-evaluator upgrade, modification of `VREC-WEX-005`, or another lifecycle decision. This work is supersession bookkeeping explicitly excluded from the eight-work-order 0.6.0 release-bearing allow-list.

## Objective

Remove three obsolete WEX candidates from the active assurance queue by naming verified aggregate `VREC-WEX-005` as their one explicit coverage-preserving successor while retaining every captured historical fact.

## In scope

- Confirm all three sources are `ready` and verified `VREC-WEX-005` is eligible.
- Confirm the successor covers every source work order and applicable verification contract.
- Confirm no active release record references a source.
- Transition only `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003` from `ready` to `superseded`.
- Add the same UTC decision time, `supersession_authorized_by = "assurance-owner"`, and exactly one `superseded_by = ["VREC-WEX-005"]` relation to each source.
- Preserve each source commit, object format, worktree assertion, capture time, artifact snapshot, evidence paths, work-order relation, and verification-contract relation byte-for-byte.
- Retain exact decision and verification evidence under this work-order key.

## Out of scope

Changing the successor; changing or deleting captured candidates or evidence; modifying another VREC, RLS, release contract, product source, managed root, package version, or Git history; candidate commit, aggregate capture, assurance over `WO-RLS-008`, release action, tag, publication, deployment, or root upgrade.

## Authorized decision envelope

The assurance owner may select `VREC-WEX-005` only after the declared status, superset, contract, cycle, and active-release checks pass. The implementation agent may choose evidence wording and deterministic verification commands but may not select a different successor or infer another lifecycle decision.

## Constraints

Use the exact external released 0.5.0 evaluator for root validation and preflight. Candidate tooling may produce read-only plans but may not mutate the installed root. Preserve historical facts and add only the authorized append-only lifecycle edges.

## Expected change surface

- The three named WEX verification records.
- This work order.
- `docs/engineering/verification-supersession/evidence/WO-VSP-006-verification.md`.

## Required verification

Run released-evaluator start and review preflight, formal validation, doctor, source/successor coverage and status checks, active-release back-reference inspection, immutable-field comparison, focused supersession tests, complete available-runtime regression, inspection, deterministic Explorer generation, protected-path inspection, and `git diff --check`.

## Evidence to record

Retain original and final file hashes, immutable field comparisons, source and successor scope, transition time and authority, graph and inspection results, tests, deviations, and every unperformed action.

## Implementation result

The assurance owner explicitly superseded `VREC-WEX-001`, `VREC-WEX-002`, and `VREC-WEX-003` with verified aggregate `VREC-WEX-005` at `2026-08-21T14:10:10Z`. Formal validation confirms one eligible successor per source, preserved coverage, no cycles, no active-release references, and no remaining stale-ready decisions. Every captured source field and original verification relation remains unchanged; `VREC-WEX-005` remains unchanged and verified.

The complete Python 3.14.6 and Python 3.11.9 suites each pass 369 tests with five conditional skips, released-evaluator validation and inspection pass, and exact evidence is retained under this work-order key.

## Stop and escalate conditions

Stop if a source is not ready, the successor is not verified or released, coverage is incomplete, a cycle would form, an active release references a source, a captured fact changes, validation fails, or another record or authority is required.

## Completion report format

Report the three explicit edges, successor rationale, preserved provenance, exact verification, evidence path, lifecycle state, uncommitted status, and excluded actions.
