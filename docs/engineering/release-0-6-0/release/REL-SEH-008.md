+++
id = "REL-SEH-008"
type = "release_contract"
title = "Correct and release se-harness 0.6.0 from a successor candidate"
status = "approved"
owners = ["release-owner", "quality-owner", "security-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[bootstrap]
schema = "se-harness-release-bootstrap-v1"
release_record = "RLS-SEH-009"
version = "0.6.0"
from_lock_schema = 2
from_lock_tool_version = "0.5.0"
from_lock_sha256 = "08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3"
evaluator_version = "0.5.0"
evaluator_archive_name = "se_harness-0.5.0-py3-none-any.whl"
evaluator_archive_sha256 = "974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f"

[relations]
gates = ["WO-DST-019", "WO-DST-020", "WO-WEX-001", "WO-WEX-002", "WO-REB-001", "WO-REB-002", "WO-REB-003", "WO-RLS-008", "WO-REB-004"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "release-owner"
+++

# Release Contract: Correct and release se-harness 0.6.0 from a successor candidate

## Lifecycle and authority

This replacement contract was approved on 2026-08-21 after candidate C exposed a real schema-2-to-schema-3 release-readiness bootstrap defect. Its approval does not supersede, reject, amend, or transition `REL-SEH-007`, candidate C, `VREC-SEH-008`, or `RLS-SEH-008`.

Approval defines the C2 release unit and bootstrap policy and, together with `WO-REB-004`, authorizes only bounded local implementation and qualification. It does not authorize a candidate commit, branch movement, credential use, hosted dispatch, VREC/RLS preparation or transition, tag, publication, deployment, maintenance mutation, external policy change, or root-evaluator upgrade.

On 2026-08-21 at `2026-08-21T16:31:42Z`, the accountable owners authorized one bounded correction: `from_lock_sha256` binds canonical `utf8-text-lf-v1` lock bytes rather than a platform-smudged CRLF checkout. The contract remains approved and every other release-unit and authority boundary is unchanged.

## Release unit

One successor 0.6.0 candidate C2 containing the previously qualified eight-work-order payload plus the bounded `WO-REB-004` correction. The exact release-bearing set is nine work orders:

- `WO-DST-019`, `WO-DST-020`;
- `WO-WEX-001`, `WO-WEX-002`;
- `WO-REB-001`, `WO-REB-002`, `WO-REB-003`;
- `WO-RLS-008`; and
- `WO-REB-004`.

Candidate C `827b2709292abaa3458bb3b4cac37b582378c585`, verified `VREC-SEH-008`, and its reproducible artifacts remain immutable historical evidence but are ineligible for this release. The current uncommitted `RLS-SEH-008` remains a stopped diagnostic proposal and is never repointed.

The proposed aggregate is `VREC-SEH-009`; it must bind one clean full C2 commit to the exact nine-work-order set, the original six verification contracts, and new `VER-REB-002`. The proposed release record is `RLS-SEH-009` and must bind the same C2 and verified aggregate.

## Required evidence

- One repository-contained evidence path keyed to each of the nine work orders. `WO-REB-004` evidence must contain full integrated C2 requalification so historical `WO-RLS-008` evidence remains accurate for C rather than being rewritten.
- Exact candidate commit/tree/epoch/archive and candidate-source/package identity observations.
- Full Python 3.11 and current-runtime regression counts, conditional skips, failures, and deviations.
- Two exact-export builds at the C2 epoch, byte-identical wheel and normalized sdist, safe equivalent payloads, valid RECORD, and byte-identical offline wheel reconstruction.
- Exact wheel, sdist, checksums, source manifest, bundle manifest, artifact snapshot, verifier contract, and dual-runtime acceptance hashes.
- Complete `VER-REB-002` bootstrap evidence, released-0.5 validation, candidate validation, formal graph, release-distribution, inspection, dashboard, doctor, managed parity, lock, archive, recovery, diff, and secret/path results.
- Hosted candidate-source/package and standard released-evaluator lanes bound to C2 after separately authorized branch publication.

## Compatibility and migration

- The operational root remains schema 2 and released 0.5.0 through release preparation and publication.
- Exact released 0.5.0 prepares and validates `RLS-SEH-009` as ready.
- The approved bootstrap tuple binds canonical `utf8-text-lf-v1` current-lock SHA-256 `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3` and public wheel SHA-256 `974ba2de5f43bb7fa5987f7e6dde7f2b4d6c4c1d76011ff4abdc142957dd812f`.
- The repository binder attaches canonical predecessor evidence without changing the root, candidate, work coverage, VREC coverage, or lifecycle state.
- Candidate validation and publication accept only the complete exact tuple; every other ready RLS retains schema-3 current-lock enforcement.
- Installing 0.6.0 never upgrades an existing repository automatically. Later root adoption requires the exact independently published 0.6.0 wheel and a separate approved evaluator-upgrade work order.

## Security and provenance

- Treat contract/RLS text, Git, paths, lock, workflows, events, evidence, archives, environments, and external bytes as untrusted.
- Acquire and hash public 0.5.0 wheel bytes before external installation and before any credential-bearing work.
- Prove released evaluator, candidate source, and candidate package independently with checkout exclusion.
- Require canonical evidence and exact contract, lock, RLS, version, candidate, aggregate, work-set, archive, and bundle agreement.
- Candidate code can bind or validate an observation but cannot prepare the RLS as evaluator, change the root, transition lifecycle, or supply expected identity from its own claims.
- Preserve every historical VREC/RLS, tag, evidence, and published-file fact byte-for-byte.

## Promotion policy

1. Approve the complete `REQ-REB-008`/`SPEC-REB-003`/`ARCH-REB-002`/`ADR-REB-002`/`VER-REB-002`/`WO-REB-004` packet and this contract.
2. Implement only `WO-REB-004`; retain evidence and pass review preflight under released 0.5.0.
3. Obtain separate authority for one clean C2 candidate commit.
4. Repeat complete local exact-candidate qualification and reproducible distribution builds from C2.
5. Obtain separate credential/branch authority and pass hosted C2 lanes.
6. Separately authorize preparation of `VREC-SEH-009`, assurance review, and its ready-to-verified transition.
7. Separately authorize released-0.5 preparation of `RLS-SEH-009` and bounded canonical bootstrap binding; require both released and candidate validation to pass.
8. Have the release owner separately transition the RLS or reject it.
9. Separately authorize tag, GitHub/PyPI publication, Pages deployment, maintenance reconciliation, and post-publication root upgrade at their action times.

Automation prepares observations and proposals only. No green check supplies an accountable decision.

## Human approval triggers

- Product/requirements owners approve `REQ-REB-008`.
- Technical/security owners approve `SPEC-REB-003`, `ARCH-REB-002`, and `ADR-REB-002`.
- Assurance/security owners approve `VER-REB-002`.
- Engineering/repository owners approve `WO-REB-004` for implementation.
- Release/quality/security owners approve this replacement contract.
- Candidate commit, branch push/credentials, VREC preparation/verification, RLS preparation/binding/release, tag, publication, deployment, maintenance state, external policy, and root adoption each retain their separate action-time authority.

## Rollback criteria and procedure

Before publication, stop on incomplete authority, scope drift, missing keyed evidence, old-lock or evaluator drift, candidate contamination, binder ambiguity, evidence mismatch, released/candidate validation failure, unexplained warning, unsafe archive, nondeterminism, hosted mismatch, provenance disagreement, or need for broader authority. Correct through a new reviewed candidate sequence; never repoint C, C2, a VREC, or an RLS and never waive a failed bootstrap criterion.

After publication, never move `v0.6.0`, replace immutable files, or rewrite bootstrap evidence. Preserve the affected release, record any defect, block unsafe adoption, and prepare a separately governed corrective release.

## Post-release observation window

After separately authorized publication, verify immutable tag/assets, PyPI hashes and attestations, fresh public Python 3.11 installation, candidate identity, clean init/adopt, doctor, validate, focus, check, inspect, dashboard, bootstrap-history validation, mutation-authority refusal, Pages provenance, maintenance-line state, and later separately governed root-upgrade readiness. Observations cannot modify published facts or create release authority.
