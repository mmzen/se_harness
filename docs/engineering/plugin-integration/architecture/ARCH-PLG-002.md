+++
id = "ARCH-PLG-002"
type = "architecture"
title = "Host adapters without lifecycle authority"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "security-privacy-or-trust-boundary", "public-interface-or-protocol"]
rationale = "Host events and context delivery are new interfaces; lifecycle authority must remain in the evaluator and accountable decisions."
assessed_by = "technical-owner"

[relations]
addresses = ["REQ-PLG-008", "REQ-PLG-009", "REQ-PLG-010", "REQ-PLG-013", "REQ-PLG-014", "REQ-PLG-024"]
conforms_to = ["SPEC-PLG-005", "SPEC-PLG-006", "SPEC-PLG-007", "SPEC-PLG-008", "SPEC-PLG-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "technical-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Architecture: Host adapters without lifecycle authority

## Context and scope

Each coding host has its own loading, trust, event, and context-delivery behavior.
Shared scripts use the existing evaluator; host differences remain explicit.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| Codex and Claude adapters | Register components and a shell guard through the documented route demonstrated for that host. |
| Session script | Verify installation, then return complete verified governance. |
| Tool-action script | Translate covered events into existing evaluator checks and host responses. |
| Skills | Explain and invoke the current workflow under actual authority. |
| Optional helpers | Return bounded read-only findings to the main agent. |

## Dependency direction

Host event → adapter → released evaluator → supported host response.
Lifecycle policy never flows from a skill or host callback into a second implementation.

## Data and control flow

Hooks can register before setup. A thin host-shell guard reports setup required if the interpreter cannot run; otherwise it invokes the Python handler. Setup alone prepares the environment. Interpreter existence does not establish readiness.
Session verification and context delivery execute in order within one handler.
Compaction and resume use the demonstrated session event; manual readiness remains available.
A tool-action result reports both the evaluator verdict and actual interception coverage.
The shared tool handler owns its inner deadline and evaluator cleanup; each host binding owns the outer timeout and supported refusal format. Qualification observes startup, timely denial and actual effects separately. A host timeout or missing response proves no prevention.

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
DEC-PLG-001 and DEC-PLG-002 record accepted activation routes for the tested
Windows configurations only. Other profiles remain unqualified. Introducing
the shared definitions does not start the production adapter work orders.

## Related ADRs

ADR-PLG-002 records this separation. Existing remote authorization work remains WO-ECP-004.
