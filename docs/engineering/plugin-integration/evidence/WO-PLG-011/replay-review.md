# Independent replay-tool review

A separate reviewer inspected the portable replay tools without changing them
or exercising assurance. The tools run actual released evaluator subprocesses
and compare their results with frozen Windows observations. Empty negative
command spans are explicitly labeled replay observations, not new model choices.

The review identified one recorder defect: a timeout or executable launch error
occurred before the per-call trace was written. Only the batch failure survived;
partial output and after-snapshots were missing. This affects failure retention
in the test tools, not the evidence skill's instructions or the already retained
successful calls.

Reviewed files and SHA-256 identities:

- `run_replay.py`: `76bb855bdabb2280c99d6a708948f1f3ce12b6cb5f300fa923e13c4968956244`
- `run_external_replay.py`: `571a4f59b55882d0254dad92b720fa353efd32911e87e83e6ce51f46bf57e57c`

The narrow correction must retain the actual error, partial output, unavailable
exit status and observed effects before failing the batch. Focused timeout and
launch-failure probes qualify that correction separately from the prior Linux
acceptance replay; original runner identities and observations remain retained.

The correction passed six real fault/control probes on each of Windows and
Linux: timeout after output and a target write, missing executable, and a normal
process for each recorder. Both failed paths retain a null process exit, actual
exception, output, snapshots and timings; the batch remains failed. See the
[report](acceptance/recorder-error-probes.json) and its retained per-platform
inputs/results. These are recorder probes, not evaluator or agent behavior.
After-state capture still requires the target to remain readable.
