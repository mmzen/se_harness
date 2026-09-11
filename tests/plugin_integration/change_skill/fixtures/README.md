# Observed command replay inputs

`observed/manifest.json` captures explicit argv arrays and expected process
exits, mutation paths and state projections from the independent Windows
acceptance run on 2026-09-10. Each command records its original transcript path
and SHA-256. The copied oracle, decisions and artifact bytes were fixed by that
run before candidate behavior. `capture_observed_inputs.py` constructs this
package from that evidence; it neither runs nor chooses lifecycle operations.

`run_workflow_replay.py` runs these sequences with external released evaluator
0.16.0. It creates a new disposable repository through that platform's actual
installer, then copies only authored fixture artifacts and two source inputs.
It never copies a Windows managed lock, environment, or Git directory. The
original reserved `acceptance` domain fixture defect remains documented;
work-order cases use the independently corrected `demo-change` fixture and its
exact reviewed hash. Raw bytes are preserved across Git checkouts.

The runner records actual calls, stdout, stderr, exit status and before/after
hashes. Setup calls are separate from replay calls. The two recorded
`QGP-G4I-EVIDENCE` failures remain expected observations. Feature evidence is
derived from this replay's command records, never copied Windows pass claims.
The corruption case rejects changed fixture inputs before creating a target.

For Linux, run with the verified external evaluator's absolute Python path:

```text
EVALUATOR/bin/python -I -B run_workflow_replay.py --sandbox NEW_DISPOSABLE_DIR --source SOURCE_CHECKOUT --wheel VERIFIED_LOCAL_016_WHEEL
```

Linux readiness recovery executes the setup reference's exact Bash block with
the already available wheel, then invokes the actual shared context handler.
No network or native host activation is used. A successful context contains its
complete end marker and leaves target files unchanged.

These are command replay regressions, not new model-behavior experiments.
CHG02/CHG06 empty mutation sequences and CHG10's unready observation are replayed
as unchanged-hash observations; they do not prove a new agent would refuse a
request. Prompt counts remain the original Windows observations and are not
invented by this script. Lost receipts are after-exit injections, with fixed
readback/recovery commands and retained actual writes. CHG07 live CI/delegated
lifecycle coverage is separate. No policy or authority selection is implemented.
