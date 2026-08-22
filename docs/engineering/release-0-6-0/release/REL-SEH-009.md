+++
id = "REL-SEH-009"
type = "release_contract"
title = "Release se-harness 0.6.0 from an LF-stable successor candidate"
status = "rejected"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-22"
rejected_at = "2026-08-22T06:50:15Z"
rejected_by = "release-owner"
rejection_reason = "Candidate C3 cannot satisfy its declared predecessor release-preparation step; successor C4 preserves it as immutable history."

[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-SEH-010"
version = "0.6.0"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"

[relations]
gates = ["WO-DST-019", "WO-DST-020", "WO-DST-021", "WO-IAR-012", "WO-WEX-001", "WO-WEX-002", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-RLS-008", "WO-REB-004", "WO-REB-005"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T21:50:56Z"
decided_by = "release-owner"

[[lifecycle_events]]
from = "approved"
to = "rejected"
decided_at = "2026-08-22T06:50:15Z"
decided_by = "release-owner"
reason = "Candidate C3 cannot satisfy its declared predecessor release-preparation step; successor C4 preserves it as immutable history."
+++

# Release Contract: Release se-harness 0.6.0 from an LF-stable successor candidate

## Lifecycle and prerequisites

On 2026-08-22, after exact local qualification of successor candidate C4 `b099a2728d945ee705c1f956ec012f9730df15ac`, the accountable release owner explicitly directed the `approved` to `rejected` transition. Candidate C3 cannot satisfy this contract's declared predecessor release-preparation step against the retained rejected bootstrap history. Rejection preserves the contract, C3, verified `VREC-SEH-010`, and reserved but uncreated `RLS-SEH-010` as immutable history; none is repointed or overwritten.

This lifecycle decision does not approve the successor contract, commit governance updates, push, use credentials, dispatch hosted lanes, prepare or transition a VREC/RLS, tag, publish, deploy, mutate maintenance state, change external policy, or upgrade the root evaluator.

No historical candidate, VREC, RLS, evidence, or contract is repointed or overwritten.

## Release unit

One successor candidate C3 for version `0.6.0`, containing the C2 candidate ancestry, the newly integrated mainline work, and the `WO-REB-005` correction. The exact release aggregate is twelve work orders:

- `WO-DST-019`, `WO-DST-020`, `WO-DST-021`;
- `WO-IAR-012`;
- `WO-WEX-001`, `WO-WEX-002`;
- `WO-REB-001`, `WO-REB-002`, `WO-REB-003`, `WO-REB-004`, `WO-REB-005`; and
- `WO-RLS-008`.

Historical maintenance `WO-HUP-001`, documentation `WO-RCA-001`, and governance-only `WO-VSP-006` retain their original exclusion from the release-bearing aggregate. Their content and lifecycle facts remain in candidate ancestry without being reclassified as 0.6.0 release work.

The proposed aggregate is `VREC-SEH-010`, covering exactly those twelve work orders, thirteen keyed evidence paths, and eleven verification contracts: the seven C2 contracts; `VER-REB-003`; `VER-IAR-012`; and `VER-DST-021` plus `VER-IAR-013` for cross-domain `WO-DST-021`. The proposed release record is `RLS-SEH-010`, bound to the same C3 and verified aggregate.

## Required evidence

- Complete `VER-REB-003` checkout-matrix evidence with exact attribute resolution and hashes.
- Retained keyed evidence and independently verified facts from `VREC-IAR-008` for `WO-IAR-012` and `VREC-DST-018` for both evidence paths of `WO-DST-021`.
- Historical preservation of C2, `VREC-SEH-009`, `RLS-SEH-009`, and evaluator evidence.
- Exact C3 commit/tree/epoch/archive and candidate-source/package identities.
- Full Python 3.11 and current-runtime regression results.
- Two exact-export builds, byte-identical wheel and normalized sdist, safe equivalent payloads, valid RECORD, and byte-identical offline wheel reconstruction.
- Exact wheel, sdist, checksum, source manifest, bundle manifest, artifact snapshot, verifier contract, and dual-runtime acceptance hashes.
- Released-0.5 validation, candidate validation, bootstrap binding, graph, distribution, inspection, dashboard, doctor, parity, archive, recovery, diff, and secret/path results.
- Hosted candidate-source/package and released-evaluator lanes bound to C3 after separately authorized publication of a dedicated candidate branch.

## Compatibility and migration

- The operational root remains schema 2 and released 0.5.0 through preparation and publication.
- Exact released 0.5.0 prepares `RLS-SEH-010`; the bounded binder attaches canonical predecessor evidence.
- Versioned Git attributes preserve evaluator JSON LF bytes across supported checkouts.
- Ordinary schema-3 evidence validation remains unchanged.
- A later root adoption requires the independently published 0.6.0 wheel and separate approved upgrade authority.

## Security and provenance

- Treat attributes, Git configuration, repository bytes, paths, JSON, hashes, locks, workflows, archives, and environments as untrusted.
- Acquire and hash exact public 0.5.0 evaluator bytes before use or credentials.
- Keep candidate, package, and released evaluator identities independent.
- Require exact agreement among contract, lock, evaluator, candidate, aggregate, RLS, work set, evidence, archive, bundle, and hosted results.
- Preserve raw-byte evidence hashing and stop before writes or credentials on mismatch.

## Promotion policy

1. Review and approve or revise `REQ-REB-009`, `REQ-REB-010`, `SPEC-REB-004`, `ARCH-REB-003`, `ADR-REB-003`, `VER-REB-003`, and `WO-REB-005`; keep this contract draft.
2. Start and implement only `WO-REB-005`; retain complete local evidence.
3. Obtain separate authority for one clean C3 candidate commit and repeat complete local exact-candidate qualification and reproducible builds.
4. Through the C3 validator, separately reject `RLS-SEH-009` and `REL-SEH-008`, prove the terminal pair valid, and only then approve this contract.
5. Obtain separate credential/branch authority and pass hosted C3 lanes.
6. Separately prepare, review, and verify twelve-work-order `VREC-SEH-010`, with exactly thirteen keyed evidence paths and eleven verification contracts.
7. Separately authorize released-0.5 preparation and canonical binding of `RLS-SEH-010`; require both validators to pass from default Windows and LF checkouts.
8. Have the release owner separately transition or reject `RLS-SEH-010`.
9. Separately authorize tag, GitHub/PyPI publication, Pages deployment, maintenance reconciliation, and post-publication root adoption.

Automation prepares evidence and proposals only. No check creates an accountable decision.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners decide their respective draft artifacts. RLS/contract disposition, work start, candidate commit, branch/credentials, VREC preparation/verification, RLS preparation/release, tag, publication, deployment, maintenance, external policy, and root adoption each retain separate action-time authority.

## Rollback criteria and procedure

Before publication, stop on incomplete authority, attribute ambiguity, checkout hash drift, historical mutation, evaluator/lock drift, candidate contamination, evidence mismatch, nondeterminism, hosted mismatch, provenance disagreement, or any failed required gate. Correct through another reviewed candidate; never repoint or amend historical candidate/VREC/RLS facts.

After publication, never move `v0.6.0` or replace immutable files. Preserve facts, block unsafe adoption, and prepare a separately governed corrective release.

## Post-release observation window

After separately authorized publication, verify immutable tag/assets, PyPI hashes and attestations, fresh public Python 3.11 installation, default-Windows and LF checkout evidence stability, candidate identity, init/adopt, doctor, validate, inspect, dashboard, bootstrap history, mutation refusal, Pages provenance, maintenance state, and later root-upgrade readiness.
