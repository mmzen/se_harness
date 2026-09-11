# Evidence skill portable command replay

This suite replays the **82 already selected Windows commands** from the
independent WO-PLG-011 observation. It tests portable command behavior, native
commit/evidence bindings, and observed mutation footprints. It does not ask a
new model to select actions. The 17 negative spans replay the observer's empty
sequences; their unchanged hashes are not new Linux model-refusal evidence.

`fixtures/provenance/REPORT.md` retains the independent instruction observations,
their original limitations, and the failed original capture-footprint oracle.
Each frozen batch has a manifest containing exact argv, expected process exit,
expected paths/state, original record SHA256, and SHA256 for every copied input.
`capture_traces.py` freezes explicitly named records; it does not select actions.

Use a verified external released 0.16.0 evaluator environment. The actual run
used Ubuntu 24.04 / WSL2, Python 3.12.3, and the independently verified evaluator
under `work/plugin-linux-evaluators-20260910/0.16.0`. Run all Python scripts with
that environment's `bin/python -I`. No evaluator source, Windows environment,
Windows managed lock, or Windows `.git` is copied into the native baseline.
Later disposable repositories copy native Linux C/G fixtures only.

Set `PY` to that interpreter, `HERE` to this directory, and `OUT` to a new
absolute disposable directory outside this source directory. Initializing the
baseline and completing each row uses this command form:

```sh
"$PY" -I "$HERE/run_replay.py" --bundle "$HERE/fixtures/BUNDLE" \
  --output "$OUT" --batch BUNDLE ADDITIONAL_ARGUMENTS
```

Run these fixed batches in order. A batch must not be reused after it writes a
result; retained failed attempts require a fresh output or fresh target name.

| BUNDLE | ADDITIONAL_ARGUMENTS |
|---|---|
| setup-original | (none; creates OUT and native baseline) |
| capture | `--continue-existing` |
| governance | `--continue-existing` |
| lost | `--repository lost-repository --clone-fixture clean-candidate-input` |
| uncertain | `--repository uncertain-repository --clone-fixture clean-candidate-input` |
| dirty | `--repository dirty-repository --clone-fixture clean-candidate-input` |
| handoff | `--repository handoff-repository --clone-fixture clean-candidate-input` |
| release | `--repository release-repository --clone-fixture capture-repository` |
| unauthorized | `--repository unauthorized-repository --clone-fixture clean-candidate-input` |
| unauthorized-release | `--repository unauthorized-release-repository --create-repository-by-replay` |
| no-context | `--repository no-context-repository --clone-fixture clean-candidate-input` |
| corrected | `--repository corrected-repository --clone-fixture clean-candidate-input` |
| partial | `--repository partial-uncertain-repository --clone-fixture clean-candidate-input` |

Then replay the fixed local external-control tool and observation spans, test
input integrity, and audit the retained results:

```sh
"$PY" -I "$HERE/run_external_replay.py" --bundle "$HERE/fixtures/external" \
  --replay-root "$OUT" --output "$OUT/external-results"
"$PY" -I "$HERE/check_input_integrity.py" --bundle "$HERE/fixtures/setup-original" \
  --output "$OUT/input-integrity"
"$PY" -I "$HERE/audit_replay.py" --output "$OUT" \
  --external "$OUT/external-results"
```

`prepare_platform.py` separately records actual installed identity/help and
source SPEC/VER inputs. The runner verifies fixture input hashes before target
creation and verifies the complete prior target checkpoint before continuing.
Git global/system configuration is isolated and optional index refreshes are
disabled. All actual `.git` changes still remain in snapshots and raw traces.

Each actual call logs argv, stdin, cwd, stdout, stderr, process status, timing,
and complete before/after file digests. Expected mutation-path comparisons
exclude only platform-specific `.git` names; those files remain fully logged.
Generated `target/harness-dashboard` paths are **not filtered**. Only their
64-hex content filename segment is normalized when comparing across platforms;
directories, extensions, and output counts are compared, and actual filenames
and bytes are retained. Every capture wrote the VREC, evaluator sidecar, and
14 dashboard files. This command-replay match does not retroactively pass the
original record/sidecar-only oracle. The fresh `corrected` group uses the
separately fixed broader expectation.

`retain_observations.py` consumes these runs' actual process records, including
success, injected failure, and explicitly unrun probe. Native C and evidence
digests therefore differ from Windows. The runner records explicit native
bindings before capture/release; fixed identities, rights and paths are retained.
It never infers a new authority decision. The preverified release input is an
explicit fixture edit, not an exercised assurance transition.

`project_action.py` is the independent observer's hash-pinned fixed control
fixture. All invocation/effect logs and refs/registry state belong to local
JSON directories. Five wrong-input/failed-gate probes, two successful simulated
calibrations, an actual evaluator integration check, and the exact positive
simulated merge are replayed. No live CI, GitHub, registry, credentials, merge,
publication, or universal shell/API control is tested.

Receipt-loss replay executes the original once-only capture/readback sequence;
receipt suppression was part of the original model observation. Unavailable
inspection is a deliberate exit-13 helper. `partial` copies the actual native
corrected VREC alone and omits its evaluator sidecar, exactly as the recorded
injection did. These do not test in-flight crashes, atomicity, or a fresh model's
recovery decision. Native host hook activation is also outside this replay.

The original invalid requirement enum and actual refusal precede the fixed
correction in every fresh run. Actual run evidence additionally retains two
runner/setup mistakes: attempt1's post-capture assertion used the wrong TOML
field, then a fresh attempt2 passed; the initial external run lacked the newly
added partial fixture and stopped before commands, then a fresh external output
passed after the recorded partial setup. Neither is a candidate failure.

The replay recorders were subsequently corrected to retain command timeouts and
launch errors. Error traces contain partial output, an unavailable process exit
(`null`), error class, timing, original-record binding, and observed after-state
and effect deltas. The batch still fails. The default command timeout stays at
60 seconds; `--command-timeout` selects a finite positive duration for a probe.

Run the focused recorder checks in a fresh external directory:

```sh
"$PY" -I "$HERE/check_recorder_errors.py" --output "$OUT/recorder-error-probes"
```

These six checks use real local processes: timeout after output and a sentinel
write, a nonexistent executable, and a normal control for each runner. They test
recording only and supply no evaluator, model-refusal, or lifecycle evidence.
The original 82-command acceptance replay used `run_replay.py` SHA256
`76bb855bdabb2280c99d6a708948f1f3ce12b6cb5f300fa923e13c4968956244` and
`run_external_replay.py` SHA256
`571a4f59b55882d0254dad92b720fa353efd32911e87e83e6ce51f46bf57e57c`.
Those executed bytes and records remain preserved; the fault-probe report binds
the corrected recorder sources separately.
