+++
id = "VER-OCA-001"
type = "verification"
title = "Verify accountable operating-contract activation"
status = "approved"
owners = ["quality-owner", "service-owner"]
created = "2026-08-16"
updated = "2026-08-16"

[relations]
verifies = ["REQ-OCA-001"]
+++

# Verification Contract: Verify accountable operating-contract activation

## Independence

Verification derives the expected contract IDs, requirement sets, section names, and lifecycle result from `SPEC-OCA-001`, then inspects the files and public command output. It does not treat the implementation's prose or status alone as proof.

## Requirement-to-evidence matrix

| Concern | Method | Pass condition |
| --- | --- | --- |
| exact activation set | metadata inspection | exactly six named OPS records change from `draft` to `approved` |
| requirement-only traceability | relation-set comparison | each `assures` set exactly matches the specification and contains only active `REQ-*` targets |
| operational completeness | section and content inspection | all nine sections exist and state actionable, current controls |
| authority separation | diff and prose inspection | no release artifact changes and approval does not imply release or verification |
| domain discoverability | index inspection | each affected domain identifies the approved OPS and still identifies its draft REL |
| authoring consistency | root/canonical parity and doctor | both templates use requirement-only example and managed integrity passes |
| lifecycle queue | deterministic inspection | `definition_pending` decreases from twelve to six, leaving only the six draft REL records |
| formal integrity | validator | zero errors and no new unexplained warnings |
| scope control | changed-path inspection | no validator, CLI, workflow, version, VREC, RLS, or executable source changes |

## Manual assessments

The accountable service owner reviews whether each objective, alert, recovery path, security control, automation boundary, runbook, and evidence set can be honored with current repository mechanisms.

## Evidence retention

Retain the before/after inspection queues, exact relation sets, section audit, validation and doctor outputs, root/canonical template hash proof, changed paths, authorization, deviations, and follow-up gaps in `docs/engineering/operating-contract-activation/evidence/WO-OCA-001-verification.md`.

## Residual uncertainty

Approval commits owners to follow the documented controls but cannot prove future human response. The current validator does not enforce `OPS.assures` target types; this transaction relies on deterministic inspection and records that limitation for separate implementation work.
