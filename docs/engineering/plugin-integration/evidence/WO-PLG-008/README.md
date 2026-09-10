# WO-PLG-008 implementation evidence

WO-PLG-008 is **in progress**. The operator authorized this work after
WO-PLG-007 on 2026-09-10. This delivery adds the shared before-tool handler and
its acceptance fixtures. Completion and independent assurance are not recorded.

## Result

The handler maps Codex `apply_patch` and Claude `Write`/`Edit` events to fresh
released `identity`, `doctor` and implementation `pre-action` checks. It passes
the selected work order and actual paths to the evaluator. Failures produce the
documented denial; a successful check preserves host permissions and grants no
additional authority.

The [invocation guide](../../../../../tests/plugin_integration/tool_action/README.md)
defines supported fields, fixed checkpoint, timing inputs and coverage gaps.
The handler reuses WO-PLG-007's runtime verifier without changing it. D04
definitions arrive through [PR #435](https://github.com/mmzen/se_harness/pull/435).

## Acceptance

[C01–C10 pass](acceptance/final2/summary.json) with provided Windows Python
3.14.6 and released evaluator 0.17.0. [Fixed identities](acceptance/final2/identities.json)
bind the handler, shared dependency, runner and fault helpers. Their bytes
were checked again after the run and remain unchanged.

| Case | Observed result | Rules |
| --- | --- | --- |
| [C01](acceptance/final2/C01/observations.json) | Real current checks precede a permitted sentinel effect in each captured host protocol. | PLG-HOOK-001, 002, 005 |
| [C02](acceptance/final2/C02/observations.json) | Real scope refusal; target hash unchanged and zero effects in both protocols. | PLG-HOOK-002 |
| [C03](acceptance/final2/C03/observations.json) | Separately failed, stalled and interrupted check processes produce timely denial. All four Windows processes exit, independent worker/child PID checks agree, and partial check writes remain inspectable. | PLG-HOOK-007, 008 |
| [C04](acceptance/final2/C04/observations.json) | Malformed, incomplete and ambiguous shell events receive coverage refusals; zero effects. | PLG-HOOK-003, 006 |
| [C05](acceptance/final2/C05/observations.json) | An unmapped event on a report-only route is unenforced. The fixture performs one observed effect; no checked-success claim. | PLG-HOOK-003, 004 |
| [C06](acceptance/final2/C06/observations.json) | Changed artifact and path each reach a fresh check. A caller-supplied checkpoint override is refused as unmapped; it cannot replace the fixed implementation checkpoint. | PLG-HOOK-001, 002, 005 |
| [C07](acceptance/final2/C07/observations.json) | Traversal, recursion spoofing and continuing-shell events are refused. An unobserved tool escapes the hook and produces one effect, recorded as unqualified. | PLG-HOOK-003, 004, 006, 009 |
| [C08](acceptance/final2/C08/observations.json) | A deliberately hung stand-in handler reaches the fixture host timeout. Missing refusal permits an observed effect; inspection records an unqualified route. | PLG-HOOK-009 |
| [C09](acceptance/final2/C09/observations.json) | Missing interpreter, removed guard, invalid output and empty output each leave refusal unobserved. Actual fixture effects are inspected and qualification fails. | PLG-HOOK-004, 009 |
| [C10](acceptance/final2/C10/observations.json) | Equal or excessive timing budgets are refused before evaluator invocation; zero fixture effects. | PLG-HOOK-007 |

Each case retains actions, raw stdout/stderr and independent target hashes and
effect counts. The runner uses synthetic work-order data inherited from the
retained WO-PLG-003 fixture, then prepares existing pre-action evidence through
the released evaluator. This setup does not exercise authority on a real work
order. C03 replaces only the final evaluator process; identity and doctor remain
real. Fault controls ship only with the tests.

[Fourteen focused tests](checks/focused-win311-final/stderr.txt) pass on provided
Python 3.11.9. They cover mapping, malformed data, path and hardlink boundaries,
refusal schemas, shared deadlines, and actual Windows process-tree cleanup.

## Timing and retained failures

The fixed fixture budget is 4 seconds of evaluator work, with 1 second for
startup, 2 for cleanup and 1 for output, below the 10-second host timeout.
[Measured host receipt](acceptance/final2/timing-observations.json) was
1.45–1.51 seconds for the two positive checks and 4.09 seconds for the stalled
check. The stalled tree's measured cleanup took about 1.2 milliseconds. The
test confirms cleanup inside its reserve and receipt before the host deadline.
These are observations on a small synthetic repository, not production latency
or an availability guarantee.

`acceptance/attempt1` retains the original C03 failure: its assertion expected
exactly two processes. The Windows virtual-environment launchers created four;
the trace shows all four exited. The correction requires at least the parent
and child, zero active processes, every observed process exited, and independent
PID inspection. No handler change or failed-check waiver was needed.

`acceptance/final` is the first passing corrected run. `acceptance/final2` is
the final runner: it additionally checks independent host receipt and the
cleanup deadline, and makes the C05 event explicitly unmapped. All attempts
retain their own source hashes and observations.

## Repository checks

- [Released doctor](governance/action-final-doctor.json): passed.
- [Released graph validation](governance/action-final-validate.json): zero errors.
- [Review preflight](governance/action-review-preflight.json): passed.
- [Release-distribution validation](checks/release-distributions/command.json): passed, no release distribution built.
- [Candidate CLI help](checks/candidate-help/command.json): passed.
- [Scope](governance/action-staged-scope.json) and [handoff](governance/action-handoff-ready.json): passed; WO-PLG-008 remains in progress.

Regression evidence is retained with the delivery as checks complete. No
passing regression or hosted verdict is inferred from this report.

## Authority and limits

The released evaluator recorded only the explicitly authorized approval and
start in this work order. [Delivery context](governance/delivery-context.json)
identifies the separate definition delivery and reserved decisions.

Process-tree control is implemented for Windows only. Other platforms return
unavailable coverage. A called handler denies unsupported routes; an unobserved
tool, missing handler or lost response cannot be assumed blocked. The independent
fixture deliberately fails open to expose that distinction. Its sentinel writes
do not reproduce native tool execution. C06 narrows checkpoint changes to
refusal of unsupported overrides rather than accepting arbitrary checkpoint
selection.

Production bindings and live interception remain WO-PLG-005/006 and
WO-PLG-015. Independent remote authorization remains issue #347. No lifecycle
completion, verification record, assurance, release, merge or universal
enforcement claim is included. The next lifecycle action comes from the
released evaluator's selected handoff.
