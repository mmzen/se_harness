+++
id = "ADR-REB-002"
type = "adr"
title = "Use one contract-bound predecessor bootstrap"
status = "approved"
owners = ["technical-owner", "security-owner", "release-owner"]
created = "2026-08-21"
updated = "2026-08-21"

[relations]
decides = ["ARCH-REB-002"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-21T15:40:28Z"
decided_by = "technical-owner"
+++

# ADR: Use one contract-bound predecessor bootstrap

## Status

Accepted on 2026-08-21 through accountable technical and security approval together with `ARCH-REB-002`. The decision authorizes only the bounded design selected by approved `WO-REB-004`; candidate, assurance, release, external, maintenance, credential, and root actions remain separately governed.

## Context

Candidate 0.6.0 requires canonical evaluator evidence on new RLS records and schema-3 current-lock equality while ready. The operational repository is correctly governed by released 0.5.0 and schema 2. Released 0.5 can prepare `RLS-SEH-008` but cannot generate the candidate evidence. Candidate code cannot upgrade or govern the root before it is independently published. The mismatch was detected after candidate C and `VREC-SEH-008` were fixed, so changing product or publication behavior requires a new candidate and assurance chain.

## Decision drivers

- Preserve released 0.5.0 as the operational evaluator until 0.6.0 is public.
- Satisfy evaluator-evidence readiness rather than waive it.
- Avoid a second product release solely to bridge the release process.
- Bind any exception to exact approved facts and one record.
- Keep credentials and external writes downstream of independent replay.
- Preserve one standard installation and the later ordinary schema-3 upgrade path.

## Considered options

1. **Ignore candidate validation and publish under legacy 0.5 rules.** This leaves the repository invalid under the released candidate and violates the approved evidence requirement.
2. **Add the new RLS to a missing-evidence legacy allowlist.** This is simple but proves no evaluator identity and creates an unaudited waiver.
3. **Use candidate source/package to prepare the RLS or mutate the root.** This is circular authority and violates the released-evaluator boundary.
4. **Publish a narrow 0.5.1 bridge and upgrade the root first.** This preserves candidate C but requires a separate maintenance release, its own bootstrap decision, and an operational root upgrade before 0.6.0.
5. **Create a new 0.6.0 candidate with one contract-bound predecessor-evaluator adapter.** Released 0.5 prepares the RLS; a bounded binder attaches canonical proof; candidate validation and publication accept only the exact approved tuple.
6. **Abandon 0.6.0.** This avoids risk but does not deliver the approved release objective.

## Decision

Select option 5.

The replacement release contract owns the expected canonical `utf8-text-lf-v1` schema-2 lock and public predecessor archive identities and names exactly one future RLS. Released 0.5.0 remains responsible for `prepare-release` and root validation. Candidate-owned repository tooling may only bind a canonical observation after independently checking the contract, root, public wheel, external installation, and immutable RLS fields. Candidate validation and publication replay that same tuple; all normal records remain subject to schema-3 current-lock equality.

The current candidate C, verified `VREC-SEH-008`, and uncommitted `RLS-SEH-008` are stopped evidence and are never repointed. Implementation produces C2, then a new aggregate `VREC-SEH-009` and `RLS-SEH-009` under a replacement release contract.

## Consequences

### Positive

- No separately published bridge or pre-publication root upgrade is needed.
- The release still retains canonical exact-evaluator evidence.
- The exception is machine-checkable, one-shot, and bound more tightly than version or ID alone.
- Ordinary consumer and later release behavior remains schema 3.

### Negative and migration cost

- Candidate C becomes ineligible for promotion and all C2 builds, hashes, VREC, RLS, and hosted qualification must be repeated.
- Candidate-owned validator, publication, and a repository-only binder gain security-sensitive bootstrap logic.
- Released 0.5 preparation metadata and candidate preparation semantics require an explicit compatibility marker.
- The replacement contract must retain exact old-lock and public-wheel facts.

### Operational and security consequences

- Any old-lock change invalidates the bootstrap packet and requires review.
- Binder and publication failures stop without root changes, credentials, or external writes.
- The new candidate never becomes evaluator authority before public release.
- A separate post-publication root-upgrade work order remains mandatory.

## Validation

Execute `VER-REB-002` plus all unchanged 0.6.0 release gates. Require adversarial contract/lock/archive/evidence/origin tests, zero-write snapshots, released-0.5 and candidate dual validation, publication replay without credentials, reproducible C2 distributions, verifier-owned acceptance, and hosted candidate-source/package checks.

## Canonical-LF correction

On 2026-08-21 at `2026-08-21T16:31:42Z`, the accountable owners preserved this accepted decision while correcting old-lock identity from a platform-specific CRLF observation to canonical `utf8-text-lf-v1` content. The exact digest is `08441ec0b4825db4c017ce4169f23092162995ff06476004d267f0671c7443b3`; no alternative, status, authority, or scope decision changed.
