+++
id = "VER-PLG-005"
type = "verification"
title = "Codex adapter conformance to accepted activation evidence"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-008"]
+++

# Verification Contract: Codex adapter conformance to accepted activation evidence

## Independence

Expected mappings come from SPEC-PLG-005, DEC-PLG-001 and the retained WO-PLG-003 host proof. Expected script effects come from SPEC-PLG-007/008.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-008 | test, inspection | C01–C08 | Observed discovery, invocation and refusal agree with the positively accepted host mapping. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-005/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Positive accepted route; packaged plugin; disposable host profile | Activate and resolve the shared skill names. | The host resolves the expected packaged skill paths; the report records package digest and active bindings. | discovery listing; manifest; package digest |
| C02 | Active adapter and current verified environment | Trigger startup, supported resume and compaction restoration. | Recorded argv invokes the absolute environment Python with -I and session-context.py; delivered bytes match the accepted session contract. | event/argv log; delivered content digest |
| C03 | Supported tool event; one permitted and one refused fixture edit | Request both edits through the real host. | check-tool-action.py runs before each effect; the refused edit leaves target bytes unchanged. | ordered event/effect log; before/after hashes |
| C04 | Event missing a required field, then malformed event data | Submit each event through the accepted test route. | The host-visible failure preserves the accepted mapping’s refusal/unready response; no successful check is reported. | raw event; script response; host response |
| C05 | Inactive required binding, then shared script returning failure | Attempt the covered session or tool operation. | Missing binding or script failure is visible; no integration-ready claim replaces the missing check. | binding state; exit status; host diagnostic |
| C06 | Paths and arguments containing spaces/quotes; an unsupported tool | Trigger supported and unsupported calls. | Supported argv boundaries match input exactly; the unsupported route is labeled as a coverage gap, without a checked-success result. | input/argv comparison; coverage output |
| C07 | Excluded or unaccepted host profile; changed decision status without a positive route | Attempt to qualify the production adapter. | No supported-profile result is issued; repository lifecycle states and helper-spawn log remain unchanged. | profile decision; result; state snapshots; spawn log |
| C08 | Thin host guard; interpreter absent, then present with wrong evaluator identity | Trigger startup before setup, after removal and with the wrong environment. | Absent runtime produces setup-required guidance without a Python call; existing runtime runs full identity/context checks and cannot report ready on identity failure. | guard output; interpreter invocation count; identity refusal; context output |

## Property and invariant tests

C02 and C06 compare complete argument arrays. C03 checks actual target bytes, not merely script exit status. C07 rejects empty or negatively selected support.

## Static and architecture checks

Retain a mapping from each host binding to its shared source under ARCH-PLG-002/ADR-PLG-002; no copied evaluator policy is accepted.

## Security and privacy checks

C03–C06 separate actual refusal from unsupported coverage. Keep external credentials out of disposable fixture logs.

## Performance and resilience checks

Retain event-receipt, script-start and script-end timestamps so adapter dispatch cost can be separated from evaluator time.

## Manual assessments

Run every positively accepted Codex/OS combination with recorded Python and evaluator versions. Offline protocol fixtures alone cannot satisfy C01–C06 live-host evidence.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-005/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

Native interception covers only the demonstrated host surface. Independent privileged-action controls in issue #347 remain separate.
