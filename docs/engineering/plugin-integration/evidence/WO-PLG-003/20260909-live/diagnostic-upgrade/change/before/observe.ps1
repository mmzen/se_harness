# Observation-only host hook; not a production readiness evaluator or policy.
$ErrorActionPreference = 'Stop'
$probeInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
$probeData = $env:PLUGIN_DATA
if ([string]::IsNullOrWhiteSpace($probeData)) { throw 'Codex did not supply PLUGIN_DATA' }
New-Item -ItemType Directory -Path $probeData -Force | Out-Null
$probeEvent = [ordered]@{
    timestamp = [DateTimeOffset]::UtcNow.ToString('o')
    hook_event_name = $probeInput.hook_event_name
    source = $probeInput.source
    cwd = $probeInput.cwd
    plugin_root = $env:PLUGIN_ROOT
    plugin_data = $probeData
    tool_name = $probeInput.tool_name
    observer = 'powershell; observation only; no evaluator invoked'
}
$probeEvent | ConvertTo-Json -Compress | Add-Content -LiteralPath (Join-Path $probeData 'events.jsonl') -Encoding utf8
# No action classifier. Preserve ordinary host permissions and permit setup.
if ($probeInput.hook_event_name -eq 'SessionStart') {
    [Console]::Out.WriteLine('CODEX_PROBE_CONTEXT_003: Setup required. This observation fixture is not governance-ready. Use the setup skill; supplied Python 3.11+ with venv/ensurepip is required. Do not perform governed writes while unready.')
} else {
    [Console]::Out.WriteLine('{"hookSpecificOutput":{"hookEventName":"PreToolUse","additionalContext":"CODEX_PROBE_UNREADY_003: setup required; fixture is not governance-ready."}}')
}
exit 0
