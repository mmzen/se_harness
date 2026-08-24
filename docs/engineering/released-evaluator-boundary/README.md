# Released Evaluator Boundary Engineering Domain

> Repository-owned index. Formal artifact authority comes from TOML metadata, typed relations, and lifecycle state—not this directory or index.

This domain defines the preventive work authorized from [GitHub issue #81](https://github.com/mmzen/se_harness/issues/81) after the factual [0.5.0 release-governance RCA](../../rca/2026-08-20-0.5.0-release-governance-deadlock.md). It preserves the ordinary standard-repository lifecycle and makes the distinction between a released evaluator and candidate code enforceable before mutation and observable at release readiness.

## Approved governing packet

- Intent: `INT-REB-001`
- Capability: `CAP-REB-001`
- Requirements: `REQ-REB-001` through `REQ-REB-007`
- Specifications: `SPEC-REB-001`, `SPEC-REB-002`
- Architecture: `ARCH-REB-001`
- Accepted decision: `ADR-REB-001`
- Verification: `VER-REB-001`

## Governed work sequence

1. `WO-REB-001` aligns active publication and Pages workflows with the standard released-evaluator contract and establishes the standard lock identity needed by later enforcement.
2. `WO-REB-002` rejects non-matching runtimes before installed-root mutation and binds evaluator identity into release-readiness evidence.
3. `WO-REB-003` adds conflicting-chain observations, a bounded recovery runbook, and disposable recovery rehearsal.

The governing packet is `approved`; `WO-REB-001` and `WO-REB-002` are `implemented` with retained evidence, and their commit-bound assurance remains pending. `WO-REB-003` remains `draft`. No root-evaluator change, release, or external publication is authorized.

## Issue #101 preventive migration packet

The later approved `REQ-REB-016`, `REQ-REB-017`, `SPEC-REB-008`, `ARCH-REB-007`, `ADR-REB-007`, and `VER-REB-007` packet defines a complete predecessor-to-successor governance migration rehearsal. `WO-REB-018` is `in_progress` for its bounded implementation and local qualification. The packet adds evidence-only candidate behavior; it does not change the selected released root evaluator or absorb the lifecycle, production-view, or production-command work tracked separately by issues #103, #104, and #109.

## Issue #109 role-specific qualification packet

Approved `REQ-REB-020` through `REQ-REB-022`, `SPEC-REB-010`, `ARCH-REB-009`, `ADR-REB-009`, and `VER-REB-009` define five closed `harnessctl qualify` operations and one canonical evidence result. `WO-REB-020` is `in_progress` for their bounded implementation, workflow migration, documentation, testing, and retained evidence.

The status-preserving bootstrap amendment allows only immutable public 0.6.0's existing `accept-candidate` contract in the first independent package lane. Its legacy schema remains explicit and cannot be relabeled as typed qualification. The exception expires when a released verifier exposes `qualify candidate-package`. The root managed workflow and evaluator remain unchanged pending separate adoption authority.

## Issue #106 entry-point safety packet

Draft `REQ-REB-023` through `REQ-REB-026`, `SPEC-REB-011`, `ARCH-REB-010`, `ADR-REB-010`, and `VER-REB-010` define one declared interpreter-safety rule for every evaluator-identity boundary. `WO-REB-021` proposes its bounded implementation. Nothing in this packet is approved, and it grants no authority while draft.

The packet answers RCA `RC-060-06`: a real POSIX virtual environment must be accepted through its lexical `bin/python` entry point, while linked parents, Windows junctions, checkout targets, unsafe aliases, non-terminal links, and escape attempts stay refused. Six boundaries in two runtimes currently decide this independently and disagree, so the correction places the rule in one declared document with one loader per runtime rather than patching the one site that fails on POSIX. The canonical evaluator-evidence document, the runtime-identity schema identifier, existing bound digests, and root managed files are unchanged. The overlap with `WO-HBI-002` on `repository_tools/release_bootstrap.py` is disclosed in the work order for owner sequencing.
