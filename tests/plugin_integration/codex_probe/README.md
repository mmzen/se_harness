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
