# WO-PLG-007 implementation evidence

WO-PLG-007 is **in progress**. The operator authorized its execution on
2026-09-10. This delivery contains the shared session handler, its acceptance
fixtures, and the D04 definition introduction from PR #416. Completion and
independent assurance have not been recorded.

## Result

The handler runs the prepared released evaluator's `identity` and `doctor`
before returning the complete managed gate and harness router. Startup, resume,
and compaction repeat those checks. A source change triggers revalidation.
When the hook is too small, a complete read uses the same script, repeats the
checks, and refuses a stale content hash.

The [invocation and test guide](../../../../../tests/plugin_integration/session_context/README.md)
defines the explicit host inputs and complete-read transport. The handler is
read-only. It neither installs components nor records authority or readiness.
Actual host receipt is distinct from preparing complete output.

## Acceptance

[All eight cases passed](acceptance/final/summary.json) with Windows,
Python 3.14.6, and released evaluator 0.17.0. The runner fixes the published
version, payload and archive identities before invoking candidate code.
Each case retains independent source bytes, actions, raw stdout/stderr,
expected/observed results, and repository inventories.

| Cases | What was observed |
| --- | --- |
| [C01](acceptance/final/C01/observations.json) | Exact complete gate/router bytes in both captured host protocols; identity and doctor precede delivery. |
| [C02](acceptance/final/C02/observations.json) | Wrong identity, modified gate, and modified router refused with evaluator findings. |
| [C03](acceptance/final/C03/observations.json) | Fresh checks on resume/compact reject changed runtime or source; restoration succeeds only after rechecking. |
| [C04](acceptance/final/C04/observations.json) | A 2,500-byte direct capacity requires a complete read, bound to the expected content digest. |
| [C05](acceptance/final/C05/observations.json) | Missing or insufficient fallback capacity blocks; a simulated truncated/interrupted receiver rejects partial output. |
| [C06](acceptance/final/C06/observations.json) | Line endings changed after a real doctor call cause identity and doctor to run again; the old fallback hash is refused. |
| [C07](acceptance/final/C07/observations.json) | The OS refuses a missing interpreter; no handler output or verification result is invented. |
| [C08](acceptance/final/C08/observations.json) | Repeated events leave repository bytes unchanged; path escapes and unrelated synthetic credential content do not enter context. |

The [ten focused boundary tests](checks/focused-win311-final/stderr.txt) also pass on
provided Python 3.11.9. They inject evaluator results for malformed data,
nonboolean success values, marker damage, continuously changing sources, and
environment isolation. They are not substitutes for the real-evaluator cases.

## Repository checks

- [Managed integrity](governance/session-final-doctor.json): passed with released 0.17.0.
- [Graph validation](governance/session-final-validate.json): zero errors.
- [Release-distribution validation](checks/release-distributions/stdout.txt): passed, no distribution built.
- [Candidate CLI help](checks/candidate-help/command.json): passed.
- [Scope](governance/session-staged-scope.json) and [handoff](governance/session-handoff-ready.json): passed; WO-PLG-007 remains in progress.
- Full repository regression results will be retained before final handoff.

The initial WSL invocation was refused by the local sandbox before any tests
started. The authorized retry uses the already installed WSL Python. Both the
launch failure and final regression result are retained separately.

`acceptance/attempt1` and `attempt2` are preliminary observations. Diagnostic
rendering changed during the second run, so neither establishes acceptance of
the final script. Only `acceptance/final`, run without implementation edits,
is the acceptance result for the retained handler digest.

## Authority and limits

[Packet provenance](governance/packet-source.json) identifies the reviewed source
commit and every imported definition. The released evaluator recorded the
approved shared definitions and WO-PLG-007's approval/start. The first incomplete
definition preview was refused; its failure is retained beside the corrected
preview and applied result. No blocked preview was applied.

DEC-PLG-001 and DEC-PLG-002 accept only the previously tested Windows activation
routes. WO-PLG-005/006/008/014 remain draft in this delivery. Their definitions
do not authorize implementation here. Existing artifacts already on `main`
were not replaced with older drafts from PR #416.

This evidence qualifies shared-handler fixtures. C05 injects failure at the
receiver; the handler cannot observe a host's later truncation. It reports
`complete-output-prepared`, and the receiver requires the full content and end
marker. Production bindings must separately qualify capacity, full-read support,
startup/resume/compaction transport, and failure behavior under WO-PLG-005/006
and WO-PLG-015. No live plugin support or universal enforcement claim is made.

No completion, verification record, assurance, release, or merge decision is
included. The next lifecycle handoff is derived from the released evaluator.
