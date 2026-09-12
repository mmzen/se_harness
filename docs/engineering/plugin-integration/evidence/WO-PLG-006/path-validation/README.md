# Fully qualified Windows binding paths

Calibration against the previous packaged guard confirmed a defect:
`C:private plugin data/evaluator` and a root-relative `\Users\...\evaluator`
were accepted by IsPathRooted, normalized through GetFullPath and invoked the
selected Python. `pre-correction.json` retains those actual observations.

The corrected guard requires a complete drive-root or ordinary UNC-share root
before any path lookup or interpreter launch. Root-relative, drive-relative and
device-namespace inputs are rejected. Accepting the syntax of a complete UNC
root does not qualify a new UNC installation profile.

`post-correction.json` repeats both inputs against an explicitly labeled source
calibration copy: both produce a covered PreToolUse denial with
interpreter_invoked=false. The new focused regression uses a working receiving
script/marker control and checks ambiguous environment, repository, host,
configuration, plugin and event paths; no marker appears for rejected inputs.

This is a production guard change. Earlier acceptance-04/05 observations and
their package identities remain historical evidence for the earlier guard bytes.
They do not qualify the corrected guard. Fresh acceptance-06 repeats all C01-C12
against committed source `fd2419f4c26b9ba4d4a97f85b7d2b08da72b8626`, including
two real startup rejections for ambiguous paths and guard removal after verified
startup. The current canonical records and candidate-binding.json use those new
package bytes. C10/C11 remain failed/unqualified; no broader support is inferred.
