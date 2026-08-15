+++
id = "WO-IAR-009"
type = "work_order"
title = "Add bounded suggestions to repository inspection"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-IAR-017"]
specifications = ["SPEC-IAR-009"]
architecture = ["ARCH-IAR-009", "ADR-IAR-009"]
verification = ["VER-IAR-009"]
+++

# Work Order: Add bounded suggestions to repository inspection

## Lifecycle and authorization

The repository owner approved `REQ-IAR-017`, `SPEC-IAR-009`, `ARCH-IAR-009`, `ADR-IAR-009`, `VER-IAR-009`, this bounded work order, and the specified IAR-008 clarification on 2026-08-15 with the instruction `ok i approve`. The bounded implementation and retained evidence are complete, so the work order is now `implemented`. Evidence is retained at `docs/engineering/instruction-architecture/evidence/WO-IAR-009-verification.md`. This state records completed work, not independent verification, and does not authorize a commit, prepare or approve a verification record, push, open a pull request, release, publish, or deploy.

## Objective

Extend the first repository inspection command with small, deterministic, non-executable suggestions that help operators find the correct accountable next step without creating new rule or lifecycle authority.

## In scope

- Explicitly narrow the conflicting recommendation exclusions in `REQ-IAR-016` and `SPEC-IAR-008`, recording the IAR-009 authorization without weakening their remaining boundaries.
- Add the closed queue and derived-warning catalog from `SPEC-IAR-009` to the root and canonical inspection scripts.
- Add structured `suggestions` to `se-harness-inspection-v1` and a compact human `Suggested next steps` section.
- Preserve all IAR-008 validation, summary, queue, finding, authority, exit, determinism, and no-write behavior.
- Add catalog-completeness, safe-omission, hostile-input, non-execution, compatibility, parity, package, and regression tests.
- Update only concise operator documentation necessary to explain what suggestions mean and do not mean.
- Synchronize canonical templates and schema-2 lock metadata through the supported managed transaction.
- Retain separate work-order-keyed evidence for IAR-009 and prepare for one later aggregate VREC covering both work orders.

## Out of scope

New validator or Explorer findings; validator-diagnostic suggestions; informational-finding suggestions; free-form or AI-generated advice; plugin or network calls; repository-configurable guidance; executable commands; interactive remediation; automatic fixes or transitions; scores; deadlines; aging policy; dashboard UI changes; evaluator-independence changes; governor reconciliation; version changes; release, tagging, publication, or deployment.

## Authorized decision envelope

If approved, implementation may choose internal catalog data structures, helper names, stable sort helpers, and compact human grouping. It may not add a trigger, action class, role, or guidance meaning outside `SPEC-IAR-009`; derive advice from repository text; emit a command or target status; mutate source observations; or expand evaluator authority.

## Expected change surface

- `REQ-IAR-016` and `SPEC-IAR-008` for the explicit bounded amendment, plus focused artifact tests.
- Root and canonical `scripts/inspect_engineering_artifacts.py`.
- Focused inspection, CLI, installer, integrity, package-data, instruction-architecture, and documentation tests.
- `docs/notes/harnessctl-reference.md` for concise operator semantics; README only if its short command description would otherwise become misleading.
- `.engineering-harness.lock`, this domain index, and `WO-IAR-009` evidence.

## Implementation plan

1. Obtain accountable approval of `REQ-IAR-017`, `SPEC-IAR-009`, `ARCH-IAR-009`, `ADR-IAR-009`, `VER-IAR-009`, and this work order.
2. Amend the two IAR-008 clauses, record the approval, transition IAR-009 work to `in_progress`, and run start preflight.
3. Capture the IAR-008 human and JSON report as the compatibility baseline.
4. Add failing tests for the complete catalog, unsupported sources, source isolation, deterministic output, grouping, non-execution, and no writes.
5. Implement the closed catalog and suggestion projection in root and canonical scripts.
6. Update concise command documentation and apply the supported managed upgrade with parity and idempotence proof.
7. Execute `VER-IAR-008` and `VER-IAR-009`, retain separate evidence for both work orders, mark completed implementation artifacts, and stop for candidate-commit authority.
8. After one clean candidate commit, prepare one aggregate VREC listing both work orders, both verification contracts, and both evidence documents.

## Stop and escalate conditions

Stop if implementation requires interpreting repository prose, adding or changing a finding, suggesting a validator remediation, adding a command or target lifecycle state, writing repository state, changing another command's semantics, weakening the IAR-008 authority boundary, redesigning evaluator independence, or exceeding this work order.
