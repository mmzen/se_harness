# Codex probe: authenticated observations

**WO-PLG-003 remains in progress.** The operator completed isolated sign-in, and real Codex conversations now support the observations below. This report does not accept completion, verify a candidate, or select production support.

Assessed host: **Codex CLI 0.153.4 on Windows 10.0.26200 x86_64**, supplied Python **3.14.6**, released evaluator **0.16.0**. Linux and macOS were unavailable. The [earlier signed-out check](20260909-resumption/auth-status.json) remains historical evidence; it is no longer the current authentication state.

## Current coverage

These are behavioral observation cases for the recorded Windows routes. The security and inventory limits below still apply to the investigation as a whole. Each Cnn directory retains the original attempt under `initial/` when its index was updated; original host traces and failures remain available.

| Case | Observed result | Assessment |
| --- | --- | --- |
| [C01](C01/observations.json) | Setup-skill discovery, trusted startup, persisted-session resume and completed compaction deliver setup guidance with no prepared interpreter. | Pass for this route. |
| [C02](C02/observations.json) | The discovered setup skill gives prerequisite guidance and stops for an observer-confirmed absent supplied-Python path; no tool runs. | Partial. This is guidance/stop evidence, not an agent-executed prerequisite check. Older/unusable installations were unavailable. |
| [C03](C03/observations.json) | Two fresh authenticated sessions deliver the prepared evaluator's current governance text. | Pass. Both identity/doctor checks and successful host turns are retained. |
| [C04](C04/observations.json) | Resume and completed compaction deliver changed governance content. | Pass. Source hashes distinguish old and new content. |
| [C05](C05/observations.json) | Declining trust leaves hooks untrusted; later UI review grants trust. The file route fails, while the separately trusted native route runs. | Pass as a trust/activation observation. |
| [C06](C06/observations.json) | Paths with spaces, version changes, process restarts, stable plugin-data location and removed-interpreter guidance are observed. | Pass for process restart; no hot-reload claim. |
| [C07](C07/observations.json) | Real tool-driven setup and repair, actual test-write refusal, fresh evaluator readiness and a complete repository-inventory window. | Pass for the recorded fresh sequence; normal-profile measurement is bounded as explained below. |

## What the successful runs establish

The local marketplace installs the fixture and exposes `codex-probe:setup`. After review through `/hooks`, the actual native command receives startup, resume and compact events. Without a prepared evaluator, each event supplies setup guidance; missing Python is not credited with a successful handler result. See [startup](20260909-live/native-missing-start/) and [resume/compact](20260909-live/native-missing-resume-compact/).

The two prepared starts are [input-diagnostic-start](20260909-live/input-diagnostic-start/) and [prepared-start-2](20260909-live/prepared-start-2/). They use distinct real threads; both turns complete without an error. Their SessionStart hooks take **2.330 s** and **2.371 s**, respectively, and each delivers **7,858 characters** of context. The separate direct diagnostic is not one of these two host observations.

After the fixture's AGENTS.md changes, [resume and compact](20260909-live/changed-resume-compact/) deliver **7,927 characters** of fresh context. The [before/after sources](20260909-live/changed-source/) and timestamped evaluator observations identify the new content. Source-file hashes describe exact file bytes; host-delivered text matches after newline normalization. These are measured local runs, not a performance guarantee.

Removing the selected interpreter produces fresh [setup-required context](20260909-live/removed-start/), with no successful result attributed to that interpreter. Cache and persistent-data paths stay under the disposable profile across the recorded restarts.

The final [C07 sequence](20260909-live/complete-sequence-summary/) starts with a fresh external environment. Actual shell tools create the venv, install the exact local wheel offline and write the runtime pointer. Fresh SessionStart observations run the released identity, doctor, preflight and check commands: all exit 0, preflight reports `ready: true`, and the host receives the nine-file reading manifest. After the observer removes only that disposable interpreter, actual shell tools repair it, reinstall the pinned wheel and restore the pointer. Fresh readiness and context are observed again. All six setup/repair commands exit 0, with ordinary one-time approvals limited to the reviewed commands and paths.

The test hook refuses actual writes to the disposable sentinel before readiness. Sanitized extracts retain the real tool-call input and same-call error from the selected owned session traces; prompt text and model summaries are not the proof. Its marker-triggered predicate is deliberately a test fixture, not an exact-path production authorization classifier.

The fresh C07 comparison covers **49 controlled repository files** from before its first setup command through the final repaired-ready observation; all are unchanged. It also covers **20 positively statted, named normal-profile inputs**, using metadata only; those are unchanged. Five older negative metadata results cannot distinguish absence from an access error and are excluded from that claim. Plugin discovery was bounded and is not an exhaustive profile audit. A later explicit-stat capture records current state only; it does not retroactively establish those initial absences. Earlier setup attempts without the initial snapshot remain functional evidence, separately labeled.

## Failures and design implications

- The original file-based guard was refused by Windows execution policy during direct calibration. The later trusted live file route also fails with code 1. No execution policy or Windows sandbox setup was changed.
- A nested PowerShell command failed; the separately registered direct native command worked. Original [file](20260909-live/trusted-file-start/) and [nested-command](20260909-live/inline-missing-start/) failures remain retained.
- A prepared-runtime hook failed before writing a runtime observation. Changing the observer's input decoding to UTF-8 with optional BOM handling preceded a successful run. The original error/input does not establish the precise cause; decoding is an inference, not a proven host defect.
- Updating the referenced Python script while keeping the hook command identical retained the host's trusted state and definition hashes. This is evidence about **hook-definition trust**, not trust of every byte in the plugin payload. The exact updates and [UI observations](20260909-live/ui-review-actions.json) are retained.
- Initial empty-thread resume and compaction requests were not successful restoration tests. Actual persisted-thread resume, completed compaction and subsequent successful turns now provide that evidence.

## Evidence quality and remaining limits

Live records are under [20260909-live](20260909-live/). Transcripts retain actual requests, hook receipts, final turn status/errors, timings and owned-process cleanup. A notification being present, an accepted request, or model prose alone does not count as success. Direct [runtime calibration](calibration-inline-corrected/) and [readiness-module calibration](20260909-live/ready-module-calibration/) remain explicitly separate from host acceptance.

The [operator actions](20260909-live/operator-actions.json) and UI review actions are labeled observer transcriptions, not byte-exact terminal logs. The initial menu's final selection screen was not retained; the following machine response independently confirms untrusted hooks and no hook delivery. Later responses confirm trusted definitions and actual hook outcomes.

Authentication uses the existing disposable file store. Login output and credential contents are excluded. The runners select isolated profile paths and do not copy normal credentials. No normal-profile before/after inventory covers the earlier C01/C03-C06 windows; their repository snapshots also cover selected files only. The bounded fresh C07 comparison does not fill those earlier gaps. This is **not a whole-session filesystem audit**, and the security assessment retains that limitation.

The [supplied-runtime inventory](repository-checks/authenticated-continuation/supplied-runtime-inventory.json) records accessible Python 3.11.9 and 3.14.6 with importable venv/ensurepip. It is not a complete machine inventory or a simulation of older/broken installations. Unavailable variants and platforms are not counted as passes.

[Repository checks](repository-checks/) and the [36 passing observer tests](20260909-live/final-complete-fixture-tests/result.json) are separate from host acceptance. Their passing results do not authorize WO completion, VREC verification or a merge. The engineering owner retains the completion decision; production support remains a separate technical decision.

Reproduction instructions: [probe README](../../../../../tests/plugin_integration/codex_probe/README.md). Assessed sources include the installed executable's help/generated schemas, [plugin packaging](https://developers.openai.com/plugins/build/plugins), [hooks](https://learn.chatgpt.com/docs/hooks), [CLI commands](https://learn.chatgpt.com/docs/cli/slash-commands), and [authentication](https://learn.chatgpt.com/docs/auth).
