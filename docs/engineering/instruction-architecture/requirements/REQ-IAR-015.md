+++
id = "REQ-IAR-015"
type = "requirement"
title = "Classify validation findings without changing gate behavior"
status = "implemented"
owners = ["repository-owner", "quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"
statement = "SE Harness SHALL assign every validator diagnostic to one stable assessment plane and expose that plane without changing existing validation rules, severities, or exit behavior."
verification_method = "Automated taxonomy coverage, output-compatibility, managed-parity, and regression tests"

[relations]
derives_from = ["CAP-IAR-001"]
+++

# Requirement: Classify validation findings without changing gate behavior

## Problem

The validator currently combines parsing, graph consistency, governance invariants, configured policy, and maintenance advisories in one error and warning stream. Codes remain precise, but an operator must know implementation details to understand what kind of assurance failed. Adding more rules before naming these boundaries would make the command harder to interpret.

## Required outcome

Every emitted diagnostic declares exactly one of four stable planes:

- `structure`: the formal graph can be parsed, identified, typed, and linked;
- `governance`: non-waivable coverage, architecture, decision, verification, supersession, and release invariants;
- `policy`: a rule activated by explicit repository configuration;
- `maintenance`: a non-blocking compatibility, placement, or migration advisory.

The plane is explanatory metadata. Existing error versus warning severity, diagnostic code, path, message, validation result, and process exit code remain authoritative and unchanged.

## Acceptance criteria

1. Every diagnostic emitted by the current validator has exactly one allowed plane.
2. JSON output exposes the plane for each diagnostic and deterministic counts per plane while retaining existing fields.
3. Human output identifies the planes without hiding individual codes, paths, or messages.
4. Existing valid and invalid fixtures produce the same pass/fail result and the same diagnostic codes, severities, paths, and messages.
5. Root, canonical template, packaged data, and managed-integrity expectations remain consistent.
6. No aggregate health score, new CLI command, validation profile, orphan rule, pending-item rule, or maintenance deadline is introduced.

## Authority boundary

Classification does not prove semantic correctness, change a warning into a gate, approve an artifact, authorize work, verify a candidate, release software, or grant automation any accountable decision right.
