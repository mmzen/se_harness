+++
id = "ARCH-RLO-003"
type = "architecture"
title = "Repository-owned maintenance-line boundary"
status = "approved"
owners = ["engineering-owner", "release-owner", "security-owner"]
created = "2026-08-19"
updated = "2026-08-19"

[relations]
addresses = ["REQ-RLO-012"]
conforms_to = ["SPEC-RLO-003"]

[decision_assessment]
outcome = "adr_required"
triggers = ["system-boundary", "security-privacy-or-trust-boundary", "deployment-or-operating-model", "concurrency-consistency-reliability-or-failure-strategy", "cross-cutting-policy"]
rationale = "The change adds a mutable hosting ref to a credentialed release transaction and must decide ownership, replay, conflict, and portable-product boundaries."
assessed_by = "engineering-owner"
+++

# Architecture: Repository-owned maintenance-line boundary

## Context and scope

The existing orchestrator derives one authorized candidate, creates its immutable tag and GitHub Release, and promotes exact outputs. Maintenance-line creation is currently an untracked manual action. This architecture adds one repository-owned reconciliation boundary after exact GitHub release materialization and before downstream promotion relies on the GitHub stage succeeding.

## Components and responsibilities

- Trusted-main release resolution remains the sole source of version and candidate identity.
- The existing GitHub release job owns the tag, GitHub Release, and derived maintenance-ref reconciliation under one contents-write permission boundary.
- GitHub stores and atomically creates the ref.
- Repository workflow tests inspect derivation, ordering, permissions, replay, and refusal semantics.
- Portable SE Harness remains unaware of this branch policy.

## Dependency direction

Repository workflow policy consumes the generic released-RLS identity. Portable `se_harness`, managed templates, and consumer CI do not import, call, or encode maintenance-line reconciliation.

## Data and control flow

`released RLS on main -> canonical plan -> qualified bundle -> exact tag and GitHub Release -> derive release/MAJOR.MINOR -> read/create/compare ref -> GitHub stage outcome -> PyPI and Pages`

On replay, the same identity is derived and every existing external object is verified before continuation.

## Trust boundaries

- Only trusted-main orchestration code executes with `contents: write`.
- Candidate source and built packages remain inert data in this job.
- Version and candidate originate in prior independently validated outputs, not operator-supplied shell fragments.
- GitHub API responses and mutable branch state are untrusted until structurally checked.

## Required patterns

- Deterministic branch derivation from canonical version.
- Create-if-absent with postcondition verification.
- Read/compare-only replay for existing refs.
- Containment check that permits legitimate maintenance advancement but rejects unrelated history.
- Stage-specific failure with no compensating destructive mutation.

## Prohibited patterns

- New `harnessctl`, package, managed-template, standard-workflow, or consumer surface.
- Per-patch maintenance branches.
- Force-push, ref update, deletion, merge, or repair automation.
- Candidate execution with repository write permission.
- Additional operator input or stored credential.

## Quality attributes

- Safety: conflicting history is never overwritten.
- Determinism: release identity uniquely derives the line name and base candidate.
- Replayability: exact prior state is accepted without mutation.
- Auditability: workflow output connects candidate, tag, release, and line.
- Simplicity: one bounded step in the existing repository workflow, with no product abstraction.

## Conformance checks

- Strictly parse workflow YAML and assert one input, job ordering, contents permission, and no new actions or secrets.
- Exercise absent, equal, descendant, conflicting, concurrent-create, malformed, and API-failure fixtures against repository-owned logic or an equivalent isolated shell/API harness.
- Inspect changed paths and built wheel/standard template inventory to prove the portable boundary is unchanged.

## Related ADRs

`ADR-RLO-003` decides automatic repository-owned line creation and fail-closed replay behavior.

## Approval

Approved by the accountable repository owner on 2026-08-19 through the statement `go implement` as part of the complete RLO-003 packet.
