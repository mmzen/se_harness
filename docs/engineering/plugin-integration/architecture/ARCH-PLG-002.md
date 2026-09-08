+++
id = "ARCH-PLG-002"
type = "architecture"
title = "Host adapters without lifecycle authority"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "public-interface-or-protocol"]
rationale = "Host events and context delivery are new interfaces; lifecycle authority must remain in the evaluator and accountable decisions."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-PLG-008", "REQ-PLG-009", "REQ-PLG-010", "REQ-PLG-013", "REQ-PLG-014", "REQ-PLG-024"]
conforms_to = ["SPEC-PLG-005", "SPEC-PLG-006", "SPEC-PLG-007", "SPEC-PLG-008", "SPEC-PLG-014"]
+++

# Architecture: Host adapters without lifecycle authority

## Context and scope

Each coding host has its own loading, trust, event, and context-delivery behavior.
Shared scripts use the existing evaluator; host differences remain explicit.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Codex and Claude adapters | Register components through the mechanism demonstrated for that host. |
| Session script | Verify installation, then return complete verified governance. |
| Tool-action script | Translate covered events into existing evaluator checks and host responses. |
| Skills | Explain and invoke the current workflow under actual authority. |
| Optional helpers | Return bounded read-only findings to the main agent. |

## Dependency direction

Host event → adapter → released evaluator → supported host response.
Lifecycle policy never flows from a skill or host callback into a second implementation.

## Data and control flow

Setup prepares the interpreter before Python-dependent hooks activate.
Session verification and context delivery execute in order within one handler.
Compaction and resume use the demonstrated session event; manual readiness remains available.
A tool-action result reports both the evaluator verdict and actual interception coverage.

## Trust boundaries

Repository text and host payloads are untrusted inputs.
Actor strings do not authenticate owners. Helper findings confer no decision rights.
Missing hooks cannot guarantee that all tools are blocked.
Remote effects require independent controls outside this adapter boundary.

## Required patterns

Keep separate host manifests, explicit supported-action mappings, and fresh evaluator inputs.
Reuse the current scope, evidence, decision, and delegation contracts.

## Prohibited patterns

No invented approval store, lifecycle API, universal interception claim, or automatic merge authority.
Do not edit cached plugin payloads to manufacture a working activation route.

## Quality attributes

One shared implementation limits drift; host-specific qualification demonstrates the actual coverage.
Performance improvements preserve required checks and current authority.

## Conformance checks

The selected host, session, tool-action, and helper verification contracts test each boundary.
DEC-PLG-001 and DEC-PLG-002 block the production specifications pending accepted host activation evidence; their work orders therefore remain ineligible for approval.

## Related ADRs

ADR-PLG-002 records this proposed separation. Existing remote authorization work remains WO-ECP-004.
