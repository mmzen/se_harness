"""Separate documented inline-command trial; never evaluates the refused ps1."""
import argparse
import importlib.util
import json
import os
from pathlib import Path

spec = importlib.util.spec_from_file_location('probe', Path(__file__).with_name('probe.py'))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)

INLINE = r'''$ErrorActionPreference = 'Stop'
$e = [Console]::In.ReadToEnd() | ConvertFrom-Json
$c = Get-Content -Raw -LiteralPath "$env:CLAUDE_PLUGIN_ROOT/probe.json" | ConvertFrom-Json
$r = [ordered]@{ at=[DateTime]::UtcNow.ToString('o'); event=$e.hook_event_name; source=$e.source; root=$env:CLAUDE_PLUGIN_ROOT; data=$env:CLAUDE_PLUGIN_DATA; interpreter=$c.interpreter; handler_invoked=$false }
if (Test-Path -LiteralPath $c.interpreter -PathType Leaf) {
  $r.handler_invoked = $true
  $out = & $c.interpreter -I "$env:CLAUDE_PLUGIN_ROOT/handler.py"
  $r.handler_exit = $LASTEXITCODE
  $r.handler_output = $out -join "`n"
} else { $out = 'PROBE: setup required. The selected interpreter is absent. No governance readiness is asserted.' }
[IO.File]::AppendAllText($c.event_log, (($r | ConvertTo-Json -Compress -Depth 8) + "`n"), [Text.UTF8Encoding]::new($false))
if ($e.hook_event_name -eq 'SessionStart') { $out }
'''


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--claude', type=Path, required=True)
    parser.add_argument('--label', default='native-inline')
    parser.add_argument('--profile-name', default='isolated profile')
    args = parser.parse_args()
    sandbox = args.sandbox.resolve()
    if probe.contained(sandbox, probe.ROOT) or not (sandbox / 'isolated profile').is_dir():
        parser.error('use the existing external disposable probe sandbox')
    if Path(args.label).name != args.label or Path(args.profile_name).name != args.profile_name:
        parser.error('label and profile-name must be single directory names')
    destination = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004' / args.label
    destination.mkdir(parents=True, exist_ok=False)
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
    profile = sandbox / args.profile_name
    profile.mkdir(exist_ok=True)
    env = probe.child_environment(profile)
    cwd = sandbox / 'disposable repository'
    settings = sandbox / 'inline-settings.json'
    probe.dump(settings, {'disableAllHooks': False})
    log = Path(config['event_log'])

    def base():
        return [str(args.claude), '--setting-sources', 'user', '--settings', str(settings), '--plugin-dir', str(plugin)]

    def run(argv):
        return probe.execute(argv, cwd, env)

    def start(label):
        before = len(probe.events(log))
        debug = sandbox / f'{label}.inline.debug.txt'
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
    off, off_events = start('C05-disabled')
    probe.dump(settings, {'disableAllHooks': False})
    on, on_events = start('C05-enabled')
    probe.save_case(destination / 'C05', [off, on], 'Only enabled hooks deliver the fixture event.',
                    {'disabled': off_events, 'enabled': on_events,
                     'interactive_trust': 'not assessed by init-only'}, 'unavailable')
    data['version'] = '0.0.2'
    probe.dump(manifest, data)
    update, update_events = start('C06-version-restart')
    runtime.rename(removed)
    absent, absent_events = start('C06-removed')
    probe.save_case(destination / 'C06', [update, absent], 'Version restart preserves data identity; removed interpreter is not invoked.',
                    {'updated': update_events, 'removed': absent_events,
                     'interactive_reload': 'not assessed; startup restart observed'}, 'unavailable')
    probe.publish_capture(log, destination / 'events.jsonl') if log.exists() else None
    print(json.dumps({'evidence': str(destination), 'startup_events': len(probe.events(log))}))


if __name__ == '__main__':
    main()
