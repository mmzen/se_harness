param([string]$Mode = 'session')
$ErrorActionPreference = 'Stop'
$raw = [Console]::In.ReadToEnd()
$event = $raw | ConvertFrom-Json
$config = Get-Content -Raw -LiteralPath (Join-Path $env:CLAUDE_PLUGIN_ROOT 'probe.json') | ConvertFrom-Json
$data = $env:CLAUDE_PLUGIN_DATA
$record = [ordered]@{
  at = [DateTime]::UtcNow.ToString('o'); pid = $PID; mode = $Mode
  event = $event.hook_event_name; source = $event.source
  plugin_root = $env:CLAUDE_PLUGIN_ROOT; plugin_data = $data
  cwd = $event.cwd; interpreter = $config.interpreter
  handler_invoked = $false; result = 'setup_required'
}
if ($Mode -eq 'observe') {
  $record.result = 'event_observed'
} elseif (Test-Path -LiteralPath $config.interpreter -PathType Leaf) {
  $record.handler_invoked = $true
  $result = & $config.interpreter -I (Join-Path $env:CLAUDE_PLUGIN_ROOT 'handler.py')
  $record.handler_exit = $LASTEXITCODE
  $record.handler_output = $result -join "`n"
  $record.result = 'handler_observed'
} else {
  $result = 'PROBE: setup required; the selected evaluator cannot run. No governance readiness is asserted.'
}
[IO.File]::AppendAllText($config.event_log, (($record | ConvertTo-Json -Compress -Depth 8) + "`n"), [Text.UTF8Encoding]::new($false))
if ($Mode -eq 'session') { $result }
# An observation fixture does not implement authorization or approve tools.
exit 0
