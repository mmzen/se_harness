+++
id = "VER-PLG-007"
type = "verification"
title = "Session governance delivery acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-010", "REQ-PLG-011", "REQ-PLG-012"]
+++

# Verification Contract: Session governance delivery acceptance

## Independence

The assurance owner fixes expected source bytes and failure outcomes before reviewing implementation evidence. Handler output alone cannot establish complete delivery.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-010 | test | Intact/damaged sources; wrong evaluator; source changed after verification | Only complete content matching verified bytes reaches readiness. |
| REQ-PLG-011 | test | Resume and compaction after source/runtime changes | Current verification repeats; stale readiness never passes. |
| REQ-PLG-012 | test | Output limit; complete/failed fallback; fallback bytes changed | Changed content is rejected and reverified before readiness. |

## Acceptance scenarios

Run explicitly captured Codex/Claude protocol fixtures against the released evaluator. Record protocol/OS/Python versions, evaluator identity and repository lock. Live delivery belongs to VER-PLG-005/006 and VER-PLG-015.

## Property and invariant tests

Change gate/router bytes between verification and direct return or fallback reading: reject and reverify. Repeated events write nothing; damaged content remains unready. Missing Python produces host-launch failure, not handler output.

## Static and architecture checks

Review PLG-CTX-001 through PLG-CTX-006 and ARCH-PLG-002/ADR-PLG-002. Confirm one verification-then-delivery path.

## Security and privacy checks

Exercise untrusted paths, altered managed content and interrupted reads. Confirm unrelated credentials and repository content are absent from output.

## Performance and resilience checks

Record typical and slow startup/restoration times, including fallback. Required verification and completeness checks remain enabled.

## Manual assessments

Inspect complete fixture outputs and readiness behavior. Actual agent-context inspection remains required in host qualification; this handler contract does not claim live delivery.

## Evidence retention

Retain commands, outputs, failures and platform identities under `evidence/WO-PLG-007/`; bind the later verification record to the exact implementation candidate.

## Residual uncertainty

Fixture acceptance qualifies the handler only, without waiting for production adapters. Host delivery remains a separate qualification boundary. These planned checks have not run.
