+++
id = "REL-SEH-010"
type = "release_contract"
title = "Release se-harness 0.6.0 through a predecessor-compatible successor"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-SEH-011"
version = "0.6.0"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"

[relations]
gates = ["WO-DST-019", "WO-DST-020", "WO-DST-021", "WO-IAR-012", "WO-WEX-001", "WO-WEX-002", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-RLS-008", "WO-REB-004", "WO-REB-005", "WO-REB-006"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-22T06:50:49Z"
decided_by = "release-owner"
+++

# Release Contract: Release se-harness 0.6.0 through a predecessor-compatible successor

## Lifecycle and prerequisites

On 2026-08-22, after successor candidate C4 `b099a2728d945ee705c1f956ec012f9730df15ac` completed exact local qualification and the separately authorized `REL-SEH-009` rejection produced a valid complete candidate graph, the accountable release owner explicitly directed this contract's `draft` to `approved` transition. `REL-SEH-009`, verified `VREC-SEH-010`, candidate C3, and reserved but uncreated `RLS-SEH-010` remain accurate immutable history; no historical artifact or candidate is repointed.

Approval defines the C4 release unit and successor policy. It does not commit this governance update, push, use credentials, dispatch hosted lanes, transition `WO-REB-006`, prepare or transition a VREC/RLS, tag, publish, deploy, mutate maintenance state, change external policy, or upgrade the root evaluator.

## Release unit

One future successor candidate C4 for version `0.6.0`, containing C3 ancestry plus only the approved `WO-REB-006` correction. The proposed release aggregate is thirteen work orders: the twelve exact work orders from `REL-SEH-009` plus `WO-REB-006`.

The future aggregate is `VREC-SEH-011`, with thirteen work orders, fourteen keyed evidence paths, and twelve verification contracts. `WO-REB-006` adds one keyed evidence path and `VER-REB-004` to the verified C3 cardinalities. The proposed release record is `RLS-SEH-011`. Reserved but uncreated `RLS-SEH-010` is never synthesized or repointed.

Historical maintenance `WO-HUP-001`, documentation `WO-RCA-001`, and governance-only `WO-VSP-006` retain their exclusions from release payload.

## Required evidence

- Complete `VER-REB-004` active-version, view, Git/path/object, isolation, TOCTOU, rollback, checkout, and full-release rehearsal evidence.
- Exact C4 commit/tree/epoch/archive, reproducible wheel/sdist/bundle/source/checksum identities, dual-runtime candidate acceptance, and hosted lanes.
- The prior twelve-work-order/thirteen-path/eleven-contract evidence replayed against C4, plus the new `WO-REB-006` path and contract.
- Exact released-0.5 interpreter, entry point, public wheel, schema-2 lock, compatibility-view command/output, omitted blob/raw hashes, canonical view evidence, bootstrap evidence, and full-graph candidate validation.
- Proof that C1/C2/C3 candidates, VRECs, RLS records, contracts, evidence, root evaluator, lock, and maintenance state are unchanged.

## Compatibility and migration

- Operational root remains schema 2 and released 0.5.0 through preparation and publication.
- Exact 0.5.0 generates `RLS-SEH-011` only inside the contract-derived compatibility view; reporting must not claim it parsed the full rejected-history graph.
- The repository adapter imports predecessor-owned output and canonical view evidence; the bounded binder independently attaches canonical evaluator evidence.
- Candidate validation assesses the complete graph and permits rejected history plus at most one active record for unpublished `0.6.0`.
- A later root adoption still requires independently published 0.6.0 and separate upgrade authority.

## Security and provenance

- Treat Git, sparse state, paths, repository bytes, metadata, JSON, hashes, locks, workflows, archives, and environments as untrusted.
- Require exact agreement among source governance commit, omitted history, old evaluator, contract, lock, candidate, VREC, work set, RLS, view/evaluator/distribution evidence, bundle, and hosted results.
- Stop before writes or credentials on any ambiguity, drift, noncanonical evidence, arbitrary omission, contaminated runtime, partial state, or rollback uncertainty.

## Promotion policy

1. Review and approve or revise `REQ-REB-011`, `REQ-REB-012`, `SPEC-REB-005`, `ARCH-REB-004`, `ADR-REB-004`, `VER-REB-004`, and `WO-REB-006`; keep this contract draft.
2. Start and implement only `WO-REB-006`; retain complete local evidence.
3. Separately authorize one clean C4 candidate commit and complete exact local qualification and reproducible builds.
4. Separately disposition `REL-SEH-009` without creating or modifying `RLS-SEH-010`, prove the resulting complete graph valid, and only then consider this contract for approval.
5. Separately authorize a dedicated candidate branch/credential use and pass hosted C4 lanes.
6. Separately prepare, review, and verify `VREC-SEH-011` with exactly thirteen work orders, fourteen keyed evidence paths, and twelve verification contracts.
7. Separately authorize contract-bound compatibility-view preparation of `RLS-SEH-011`, canonical view/evaluator/distribution binding, and complete-graph replay from default Windows and LF checkouts.
8. Have the release owner separately release or reject `RLS-SEH-011`.
9. Separately authorize tag, GitHub/PyPI publication, Pages deployment, maintenance reconciliation, and post-publication root adoption.

Automation prepares observations and proposals only. No step exercises accountable authority for a later step.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners decide their artifacts. Work start, candidate commit, contract disposition/approval, branch/credentials, VREC preparation/verification, RLS preparation/release, tag, publication, deployment, maintenance, external policy, and root adoption remain separate action-time decisions.

## Rollback criteria and procedure

Before publication, stop on incomplete authority, multiple active version claims, arbitrary or nonexact omission, historical drift, predecessor/output mismatch, view/evaluator evidence mismatch, candidate contamination, nondeterminism, hosted mismatch, unsafe archive, provenance disagreement, or any failed gate. Remove only exclusive new uncommitted outputs after digest verification; never rewrite historical facts. Correct through another reviewed candidate if trusted candidate state changes.

After publication, never move `v0.6.0` or replace immutable files. Preserve facts, block unsafe adoption, and prepare a separately governed corrective release.

## Post-release observation window

After separately authorized publication, verify immutable tag/assets, PyPI hashes/attestations, fresh Python 3.11 installation, default-Windows/LF evidence stability, candidate identity, init/adopt, doctor, validate, inspect, dashboard, rejected-history plus active-version behavior, preparation-view/evaluator provenance, mutation refusal, Pages provenance, maintenance state, and later root-upgrade readiness.
