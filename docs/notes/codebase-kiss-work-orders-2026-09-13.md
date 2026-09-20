# Codebase KISS work orders

> **Historical plan — 2026-09-13; status note added 2026-09-16.** The seven work
> orders below are implemented and have owner-verified records, linked in the
> [packet index](../engineering/harness-simplification/README.md). This repository
> subsequently adopted released 0.18.0 under [WO-HUP-019](../engineering/repository-harness-upgrade/work-orders/WO-HUP-019.md).
> The original planning text below is preserved; current contributor instructions
> are in [Developing SE Harness](developing-se-harness.md).

The owner accepted the complete codebase simplification review. Seven work orders cover all 38 candidates; seven useful protections remain.

1. WO-KIS-001: Remove everyday input and writing blockers.
2. WO-KIS-002: Let local work progress on its own evidence.
3. WO-KIS-003: Cut repeated identity proofs and locked guidance.
4. WO-KIS-004: Simplify verification and release records.
5. WO-KIS-005: Shorten CI and resume interrupted publication.
6. WO-KIS-006: Keep new evidence small and assess historical archives.
7. WO-KIS-007: Delete tests for the restrictions we removed.

The [packet index](../engineering/harness-simplification/README.md) links the exact scope, replacement rules, coverage and checks.
The current root stays on released 0.17.0. This packet prepares delegated implementation; it does not claim completed changes or new verification results.
Run the slices sequentially after the approved packet reaches main, using the currently governing evaluator at every lifecycle checkpoint.
