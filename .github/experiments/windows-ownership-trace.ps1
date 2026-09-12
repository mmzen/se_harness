param([ValidateSet('disk','ramdisk')][string]$Storage)
$ErrorActionPreference = 'Stop'
$root = if ($Storage -eq 'ramdisk') { 'R:\ownership-trace' } else { Join-Path $env:RUNNER_TEMP 'ownership-trace' }
if (Test-Path -LiteralPath $root) { throw 'Experiment destination must be fresh' }
New-Item -ItemType Directory -Path $root | Out-Null
$source = Join-Path $root 'source'
& git clone --quiet --no-hardlinks --no-checkout $env:GITHUB_WORKSPACE $source
if ($LASTEXITCODE -ne 0) { throw 'Clone failed' }
& git -C $source checkout --quiet --detach $env:RAMDISK_TESTED_COMMIT
if ($LASTEXITCODE -ne 0) { throw 'Candidate checkout failed' }
$runtime = Join-Path $root 'python313'
& robocopy $env:RAMDISK_PY313 $runtime /E /COPY:DAT /DCOPY:DAT /R:1 /W:1 /NFL /NDL /NP /NJH /NJS
if ($LASTEXITCODE -ge 8) { throw 'Runtime copy failed' }
$env:TEMP = Join-Path $root 'temp'
$env:TMP = $env:TEMP
$env:TMPDIR = $env:TEMP
$env:SE_HARNESS_OWNERSHIP_COMMIT = $env:RAMDISK_TESTED_COMMIT
New-Item -ItemType Directory -Path $env:TEMP | Out-Null
$scripts = Join-Path $env:GITHUB_WORKSPACE '.github/experiments'
$wrapper = Join-Path $root 'ownership-profile.py'
Copy-Item -LiteralPath (Join-Path $scripts 'ownership-profile.py') -Destination $wrapper
$output = Join-Path $root 'result'
$tracePath = Join-Path $env:RUNNER_TEMP "$Storage-ownership.etl"
$wpr = Join-Path $env:SystemRoot 'System32/wpr.exe'
$profile = (Join-Path $scripts 'Ownership.wprp') + '!Ownership'
$instance = "Ownership-$Storage"
Set-Location -LiteralPath $source
Write-Host "TRACE_START $Storage"
& $wpr -start $profile -instancename $instance
if ($LASTEXITCODE -ne 0) { throw 'WPR start failed' }
$testStatus = 1
try {
    & (Join-Path $runtime 'python.exe') -I -B $wrapper $source $output
    $testStatus = $LASTEXITCODE
    & $wpr -status -instancename $instance
} finally {
    # The ETL is written to normal storage only after the measured test window.
    & $wpr -stop $tracePath -instancename $instance
    if ($LASTEXITCODE -ne 0) {
        & $wpr -cancel -instancename $instance
        throw 'WPR stop failed'
    }
}
Write-Host "TRACE_ANALYSIS $Storage TEST_EXIT=$testStatus"
& dotnet (Join-Path $env:RUNNER_TEMP 'trace-analyzer/TraceAnalyzer.dll') $tracePath (Join-Path $output 'window.json') (Join-Path $output 'etw-summary.json')
if ($LASTEXITCODE -ne 0) { throw 'Trace analysis failed or recording incomplete' }
Write-Host "TRACE_DONE $Storage TEST_EXIT=$testStatus"
if ($testStatus -ne 0) { throw 'Profiled acceptance failed' }
