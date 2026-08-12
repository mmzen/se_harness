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

## Boundary summary

The released governor, candidate source, and installed candidate package are distinct identities with distinct targets. The governor operates only from an isolated released installation; candidate source supplies implementation evidence; candidate packages are accepted only in fresh temporary repositories. A separately governed post-release change promotes a published candidate to become the next governor.

Closed PR #28 and its branch retain the failed `VREC-SEH-003` and `RLS-SEH-003` attempt as immutable audit history. The clean recovery branch excludes those governance files, retains the valid 0.2.2 implementation lineage, and requires new aggregate verification and release record IDs before external promotion.

## Status

The accountable owner approved implementation with the instruction `go for implementation` on 2026-08-12. The bounded implementation is complete and `WO-SHB-001` is `implemented`. After the failed CI attempt, the owner approved `REL-SHB-001` as the clean 0.2.2 recovery contract. `VREC-SEH-004` is `verified` and `RLS-SEH-004` is `released`; both bind candidate commit `8ffb5e9386c3dc75b637092f93d372936ae7a290`, selected by tag `v0.2.2`.

The repository's public release and PyPI promotion were later completed under separate accountable actions. That external availability does not itself promote the independent self-hosting governor: `.self-hosting/governor.toml` still selects released version 0.2.1. Moving the governor pin to 0.2.2 remains a distinct governed change so candidate publication cannot silently make a candidate its own baseline.
