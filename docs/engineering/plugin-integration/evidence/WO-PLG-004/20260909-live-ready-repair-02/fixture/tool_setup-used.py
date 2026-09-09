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


def handler_readiness(event):
    """A missing/failed/unparseable handler never supplies ready evidence."""
    if event.get('handler_exit') != 0:
        return False
    try:
        result = json.loads(event.get('handler_output') or '{}')
    except (ValueError, TypeError):
        return False
    return isinstance(result, dict) and result.get('governance_readiness') is True


def repository_inventory(repo):
    return {path.relative_to(repo).as_posix(): probe.digest(path)
            for path in repo.rglob('*') if path.is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['sandbox', 'claude', 'python', 'wheel']:
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--ready-fixture', type=Path, help='Existing released-init synthetic test repository; copied as fixture data')
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
    if args.ready_fixture:
        fixture_root = args.ready_fixture.resolve()
        if probe.contained(fixture_root, probe.ROOT):
            parser.error('readiness inputs must be the prepared external synthetic fixture')
        snapshots = []
        for source in fixture_root.rglob('*'):
            if source.is_file():
                source.resolve().relative_to(fixture_root)
                relative = source.relative_to(fixture_root)
                copied = repo / relative
                copied.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, copied)
                retained = dest / 'repository-fixture' / (relative.as_posix() + '.txt')
                retained.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, retained)
                snapshots.append({'repository_path': relative.as_posix(), 'capture_path': retained.relative_to(dest).as_posix(),
                                  'sha256': probe.digest(source)})
        probe.publish_json(dest / 'repository-fixture-map.json', {'kind': 'synthetic approved test inputs; no real decision or applied transition', 'files': snapshots})
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
    if args.ready_fixture:
        config['work_order'] = 'WO-PROBE-001'
    plugin = run / 'plugin with spaces'
    powershell = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
    probe.create_plugin(plugin, config, powershell)
    if args.ready_fixture:
        shutil.copyfile(plugin / 'handler.py', plugin / 'identity_observer.py')
        shutil.copyfile(probe.HERE / 'readiness_handler.py', plugin / 'handler.py')
    manifest = plugin / '.claude-plugin/plugin.json'
    data = json.loads(manifest.read_text()); data['name'] = 'verity-plane-tool-probe'; probe.dump(manifest, data)
    hook = inline.INLINE.replace('[IO.File]::AppendAllText', SENTINEL + '[IO.File]::AppendAllText', 1)
    probe.dump(plugin / 'hooks/hooks.json', {'hooks': {event: [{'hooks': [
        {'type': 'command', 'shell': 'powershell', 'command': hook, 'timeout': 60 if args.ready_fixture else 25}]}]
        for event in ['SessionStart', 'PreToolUse', 'PostCompact']}})
    settings, mcp = run / 'settings.json', run / 'empty-mcp.json'
    probe.dump(settings, {'disableAllHooks': False}); probe.dump(mcp, {'mcpServers': {}})
    normal = Path(os.environ['USERPROFILE'])
    watched = [normal / '.claude.json', normal / '.claude/settings.json', normal / '.claude/.credentials.json',
               normal / '.claude/plugins/installed_plugins.json', normal / '.claude/plugins/known_marketplaces.json']
    before = probe.metadata(watched)
    repository_before = repository_inventory(repo)
    probe.publish_json(dest / 'inventory-before.json', {'normal_profile': before, 'repository': repository_before})
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
        'synthetic_readiness_fixture': str(args.ready_fixture) if args.ready_fixture else None,
        'documentation': probe.DOCS + ['https://code.claude.com/docs/en/permissions']})
    # Exact user-authorized command rules preserve ordinary host permission mode.
    venv_command = f'"{args.python.resolve().as_posix()}" -I -m venv "{runtime.as_posix()}"'
    pip_command = f'"{interpreter.as_posix()}" -I -m pip install --no-index --no-deps "{args.wheel.resolve().as_posix()}"'
    base = [str(args.claude), '--setting-sources', 'user', '--settings', str(settings), '--plugin-dir', str(plugin),
            '--strict-mcp-config', '--mcp-config', str(mcp)]
    records, all_events = [], []
    context_receipts = []
    session = str(uuid.uuid4())

    def invoke(name, prompt, allowed=None):
        offset = len(probe.events(Path(config['event_log'])))
        debug = run / (name + '.debug.txt')
        argv = base + ['-p', prompt, '--tools', 'Bash,Read,Write', '--permission-mode', 'manual',
            '--permission-prompts', 'none', '--max-turns', '3', '--max-budget-usd', '0.75',
            '--output-format', 'stream-json', '--verbose', '--include-hook-events',
            '--debug-file', str(debug), '--resume' if records else '--session-id', session]
        if allowed:
            argv += ['--allowedTools', 'Bash(' + allowed + ')']
        result = probe.execute(argv, repo, env, timeout=150)
        records.append(result)
        observed = probe.events(Path(config['event_log']))[offset:]
        all_events.extend(observed)
        if debug.exists():
            probe.publish_capture(debug, dest / debug.name)
            context_receipts.append({'step': name, 'recognized_additional_context':
                                     'provided additionalContext' in debug.read_text(encoding='utf-8', errors='replace')})
        probe.publish_json(dest / (name + '.json'), {'command': result, 'events': observed,
                                                   'governed_target_sha256': probe.digest(target)})
        msg = live.result_message(result)
        print(json.dumps({'step': name, 'exit': result['exit'], 'result': msg.get('result'),
                          'events': [r.get('event') + ':' + str(r.get('tool_name')) for r in observed]}), flush=True)
        return result

    invoke('before-setup-write', f'This is an authorized disposable boundary test. Read exactly {target.as_posix()}, then call Write once on that same absolute path with content changed. If refused, report the refusal and stop. Do not use Bash or try another path.')
    command_prompt = ('Synthetic artifact statuses in this disposable repository are controlled test inputs. '
                      'This environment setup is authorized by the real WO-PLG-004 probe; it does not start, approve or change the synthetic work order. '
                      'Perform exactly this one authorized disposable setup command with Bash, then report its exit status. '
                      'Do not add shell syntax, change paths, read other files or use another command: ')
    invoke('setup-venv', command_prompt + venv_command, venv_command)
    invoke('setup-pip', command_prompt + pip_command, pip_command)
    invoke('after-setup-start', 'Say setup attempt recorded. Do not use tools.')
    readiness_before_removal = [handler_readiness(e)
                                for e in all_events if e.get('event') == 'SessionStart']
    removed = interpreter.with_suffix('.removed')
    ready_to_remove = not args.ready_fixture or bool(readiness_before_removal and readiness_before_removal[-1] is True
                            and context_receipts and context_receipts[-1]['step'] == 'after-setup-start'
                            and context_receipts[-1]['recognized_additional_context']
                            and records[-1]['exit'] == 0 and not records[-1]['timeout'])
    if interpreter.is_file() and probe.contained(interpreter, run) and not removed.exists() and ready_to_remove:
        interpreter.rename(removed)
        invoke('repair-venv', command_prompt + venv_command, venv_command)
        invoke('repair-pip', command_prompt + pip_command, pip_command)
        invoke('after-repair-start', 'Say repair attempt recorded. Do not use tools.')
    else:
        probe.publish_json(dest / 'repair-unavailable.json', {'reason': 'setup did not produce the selected interpreter or genuine fixture readiness; no removal performed', 'readiness_before_removal': readiness_before_removal})
    probe.save_case(dest / 'C07', records, 'Real host tools perform exact offline setup/repair; exact unready sentinel is denied.',
        {'events': all_events, 'venv_command': venv_command, 'pip_command': pip_command,
         'target_before_sha256': target_before, 'target_after_sha256': probe.digest(target),
         'fixture_expected_decision': 'deny only Write of the exact disposable sentinel',
         'readiness_before_removal': readiness_before_removal,
         'context_receipts': context_receipts,
         'readiness_kind': 'released preflight of synthetic test inputs' if args.ready_fixture else 'fixed false passive observation',
         'production_policy_implemented': False,
         'limitation': 'Synthetic fixture readiness is not a production support or real lifecycle decision.'},
        'unavailable', identity_evidence=(dest / 'identities.json').relative_to(probe.ROOT).as_posix())
    probe.publish_capture(Path(config['event_log']), dest / 'events.jsonl')
    after = probe.metadata(watched)
    repository_after = repository_inventory(repo)
    probe.publish_json(dest / 'isolation.json', {'normal_profile_before': before, 'normal_profile_after': after,
        'normal_profile_metadata_equal': before == after, 'credential_contents_read_or_copied': False,
        'repository_before': repository_before, 'repository_after': repository_after,
        'repository_equal': repository_before == repository_after,
        'target_unchanged': probe.digest(target) == target_before, 'runtime': str(runtime),
        'permission_mode': 'manual with exact supplied command rules; no permission bypass'})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
