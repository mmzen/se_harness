+++
id = "VER-PLG-009"
type = "verification"
title = "Repository connection and discovery acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-015", "REQ-PLG-016"]
+++

# Verification Contract: Repository connection and discovery acceptance

## Independence

The assurance owner retains original repository bytes and expects results from inspected released installer behavior. Discovery is judged through actual host selection, not skill filenames.

## Requirement-to-evidence matrix

| Requirement | Method | Case/evidence | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-015 | test | New/existing target; explicit upgrade; customized managed file | Only the reviewed authorized installer operation changes the target; conflicts preserve files. |
| REQ-PLG-016 | test | Repository/plugin duplicate names and incompatible local contracts | One approved compatible implementation is active, or readiness is blocked without destructive migration. |

## Acceptance scenarios

Use disposable repositories and the selected released evaluator. Live coexistence acceptance requires resolution of DEC-PLG-004 and its supported route.

## Property and invariant tests

Compare owner content, managed digests and version lock before/after. A plugin-only update cannot silently upgrade the repository.

## Static and architecture checks

Review PLG-REPO-001 through PLG-REPO-005 against current installer contracts and SPEC-AEX-005. Verify examples against released command help.

## Security and privacy checks

Exercise conflicting target paths and customized files. No manual locked-file deletion or new installer behavior is accepted under this packet.

## Performance and resilience checks

Record setup operations and prompts. Reuse an unchanged covered request; rerun affected checks when the reviewed target or operation changes.

## Manual assessments

Observe actual host skill resolution on each claimed platform. A clean new repository alone does not qualify existing-repository migration.

## Evidence retention

Retain commands, outputs, failures and platform identities under `evidence/WO-PLG-009/`; bind the later verification record to the exact implementation candidate.

## Residual uncertainty

Existing ownership compatibility remains undecided until DEC-PLG-004 is disposed. Evidence described here is planned, not an executed migration result.
