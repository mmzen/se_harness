+++
id = "VER-PLG-002"
type = "verification"
title = "Independent provided-Python environment evidence"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-003","REQ-PLG-004","REQ-PLG-005"]
+++

# Verification Contract: Independent provided-Python environment evidence

## Independence

Use SPEC-PLG-002 and existing released-evaluator identity contracts to set expectations before executing the setup instructions.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-003 | Test, demonstration | Supported Python; missing, old, or incomplete Python | Supported setup proceeds; every missing prerequisite produces guidance without Python installation. |
| REQ-PLG-004 | Test, inspection | Offline setup; network disabled; interrupted installation | Supplied wheel installs externally; no network request or checkout mutation; incomplete environments stay unavailable. |
| REQ-PLG-005 | Test, inspection | Exact identity; wrong version; modified payload; unsafe origin | Existing identity checks accept only the matching released evaluator. |

## Acceptance scenarios

Execute the skill's documented commands in disposable fixtures, including paths with spaces.
Rerun matching setup and compare repository snapshots before and after every case.

## Property and invariant tests

Repeated setup reuses the verified environment.
No global command lookup replaces the selected absolute interpreter.
Inherited PYTHONPATH and an unrelated global harnessctl cannot affect identity; process-local PATH and explicit identity roots select the installed entry point.

## Static and architecture checks

Confirm instructions use existing commands, not a new bootstrap executable.

## Security and privacy checks

Reuse interpreter-safety negative cases from SPEC-REB-011 rules 1–11 and SPEC-REB-015.

## Performance and resilience checks

Record setup and matching-reuse durations; incomplete installation never becomes ready.

## Manual assessments

Protocol fixtures cover Windows and Linux command construction, including no-Python bootstrap discovery.
Run available Windows, Linux, and macOS environment cases, including Python 3.11; record the exact released evaluator and unavailable combinations.
Live host support requires separately accepted profile evidence.

## Evidence retention

Retain transcripts, identity results, wheel provenance, and snapshot comparisons under `evidence/WO-PLG-002/`.

## Residual uncertainty

These checks establish environment preparation, not repository adoption or native host activation.
