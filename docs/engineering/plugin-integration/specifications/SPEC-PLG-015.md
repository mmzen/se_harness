+++
id = "SPEC-PLG-015"
type = "specification"
title = "Host qualification and measured workflow overhead"
status = "draft"
owners = ["technical-owner"]
created = "2026-09-08"
updated = "2026-09-08"
contract = "Qualification retains reproducible evidence across the accepted host matrix and reports timing and prompt measurements against owner-selected acceptance criteria."

[relations]
specifies = ["REQ-PLG-025", "REQ-PLG-026"]
+++

# Specification: Host qualification and measured workflow overhead

## In plain words

Qualification connects support claims to observed host behavior and measured overhead.

## Scope

This contract covers operation qualification. DEC-PLG-005 blocks VER-PLG-015 approval, which keeps WO-PLG-015 ineligible.

## Terms

- **Measurement condition.** Recorded versions, model settings, workload, cache state and repetitions.
- **Offline check.** Credential-free protocol or component fixtures.
- **Live proof.** Observed operations in a trusted actual host.

## Rules

**PLG-QLF-001.** Qualification MUST name the owner-selected host/platform matrix before claiming support.

**PLG-QLF-002.** Every selected scenario MUST retain reproducible inputs, outcomes, versions, evaluator identity and missing or failed cases.

**PLG-QLF-003.** Measurements MUST report startup, each tool check and total-operation milliseconds, plus prompt counts and conditions.

**PLG-QLF-004.** Reports MUST retain failed, interrupted and missing samples without converting them into zero durations or successful coverage.

**PLG-QLF-005.** Reports MUST separate accountable decisions from duplicate requests for unchanged valid authority.

**PLG-QLF-006.** Qualification MUST require DEC-PLG-005's approved positive profile, approved VER-PLG-015, and passing evidence for the complete matrix and numeric or relative criteria.

**PLG-QLF-007.** Offline protocol checks MUST remain separate from live proof; untrusted PR jobs MUST NOT receive host credentials or execute authenticated hosts.

**PLG-QLF-008.** Live proof MUST record authorized revision, trusted run environment, authentication method and scope; retained evidence MUST exclude credentials.

**PLG-QLF-009.** The profile MUST define repetitions, recorded model settings, timing boundaries and prompt counting: accountable decisions, duplicate requests, host permission/trust interactions, and recovery questions.

**PLG-QLF-010.** Reports MUST retain per-run samples and aggregate calculations; preliminary CLI timings MUST remain baselines, never plugin overhead measurements or accepted limits.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing coverage, samples or criteria | Withhold qualification; report gaps. | missing input |
| Preview-only or another non-qualification decision | Withhold qualification; require appropriate artifact disposition or amendment. | qualification profile not approved |
| Only offline fixtures or an untrusted authenticated run | Withhold live-host acceptance; identify the missing trusted proof. | live proof unavailable |

## Examples

**Given** an interrupted run, **when** summarized, **then** its sample remains missing and qualification incomplete (PLG-QLF-004, PLG-QLF-006).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-025` | PLG-QLF-001, PLG-QLF-002, PLG-QLF-006, PLG-QLF-007, PLG-QLF-008 |
| `REQ-PLG-026` | PLG-QLF-003, PLG-QLF-004, PLG-QLF-005, PLG-QLF-006, PLG-QLF-009, PLG-QLF-010 |

## Not decided here

- Budgets and support scope belong to DEC-PLG-005; no universal tool coverage is claimed.
