+++
id = "VER-PLG-008"
type = "verification"
title = "Supported tool-action enforcement acceptance"
status = "draft"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-08"

[relations]
verifies = ["REQ-PLG-013", "REQ-PLG-014"]
+++

# Verification Contract: Supported tool-action enforcement acceptance

## Independence

Expected allowed/refused effects derive from the installed evaluator contract. The assurance owner compares raw results and target changes independently of adapter classification.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-013 | test, inspection | C01–C03, C06, C07 | Current evaluator checks precede mapped effects; refused targets remain unchanged. |
| REQ-PLG-014 | test, inspection | C04, C05, C07 | Unmapped effects are refused where possible and otherwise explicitly identified as unenforced. |

## Acceptance scenarios

Each case creates new test evidence under `evidence/WO-PLG-008/Cnn/`: `actions.txt`, `stdout.txt`, `stderr.txt`, and `observations.json`; these are not plugin APIs.
`observations.json` records expected/observed values, exit status, source evidence paths and a pass/fail/unavailable conclusion. The Evidence column names additional captures.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Selected approved WO; mapped in-scope edit; target sentinel | Replay the captured host event through check-tool-action.py. | The evaluator receives the selected artifact/checkpoint/path before the fixture effect; the permitted target change follows its result. | event; evaluator argv/result; ordered effect log |
| C02 | Mapped edit outside the WO scope | Request the fixture edit. | The host-protocol refusal precedes execution; target SHA-256 and effect count remain unchanged. | refusal response; before/after hash; effect count |
| C03 | Required evaluator check fails, times out, or is interrupted | Attempt the mapped effect for each condition. | The failure is retained and no target effect occurs; failure is not converted into a checked-success response. | exit/timeout trace; raw response; target hash |
| C04 | Malformed or ambiguous governed event; refusal-capable protocol | Replay missing fields and ambiguous shell writes. | The response refuses the governed action and identifies unavailable coverage; effect count stays zero. | raw events; refusal; effect log |
| C05 | Same unmappable event; protocol cannot enforce refusal | Replay the event through that protocol fixture. | Output identifies the route as unenforced and does not claim readiness or checked success for that action. | protocol definition; output; observed effect log |
| C06 | Prior passing result; artifact, checkpoint or actual path then changes | Replay the changed action. | A fresh check uses the changed inputs; the earlier result is not reused to permit the new effect. | old/new argv; check invocation count; result bindings |
| C07 | Spoofed path, recursive check marker, unobserved tool or continuing shell session | Attempt an unrelated governed effect through each gap. | A recursion marker does not exempt the unrelated effect; observed refusals and unobserved routes are separately recorded, without universal-coverage claims. | event sources; recursion trace; effect/coverage logs |

## Property and invariant tests

C01–C04 establish effect ordering and unchanged refusal targets. C06 binds checking to current inputs; C07 limits recursion exemptions.

## Static and architecture checks

Map cases to PLG-HOOK-001–006 and ARCH-PLG-002/ADR-PLG-002. Retain evidence that checks call the released evaluator rather than copied policy.

## Security and privacy checks

C07 uses synthetic spoofing inputs. Do not treat an unobserved route as denied merely because its log is empty.

## Performance and resilience checks

Retain separate event, evaluator and effect timestamps, including slow refusals; never omit required checks from timing runs.

## Manual assessments

Use captured host-protocol fixtures with recorded OS/Python/evaluator versions. Real host interception and refusal require VER-PLG-005/006 and VER-PLG-015.

## Evidence retention

Retain each case’s fixture revision, argv, exit status, raw output and listed observations under `evidence/WO-PLG-008/Cnn/`.
Record expected and observed values separately, with a pass/fail/unavailable conclusion. Keep original failures and bind later assurance to the exact implementation candidate.

## Residual uncertainty

Fixture refusal proves the handler response, not independent external authorization. Issue #347 remains a separate control boundary.
