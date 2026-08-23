+++
id = "ADR-REB-007"
type = "adr"
title = "Contract-driven dual-runtime rehearsal for evaluator succession"
status = "approved"
owners = ["technical-owner", "security-owner", "quality-owner", "release-owner"]
created = "2026-08-23"
updated = "2026-08-23"

[relations]
decides = ["ARCH-REB-007"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-08-23T07:56:21Z"
decided_by = "technical-owner"
+++

# ADR: Contract-driven dual-runtime rehearsal for evaluator succession

## Status

Accepted.

## Context

The 0.6.0 release had strong individual checks but no complete N-1-to-N migration test. The released 0.5.0 evaluator retained authority while candidate 0.6.0 introduced new evidence and lifecycle behavior. Missing handover steps appeared serially during release preparation, rejection, corrected succession, hosted assessment, publication, rendering, and Pages recovery.

A preventive design must prove the whole transition without making the candidate authoritative, weakening predecessor checks, rewriting history, or performing a real release or root upgrade during testing.

## Decision drivers

- Preserve predecessor authority until a separate post-publication adoption transaction.
- Exercise every material 0.6.0 failure boundary before the next incompatible release.
- Make evaluator roles, repository views, decisions, mutations, and failures machine-assessable.
- Produce deterministic evidence on Windows and Linux without credentials or privileged side effects.
- Reuse existing narrow adapters while keeping #103, #104, and #109 as separate root-cause remediations.
- Support future N-1-to-N scenarios without rewriting historical fixtures or embedding version-specific policy in the runner.

## Considered options

1. **Documentation checklist only.** Rejected because the 0.6.0 process already had documentation; missing executable cross-stage assumptions still escaped.
2. **Continue testing components independently.** Rejected because preparation, validation, rejected succession, publication, rendering, and adoption can each pass while their identities and authority boundaries disagree.
3. **Let the successor candidate temporarily govern the root during migration.** Rejected because it recreates candidate self-authorization and the circular dependency from the 0.5.0 incident.
4. **Allow known predecessor errors and continue.** Rejected because diagnostic allowlists cannot prove the remaining graph and turn incompatibility into an unreviewable bypass.
5. **Use one versioned contract, two isolated runtimes, disposable state, a closed stage graph, and an authority oracle.** Selected because it tests the handover while preserving distinct claims and decision rights.

## Decision

Select option 5.

Add a packaged `se-harness-governance-migration-v1` contract and a read-only `rehearse-migration` operation. The operation resolves predecessor and successor runtimes independently outside the operational checkout, validates one canonical scenario, and drives the required stages through typed adapters against disposable state. An authority oracle enforces the evaluator role, target view, attributed decision fixture, and allowed mutation set around every stage.

The first retained scenario covers the 0.5.0-to-0.6.0 class of incompatibility, including failed/rejected bootstrap history and corrected succession. Unit and hermetic integration tests need no network. A hosted unprivileged lane may separately acquire and digest-check the already public predecessor wheel, build a non-promotable successor wheel, and run the same scenario with only local paths.

Release/publication/render stages are plans or disposable outputs. The final adoption stage requires a separately attributed fixture and simulated immutable public successor fact, uses the ordinary upgrade transaction, and is the only stage allowed to change evaluator selection in the disposable root.

## Consequences

### Positive

- Future incompatible releases have one executable definition of the complete handover.
- Candidate self-authorization, undeclared views, missing rejection/succession behavior, and combined publication/adoption are detected before release.
- Exact stage evidence makes failures reviewable without privileged log access.
- Historical scenarios become regression contracts for later versions.

### Negative

- The runner, contract schema, fixtures, package-data checks, cross-platform CI, and independent replay add maintenance and runtime cost.
- An exact historical lane needs controlled acquisition of the already public predecessor bytes before runner execution.
- Existing release components need typed test adapters even when their production interfaces remain unchanged.

### Operational, security, and migration consequences

- The operation is evidence-only and receives no production credentials, publication permissions, or operational mutation target.
- A passing rehearsal does not approve the candidate, verify a VREC, release an RLS, publish, deploy, or adopt the successor.
- Existing 0.6.0 history, candidate C6, release records, distributions, tag, root evaluator, and published state remain unchanged.
- Fixes discovered in lifecycle rules, shared compatibility views, or production evaluator-role commands stop and move to #103, #104, or #109 rather than expanding `WO-REB-018` silently.

## Validation

Execute `VER-REB-007`: validate the contract and package data; run exact stage-order and authority tests; run positive, tampered, skipped, reordered, role-substitution, view, decision, credential, path, timeout, cleanup, and source-mutation cases; repeat deterministic runs on Windows and Linux; and independently replay the exact historical migration result.
