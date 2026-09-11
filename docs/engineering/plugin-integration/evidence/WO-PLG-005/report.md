# WO-PLG-005 interim implementation report

WO-PLG-005 remains **in_progress**. This candidate implements the selected Codex transport and has focused test evidence; it is **not qualified** under VER-PLG-005. No C01–C12 case currently has a passing live acceptance result. Verification, completion, release and publication are not claimed.

## Implementation and identity

`plugins/verity-plane/codex/` contains the native manifest, generated synchronous inline PowerShell guards, and the Codex dispatcher. The guards reject unsupported profile/decision selections before invoking Python, preserve an independently registered event for malformed-input refusal, and give explicit missing-runtime guidance. The dispatcher calls the unchanged shared handlers with the absolute selected Python, `-I -B`, released 0.16.0 identities and fixed context/timing bounds. It returns only the supported deny/context envelopes and rejects empty context, authority-granting decisions and unknown fields. Unsupported tools receive an explicit coverage-gap message.

The profile is confined to DEC-PLG-001's Codex 0.153.4, Windows, Python 3.14.6 and evaluator 0.16.0. Profile labels and selected decision fields are eligibility inputs, not evidence of a running host or new artifact authority. `preparation/accepted-profile/identity.json` retains the selected real executable/version/digest. The root's governing released evaluator remains 0.17.0; neither shared components nor approved SPEC/VER/DEC definitions were amended.

`tests/plugin_integration/codex_adapter/` contains focused transport and observer tests, disposable repository/package preparation and a prepared read-only app-server observer. The observer uses the accepted process observer, refuses every incoming server request without answering it, and requires exact package/cache and enabled/trusted binding identities before thread work. It does not contain an edit or setup mode. The loaded-payload comparison excludes no files. The prior process-local plugin-disable attempt did not disable the old probe hooks; native review subsequently disabled those two hooks, as preserved in the incident record.

The checked historical package selects committed source `ab8d6e2049f87a2d5f1820590f86dfaafdf40416` and bundles the released 0.16 wheel. `preparation/package-02/package.json` retains its archive digest and every payload digest. The unchanged assembler's build and independent check passed; native marketplace/plugin installation succeeded. That package predates the guard's pre-Python eligibility fix, and is now stale relative to this interim candidate. It cannot prove qualification of the changed adapter. A fresh checked package and actual native loaded/trusted identity are still required.

## Checks and retained failures

The explicit focused command is the external 0.16 environment's Python with `-I -B -m unittest discover -s tests/plugin_integration/codex_adapter -p test_*.py -v`. `checks/focused-interim-01/` records seven passing tests and `checks/focused-interim-02/` records eleven passing tests; `checks/focused-interim-03/` records twelve passing tests after the payload comparison was added. Top-level discovery alone does not discover these tests. These are boundary/calibration checks, not substitutes for the real-host scenarios below. Parent-coordinated broad checks and CI remain separate.

Released evaluator 0.17.0 generated the handoff evidence packet and passed the handoff checkpoint against `origin/main` at `78cd64df7c130a6f42ab357836093db30f710753`. `checks/interim-handoff-01/` retains both commands and outputs; the bound formal snapshot is `adcc15b6639b67810dd01e44d67204feeef49a4051759c6d659a6678aadf1716`. This checkpoint does not complete the work or qualify unrun cases. Its separate delegated-completion gate lookup was unavailable under the restricted network; no completion decision was attempted. Evidence ordering is the actual interim handoff ordering, not a claim about the initial edits.

The first package attempt used a forbidden destination for the dispatcher. Its failure is preserved in `preparation/package-01/`; the corrected existing `scripts/` destination is in the successful later package. The initial pre-action checkpoint ordering deviation, original failed path arguments and passing correction are preserved in `checks/pre-action-after-initial-edits/`. No checkpoint is falsely described as preceding the initial edits.

The generic Plugin Creator validator could not start with either the selected external Python or the bundled authoring Python because both lacked PyYAML. Both actual failures are in `checks/generic-plugin-validator-01/` and `-02/`; no package installation was attempted to repair those runtimes. Static inspection of the retained validator identity's `validate_manifest_shape` allowlist shows it also excludes the accepted native `hooks` key. This is a generic-authoring-validator limitation, not a native-host validation pass. The parent explicitly retained DEC-PLG-001's native route; the accepted key was not removed to satisfy a different validator.

## Acceptance status

Each status below is **unavailable**, meaning the required complete case has not been run against this candidate. No absence of evidence is interpreted as prevention.

| Case | Available preparation/calibration | Remaining evidence |
| --- | --- | --- |
| C01 | Historical package build/check and native install | Current package-to-loaded-payload mapping, actual active bindings and shared skill resolution |
| C02 | Absolute argv mapping and prepared read-only observer | Actual startup, resume, compaction and complete delivered-byte/digest receipts |
| C03 | Shared handler selected for native apply_patch | Real permitted/refused edits, ordered events and independent effects |
| C04 | Trusted binding event, malformed data and strict output calibration | Complete retained accepted-test-route case and host-visible responses |
| C05 | Explicit coverage/unready output; historical disabled old probe hooks | Required-binding absence and shared-script-failure host observations |
| C06 | Native shell Unicode/quotes/absolute argv calibration | Real supported and unsupported host calls with input comparison |
| C07 | Shell negative selection refuses before fixture dispatcher runs | Complete qualification attempt with actual selected decision/state/spawn snapshots |
| C08 | Missing-binding/runtime guidance calibration | Startup before setup/after removal/wrong evaluator identity observations |
| C09 | Fixed synchronous 30-second host and 8-second inner budgets | Real failed/interrupted/stalled children, full transport/host-denial timing and zero effects |
| C10 | No assumed fail-closed claim | Actual host timeout and independent pending-edit effects |
| C11 | Invalid/empty shared-output calibration | Actual missing/unstartable guard and invalid-output effects/blocking control |
| C12 | Static synchronous mode and budget checks | Loaded asynchronous/insufficient-budget variants and rejected qualification |

## Native menu incident and boundary

`preparation/native-menu-deviation-01/README.md` records the actual sequence: batched navigation unintentionally selected Windows sandbox setup; Ctrl-C displayed shutdown, but a later scoped observation found the owned process still active and two newly created, empty disposable sandbox directories. Parent-authorized containment revalidated the full known ancestry and stopped only the exact owned Codex process; its helper and shell exited, and the PTY completed with exit status 1.

The historical still-active observation remains intact. No elevation approval was accepted, but the evidence does **not** establish whether a short-lived/detached setup helper or any operating-system security change occurred. No absent-OS-effect claim, silent undo, or settings alteration is made. No acceptance case passes because of that interaction. Further UI/setup/security operations are not authorized by this report. The parent may allow only the bounded reviewed read-only app-server observation; stale/untrusted bindings must stop it before thread or model work.

The next work is to retain the allowed read-only inventory result, then resolve the exact current-package/trust prerequisite through the accountable parent before broader live qualification. This report leaves lifecycle state unchanged.
