+++
id = "REL-SEH-011"
type = "release_contract"
title = "Release se-harness 0.6.0 through hosted predecessor assessment"
status = "draft"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-22"
updated = "2026-08-22"

[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-SEH-012"
version = "0.6.0"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"

[relations]
gates = ["WO-DST-019", "WO-DST-020", "WO-DST-021", "WO-IAR-012", "WO-WEX-001", "WO-WEX-002", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-RLS-008", "WO-REB-004", "WO-REB-005", "WO-REB-006", "WO-REB-007"]
+++

# Release Contract: Release se-harness 0.6.0 through hosted predecessor assessment

## Lifecycle and prerequisites

This draft grants no authority. C4 `b099a2728d945ee705c1f956ec012f9730df15ac`, governance commit `39fac46b009727529b6b65f5d8e63972155b0590`, branch `candidate/0.6.0-c4`, and hosted runs `32558379907`/`32558379908` remain accurate failed qualification history. C5 `5653cb52e729ad5d48683bc7e28ee3f0478e2e2c`, branch `candidate/0.6.0-c5`, successful candidate-evidence run `32562498151`, expected-red legacy run `32562498162`, and failed predecessor-assessment run `32562498180` are also immutable history. `REL-SEH-010` remains approved until separately dispositioned; reserved but uncreated `VREC-SEH-011` and `RLS-SEH-011` are never synthesized or repointed.

C5 implemented the initial `WO-REB-007` correction but the first real POSIX virtual-environment assessment exposed lexical interpreter-root handling that the Windows and mocked-path tests did not exercise. A future C6 must complete and qualify the same still-`in_progress` work order before the release owner may reject `REL-SEH-010` and consider this contract for approval. No prior candidate, contract, aggregate, release record, evidence, branch, or external fact is rewritten.

## Release unit

One future successor candidate C6 for version `0.6.0`, containing C5 ancestry plus only the bounded completion of approved `WO-REB-007`. The proposed release aggregate remains fourteen work orders: the thirteen exact work orders from `REL-SEH-010` plus `WO-REB-007`.

The future aggregate is `VREC-SEH-012`, with fourteen work orders, fifteen keyed evidence paths, and thirteen verification contracts. `WO-REB-007` adds one keyed evidence path and `VER-REB-005`. The proposed release record is `RLS-SEH-012`.

Historical maintenance `WO-HUP-001`, documentation `WO-RCA-001`, and governance-only `WO-VSP-006` retain their exclusions from the release payload.

## Required evidence

- Complete `VER-REB-005` exact-diagnostic, assessment-view, Git/path/object, runtime, canonical-evidence, cleanup, and workflow evidence.
- Immutable C4 failure evidence: Engineering Harness run `32558379907`, job `96996045728`; Candidate Evidence run `32558379908`, source job `96996045654`, skipped package job `96996119243`.
- Immutable C5 commit/tree/branch plus exact hosted run/job/log identities, including the green source/package jobs, exact expected legacy `E009`, and failed POSIX predecessor-assessment boundary.
- Exact C6 commit/tree/epoch/archive, reproducible wheel/sdist/bundle/source/checksum identities, dual-runtime candidate acceptance, and hosted run/job/artifact identities.
- The prior thirteen-work-order/fourteen-path/twelve-contract evidence replayed against C6, plus the same `WO-REB-007` path and `VER-REB-005`; no work-order, evidence-path, or verification-contract count is added for completing already-governed portability scope.
- Exact released-0.5 interpreter, entry point, wheel/payload, schema-2 lock, full-checkout `E009`, assessment-view commands/output, omitted blob/raw hashes, and complete candidate graph.
- Proof that C1-C5 candidates, VRECs, RLS records, contracts, rejected history/evidence, root managed files, maintenance state, and external policy remain unchanged.

## Compatibility and migration

- Operational root remains schema 2 and released 0.5.0 through preparation and publication.
- The unchanged legacy full-checkout workflow is expected to fail only with exact `E009`; it is retained as predecessor-boundary evidence and is never called passing.
- A new candidate-owned hosted lane runs exact released 0.5.0 against the contract-derived two-artifact assessment view and must pass identity, `doctor`, `validate`, and dashboard.
- Candidate validation assesses the complete graph before and after assessment.
- Exact 0.5.0 later prepares `RLS-SEH-012` only in the same derived view; view/evaluator/distribution binding remains separately authorized.
- Root adoption still requires independently published 0.6.0 and separate authority.

## Security and provenance

- Treat Git, paths, sparse state, workflow context, logs, artifacts, evaluator bytes, commands, JSON, hashes, locks, and environments as untrusted.
- Require exact agreement among C6, source governance, rejected history, evaluator, old lock, contract, work set, VREC, RLS, assessment/preparation/evaluator/distribution evidence, builds, and hosted observations.
- Exact expected-red matching accepts no other diagnostic and grants no authority.
- Stop before writes or credentials on ambiguity, contamination, drift, partial output, unsafe cleanup, or provenance disagreement.

## Promotion policy

1. Review and approve or revise `REQ-REB-013`, `REQ-REB-014`, `SPEC-REB-006`, `ARCH-REB-005`, `ADR-REB-005`, `VER-REB-005`, and `WO-REB-007`; keep this contract draft.
2. Start and implement only `WO-REB-007`; retain complete local evidence while `WO-REB-006` remains in progress.
3. Separately authorize one clean C6 candidate commit and complete exact local Windows/Python-3.11 qualification and reproducible builds.
4. Separately disposition `REL-SEH-010`, prove the complete graph valid, and only then consider this contract for approval.
5. Separately authorize a dedicated candidate branch/credential use. Require green candidate-source/package and predecessor-assessment jobs plus the exact expected legacy `E009`; no other hosted failure is acceptable.
6. Separately transition `WO-REB-006` and `WO-REB-007` only after complete local and hosted evidence.
7. Separately prepare, review, and verify `VREC-SEH-012` with exactly fourteen work orders, fifteen keyed evidence paths, and thirteen verification contracts.
8. Separately authorize compatibility-view preparation and canonical binding of `RLS-SEH-012`, then have the release owner release or reject it.
9. Separately authorize tag, GitHub/PyPI publication, Pages deployment, maintenance reconciliation, and post-publication root adoption.

Automation creates observations and proposals only. No expected or passing result exercises accountable authority.

## Human approval triggers

Requirements, technical, security, assurance, engineering, and release owners decide their artifacts. Work start, candidate commit, contract disposition/approval, branch/credentials, hosted expected-failure disposition, work-order completion, VREC preparation/verification, RLS preparation/release, tag, publication, deployment, maintenance, external policy, and root adoption remain separate action-time decisions.

## Rollback criteria and procedure

Before publication, stop on incomplete authority, unexpected legacy output, arbitrary omission, historical/root drift, evaluator mismatch, candidate contamination, nondeterminism, hosted mismatch, unsafe cleanup/archive, evidence disagreement, or any failed required replacement gate. Remove only exact temporary/uncommitted outputs after path/digest verification; never rewrite history. Correct through another governed candidate if trusted candidate state changes.

After publication, never move `v0.6.0` or replace immutable files. Preserve facts, block unsafe adoption, and prepare a separately governed corrective release.

## Post-release observation window

After separately authorized publication, verify immutable tag/assets, PyPI hashes/attestations, fresh Python 3.11 installation, Windows/LF evidence stability, candidate identity, init/adopt, doctor, validate, inspect, dashboard, rejected-history succession, assessment/preparation-view provenance, mutation refusal, Pages provenance, maintenance state, and later root-upgrade readiness.
