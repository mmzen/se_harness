+++
id = "VER-IAR-010"
type = "verification"
title = "Verify typed temporal reassessment semantics"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-IAR-018"]
+++

# Verification Contract: Verify typed temporal reassessment semantics

## Lifecycle

Approved on 2026-08-16 as the independent evidence contract for `REQ-IAR-018`.

## Independence

Tests derive expected eligibility from the explicit table and lifecycle rules in `SPEC-IAR-010`, not by importing the implementation's policy constants. Controlled artifacts and relations isolate each positive and negative boundary from the current repository's changing maintenance state.

## Requirement-to-evidence matrix

| Requirement concern | Method | Pass condition |
| --- | --- | --- |
| declared supported dependency | controlled positive cases | each applicable living definition emits one relation-specific `W-HEX-003` |
| active work | draft, approved, and in-progress fixtures | eligible older work emits the finding |
| completed work | implemented, verified, and released fixtures | no generic temporal finding is emitted |
| immutable records | ready/verified/released/superseded VREC and ready/released RLS fixtures | no generic temporal finding is emitted |
| inactive definitions | rejected and superseded fixtures | no generic temporal finding is emitted |
| authority and relation boundary | derived, `superseded_by`, and unknown-relation fixtures | no generic temporal finding is emitted |
| date boundary | missing, equal, older-target, and newer-target dates | only strict older-source comparisons emit |
| public contract | exact finding assertions | rule, authority, severity, artifacts, relation evidence, and message match the specification |
| suggestion compatibility | inspection projection tests | existing action and `automatic = false` remain unchanged |
| version and determinism | repeated generation and permuted input | rules version is v7 and JSON is byte-stable |
| distribution | parity, package-data, install, lock, and upgrade checks | root and canonical behavior remain synchronized |

## Current-repository assessment

The pre-change snapshot contains nineteen `W-HEX-003` findings: three living-architecture observations, thirteen completed-work observations, and three VREC observations. Under this contract, only the three declared living-architecture observations should remain. This count is retained as transaction evidence, not used as the sole unit-test oracle.

## Security and boundary checks

- Unknown artifact and relation values fail closed without executing repository content.
- Finding and suggestion generation remain read-only and invoke no command or transition.
- Formal validator outcomes and commit-bound provenance rules remain unchanged.

## Regression

Run focused dashboard and inspection tests, full Python tests on Python 3.11 and the local supported runtime, formal artifact validation, doctor, start/review preflight, deterministic dashboard/inspection generation, root/canonical parity, package-data checks, and `git diff --check`.

## Evidence retention

Retain commands, runtimes, test counts, before/after finding breakdowns, representative JSON, deterministic hashes, root/canonical and lock proof, changed paths, deviations, and residual risks under `docs/engineering/instruction-architecture/evidence/WO-IAR-010-verification.md`.

## Residual uncertainty

An eligible warning still requires accountable human judgment. Timestamp granularity cannot prove semantic impact, and excluded commit-bound provenance may warrant a future dedicated observation.
