+++
id = "REQ-IAR-017"
type = "requirement"
title = "Offer bounded next-step guidance for inspection observations"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "WHEN repository inspection exposes an existing lifecycle queue item or supported derived finding, SE Harness SHALL offer deterministic non-authoritative next-step guidance without inferring eligibility, changing the observation, or performing the action."
verification_method = "Automated catalog, projection, determinism, no-write, boundary, compatibility, distribution, and regression tests"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Offer bounded next-step guidance for inspection observations

## Lifecycle

Approved on 2026-08-15 through the repository owner's instruction `ok i approve` as part of the complete `IAR-009` packet.

## Problem

`harnessctl inspect` makes existing lifecycle queues and findings visible, but an operator must still know the harness model well enough to choose a safe next step. The `W-REV-004` observation is a concrete example: it correctly exposes a stale ready verification record, but the operator must independently discover that supersession is a separate accountable decision rather than an automatic cleanup.

Useful guidance must not become a second rule engine, an eligibility decision, or an automated remediation system.

## Required outcome

`harnessctl inspect [TARGET]` supplements supported existing observations with structured suggestions that:

- are selected only by a closed catalog keyed by an existing queue action class or existing derived finding rule ID;
- preserve the source queue item or finding and identify its affected artifacts;
- state one bounded next step, the accountable role, and that execution is never automatic;
- remain separate from validation, finding severity, lifecycle state, and authority;
- omit unknown or unsupported sources rather than guessing from titles, prose, paths, or repository content.

## Acceptance criteria

1. Human and JSON inspection output expose deterministic structured suggestions without removing or rewriting existing queues or findings.
2. Every suggestion records its source kind, source ID, affected artifact IDs, stable action class, static guidance, accountable role, and `automatic = false`.
3. Queue guidance is limited to the existing mechanical action classes defined by `SPEC-IAR-008`.
4. Finding guidance is limited to an explicit catalog of current actionable derived warning rules; validator diagnostics, informational observations, and unknown future rules receive no inferred suggestion.
5. A suggestion does not assert that its action is eligible, approved, verified, released, safe, or complete.
6. Suggestions contain no executable command, shell fragment, generated path, deadline, score, or automatic lifecycle target.
7. Repeated observations may be grouped in human output, while JSON preserves deterministic source-to-suggestion traceability.
8. Inspection remains read-only and observational; its exit behavior and the behavior of `validate`, `doctor`, `preflight`, and `dashboard` remain unchanged.
9. The conflicting recommendation exclusions in `REQ-IAR-016` and `SPEC-IAR-008` are explicitly narrowed before implementation so both work orders can be assessed at one final candidate commit.

## Deferred questions

Repository-configurable guidance, validator-diagnostic remediation, interactive confirmation, command execution, automatic fixes, aging thresholds, and AI-generated advice remain separately governed work.

## Authority boundary

A suggestion helps a human find the next decision boundary. It cannot decide that a transition is eligible, authorize a change, mutate an artifact, run a command, verify a candidate, supersede a record, or release software.
