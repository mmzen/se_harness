+++
id = "VER-PLG-010"
type = "verification"
title = "Change skill workflow acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-017", "REQ-PLG-018"]
+++

# Verification Contract: Change skill workflow acceptance

## Independence

The assurance owner supplies scenarios and expected states from installed workflow and decision-rights rules. Review transcripts and repository effects independently of the skill's narrative.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-017 | test | Package including a DEC; amendment; WO lifecycle; partial failure | Definitions/WOs begin draft, DEC begins open; operations, states and partial writes match the evaluator. |
| REQ-PLG-018 | test | Covered continuation; changed scope; missing authority; eligible/ineligible delegation | No duplicate prompt for covered work; affected unauthorized work stops. |

## Acceptance scenarios

Exercise the skill with the verified released evaluator in disposable repositories. Record host/OS, Python, evaluator and command-help identities.

## Property and invariant tests

Create a package with a decision record: definitions/WOs stay draft and the DEC stays open. Creation does not approve or dispose; approval does not start. Actor assertions grant no authority.

## Static and architecture checks

Review PLG-CHANGE-001 through PLG-CHANGE-005 against installed authoring, workflow and DR-015 rules. Reject invented commands or state transitions.

## Security and privacy checks

Test branch-only delegation, stale CI, missing owner decisions and scope expansion. Do not extend delegation beyond its existing three mechanical decisions.

## Performance and resilience checks

Count invocations and decision prompts across an unchanged authorized sequence and a materially changed sequence; required checks remain enabled.

## Manual assessments

Verify clear restitution of actual effects, blockers and one next step. Inspect interrupted application before any retry.

## Evidence retention

Retain commands, outputs, failures and platform identities under `evidence/WO-PLG-010/`; bind the later verification record to the exact implementation candidate.

## Residual uncertainty

Skill instructions do not provide deterministic authentication or external enforcement. All checks here are future acceptance work, not completed verification.
