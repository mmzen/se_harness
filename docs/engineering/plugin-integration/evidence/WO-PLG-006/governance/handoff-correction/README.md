# Draft handoff checkpoint correction

Initial PR #456 `validate` job 103395218289 in run 34639430402 failed at
candidate `4549f19f562841f461961a21a83c02bd194a9d36`: QGP-G4I-EVIDENCE required
a handoff packet for formal snapshot
`d486c36a30fdc1eeec9d0169de12a6a270105cdb20f874ce5f788496fb30742e`.
The scope and preflight checks passed; qualification was skipped by that job.

`initial-job.json` and `initial-job.log` are scoped copies of the parent's GitHub
API captures, serialized as UTF-8 text lines by PowerShell. No raw HTTP byte
identity is claimed. The failure remains retained.

Correction used the external released 0.17.0 evaluator:

```
../se-harness-plugin-eval-017/Scripts/python.exe -I -B -m se_harness evidence . --artifact WO-PLG-006 --checkpoint handoff --json
../se-harness-plugin-eval-017/Scripts/python.exe -I -B -m se_harness check . --artifact WO-PLG-006 --checkpoint handoff --from-git origin/main --json
```

The authored packet explicitly records incomplete live acceptance and an
in-progress draft. This is evidence for review, not a lifecycle transition or
claim that the adapter is qualified. `evidence-result.json`, `check-result.json`
and `check-stderr.txt` retain the correction commands' results.

`initial-job-log-text.json` preserves the original serialized log text. The
readable `.log` projection trims trailing whitespace only; its original bytes
were not an HTTP-wire capture. Handoff check completed with exit 0; live GitHub
gate retrieval was unavailable in the default network sandbox, so no delegated
completion authority was inferred.
