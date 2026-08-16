+++
id = "VER-OCA-002"
type = "verification"
title = "Verify operating assurance readiness enforcement"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-OCA-002"]
+++

# Verification Contract: Verify operating assurance readiness enforcement

## Independence

Controlled fixtures derive their expected target type, active-state sets, completed-work states, and eligible-VREC states from `SPEC-OCA-002`, not by importing the implementation's new lookup entry or helper predicate. Current-repository migration checks enumerate the accepted DST and REV scopes explicitly.

## Requirement-to-evidence matrix

| Concern | Method | Pass condition |
| --- | --- | --- |
| typed assurance | OPS fixtures targeting REQ, REL, SPEC, and unknown ID | REQ passes; known wrong types emit `E011`; unknown target retains the existing diagnostic |
| inactive requirement | draft, ready, rejected, and superseded requirement fixtures | each active OPS claim emits `E017` |
| completed implementation | absent, approved, in-progress, implemented, verified, and released WO fixtures | only completed/releasable work satisfies the path |
| optional provenance | policy-disabled fixtures | completed work passes without VREC coverage |
| configured provenance | policy-enabled VREC state matrix | only verified or released coverage of a selected completed WO satisfies the path |
| multiple paths | mixed implementing WOs | one eligible path passes; unrelated incomplete work is ignored |
| inactive OPS | draft and ready OPS fixtures | readiness checks do not claim assurance; type checking still applies |
| taxonomy | exact diagnostic assertions | `E011` is structure, `E017` governance, and `E018` policy |
| repository migration | exact relation and reachability audit | DST 001..006 and REV 001..008 pass; all eight approved OPS pass |
| distribution | parity, lock, fresh install, upgrade, and package tests | released template installs identical enforcement |
| regression | full supported Python test matrix | existing validation, provenance, dashboard, and command behavior pass |

## Manual assessment

Confirm that the two migrated relation sets match their original accepted operating prose and are not expanded to later requirements merely because those requirements share a domain prefix.

## Evidence retention

Retain before/after repository failures, exact migrations, focused case results, diagnostic planes, policy-on/off output, full tests, validation, doctor, preflight, parity, deterministic inspection, changed paths, deviations, and residual risk under `docs/engineering/operating-contract-activation/evidence/WO-OCA-002-verification.md`.

## Residual uncertainty

Reachability proves that at least one verified implementation path exists. It does not prove that the service owner currently follows the operating contract, that every later work order is verified, or that all requirements in a domain need an OPS claim.
