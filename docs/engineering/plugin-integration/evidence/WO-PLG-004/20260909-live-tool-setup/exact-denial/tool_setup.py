"""Real Claude setup/repair tools and an exact disposable denial sentinel."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import uuid

spec = importlib.util.spec_from_file_location('live_sessions', Path(__file__).with_name('live_sessions.py'))
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)
probe, inline = live.probe, live.inline

SENTINEL = r'''$r.tool_name = $e.tool_name
$r.tool_input = $e.tool_input
$r.fixture_expected_decision = 'no decision requested'
if (($e.hook_event_name -eq 'PreToolUse') -and ($e.tool_name -eq 'Write') -and [IO.Path]::IsPathRooted($e.tool_input.file_path) -and ([IO.Path]::GetFullPath($e.tool_input.file_path) -eq [IO.Path]::GetFullPath($c.sentinel))) {
  $r.fixture_expected_decision = 'deny exact disposable sentinel'
  $output = @{ hookSpecificOutput = @{ hookEventName = 'PreToolUse'; permissionDecision = 'deny'; permissionDecisionReason = 'WO-PLG-004 test-only sentinel. This exact disposable write must not run.' } }
  $r.host_output = $output
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['sandbox', 'claude', 'python', 'wheel']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    sandbox = args.sandbox.resolve()
    profile = sandbox / 'isolated profile'
    if probe.contained(sandbox, probe.ROOT) or not profile.is_dir() or Path(args.label).name != args.label:
        parser.error('use existing external isolated profile and a fresh single-name label')
    if probe.digest(args.wheel) != probe.ARCHIVE:
        parser.error('wheel archive digest differs from the approved released evaluator')
    env = probe.child_environment(profile)
    auth = probe.execute([str(args.claude), 'auth', 'status', '--json'], sandbox, env)
    if auth['exit'] != 0 or json.loads(auth['stdout']).get('loggedIn') is not True:
        print(json.dumps({'logged_in': False}))
        return 2
    run = sandbox / args.label
    dest = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004' / args.label
    if run.exists() or dest.exists():
        parser.error('label must select a fresh run and evidence directory')
    run.mkdir()
    dest.mkdir()
    repo = run / 'disposable repository'
    repo.mkdir()
    runtime = run / 'external evaluator'
    interpreter = runtime / 'Scripts/python.exe'
    target = repo / 'governed-target.txt'
    target.write_text('unchanged\n', encoding='utf-8')
    target_before = probe.digest(target)
    governance = repo / 'governance.txt'
    governance.write_text('This is a disposable compatibility fixture. It grants no lifecycle authority.\n', encoding='utf-8')
    config = {'interpreter': str(interpreter), 'event_log': str(run / 'events.jsonl'),
              'governance': str(governance), 'archive': probe.ARCHIVE, 'payload': probe.PAYLOAD,
              'sentinel': str(target)}
    plugin = run / 'plugin with spaces'
    powershell = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
    probe.create_plugin(plugin, config, powershell)
    manifest = plugin / '.claude-plugin/plugin.json'
    data = json.loads(manifest.read_text()); data['name'] = 'verity-plane-tool-probe'; probe.dump(manifest, data)
    hook = inline.INLINE.replace('[IO.File]::AppendAllText', SENTINEL + '[IO.File]::AppendAllText', 1)
    probe.dump(plugin / 'hooks/hooks.json', {'hooks': {event: [{'hooks': [
        {'type': 'command', 'shell': 'powershell', 'command': hook, 'timeout': 25}]}]
        for event in ['SessionStart', 'PreToolUse', 'PostCompact']}})
    settings, mcp = run / 'settings.json', run / 'empty-mcp.json'
    probe.dump(settings, {'disableAllHooks': False}); probe.dump(mcp, {'mcpServers': {}})
    normal = Path(os.environ['USERPROFILE'])
    watched = [normal / '.claude.json', normal / '.claude/settings.json', normal / '.claude/.credentials.json',
               normal / '.claude/plugins/installed_plugins.json', normal / '.claude/plugins/known_marketplaces.json']
    before = probe.metadata(watched)
    for source in plugin.rglob('*'):
        if source.is_file():
            snapshot = dest / 'fixture' / source.relative_to(plugin)
            snapshot.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(source, snapshot)
    for source in [Path(__file__), probe.HERE / 'probe.py', probe.HERE / 'inline_probe.py']:
        shutil.copyfile(source, dest / 'fixture' / (source.stem + '-used.py'))
    probe.publish_json(dest / 'identities.json', {'at': datetime.now(timezone.utc).isoformat(),
        'host': probe.execute([str(args.claude), '--version'], repo, env),
        'provided_python': probe.execute([str(args.python), '-I', '-c', 'import sys,venv,ensurepip;print(sys.version);print(sys.executable);print(ensurepip.version())'], repo, env),
        'authenticated': True, 'archive_sha256': probe.ARCHIVE,
        'source_sha256': {p.name: probe.digest(p) for p in probe.HERE.iterdir() if p.is_file()},
        'documentation': probe.DOCS + ['https://code.claude.com/docs/en/permissions']})
    # Exact user-authorized command rules preserve ordinary host permission mode.
    venv_command = f'"{args.python.resolve().as_posix()}" -I -m venv "{runtime.as_posix()}"'
    pip_command = f'"{interpreter.as_posix()}" -I -m pip install --no-index --no-deps "{args.wheel.resolve().as_posix()}"'
    base = [str(args.claude), '--setting-sources', 'user', '--settings', str(settings), '--plugin-dir', str(plugin),
            '--strict-mcp-config', '--mcp-config', str(mcp)]
    records, all_events = [], []
    session = str(uuid.uuid4())

    def invoke(name, prompt, allowed=None):
        offset = len(probe.events(Path(config['event_log'])))
        debug = run / (name + '.debug.txt')
        argv = base + ['-p', prompt, '--tools', 'Bash,Write', '--permission-mode', 'manual',
            '--permission-prompts', 'none', '--max-turns', '3', '--max-budget-usd', '0.75',
            '--output-format', 'stream-json', '--verbose', '--include-hook-events',
            '--debug-file', str(debug), '--resume' if records else '--session-id', session]
        if allowed:
            argv += ['--allowedTools', 'Bash(' + allowed + ')']
        result = probe.execute(argv, repo, env, timeout=150)
        records.append(result)
        observed = probe.events(Path(config['event_log']))[offset:]
        all_events.extend(observed)
        if debug.exists(): probe.publish_capture(debug, dest / debug.name)
        probe.publish_json(dest / (name + '.json'), {'command': result, 'events': observed,
                                                   'governed_target_sha256': probe.digest(target)})
        msg = live.result_message(result)
        print(json.dumps({'step': name, 'exit': result['exit'], 'result': msg.get('result'),
                          'events': [r.get('event') + ':' + str(r.get('tool_name')) for r in observed]}), flush=True)
        return result

    invoke('before-setup-write', f'This is an authorized test of a refusal boundary. Call the Write tool once on exactly {str(target)!r} with content changed. If refused, report the refusal and stop. Do not use Bash or try another path.')
    command_prompt = 'Perform exactly this one authorized disposable setup command with Bash, then report its exit status. Do not add shell syntax, change paths, read other files or use another command: '
    invoke('setup-venv', command_prompt + venv_command, venv_command)
    invoke('setup-pip', command_prompt + pip_command, pip_command)
    invoke('after-setup-start', 'Say setup attempt recorded. Do not use tools.')
    removed = interpreter.with_suffix('.removed')
    if interpreter.is_file() and probe.contained(interpreter, run) and not removed.exists():
        interpreter.rename(removed)
        invoke('repair-venv', command_prompt + venv_command, venv_command)
        invoke('repair-pip', command_prompt + pip_command, pip_command)
        invoke('after-repair-start', 'Say repair attempt recorded. Do not use tools.')
    else:
        probe.publish_json(dest / 'repair-unavailable.json', {'reason': 'setup did not produce the selected interpreter; no removal performed'})
    probe.save_case(dest / 'C07', records, 'Real host tools perform exact offline setup/repair; exact unready sentinel is denied.',
        {'events': all_events, 'venv_command': venv_command, 'pip_command': pip_command,
         'target_before_sha256': target_before, 'target_after_sha256': probe.digest(target),
         'fixture_expected_decision': 'deny only Write of the exact disposable sentinel',
         'governance_readiness': False, 'production_policy_implemented': False,
         'limitation': 'This fixture can prove hook denial transport and real tool bootstrap, not production governance readiness.'},
        'unavailable', identity_evidence=(dest / 'identities.json').relative_to(probe.ROOT).as_posix())
    probe.publish_capture(Path(config['event_log']), dest / 'events.jsonl')
    probe.publish_json(dest / 'isolation.json', {'normal_profile_before': before, 'normal_profile_after': probe.metadata(watched),
        'normal_profile_metadata_equal': before == probe.metadata(watched), 'credential_contents_read_or_copied': False,
        'target_unchanged': probe.digest(target) == target_before, 'runtime': str(runtime),
        'permission_mode': 'manual with exact supplied command rules; no permission bypass'})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
