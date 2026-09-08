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

Support claims need results from selected tools and computers. Reports expose missing checks, time spent, and operator interruptions.

## Scope

This contract qualifies the plugin operation scenarios. DEC-PLG-005 blocks VER-PLG-015 approval until its qualification profile is settled; the unapproved verification contract keeps WO-PLG-015 ineligible.

## Terms

- **Measurement condition.** Recorded host, platform, versions, workload, cache state and repetition settings.

## Rules

**PLG-QLF-001.** Qualification MUST identify the owner-selected host and platform matrix before claiming a combination supported.

**PLG-QLF-002.** Every selected operation scenario MUST retain reproducible inputs, actual outcomes, versions, evaluator identity and explicit untested or failed cases.

**PLG-QLF-003.** Measurements MUST separately report startup, tool-check and total-operation durations in milliseconds, plus operator prompts per operation and their conditions.

**PLG-QLF-004.** Reports MUST retain failed, interrupted and missing samples without converting them into zero durations or successful coverage.

**PLG-QLF-005.** Reports MUST distinguish required accountable decisions from duplicate prompts for unchanged valid authority.

**PLG-QLF-006.** Qualification MUST require an approved positive profile from DEC-PLG-005, approved VER-PLG-015, and passing evidence for its complete matrix and numeric or relative criteria.

## Failure behaviour

| Trigger | Response | Diagnostic |
| --- | --- | --- |
| Missing host coverage, samples, or accepted criteria | Report the gap and withhold qualification acceptance. | unqualified combination or undecided criteria |
| Preview-only or another non-qualification decision | Withhold qualification; require appropriate artifact disposition or amendment. | qualification profile not approved |

## Examples

**Given** an interrupted measurement, **when** results are summarized, **then** that sample remains missing and qualification stays incomplete (PLG-QLF-004, PLG-QLF-006).

## Coverage

| Requirement | Rules |
| --- | --- |
| `REQ-PLG-025` | PLG-QLF-001, PLG-QLF-002, PLG-QLF-006 |
| `REQ-PLG-026` | PLG-QLF-003, PLG-QLF-004, PLG-QLF-005, PLG-QLF-006 |

## Not decided here

- DEC-PLG-005 owns support scope and acceptable overhead.
- No arbitrary timing threshold or universal tool coverage.
