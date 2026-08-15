+++
id = "WO-IAR-008"
type = "work_order"
title = "Implement the first repository inspection command"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
implements = ["REQ-IAR-016"]
specifications = ["SPEC-IAR-008"]
architecture = ["ARCH-IAR-008", "ADR-IAR-008"]
verification = ["VER-IAR-008"]
+++

# Work Order: Implement the first repository inspection command

## Lifecycle and authorization

The repository owner approved `REQ-IAR-016`, `SPEC-IAR-008`, `ARCH-IAR-008`, `ADR-IAR-008`, `VER-IAR-008`, and this bounded work order on 2026-08-15 with the instruction `go for implementation`. The bounded implementation and retained evidence are complete, so the work order is now `implemented`. Evidence is retained at `docs/engineering/instruction-architecture/evidence/WO-IAR-008-verification.md`. This state records completed work, not independent verification, and does not authorize commit, push, pull-request creation, VREC preparation or transition, release, tag, publication, or deployment.

## Objective

Add a small, deterministic, read-only `harnessctl inspect` command that makes existing validation, lifecycle, and Explorer observations practical in a terminal without introducing new rule authority.

## In scope

- Add `inspect [TARGET] [--json]` to source and installed CLI behavior.
- Add one managed standard inspection script that reuses the existing in-memory Explorer snapshot.
- Produce the `se-harness-inspection-v1` human and JSON reports defined by `SPEC-IAR-008`.
- Preserve validator diagnostics and Explorer findings exactly while adding mechanical lifecycle queues.
- Make derived authority and repository-local production explicit.
- Add deterministic, no-write, boundary, CLI, package, parity, and regression tests.
- Update concise operator documentation and the review workflow where it names inspection operations.
- Synchronize canonical templates and schema-2 lock metadata through the supported managed transaction.
- Retain work-order-keyed verification evidence.

## Out of scope

New validator or Explorer rules; new orphan semantics; aging or SLA thresholds; configurable inspection policy; health scores; automatic remediation; lifecycle transitions; interactive filtering; dashboard UI changes; evaluator-independence changes from issue #46; governor reconciliation; package version changes; release, tagging, publication, or deployment.

## Authorized decision envelope

If approved, implementation may choose internal data classes, helper names, concise human layout, and test-fixture organization. It may not add another queue condition, reinterpret severity or validity, change snapshot or existing command behavior, add writes, add a score, or expand evaluator authority.

## Expected change surface

- `se_harness/cli.py` and focused CLI tests.
- A new root and canonical `scripts/inspect_engineering_artifacts.py`.
- Existing snapshot API only where a minimal compatibility seam is needed; no finding-rule redesign.
- Canonical package-data and managed-integrity expectations.
- `docs/notes/harnessctl-reference.md`, managed `WORKFLOW.md` if required for the review command sequence, and concise root README command inventory only if the existing structure requires it.
- Focused inspection, validator, Explorer, installer, package, integrity, instruction-architecture, and documentation tests.
- `.engineering-harness.lock`, this domain index, and `WO-IAR-008` evidence.

## Implementation plan

1. Obtain accountable approval and run start preflight for `WO-IAR-008`.
2. Capture current CLI, validator, snapshot, finding, filesystem, and exit-code baselines.
3. Add failing tests for the command, queues, preserved findings, deterministic outputs, invalid-graph behavior, operational failures, no writes, and distribution parity.
4. Implement the repository-local inspection projection and CLI adapter.
5. Update concise operator and workflow documentation without duplicating rule catalogs.
6. Apply the supported managed upgrade and prove parity and idempotence.
7. Execute `VER-IAR-008` on Python 3.11 and the local runtime, retain evidence, and stop for separate candidate-commit authority.

## Stop and escalate conditions

Stop if implementation requires a new finding rule, ambiguous lifecycle inference, a validator or dashboard semantic change, a write operation, repository-specific configuration, evaluator-independence redesign, package version change, historical artifact rewrite, or authority beyond this work order.
