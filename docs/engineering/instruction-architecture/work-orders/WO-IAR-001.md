+++
id = "WO-IAR-001"
type = "work_order"
title = "Rationalize and enforce the instruction architecture"
status = "implemented"
owners = ["repository-owner", "engineering-owner", "quality-owner"]
created = "2026-08-11"
updated = "2026-08-11"

[relations]
implements = ["REQ-IAR-001", "REQ-IAR-002", "REQ-IAR-003", "REQ-IAR-004", "REQ-IAR-005", "REQ-IAR-006", "REQ-IAR-007", "REQ-IAR-008", "REQ-IAR-009"]
specifications = ["SPEC-IAR-001"]
architecture = ["ARCH-IAR-001", "ADR-IAR-001"]
verification = ["VER-IAR-001"]
+++

# Work Order: Rationalize and enforce the instruction architecture

## Objective

Replace redundant harness navigation with one managed router, preserve repository-owned agent instructions and context, add deterministic implementation preflight, and strengthen required CI with an independent exact harness pin.

## Authorization

The repository owner approved this packet and authorized implementation on 2026-08-11 with the instruction `i approve, you can implement`. Commit, verification capture, governance commit, push, and pull-request creation were separately authorized in the immediately preceding instruction.

## In scope

- Update canonical `AGENTS.md`, `CLAUDE.md`, `ENGINEERING_HARNESS.md`, engineering README, context, workflow, decision-rights, quality-gates, and traceability templates as required by the specification.
- Add ownership-mode declarations and safe managed-to-seed migration behavior.
- Add read-only `harnessctl preflight` text and JSON interfaces using shared integrity and artifact parsing.
- Add a structured pull-request work-order declaration and independently pinned GitHub required-check template.
- Reconcile self-hosted root files and lock entries through the supported upgrade path.
- Add deterministic focused tests, acceptance coverage, documentation, and retained evidence.

## Out of scope

Adding installation profiles; implementing agent adapters beyond AGENTS and Claude; interpreting arbitrary natural-language instruction conflicts; automatically configuring GitHub branch protection or CODEOWNERS approval; executing repository context commands; changing existing formal artifact authority; committing; pushing; opening or merging a pull request; transitioning verification or release records; tagging; publishing; or deploying.

## Authorized decision envelope

Implementation may choose stable diagnostic-code names, internal helper boundaries, JSON field ordering, and concise template wording consistent with the requirements. It may not introduce a second harness route, make owner context content-managed, weaken fail-closed conflicts, use candidate scripts as the sole required check, or infer an accountable decision.

## Expected change surface

Canonical standard templates; installer and integrity mode handling; CLI and shared preflight logic; GitHub workflow and pull-request template; self-hosted operational files and lock; focused installer, CLI, security, distribution, and self-hosting tests; public and engineering documentation; work-order-keyed evidence.

## Implementation sequence

1. Approve the intent-to-verification chain, ADR, and this bounded work order.
2. Implement canonical templates and ownership-mode migration with focused tests.
3. Implement preflight and deterministic output with negative security tests.
4. Implement independent CI, the self-hosting bootstrap lanes, and structured work-order selection.
5. Apply the supported self-upgrade and reconcile lock parity.
6. Run `VER-IAR-001`, inspect the full diff, and retain exact evidence.
7. Stop for separate commit and verification-capture authority.

## Required verification

Perform every check in `VER-IAR-001`, validate the formal graph before and after implementation, exercise all migration states, run the full unit suite and CLI help, verify managed integrity and dashboard generation, inspect canonical/root parity, and retain exact results and residual risks.

## Stop and escalate conditions

Stop if owner content would be overwritten, a mode transition is ambiguous, baseline and candidate assurance cannot be distinguished honestly, the work-order declaration can reach a shell, self-hosting parity requires a hand-edited digest, a test fails, the artifact chain materially conflicts, or completion requires authority listed as out of scope.

## Completion evidence

Exact commands, results, migration cases, independent-baseline observations, deviations, and residual risks are retained in `docs/engineering/instruction-architecture/evidence/WO-IAR-001-verification.md`.

## Implementation result

The canonical and self-hosted instruction route now converges through one managed router; the engineering index and repository context are explicit owner seeds; upgrades handle managed-to-seed transitions transactionally; preflight provides deterministic start/review manifests; pull-request selection is strict; and CI distinguishes the exact released baseline from candidate verification.
