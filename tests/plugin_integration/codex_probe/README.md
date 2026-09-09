# Codex compatibility probe

Disposable observation fixtures for WO-PLG-003. These files do not implement the production plugin or make a support decision.

`probe.py` creates a local marketplace, installs the fixture into a separate Codex home, captures skill discovery and attempts a bounded model turn. `--local-only` omits that model turn. Every run needs a fresh sandbox. Use a fresh evidence directory when repeating an observation; retain earlier failures.

`observe.ps1` is the original file-based launch trial. Windows execution policy refused it in the assessed environment. `--inline` selects a separate native command embedded in the manifest; it never reads or evaluates that refused script. `observe_runtime.py` records the selected interpreter, released evaluator identity, `doctor`, and source bytes. It makes no production readiness claim.

`calibrate.py` invokes the fixture directly, creates a private environment using supplied Python, installs the exact local wheel offline, and checks missing/prepared/removed-runtime behavior. **Calibration is not evidence that Codex delivers an event or that an agent follows a skill.**

From this worktree, in PowerShell:

```powershell
$probePython = '..\se-harness-plugin-eval-016\Scripts\python.exe'
$probeCodex = 'C:\Users\mathi\AppData\Local\OpenAI\Codex\bin\8e5b6932251c2c1c\codex.exe'
$probeSandbox = '..\plugin-probe-sandboxes\codex\NEW RUN with spaces'
$probeEvidence = 'docs/engineering/plugin-integration/evidence/WO-PLG-003/NEW RUN'
& $probePython -I tests/plugin_integration/codex_probe/probe.py --codex $probeCodex --sandbox $probeSandbox --evidence $probeEvidence --inline --local-only
& $probePython -I tests/plugin_integration/codex_probe/probe.py --codex $probeCodex --sandbox $probeSandbox --evidence $probeEvidence --schemas-only
& $probePython -I tests/plugin_integration/codex_probe/probe.py --codex $probeCodex --sandbox $probeSandbox --evidence $probeEvidence --app-server
& $probePython -I -m unittest discover -s tests/plugin_integration/codex_probe -p 'test_*.py' -v
```

`--network-retry` runs only the bounded model turn in an existing profile. It does not weaken Codex permissions. Network permission must be supplied by the outer execution environment when required.

For an authorized operator login, `login_isolated.py` uses the same profile and prints the official device flow directly to its terminal. Never redirect its output into evidence. Never copy a normal profile's authentication files. Complete hook trust separately through Codex's `/hooks`; no trust-bypass flag is used here.

The child process receives an allow-list of operating-system inputs and disposable HOME, USERPROFILE, CODEX_HOME, APPDATA, LOCALAPPDATA and temporary paths. It does not inherit account-token variables, PYTHONPATH, or the normal PATH. This is profile isolation, not a claim to override enterprise policy.

On Windows, `processes.py` assigns a suspended child to a private job before starting it. Timeout and app-server cleanup stop that job's processes, including descendants of an already-exited parent. No process-name matching, execution-policy change, or permission-bypass flag is used. The process-group fallback for other platforms is not qualified by this Windows run.

See the [current evidence report](../../../docs/engineering/plugin-integration/evidence/WO-PLG-003/report.md) for completed observations and remaining live cases.

## Authenticated continuation

`interactive_isolated.py` opens the real CLI against an existing disposable profile. Review each changed hook through the built-in hook UI. This helper does not alter trust records or complete Windows sandbox setup.

`upgrade_inline.py` retains before/after sources and uses the actual plugin update command. The observed Windows route uses `--native-inline`: a direct native command, without a second nested PowerShell invocation. `--readiness` additionally installs `observe_ready_runtime.py` and a marker-triggered test refusal. The requested sentinel write includes that marker; the predicate is not an exact-path or production command classifier.

`live_session.py` records actual app-server conversations, source snapshots, hook completion/context entries and cleanup. It normally requests a no-tools `READY` response. `--resume THREAD_ID --compact` uses the real persisted thread and waits for compaction and the following turn. `--setup-skill-missing` invokes the discovered setup skill with an actually absent selected interpreter path; it does not claim all machine interpreters are missing.

```powershell
& $probePython -I tests/plugin_integration/codex_probe/interactive_isolated.py --codex $probeCodex --sandbox $probeSandbox
& $probePython -I tests/plugin_integration/codex_probe/live_session.py --codex $probeCodex --sandbox $probeSandbox --evidence "$probeEvidence/fresh-start"
& $probePython -I tests/plugin_integration/codex_probe/live_session.py --codex $probeCodex --sandbox $probeSandbox --evidence "$probeEvidence/fresh-restoration" --resume ACTUAL_THREAD_ID --compact
```

`live_fixture_state.py` records direct observer preparation, source changes or removal of a disposable interpreter. Preparation checks the pinned wheel digest before installation. These direct actions do not substitute for C07's model-origin shell tools.

For C07, `live_session.py --tool-setup-probe` requests only fixed disposable setup commands. `--approved-setup` reuses the operator's existing explicit authorization through one-shot approvals of exact commands and the named fixture skill read; mismatches are cancelled. It never grants an execution-policy amendment. `--tool-stage complete` finishes a previously observed install; `--tool-stage repair` repairs a removed interpreter. Each stage requires a new evidence directory and the expected existing runtime state.

`--tool-environment-name` selects one plain directory name inside the fixture's plugin-data directory. A complete repeated sequence can therefore start with a genuinely absent environment. `--inventory-static-profile PATH` records only size, modification time and presence of named config/auth inputs and plugin manifests; it never reads credential contents or session databases. The same run also records the complete controlled repository's file hashes before and after.

The readiness observer calls the installed released evaluator's identity, doctor, preflight and checkpoint-free check. It relays actual readiness and the returned reading manifest for six synthetic fixture artifacts. Their approved-status fields are controlled test inputs, not real approval transitions. Successful observations do not authorize production work or establish support.
