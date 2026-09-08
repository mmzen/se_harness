+++
id = "VER-PLG-003"
type = "verification"
title = "Codex compatibility evidence before support selection"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-006"]
+++

# Verification Contract: Codex compatibility evidence before support selection

## Independence

Derive expected observations from SPEC-PLG-003 and the exact host documentation assessed.
Compare those expectations with observed host events, not fixture claims.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-006 | Demonstration, inspection | Repeated activation; missing Python; inactive event | Every assessed combination has reproducible actions and evidence of activation or a precise incompatibility. |

## Acceptance scenarios

Attempt discovery and new-session activation in a disposable Codex profile.
Attempt resume and compaction, before and after private evaluator preparation.
Repeat the observed working route; retain missing-Python and disabled-hook outcomes.

## Property and invariant tests

Each support statement points to recorded host/version/platform evidence.
An unavailable check cannot become a passing observation.

## Static and architecture checks

The fixture contains observation code only; it adds no alternative evaluator policy.

## Security and privacy checks

Normal host configuration and repositories remain unchanged.
Redact credentials from retained host transcripts.

## Performance and resilience checks

Record required restarts, trust interactions, and activation durations.

## Manual assessments

Assess available Windows, Linux, and macOS combinations.
Record host version, Python version, and selected published evaluator version; mark every other combination unavailable or unsupported with reasons.

## Evidence retention

Retain fixture revision, referenced documentation, ordered actions, event transcripts, and compatibility table under `evidence/WO-PLG-003/`.

## Residual uncertainty

A documented incompatibility can satisfy this investigation.
Production support remains undecided until DEC-PLG-001; absent evidence cannot authorize a production adapter.
