# Codex adapter acceptance

Run focused transport tests explicitly; top-level discovery does not descend
into this directory:

```text
<absolute-evaluator-016-python> -I -B -m unittest discover -s tests/plugin_integration/codex_adapter -p "test_*.py" -v
```

`fixture.py prepare` initializes a fresh disposable repository using released
0.16.0, applies explicitly synthetic fixture inputs and records fresh pre-action
evidence. It records the actual accepted host executable/version/digest. It
never copies credentials. The already authenticated WO-PLG-003 disposable
profile is selected explicitly. The initial process-local plugin-disable
override did not disable the old probe hooks. Those hooks were then disabled
through native `/hooks` review; every later run must inspect actual loaded state.

Commit package inputs before `fixture.py assemble --revision FULL_COMMIT`.
The unchanged WO-PLG-001 builder selects the released 0.16 wheel and runs both
build and independent check. The companion Claude manifest is deliberately
inert; only the Codex package is installed and assessed here. Native marketplace
installation and `/hooks` review retain host receipts without cache edits.

The [acceptance report](../../../docs/engineering/plugin-integration/evidence/WO-PLG-005/report.md)
maps current observations and historical attempts to VER-PLG-005 C01–C12.
Passing cases do not complete or qualify the adapter while required cases remain
unobserved or required enforcement fails. Original failed attempts and the
native-menu incident remain evidence; later successful runs do not erase them.

## Test routes

| Runner | Purpose and boundary |
| --- | --- |
| `calibration.py` | C04/C07 call the registered PowerShell command with synthetic inputs, positive sentinel controls and spawn/state snapshots. These are registered-shell tests, not pending native edits. |
| `live.py` | Native inventory, startup, resume and compaction through app-server. It fixes read-only/on-request permissions, checks the complete loaded package and bindings, and stops without answering any incoming approval request. |
| `edit_observer.py` | Native mapped-edit observations. Preflight is the default. Execution can accept at most one correlated update to the exact reviewed synthetic path and bytes. Missing or ambiguous patches, extra changes and other approval types stop the owned job. |
| `c05_runner.py` | Select a disabled SessionStart binding, retain actual native inventory and context observations, then restore and check the exact original configuration. C05's shared-script logical failure reuses the actual C08 wrong-identity capture. |
| `c08_runner.py` | Exercise an absent interpreter, a ready owned runtime, literal removal and a wrong evaluator identity. Shared evaluator environments remain untouched; original binding inputs are restored. |
| `c09_runner.py` | Exercise failed, interrupted and stalled evaluator children in a separately owned, explicitly instrumented fault runtime. `c09_fault_sitecustomize.py` selects only the reviewed evaluator-check call. This runtime is fault instrumentation, not a normal-runtime qualification. |
| `c10_c11_runner.py` | Exercise a stalled dispatcher and missing/truncated output in a distinct owned runtime. `c10_c11_fault_sitecustomize.py` requires the exact dispatcher invocation and synthetic patch. Retain native timeout/output, one-edit effects and final restoration separately from enforcement. |
| `c11_binding_loss.py` | Observe real readiness, disable only PreToolUse, then request one reviewed edit in a fresh session. Preserve the actual disabled inventory and its normal validation failure; restore the original configuration and confirm native inventory. This does not exercise OS shell-start failure. |
| `c12_binding_observer.py` | Observe separately invalid timeout and asynchronous bindings through native installation and inventory only. It starts no thread, grants no trust and edits no native cache. It restores the original source, native selection, full payload and bindings. |

Native runs require a reviewed concrete plan and exclusive ownership of the
disposable profile. Use a fresh evidence directory, record the plan digest and
retain restoration and owned-process cleanup. Preflight does not launch the
host or authorize execution. Existing operator consent for the bounded
public/synthetic test payload does not authorize a different payload, host
permission, setup operation or lifecycle decision.

`interactive.py` is reserved for separately reviewed native UI trust actions;
do not use it as an acceptance runner or automate menu navigation. Its retained
external stop/deadline controls do not resolve the earlier incident's unknown
historical operating-system effects.

A blocked native edit may emit no `fileChange` item. The edit observer's original
unavailable result is preserved in that case. A separate assessment may establish
refusal only from the actual native blocked status, matching dispatcher/evaluator
evidence, unchanged targets and confirmed cleanup. A prompt or unchanged target
alone is insufficient.

Direct guard and script tests are calibration. VER-PLG-005 C01–C12 additionally
need the specified native discovery, session restoration, tool effects and fault
observations. Canonical case files under the evidence directory index the original
nested commands, outputs and digests; they are not replacement raw output. No
missing run counts as passing, and rejection of an invalid configuration does
not prove that its hook executed or prevented an effect.

The current [qualification limit](../../../docs/engineering/plugin-integration/evidence/WO-PLG-005/qualification-limit.md)
records C10/C11 failed enforcement: the reviewed edit proceeded after timeout,
missing/invalid output or binding loss. Their observation runners may exit zero
when the negative capture is complete; that is never a passing enforcement
verdict. Literal OS shell-start failure remains unavailable. The original
Windows preview-decoding failure is retained under C11 preparation evidence.
