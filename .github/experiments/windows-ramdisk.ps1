param([ValidateSet('disk','ramdisk')][string]$Storage)
$ErrorActionPreference = 'Stop'
$root = if ($Storage -eq 'ramdisk') { 'R:\ownership-benchmark' } else { Join-Path $env:RUNNER_TEMP 'ownership-benchmark' }
if (Test-Path -LiteralPath $root) { throw 'Experiment destination must be fresh' }
New-Item -ItemType Directory -Path $root | Out-Null
$setupTimer = [Diagnostics.Stopwatch]::StartNew()
$source = Join-Path $root 'source'
function Copy-Tree([string]$From, [string]$To) {
    & robocopy $From $To /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NFL /NDL /NP /NJH /NJS /XD .git
    if ($LASTEXITCODE -ge 8) { throw "Copy failed: $From" }
}
& git clone --quiet --no-hardlinks --no-checkout $env:GITHUB_WORKSPACE $source
if ($LASTEXITCODE -ne 0) { throw 'Disposable clone failed' }
& git -C $source checkout --quiet --detach $env:RAMDISK_TESTED_COMMIT
if ($LASTEXITCODE -ne 0) { throw 'Fixed implementation checkout failed' }
Copy-Tree $env:RAMDISK_PY311 (Join-Path $root 'python311')
Copy-Tree $env:RAMDISK_PY313 (Join-Path $root 'python313')
Copy-Tree (Join-Path $env:RUNNER_TEMP 'candidate-dist') (Join-Path $root 'candidate-dist')
Copy-Tree (Join-Path $env:RUNNER_TEMP 'predecessor-dist') (Join-Path $root 'predecessor-dist')
$python311 = Join-Path $root 'python311/python.exe'
$python313 = Join-Path $root 'python313/python.exe'
$env:TEMP = Join-Path $root 'temp'
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
New-Item -ItemType Directory -Path $env:TEMP | Out-Null
$env:PYTHONNOUSERSITE = '1'
$env:PYTHONPATH = ''
$candidateWheel = (Get-ChildItem -LiteralPath (Join-Path $root 'candidate-dist') -Filter '*.whl').FullName
$predecessorWheel = (Get-ChildItem -LiteralPath (Join-Path $root 'predecessor-dist') -Filter '*.whl').FullName
$env:SE_HARNESS_OWNERSHIP_WHEEL = $candidateWheel
$env:SE_HARNESS_OWNERSHIP_SDIST = (Get-ChildItem -LiteralPath (Join-Path $root 'candidate-dist') -Filter '*.tar.gz').FullName
$env:SE_HARNESS_OWNERSHIP_SOURCE_MANIFEST = Join-Path $root 'candidate-dist/SOURCES.txt'
$env:REHEARSAL_HEAD_SHA = $env:RAMDISK_TESTED_COMMIT
$runner = Join-Path $root 'run-acceptance.py'
@'
import contextlib
import hashlib
import importlib.util
import json
import os
import pathlib
import platform
import sys
import traceback
import unittest
import time

test_path, mode, selection, output = sys.argv[1:]
test_path = pathlib.Path(test_path).resolve()
checkout = test_path.parents[1]
evidence = pathlib.Path(output).resolve()
assert not evidence.is_relative_to(checkout)
evidence.mkdir(parents=True, exist_ok=True)
assert mode in ("source", "package") and selection in ("smoke", "full")
os.environ["SE_HARNESS_OWNERSHIP_PACKAGE"] = "1" if mode == "package" else "0"
os.environ["SE_HARNESS_OWNERSHIP_EVIDENCE"] = str(evidence / "cases")
if os.environ.get("RAMDISK_TESTED_COMMIT"):
    os.environ["SE_HARNESS_OWNERSHIP_COMMIT"] = os.environ["RAMDISK_TESTED_COMMIT"]
if mode == "source":
    sys.path.insert(0, str(checkout))
wheel = pathlib.Path(os.environ["SE_HARNESS_OWNERSHIP_WHEEL"])
facts = {
    "schema": "se-harness-skill-ownership-ci-v1",
    "status": "incomplete", "mode": mode, "selection": selection,
    "argv": sys.orig_argv, "python": sys.version, "python_executable": sys.executable,
    "isolated": sys.flags.isolated, "platform": platform.platform(),
    "runner_os": os.environ.get("RUNNER_OS"),
    "runner_image": os.environ.get("ImageOS"),
    "runner_image_version": os.environ.get("ImageVersion"),
    "candidate_commit": os.environ.get("RAMDISK_TESTED_COMMIT"),
    "head_commit": os.environ.get("REHEARSAL_HEAD_SHA"),
    "run_id": os.environ.get("GITHUB_RUN_ID"),
    "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
    "wheel_name": wheel.name,
    "wheel_sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
    "test_module_sha256": hashlib.sha256(test_path.read_bytes()).hexdigest(),
    "source_inventory_sha256": hashlib.sha256(pathlib.Path(os.environ["SE_HARNESS_OWNERSHIP_SOURCE_MANIFEST"]).read_bytes()).hexdigest(),
    "source_archive_sha256": hashlib.sha256(pathlib.Path(os.environ["SE_HARNESS_OWNERSHIP_SDIST"]).read_bytes()).hexdigest(),
    "promotable": False,
}
runtime_path = evidence / "runtime.json"
runtime_path.write_text(json.dumps(facts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
passed = False
try:
    with (evidence / "test-output.log").open("w", encoding="utf-8") as log:
        with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
            import se_harness
            imported = pathlib.Path(se_harness.__file__).resolve()
            facts["imported_evaluator"] = str(imported)
            facts["candidate_version"] = se_harness.__version__
            if mode == "package":
                assert sys.flags.isolated, "installed acceptance requires -I"
                assert imported.is_relative_to(pathlib.Path(sys.prefix).resolve())
                assert not imported.is_relative_to(checkout), "checkout evaluator imported"
            else:
                assert imported.is_relative_to(checkout), "source evaluator was shadowed"
            spec = importlib.util.spec_from_file_location("ownership_acceptance", test_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = module
            spec.loader.exec_module(module)
            suite = module.acceptance_suite(smoke=selection == "smoke")
            class TimedResult(unittest.TextTestResult):
                def startTest(self, test):
                    super().startTest(test)
                    self.began = time.perf_counter()
                    print("CASE_START " + test.id(), file=sys.__stdout__, flush=True)
                def stopTest(self, test):
                    seconds = time.perf_counter() - self.began
                    facts.setdefault("case_seconds", {})[test.id()] = seconds
                    print("CASE_SECONDS " + json.dumps({"test": test.id(), "seconds": seconds}), file=sys.__stdout__, flush=True)
                    super().stopTest(test)
            started = time.perf_counter()
            result = unittest.TextTestRunner(stream=log, verbosity=2, resultclass=TimedResult).run(suite)
            facts["elapsed_seconds"] = time.perf_counter() - started
            passed = result.wasSuccessful() and result.testsRun > 0
            facts.update(status="pass" if passed else "fail", tests=result.testsRun,
                         failures=len(result.failures), errors=len(result.errors),
                         skipped=[{"test": str(test), "reason": reason} for test, reason in result.skipped])
except BaseException:
    facts["status"] = "error"
    facts["error"] = traceback.format_exc()
    raise
finally:
    runtime_path.write_text(json.dumps(facts, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(json.dumps(facts, sort_keys=True))
raise SystemExit(0 if passed else 1)
'@ | Set-Content -LiteralPath $runner -Encoding utf8
$testPath = Join-Path $source 'tests/test_skill_ownership.py'
Set-Location -LiteralPath $source
$runtimes = @{}
foreach ($pair in @(@('311', $python311), @('313', $python313))) {
    $version = $pair[0]
    $python = $pair[1]
    foreach ($distribution in @('candidate', 'predecessor')) {
        $venv = Join-Path $root "$distribution-$version"
        & $python -m venv $venv
        if ($LASTEXITCODE -ne 0) { throw 'Venv creation failed' }
        $installed = Join-Path $venv 'Scripts/python.exe'
        $wheel = if ($distribution -eq 'candidate') { $candidateWheel } else { $predecessorWheel }
        & $installed -m pip install --disable-pip-version-check --no-index --no-deps $wheel
        if ($LASTEXITCODE -ne 0) { throw 'Wheel install failed' }
        $runtimes["$distribution-$version"] = $installed
    }
}
$setupTimer.Stop()
$allPassed = $true
$results = @()
function Invoke-Measured([string]$Name, [string]$Python, [string[]]$Arguments) {
    Write-Host "BENCHMARK_START $Storage $Name"
    $timer = [Diagnostics.Stopwatch]::StartNew()
    & $Python @Arguments
    $status = $LASTEXITCODE
    $timer.Stop()
    $entry = [ordered]@{storage=$Storage; name=$Name; seconds=$timer.Elapsed.TotalSeconds; exit_code=$status}
    Write-Host ('BENCHMARK_RESULT ' + ($entry | ConvertTo-Json -Compress))
    $script:results += [pscustomobject]$entry
    if ($status -ne 0) { $script:allPassed = $false }
}
# Preserve the existing Windows upgrade/inventory/smoke/full test selection.
foreach ($number in @(1,2)) {
    Invoke-Measured "upgrade-$number" $python311 @('-B', '-m', 'repository_tools.upgrade_rehearsal', '--repository', $source, '--predecessor-python', $runtimes['predecessor-311'], '--successor-python', $runtimes['candidate-311'], '--output', (Join-Path $root "upgrade-$number"), '--workspace', $env:TEMP, '--timings')
}
$firstUpgrade = Join-Path $root 'upgrade-1/upgrade-rehearsal-result.json'
$secondUpgrade = Join-Path $root 'upgrade-2/upgrade-rehearsal-result.json'
if ((Test-Path -LiteralPath $firstUpgrade) -and (Test-Path -LiteralPath $secondUpgrade)) {
    $first = Get-Content -Raw -LiteralPath $firstUpgrade | ConvertFrom-Json
    $second = Get-Content -Raw -LiteralPath $secondUpgrade | ConvertFrom-Json
    if ($first.semantic_sha256 -ne $second.semantic_sha256 -or $first.overall_result -ne 'pass' -or $second.overall_result -ne 'pass') { $allPassed = $false }
} else { $allPassed = $false }
Invoke-Measured 'distribution-inventory' $python311 @('-B', '-m', 'unittest', 'tests.test_integration_package.OwnershipDistributionInventoryTests', '-v')
foreach ($version in @('311','313')) {
    $selection = if ($version -eq '311') { 'smoke' } else { 'full' }
    $sourcePython = if ($version -eq '311') { $python311 } else { $python313 }
    $env:SE_HARNESS_OWNERSHIP_LEGACY_PYTHON = $runtimes["predecessor-$version"]
    foreach ($mode in @('source','package')) {
        $selectedPython = if ($mode -eq 'source') { $sourcePython } else { $runtimes["candidate-$version"] }
        $output = Join-Path $root "results/$version/$mode"
        Invoke-Measured "$version-$mode-$selection" $selectedPython @('-I', '-B', $runner, $testPath, $mode, $selection, $output)
        # Logs remain ordinary CI logs; no upload-artifact step or formal record.
        $testLog = Join-Path $output 'test-output.log'
        if (Test-Path -LiteralPath $testLog) { Get-Content -LiteralPath $testLog }
    }
}
$result = [ordered]@{storage=$Storage; passed=$allPassed; setup_seconds=$setupTimer.Elapsed.TotalSeconds; tested_commit=$env:RAMDISK_TESTED_COMMIT; runs=$results; temp=$env:TEMP; source=$source; root=$root}
$result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $root 'summary.json') -Encoding utf8
Write-Host ('BENCHMARK_SUMMARY ' + ($result | ConvertTo-Json -Depth 5 -Compress))
"### $Storage (exploratory only)" | Out-File -FilePath $env:GITHUB_STEP_SUMMARY -Append
"Setup/copy/install: $([math]::Round($setupTimer.Elapsed.TotalSeconds, 2)) seconds. All selected commands passed: $allPassed." | Out-File -FilePath $env:GITHUB_STEP_SUMMARY -Append
"| Command | Seconds | Exit |`n|---|---:|---:|" | Out-File -FilePath $env:GITHUB_STEP_SUMMARY -Append
foreach ($entry in $results) { "| $($entry.name) | $([math]::Round($entry.seconds,2)) | $($entry.exit_code) |" | Out-File -FilePath $env:GITHUB_STEP_SUMMARY -Append }
if (-not $allPassed) { exit 1 }