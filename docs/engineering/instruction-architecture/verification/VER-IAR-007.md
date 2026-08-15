+++
id = "VER-IAR-007"
type = "verification"
title = "Verify additive validation taxonomy compatibility"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-15"
updated = "2026-08-15"

[relations]
verifies = ["REQ-IAR-015"]
+++

# Verification Contract: Verify additive validation taxonomy compatibility

## Independence

Expected planes derive from the approved taxonomy and rule authority, not from the implementation's chosen mapping. Existing fixtures provide the compatibility oracle for codes, paths, messages, severity, validity, and exit behavior.

## Required checks

| Check | Pass condition |
| --- | --- |
| vocabulary | Exactly `structure`, `governance`, `policy`, and `maintenance` are accepted. |
| emission coverage | Every current diagnostic construction supplies one valid plane; missing and unknown values fail deterministically. |
| structural fixtures | Parse, metadata, identity, relation, and target-type failures report `structure`. |
| governance fixtures | Coverage, architecture, ADR, evidence, VREC, supersession, and RLS failures report `governance`. |
| configured-policy fixture | A failure activated by repository configuration reports `policy`. |
| maintenance fixtures | Existing non-canonical and legacy advisories report `maintenance` and remain warnings. |
| compatibility oracle | Removing additive taxonomy fields yields the same valid flag, artifact inventory, diagnostics, messages, ordering, severity, and exit code as the baseline. |
| JSON | Taxonomy version, per-diagnostic planes, and deterministic four-plane counts are present without removing existing fields. |
| human output | Overall result and individual diagnostics remain visible; plane summary is present; no score appears. |
| distribution | Root and canonical validators agree; upgrade is idempotent; package/fresh-install behavior agrees when packaging is authorized. |

## Regression

Run focused validator, instruction-architecture, preflight, dashboard-consumer, installer, integrity, and documentation tests plus the complete suite on Python 3.11 and the local supported runtime. Run formal graph validation, `doctor`, phase-appropriate preflight, CLI help, and diff hygiene.

## Evidence

Retain the rule-to-plane matrix, baseline comparison, commands, runtimes, test counts, managed transaction, changed paths, deviations, and residual risks under `docs/engineering/instruction-architecture/evidence/WO-IAR-007-verification.md`.

## Residual uncertainty

The taxonomy clarifies machine findings but does not prove that a rule belongs in the ideal long-term plane or that users will interpret governance and policy distinctions correctly. Accountable review remains required.
