# Self-Hosting Boundary

This domain governs how `se_harness` develops itself without allowing an unreleased candidate to become its own sole governor.

## Formal chain

- Intent: `INT-SHB-001`
- Capability: `CAP-SHB-001`
- Requirements: `REQ-SHB-001` through `REQ-SHB-006`
- Specification: `SPEC-SHB-001`
- Architecture: `ARCH-SHB-001`
- Decision: `ADR-SHB-001`
- Verification: `VER-SHB-001`
- Work order: `WO-SHB-001`
- Release contract: `REL-SHB-001`
- Operations guide: `SELF_HOSTING.md`

Protected-upgrade and replayable-acceptance extension:

- Requirements: `REQ-SHB-007` through `REQ-SHB-009`
- Specification: `SPEC-SHB-002`
- Architecture: `ARCH-SHB-002`
- Decision: `ADR-SHB-002`
- Verification: `VER-SHB-002`
- Work order: `WO-SHB-002`
- Acceptance examples: `acceptance/self-hosting-upgrade-and-replay.feature`
- Implementation evidence: `evidence/WO-SHB-002-verification.md`

## Boundary summary

The released governor, target published release, candidate source, and installed candidate package are distinct identities with distinct roles. The governor operates only from an isolated released installation; target release migration and workflow material are verified data and are not executed during reconciliation; candidate source supplies implementation evidence; candidate packages are accepted only in fresh temporary repositories. A separately governed post-release change may use the published reconciler to promote a published candidate to become the next governor.

Normal `harnessctl upgrade` protects the implementation repository's `.engineering-harness.toml` and `.github/workflows/engineering-harness.yml`. The proposed `harnessctl reconcile-governor` is the separate plan-first mechanism for an authorized transition to an exact published target: it preserves field-owned repository policy, selects only role-correct self-hosting workflow material, requires explicit authority-bearing decisions, and changes the descriptor, controls, and lock through one recoverable transaction. The implementation delivered by this packet cannot reconcile or govern its own creation release.

Closed PR #28 and its branch retain the failed `VREC-SEH-003` and `RLS-SEH-003` attempt as immutable audit history. The clean recovery branch excludes those governance files, retains the valid 0.2.2 implementation lineage, and requires new aggregate verification and release record IDs before external promotion.

## Status

The accountable owner approved implementation with the instruction `go for implementation` on 2026-08-12. The bounded implementation is complete and `WO-SHB-001` is `implemented`. After the failed CI attempt, the owner approved `REL-SHB-001` as the clean 0.2.2 recovery contract. `VREC-SEH-004` is `verified` and `RLS-SEH-004` is `released`; both bind candidate commit `8ffb5e9386c3dc75b637092f93d372936ae7a290`, selected by tag `v0.2.2`.

The repository's public release and PyPI promotion were later completed under separate accountable actions. That external availability does not itself promote the independent self-hosting governor: `.self-hosting/governor.toml` still selects released version 0.2.1. Moving the governor pin to 0.2.2 remains a distinct governed change so candidate publication cannot silently make a candidate its own baseline.

On 2026-08-15, a read-only consistency audit confirmed that the prior normal upgrade planner would propose replacing both valid repository-specific controls with their consumer-template forms. The owner requested the Phase 1 packet after affirming the released-governor, candidate-evidence, source/package isolation, non-self-authorization, and replayable-functional-test principles, then clarified field-aware TOML migration and role-specific workflow replacement semantics. The owner approved `REQ-SHB-007..009`, `SPEC-SHB-002`, `ARCH-SHB-002`, `ADR-SHB-002`, and `VER-SHB-002` and explicitly authorized implementation under `WO-SHB-002` on the same date.

The correction is implemented and local source, package, migration, recovery, and Python 3.11 evidence is retained under `WO-SHB-002`. Normal root upgrade reports both repository-specific controls as `protected`. The work order is `implemented`, which records completed work rather than independent correctness. The authorized candidate commit permits the next exact commit-bound acceptance and hosted-CI steps; accountable assessment and any VREC remain separate. Do not run root reconciliation or `harnessctl upgrade . --apply` as a substitute for those pending decisions.
