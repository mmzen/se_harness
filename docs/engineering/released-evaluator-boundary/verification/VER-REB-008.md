+++
id = "VER-REB-008"
type = "verification"
title = "Lifecycle source-of-truth and rejected-history assurance"
status = "approved"
owners = ["quality-owner", "security-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
verifies = ["REQ-REB-018", "REQ-REB-019"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T10:01:59Z"
decided_by = "quality-owner"
+++

# Verification Contract: Lifecycle source-of-truth and rejected-history assurance

## Independence

Verification reads the canonical contract independently, enumerates every family/state/property, and compares each consumer's observable result rather than trusting exported constants or implementation success flags. Test fixtures include generated valid matrices and one-field mutations. Historical 0.6 records are read-only inputs and their bytes are compared before and after.

The implementation actor may write the contract loader and consumers, but cannot select only favorable states, redefine authority in tests, omit predecessor-boundary cases, or replace exact rejected history with a synthetic success-only graph.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| `REQ-REB-018` | Contract schema and parity | Source, managed template, installed fixture, sdist, wheel | Contract bytes and lifecycle matrix agree exactly; package contains v3 |
| `REQ-REB-018` | Strict parser properties | Missing/extra family, state, field; duplicate key/target; wrong type; unknown target; inconsistent transitionability; illegal reservation; oversized/non-UTF-8 input | Every invalid contract fails before a usable index or write |
| `REQ-REB-018` | Transition conformance | Every declared edge and every undeclared family-state pair | Planner accepts exactly declared edges and rejects all others |
| `REQ-REB-018` | Validator conformance | Every admitted state per family plus unknown/cross-family states | Validator admits exactly registry states and reports deterministic type-specific failures |
| `REQ-REB-018` | Authority/version consumers | Package transition, release preparation, complete validator, dashboard/inspection derived state | Consumers agree with registry flags and contain no policy-bearing fallback set |
| `REQ-REB-019` | Rejected VREC/RLS validity | Canonical rejection; missing/mismatched timestamp, actor, reason, event | Only complete attributed terminal rejection passes |
| `REQ-REB-019` | Same-version succession | rejected+ready, rejected+released, rejected+rejected, ready+ready, ready+released, released+released | Rejected records never reserve; every pair containing two reserving records fails |
| `REQ-REB-019` | Non-authority and immutability | rejected assurance/release selection, outgoing transition, byte mutation, omission, reopen | Every attempt fails; rejected bytes and visibility remain unchanged |
| Both | Predecessor boundary | Exact 0.5 full graph and declared compatibility assessment; current complete graph | Incompatibility remains explicit; no root/candidate hybrid; successor complete graph passes |

## Required automated tests

1. Validate the exact workflow v3 lifecycle matrix and recompute the transition, authority, reservation, transitionability, visibility, and predecessor-adapter indexes independently.
2. Prove packaged and managed-template contracts are byte-identical before and after wheel/sdist installation.
3. Exercise every declared transition and the Cartesian complement of undeclared transitions for all four families.
4. Feed every family/state to the standalone validator and prove no separately maintained VREC/RLS status vocabulary remains.
5. Run a property matrix for active-version uniqueness and `prepare-release` using any future state rows marked `reserves_version`, not state names embedded in the test oracle.
6. Validate canonical and malformed rejected VREC/RLS metadata and latest lifecycle events.
7. Prove rejected records cannot cover work, satisfy release readiness, authorize external action, transition, or disappear from graph/dashboard resources.
8. Re-run the immutable `RLS-SEH-009` plus `RLS-SEH-012` regression and the issue #101 historical/synthetic migration rehearsals.
9. Prove root managed files, root lock/configuration, historical VREC/RLS/REL bytes, release tag/distribution identities, Git refs, credentials, and external services are unchanged.

10. Exercise all seven approved terminal compatibility rows. Prove they remain
    visible, add no planner edge or version reservation, preserve their exact
    authority flags, and allow the existing superseded requirements and ready
    definition fixture to validate without a fallback vocabulary.

## Required repository qualification

- Focused lifecycle-contract, workflow, provenance, validation, dashboard, and migration tests.
- Full `python -m unittest discover -s tests -p "test_*.py"` on supported Python.
- Candidate complete-graph validation, release-distribution validation, portable-surface check, CLI help, candidate-source/package qualification, managed-template parity, and diff/whitespace checks.
- Exact released 0.5 `doctor` and explicit predecessor assessment, labeled as predecessor results rather than candidate validation.
- Windows and Linux hosted candidate lanes because contract bytes, JSON ordering, and standalone path resolution must remain platform-stable.

## Security and resilience cases

Exercise duplicate JSON keys, control characters, deep/large objects, path substitution, contract swap after load, symlink/junction paths, editable/current-directory import contamination, and partial managed-template upgrade. Failure must precede artifact mutation and retain bounded diagnostics without repository body or credential content.

## Evidence retention

Retain under `WO-REB-019`: exact contract bytes/hash and independently decoded matrix; source/template/package parity; per-consumer matrix results; hostile-input results; rejected-history before/after hashes; `RLS-SEH-009`/`RLS-SEH-012` regression; predecessor/current validation distinction; focused/full/package/platform commands and outputs; changed-path inventory; and explicit non-actions.

## Residual uncertainty

The table can prevent consumer drift only for semantics represented in its schema. A future new authority dimension requires a new contract version and governed migration. Compatibility-view construction and operational root adoption remain separately governed.
