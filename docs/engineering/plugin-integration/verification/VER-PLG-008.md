+++
id = "VER-PLG-008"
type = "verification"
title = "Supported tool-action enforcement acceptance"
status = "approved"
owners = ["assurance-owner"]
created = "2026-09-08"
updated = "2026-09-10"

[relations]
verifies = ["REQ-PLG-013", "REQ-PLG-014"]

[[lifecycle_events]]
from = "draft"
to = "approved"
decided_at = "2026-09-10T06:11:30Z"
decided_by = "assurance-owner"
reason = "The operator explicitly approved the reviewed plugin packets in this task: \"i approve the packets, i authorize the work\". On 2026-09-10 they selected \"we will merge later: GO for WO-PLG-007  and then WO-PLG-008\" after deciding DEC-PLG-001 and DEC-PLG-002 for the tested Windows activation routes. Record only the named definitions decision for the D04 governing chain or WO-PLG-007, from reviewed proposal 0b42325b. Sibling work-order states, completion, assurance, release and merge remain separate."
+++

# Verification Contract: Supported tool-action enforcement acceptance

## Independence

The assurance owner fixes allowed/refused effects from the installed evaluator contract and expected wire behavior from the assessed host documentation. Inspect target bytes and effect counts independently of handler output.

## Requirement-to-evidence matrix

| Requirement | Method | Cases | Pass condition |
| --- | --- | --- | --- |
| REQ-PLG-013 | test, inspection | C01–C03, C06–C10 | Current checks precede effects; inner failures produce timely refusals; missing enforcement cannot pass qualification. |
| REQ-PLG-014 | test, inspection | C04, C05, C07–C09 | Refusal-capable routes refuse; missing/unenforced routes remain explicit gaps with observed effects. |

## Acceptance scenarios

Each case retains `actions.txt`, `stdout.txt`, `stderr.txt` and `observations.json` under `evidence/WO-PLG-008/Cnn/`. These are evidence files, not plugin APIs. Fix host timeout, inner deadline and margins before testing; never derive expected denial from candidate output.

| Case | Starting fixture | Action | Observable result | Evidence |
| --- | --- | --- | --- | --- |
| C01 | Approved WO; mapped in-scope edit; target sentinel | Replay the captured host event through check-tool-action.py | Current artifact/checkpoint/path reach the evaluator before the permitted fixture effect | event; argv/result; ordered effects; target hashes |
| C02 | Mapped edit outside approved scope | Request fixture edit | Supported denial precedes execution; target hash unchanged and effect count zero | raw refusal; before/after SHA-256; effect count |
| C03 | Running handler; separately failed evaluator, stalled child, interrupted evaluator | Attempt mapped effect; trigger inner deadline before host timeout | Evaluator process tree stopped and exits collected within reserved margin; valid denial reaches host before timeout; target unchanged, effect count zero; partial check writes reported | child/process trace; deadlines/timestamps; raw denial; target/check-output hashes |
| C04 | Malformed or ambiguous governed event; refusal-capable protocol | Replay missing fields and ambiguous shell writes | Response refuses and reports unavailable coverage; target unchanged, effect count zero | events; refusal; hashes; effect count |
| C05 | Unmappable event; protocol cannot enforce refusal | Replay event and observe target independently | Output identifies unenforced route; actual target hash/effect count retained even if the effect occurs; no readiness or checked-success claim | protocol definition; output; before/after hashes; effect count |
| C06 | Prior pass; artifact, checkpoint or path then changes | Replay changed action | Fresh check uses changed inputs; prior result cannot permit it | old/new argv; invocation count; result bindings |
| C07 | Spoofed path, recursion marker, unobserved tool or continuing shell session | Attempt unrelated governed effect through each gap | Marker grants no exemption; actual hashes/effect counts distinguish refusal from escaped or unobserved effects; escaped required refusal fails qualification | event/recursion traces; before/after target SHA-256; effect count; coverage conclusion |
| C08 | Handler hangs beyond host timeout; no accepted refusal reaches host | Let protocol fixture cancel the hook, then observe pending tool behavior | Host timeout recorded separately from inner expiry; actual effects inspected before retry; no guaranteed no-effect result; absent required denial fails qualification | host timeout/output trace; target hashes; effect count; refusal-observation flag |
| C09 | Guard fails to start, disappears after readiness, or produces invalid/missing refusal output | Attempt pending governed effect for each variant | No successful guard execution or denial inferred; target/effect observations retained; missing enforcement marks route unqualified | launch/host error; raw output; hashes; effect count |
| C10 | Inner budget plus startup/cleanup/output margins reaches or exceeds host timeout | Inspect binding configuration and attempt qualification | Invalid timing relationship refuses qualification; no claim that late output protects effects | configured budgets; rejection; qualification result |

## Property and invariant tests

C03 compares monotonic timestamps against the configured host deadline and confirms child termination before completion. C08/C09 never use empty hook logs as evidence of unchanged targets.

## Static and architecture checks

Map cases to PLG-HOOK-001–009 and ARCH-PLG-002/ADR-PLG-002. Verify synchronous bindings and exact host refusal schema. Both references document `hookSpecificOutput` with `hookEventName: PreToolUse`, `permissionDecision: deny` and `permissionDecisionReason`; arbitrary error exits are not substitutes.

## Security and privacy checks

Use disposable targets and synthetic spoofing inputs. Inspect effects outside the handler's own logs; retain no credentials.

## Performance and resilience checks

Retain event, startup, evaluator, cleanup, response and effect timestamps. C03 reserves measured response/cleanup time; required checks are never omitted to meet a deadline.

## Manual assessments

Captured protocol fixtures prove handler behavior only. Repeat C03/C08/C09 in VER-PLG-005/006 and VER-PLG-015 on each claimed host/version/platform. A handler that cannot start or whose output is discarded cannot establish refusal.

## Evidence retention

Retain fixed inputs, fixture revision, OS/Python/evaluator identities, argv, exit status, raw outputs and independent target observations. Record handler correctness and host-coverage qualification separately.

## Residual uncertainty

Claude command-hook timeout and start failure are non-blocking under its [reference](https://code.claude.com/docs/en/hooks#timeouts). The [Codex reference](https://learn.chatgpt.com/docs/hooks#pretooluse) documents denial forms and unsupported-output failure; timeout/start behavior still requires exact-profile observation. Inner deadlines reduce timeout risk without proving future availability or independent authorization.
