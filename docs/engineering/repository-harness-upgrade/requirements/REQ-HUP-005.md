+++
id = "REQ-HUP-005"
type = "requirement"
title = "Apply the exact schema-3 standard-root transaction"
status = "approved"
owners = ["engineering-owner", "repository-owner"]
created = "2026-08-23"
updated = "2026-08-23"
statement = "WHEN an accountable owner authorizes WO-HUP-002, THE SYSTEM SHALL atomically apply only the reviewed 0.6.0 managed-root plan, advance the lock from schema 2 to schema 3 with the exact evaluator identity, retain keyed transition evidence, and fail without partial mutation on any predecessor or plan mismatch."
verification_method = "automated-test"

[relations]
derives_from = ["CAP-HUP-002"]
+++

# Requirement: Apply the exact schema-3 standard-root transaction

## Rationale

The governor is selected jointly by the runtime, managed configuration and policy, evaluator workflow, and integrity lock. A hand-edited or partially applied change would create split authority and lose the target archive proof.

## Preconditions and trigger

- `WO-HUP-002` is approved or in progress and its exact `[evaluator_upgrade]` packet matches the current lock and target runtime.
- Released 0.6.0 identity passes `REQ-HUP-004`.
- Read-only upgrade planning reports exactly the approved managed additions and updates.

## Required response

- Apply only through the exact external public 0.6.0 evaluator with `--work-order WO-HUP-002` and work-order-keyed JSON evidence output.
- Recheck prior lock SHA-256, target payload/archive identity, and managed predecessor safety immediately before writing.
- Apply all managed changes, schema-3 lock regeneration, and evaluator evidence as one recoverable transaction.
- Prove the post-apply plan is a no-op and every managed hash matches the resulting lock.

## Exact reviewed managed plan

Updates: `.engineering-harness.toml`, `.github/workflows/engineering-harness.yml`, the managed marker blocks in `AGENTS.md` and `CLAUDE.md`, `ENGINEERING_HARNESS.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `TRACEABILITY.md`, `WORKFLOW.md`, three formal templates, and four managed validation/inspection/dashboard files.

Adds: `docs/engineering/QUALITY_GATES.json` and `docs/engineering/WORKFLOW.json`.

The read-only plan reports 36 managed paths in total: 18 additions or updates and 18 unchanged. Installer-owned lock reconciliation and `WO-HUP-002-evaluator-upgrade.json` are additional transactional outputs.

## Failure and boundary behavior

Wrong prior lock, wrong target identity, customized or ambiguous managed content, changed plan membership, unsafe path, symlink, concurrent change, evidence collision, write failure, or failed postcondition restores the pre-write snapshot or stops without partial state. Retrying with broader scope or hand-editing the result is prohibited.

## Acceptance examples

### Example: exact transition

**Given** the approved work order, matching prior lock, exact target evaluator, and unchanged reviewed plan

**When** apply runs

**Then** the managed root and schema-3 lock converge on 0.6.0, keyed evidence is retained, and replay is a no-op.

### Example: plan expansion

**Given** any additional managed path becomes add, update, customized, or conflict

**When** apply is considered

**Then** implementation stops for an amended work order and renewed approval.

## Open decisions

The accountable owner accepted the complete 18-change plan and schema-3 identity transition on 2026-08-23. Any immediate plan difference requires an amendment and renewed approval.
