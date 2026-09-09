"""Separate documented inline-command trial; never evaluates the refused ps1."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
from datetime import datetime, timezone

spec = importlib.util.spec_from_file_location('probe', Path(__file__).with_name('probe.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

INLINE = r'''$ErrorActionPreference = 'Stop'
$e = [Console]::In.ReadToEnd() | ConvertFrom-Json
$c = Get-Content -Raw -LiteralPath "$env:CLAUDE_PLUGIN_ROOT/probe.json" | ConvertFrom-Json
$r = [ordered]@{ at=[DateTime]::UtcNow.ToString('o'); event=$e.hook_event_name; source=$e.source; root=$env:CLAUDE_PLUGIN_ROOT; data=$env:CLAUDE_PLUGIN_DATA; interpreter=$c.interpreter; handler_invoked=$false }
$context = 'PROBE: setup required. The selected interpreter is absent. No governance readiness is asserted.'
if (Test-Path -LiteralPath $c.interpreter -PathType Leaf) {
  $r.handler_invoked = $true
  $out = & $c.interpreter -I "$env:CLAUDE_PLUGIN_ROOT/handler.py"
  $r.handler_exit = $LASTEXITCODE
  $r.handler_output = $out -join "`n"
  $context = 'PROBE: evaluator identity was not established. No governance readiness is asserted.'
  if ($r.handler_exit -eq 0) {
    $observation = $r.handler_output | ConvertFrom-Json
    if (($observation.identity_exit -eq 0) -and ($observation.identity.passed -eq $true)) {
      $context = $observation.context
    }
  }
}
# Telemetry belongs in the event log; Claude ignores arbitrary JSON stdout keys.
$output = $null
if ($e.hook_event_name -eq 'SessionStart') {
  $output = @{ hookSpecificOutput = @{ hookEventName = 'SessionStart'; additionalContext = $context } }
  $r.host_output = $output
}
[IO.File]::AppendAllText($c.event_log, (($r | ConvertTo-Json -Compress -Depth 8) + "`n"), [Text.UTF8Encoding]::new($false))
if ($null -ne $output) { $output | ConvertTo-Json -Compress -Depth 4 }
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--claude', type=Path, required=True)
    parser.add_argument('--label', default='native-inline')
    parser.add_argument('--profile-name', required=True)
    args = parser.parse_args()
    sandbox = args.sandbox.resolve()
    if probe.contained(sandbox, probe.ROOT) or not (sandbox / 'isolated profile').is_dir():
        parser.error('use the existing external disposable probe sandbox')
    if Path(args.label).name != args.label or Path(args.profile_name).name != args.profile_name:
        parser.error('label and profile-name must be single directory names')
    profile = sandbox / args.profile_name
    if profile.exists():
        parser.error('profile-name must select a fresh profile; existing login profiles are never reused here')
    destination = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004' / args.label
    destination.mkdir(parents=True, exist_ok=False)
    run_directory = sandbox / f'{args.label}-run'
    run_directory.mkdir(exist_ok=False)
    plugin = sandbox / f'{args.label} command plugin with spaces'
    runtime = sandbox / 'selected evaluator/Scripts/python.exe'
    original = json.loads((sandbox / 'plugin with spaces/probe.json').read_text())
    config = dict(original, event_log=str(sandbox / f'{args.label}-events.jsonl'))
    powershell = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
    probe.create_plugin(plugin, config, powershell)
    manifest = plugin / '.claude-plugin/plugin.json'
    data = json.loads(manifest.read_text())
    data['name'] = 'verity-plane-inline-probe'
    probe.dump(manifest, data)
    hooks = {'hooks': {event: [{'hooks': [{'type': 'command', 'shell': 'powershell',
              'command': INLINE, 'timeout': 25}]}] for event in ['SessionStart', 'PreToolUse', 'PostCompact']}}
    probe.dump(plugin / 'hooks/hooks.json', hooks)
    # Keep the exact applied inline command, not just a prose claim.
    probe.publish_json(destination / 'hooks.json', hooks)
    probe.publish_json(destination / 'plugin.json', data)
    profile.mkdir()
    env = probe.child_environment(profile)
    cwd = sandbox / 'disposable repository'
    settings = run_directory / 'settings.json'
    probe.dump(settings, {'disableAllHooks': False})
    log = Path(config['event_log'])
    normal = Path(os.environ['USERPROFILE'])
    watched = [normal / '.claude.json', normal / '.claude/settings.json',
               normal / '.claude/.credentials.json', normal / '.claude/plugins/installed_plugins.json',
               normal / '.claude/plugins/known_marketplaces.json']
    before = probe.metadata(watched)
    repository_before = {p.name: probe.digest(p) for p in cwd.iterdir() if p.is_file()}
    probe.publish_json(destination / 'normal-profile-before.json', before)
    probe.publish_json(destination / 'identities.json', {
        'at': datetime.now(timezone.utc).isoformat(),
        'host_version': probe.execute([str(args.claude), '--version'], cwd, env),
        'source_files': {p.name: probe.digest(p) for p in probe.HERE.iterdir() if p.is_file()},
        'archive_sha256': probe.ARCHIVE, 'payload_sha256': probe.PAYLOAD,
        'documentation': probe.DOCS, 'fixture_mode': 'inline plugin; fresh unauthenticated profile',
        'platforms': {'Windows': 'assessed', 'Linux': 'unavailable', 'macOS': 'unavailable'}})
    for name in ['probe.json', 'handler.py', 'guard.ps1', 'hooks/hooks.json', '.claude-plugin/plugin.json', 'skills/setup/SKILL.md']:
        probe.publish_capture(plugin / name, destination / 'fixture' / name)

    def base():
        return [str(args.claude), '--setting-sources', 'user', '--settings', str(settings), '--plugin-dir', str(plugin)]

    def run(argv):
        return probe.execute(argv, cwd, env)

    def start(label):
        before = len(probe.events(log))
        debug = run_directory / f'{label}.debug.txt'
        result = run(base() + ['--strict-mcp-config', '--mcp-config', str(sandbox / 'empty-mcp.json'),
                             '--debug-file', str(debug), '--init-only'])
        if debug.exists():
            probe.publish_capture(debug, destination / f'{label}.debug.txt')
        return result, probe.events(log)[before:]

    inventory = [run([str(args.claude), 'plugin', 'validate', str(plugin), '--json', '--strict']),
                 run(base() + ['plugin', 'list', '--json']),
                 run(base() + ['plugin', 'details', 'verity-plane-inline-probe'])]
    missing, missing_events = start('C01-missing')
    probe.save_case(destination / 'C01', inventory + [missing], 'Actual inline guard observes missing interpreter.',
                    {'events': missing_events, 'startup': probe.classify_start(missing, missing_events, False),
                     'resume_compact': 'not assessed in this startup-only trial'}, 'unavailable')
    removed = runtime.with_suffix('.removed')
    if not probe.contained(runtime, sandbox) or not removed.is_file():
        raise RuntimeError('expected task-owned removed interpreter for restoration')
    removed.rename(runtime)
    first, first_events = start('C03-first')
    second, second_events = start('C03-second')
    probe.save_case(destination / 'C03', [first, second], 'Two startups call the restored disposable evaluator and retain its returned context.',
                    {'first': first_events, 'second': second_events,
                     'first_start': probe.classify_start(first, first_events, True),
                     'second_start': probe.classify_start(second, second_events, True),
                     'restoration_actor': 'observer; not Claude tool or C07 evidence',
                     'model_context_delivery': 'not assessed by init-only'}, 'unavailable')
    probe.dump(settings, {'disableAllHooks': True})
    probe.publish_capture(settings, destination / 'C05/settings-disabled.json')
    off, off_events = start('C05-disabled')
    probe.dump(settings, {'disableAllHooks': False})
    probe.publish_capture(settings, destination / 'C05/settings-enabled.json')
    on, on_events = start('C05-enabled')
    enablement_observed = (off['exit'] == on['exit'] == 0 and not off['timeout'] and not on['timeout']
                          and not off_events and probe.classify_start(on, on_events, True) == 'observed')
    probe.save_case(destination / 'C05', [off, on], 'Only enabled hooks deliver the fixture event.',
                    {'disabled': off_events, 'enabled': on_events,
                     'enablement_interaction': 'observer changed only explicit --settings file: disableAllHooks true, then false',
                     'interactive_trust': 'no dialog in this init-only route; interactive UI not assessed',
                     'settings_evidence': ['settings-disabled.json', 'settings-enabled.json']},
                    'pass' if enablement_observed else 'fail')
    data_paths_before = {r['data'] for r in on_events if r.get('data')}
    data_before = probe.metadata(data_paths_before)
    probe.publish_capture(manifest, destination / 'C06/manifest-before.json')
    manifest_before_digest = probe.digest(manifest)
    data['version'] = '0.0.2'
    probe.dump(manifest, data)
    probe.publish_capture(manifest, destination / 'C06/manifest-after.json')
    manifest_after_digest = probe.digest(manifest)
    update, update_events = start('C06-version-restart')
    runtime.rename(removed)
    absent, absent_events = start('C06-removed')
    data_paths_after = {r['data'] for r in update_events + absent_events if r.get('data')}
    data_after = probe.metadata(data_paths_after)
    restart_observed = (probe.classify_start(update, update_events, True) == 'observed'
                        and probe.classify_start(absent, absent_events, False) == 'observed'
                        and data_paths_before == data_paths_after and bool(data_paths_before)
                        and all(item.get('exists') for item in data_before.values())
                        and all(item.get('exists') for item in data_after.values()))
    probe.save_case(destination / 'C06', [update, absent], 'Version restart preserves data identity; removed interpreter is not invoked.',
                    {'updated': update_events, 'removed': absent_events,
                     'manifest_before_sha256': manifest_before_digest, 'manifest_after_sha256': manifest_after_digest,
                     'plugin_data_before': data_before, 'plugin_data_after': data_after,
                     'restart_count': 2, 'permission_interactions': 'none in init-only route',
                     'reload_route': 'process restart with the same --plugin-dir after version change; no hot reload claim'},
                    'pass' if restart_observed else 'fail')
    probe.publish_capture(log, destination / 'events.jsonl') if log.exists() else None
    after = probe.metadata(watched)
    repository_after = {p.name: probe.digest(p) for p in cwd.iterdir() if p.is_file()}
    probe.publish_json(destination / 'isolation.json', {
        'normal_profile_before': before, 'normal_profile_after': after,
        'normal_profile_metadata_equal': before == after,
        'repository_before': repository_before, 'repository_after': repository_after,
        'repository_equal': repository_before == repository_after,
        'credential_contents_read_or_copied': False,
        'limitation': 'Only listed normal-profile metadata and top-level disposable repository file hashes are compared.'})
    print(json.dumps({'evidence': str(destination), 'startup_events': len(probe.events(log))}))


if __name__ == '__main__':
    main()
