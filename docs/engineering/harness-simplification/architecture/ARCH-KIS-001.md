+++
id = "ARCH-KIS-001"
type = "architecture"
title = "Check at the boundary where the result matters"
status = "approved"
owners = ["technical-owner"]
created = "2026-09-13"
updated = "2026-09-13"

[decision_assessment]
outcome = "adr_required"
triggers = ["responsibility-or-dependency-direction", "public-interface-or-protocol", "security-privacy-or-trust-boundary", "cross-cutting-policy"]
rationale = "This packet moves checks to meaningful boundaries and changes local authorization, identity and provenance interfaces."
assessed_by = "implementation-planner"

[relations]
addresses = ["REQ-KIS-001", "REQ-KIS-002", "REQ-KIS-003", "REQ-KIS-004", "REQ-KIS-005"]
conforms_to = ["SPEC-KIS-001"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-13T16:40:43Z"
decided_by = "technical-owner"
reason = "The owner accepted all 38 candidates in the retained 2026-09-13 codebase KISS review and requested the work orders: \"OK ! Let's create the work orders to implement all candidates\". Record the technical-owner approval of ARCH-KIS-001 within that accepted scope and the established delegated route. SPEC-KIS-001 makes the replacement contracts and seven retained protections explicit; the coverage map assigns all candidates. This records definition approval or bounded execution delegation only, not implementation start, completion, verification, release, merge, publication, live adoption or historical evidence deletion."
+++

# Check at the boundary where the result matters

## Context and scope

Ordinary work should not repeatedly prove installation or publication facts. SPEC-KIS-001 assigns each retained check to the operation that uses it.

## Components and responsibilities

| Component | Responsibility |
| --- | --- |
| CLI and selected-scope checker | Normalize ordinary inputs, read approved scope and report relevant local results. |
| Runtime identity | Identify the effective checker origin and version for the invoked route. |
| Installer and full inspection | Verify package contents and manage the smaller explicit inventory. |
| Provenance | Record the actual tested commit and relevant inputs without dashboard or human-text dependencies. |
| CI qualification | Run normal checks once, and release rehearsals only for relevant changes or release preparation. |
| Publication | Verify required assets, resume unpublished drafts and keep credentials behind the existing publication boundary. |

## Dependency direction

Presentation reads structured workflow results. Workflow does not depend on its prose renderer or dashboard.
Local scope evaluation reads the repository and retained checks. GitHub status is a separate integration input.
Installation and publication perform full artifact verification. Ordinary commands use the already selected checker origin and version.

## Trust boundaries

The owner still explicitly approves scope, assurance and release. Candidate code does not become its own governing evaluator.
Local delegation is a recorded owner decision, not a network response or a class inferred from arbitrary metadata.
Writes remain confined to the selected target, owner fragments survive, and published bytes and credentials retain their boundaries.

## Recovery and compatibility

Retry ordinary operations. Use atomic files and bounded rollback where needed; do not introduce a transaction service.
Read old records under their recorded formats. New operations use the smaller contracts, including an explicit ready successor after a safe refresh.
ADR-KIS-001 records the chosen tradeoff for this one-user development stage.
