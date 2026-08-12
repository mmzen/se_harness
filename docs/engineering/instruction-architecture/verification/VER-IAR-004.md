+++
id = "VER-IAR-004"
type = "verification"
title = "Verify conditional ADR applicability and coverage"
status = "approved"
owners = ["quality-owner"]
created = "2026-08-12"
updated = "2026-08-12"

[relations]
verifies = ["REQ-IAR-012"]
+++

# Verification Contract: Verify conditional ADR applicability and coverage

## Independence

Verification uses the approved trigger and outcome contract rather than implementation-selected heuristics. Automated tests check declared structure and graph coverage; human inspection separately challenges whether examples and policies preserve architecture accountability without encouraging ceremonial ADRs.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| `REQ-IAR-012` | metadata matrix | every outcome, trigger, rationale, assessor, and type boundary | Valid combinations pass; each missing, unknown, duplicate, empty, or contradictory value has deterministic diagnostics. |
| `REQ-IAR-012` | preflight graph cases | zero, one, and multiple architectures/ADRs | Coverage is enforced separately for each architecture; unrelated ADRs cannot satisfy it. |
| `REQ-IAR-012` | authoring and policy inspection | managed templates and four focused policies | Agents receive clear significance guidance, no-ADR process, cardinality rule, and decision-right boundary. |
| `REQ-IAR-012` | Explorer and CI tests | every assessment state | State and anomalies agree with validation/preflight; no authority claim is introduced. |
| `REQ-IAR-012` | compatibility tests | draft/approved/in-progress, completed legacy with/without ADR, and completed-artifact rewrite review | Migration follows the deterministic state-bounded exception and never rewrites owner artifacts. |

## Acceptance scenarios

- First design activates significant boundary and persistence triggers and cannot pass without a deciding ADR.
- Routine conformance uses an accountable `no_significant_decision` rationale and passes without an ADR.
- One coherent ADR covers a decision affecting several requirements.
- Two selected significant architectures require coverage of both; one unrelated or partially related ADR does not pass.
- Missing assessment cannot be treated as an implicit no-ADR outcome.

## Property and invariant tests

- Validate controlled trigger vocabulary, uniqueness, outcome-trigger cardinality, and non-empty rationale/assessor.
- Validate metadata on non-architecture artifacts is rejected.
- Confirm `adr_required` requires at least one selected active ADR whose `decides` contains that architecture.
- Confirm `no_significant_decision` passes with no selected ADR for that architecture and fails when trigger metadata contradicts it.
- Confirm an ADR may decide several selected architectures and a selected architecture may have several coherent ADRs.
- Confirm deterministic text and JSON preflight diagnostics and manifest inclusion.
- Confirm draft, approved, and in-progress architecture cannot use the legacy exception and authoring placeholders cannot be approved accidentally.

## Static and architecture checks

- Inspect `WORKFLOW.md`, `DECISION_RIGHTS.md`, `QUALITY_GATES.md`, `TRACEABILITY.md`, and architecture/ADR/work-order templates.
- Run formal validation, doctor, start and review preflight, CLI help, and deterministic dashboard generation.
- Confirm canonical templates, installed scripts/policies, and schema-2 lock parity after supported self-upgrade.
- Confirm the independent-baseline and candidate CI lanes describe assurance honestly while the new behavior remains unreleased.

## Security and resilience checks

Exercise non-string, oversized, unknown, duplicate, Unicode, and injection-shaped assessment inputs; path and relation failures; customized managed content; transactional no-partial-write upgrade; and deterministic repeated application. Rationale and assessor values must never enter a shell.

## Full regression

Run focused validator, preflight, dashboard, authoring, installation, and instruction tests plus the full unit suite on Python 3.11 and the local supported runtime.

## Manual assessments

- Confirm triggers catch significant initial design without stating that every initial design automatically requires an ADR.
- Confirm routine application of an existing architecture does not require a ceremonial ADR.
- Confirm technical-owner accountability cannot be silently delegated to an implementation agent.
- Confirm no historical artifact, command side effect, lifecycle state, or external authority changes merely from a finding.

## Evidence retention

Retain exact commands, runtimes, fixtures, diagnostic matrices, migration outcomes, CI assurance source, Explorer states and snapshots, changed paths, deviations, and residual risks under `WO-IAR-004`.

## Residual uncertainty

Structured triggers cannot prove that an author disclosed every material decision. Protected technical review must challenge suspicious `no_significant_decision` assessments using architecture content and the candidate diff.
