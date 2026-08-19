+++
id = "VER-AGR-001"
type = "verification"
title = "Verify aggregate release provenance"
status = "approved"
owners = ["quality-owner", "security-owner"]
created = "2026-08-11"
updated = "2026-08-19"

[relations]
verifies = ["REQ-AGR-001", "REQ-AGR-002", "REQ-AGR-003", "REQ-AGR-004", "REQ-AGR-005", "REQ-AGR-006", "REQ-AGR-007", "REQ-AGR-008"]
+++

# Verification Contract: Verify aggregate release provenance

## Independence

Verification is derived from the normative artifact graph and public CLI behavior rather than implementation helper choices. Temporary repositories provide isolated Git and filesystem state. Expected relations, commits, lifecycle states, and side effects are asserted directly.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
|---|---|---|---|
| REQ-AGR-001 | CLI integration | two work orders, distinct contracts, flat-filename and directory-component evidence for each | one ready aggregate VREC contains the exact sorted sets at clean HEAD and both governed evidence layouts key exact work-order IDs |
| REQ-AGR-002 | CLI integration | aggregate VREC and contract gating all selected work | one ready RLS contains the exact verified work set |
| REQ-AGR-003 | validator and CLI tests | SHA-1, SHA-256, mixed commits and formats | matching candidates pass; every mismatch fails |
| REQ-AGR-004 | regression and property cases | repeated, single, duplicate, reordered, unknown, unsafe input | valid output is deterministic; invalid input is atomic and specific |
| REQ-AGR-005 | validator tests | missing, extra, ungated and lifecycle-incompatible relations | each inconsistency is blocking with affected IDs |
| REQ-AGR-006 | snapshot and visual review | one release linked to multiple work orders | JSON and Explorer expose all paths and label observed state as derived |
| REQ-AGR-007 | Git-state assertions and review | capture and prepare success/failure | HEAD, index, tags, lifecycle and remotes are unchanged |
| REQ-AGR-008 | init/adopt/upgrade and wheel tests | new, unmodified old, customized installations | standard template updates safely; existing records and customizations survive |

## Acceptance scenarios

The executable feature scenarios under `acceptance/aggregate-release.feature` are the minimum behavior contract.

## Property and invariant tests

- Input ordering does not change emitted relation ordering.
- Duplicate values never produce duplicate relations and are rejected before output.
- Released work equals the union of included verification coverage.
- Selected verification contracts equal the union declared by aggregate work orders.
- All candidate identities in one release are identical.
- Single-item input remains a valid aggregate of cardinality one.
- Flat filenames and components at or below a literal `evidence` directory produce the same exact aggregate key coverage under `SPEC-EVK-001`.

## Static and architecture checks

Run the artifact validator, inspect dependency direction, confirm source/canonical-template parity, and confirm no network or approval logic enters record preparation.

## Security and privacy checks

Exercise absolute, escaping, missing, directory, and symlink evidence paths; wrong artifact types; malicious-looking IDs and tags; dirty worktrees; absent HEAD; and existing destinations. No artifact body may execute.

## Performance and resilience checks

Exercise a bounded large work-order set and verify deterministic completion without network access. Interruptions or validation failures leave no partial output.

## Manual assessments

Review terminology distinguishing release payload from governance-only work. Inspect the Explorer for readable many-to-one lineage and a release-centric record identity.

## Evidence retention

Retain exact commands, test counts, requirement mapping, deviations, residual risks, and visual-review results in `docs/engineering/aggregate-release/evidence/WO-AGR-001-verification.md`.

## Residual uncertainty

Human owners remain responsible for selecting the correct release-bearing work. The harness can validate explicit consistency but cannot determine product scope automatically.
