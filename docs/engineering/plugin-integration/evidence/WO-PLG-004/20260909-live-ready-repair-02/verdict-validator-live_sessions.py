"""Authenticated, no-tools context observations in an existing isolated profile."""
import argparse
from datetime import datetime, timezone
import importlib.util
import json
import os
from pathlib import Path
import shutil
import uuid


def module(name):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(name + '.py'))
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


probe = module('probe')
inline = module('inline_probe')


def result_message(record):
    for line in reversed(record['stdout'].splitlines()):
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if isinstance(value, dict) and value.get('type') == 'result':
            return value
    return {}


def completed_successfully(record):
    result = result_message(record)
    return (record.get('exit') == 0 and not record.get('timeout')
            and result.get('subtype') == 'success' and result.get('is_error') is False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--claude', type=Path, required=True)
    parser.add_argument('--label', required=True)
    args = parser.parse_args()
    sandbox = args.sandbox.resolve()
    profile = sandbox / 'isolated profile'
    if probe.contained(sandbox, probe.ROOT) or not profile.is_dir():
        parser.error('use the existing external sandbox and its isolated login profile')
    if Path(args.label).name != args.label:
        parser.error('label must be a single directory name')
    env = probe.child_environment(profile)
    auth = probe.execute([str(args.claude), 'auth', 'status', '--json'], sandbox, env)
    status = json.loads(auth['stdout'])
    if auth['exit'] != 0 or status.get('loggedIn') is not True:
        print(json.dumps({'logged_in': False, 'action': 'operator login required'}))
        return 2
    # No account data, raw auth output or credential content is retained.
    run = sandbox / args.label
    evidence = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004' / args.label
    if run.exists() or evidence.exists():
        parser.error('label must select a fresh run and evidence directory')
    run.mkdir()
    evidence.mkdir()
    repo = run / 'disposable repository'
    repo.mkdir()
    governance = repo / 'governance.txt'
    target = repo / 'governed-target.txt'
    target.write_text('unchanged\n', encoding='utf-8')
    normal = Path(os.environ['USERPROFILE'])
    watched = [normal / '.claude.json', normal / '.claude/settings.json', normal / '.claude/.credentials.json',
               normal / '.claude/plugins/installed_plugins.json', normal / '.claude/plugins/known_marketplaces.json']
    before = probe.metadata(watched)
    runtime = sandbox / 'selected evaluator/Scripts/python.exe'
    removed = runtime.with_suffix('.removed')
    if not runtime.is_file():
        if not probe.contained(runtime, sandbox) or not removed.is_file():
            parser.error('expected task-owned prepared environment or its renamed interpreter')
        removed.rename(runtime)
    plugin = run / 'plugin with spaces'
    config = {'interpreter': str(runtime), 'event_log': str(run / 'events.jsonl'),
              'governance': str(governance), 'archive': probe.ARCHIVE, 'payload': probe.PAYLOAD}
    powershell = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
    probe.create_plugin(plugin, config, powershell)
    manifest = plugin / '.claude-plugin/plugin.json'
    data = json.loads(manifest.read_text())
    data['name'] = 'verity-plane-live-probe'
    probe.dump(manifest, data)
    probe.dump(plugin / 'hooks/hooks.json', {'hooks': {event: [{'hooks': [
        {'type': 'command', 'shell': 'powershell', 'command': inline.INLINE, 'timeout': 25}]}]
        for event in ['SessionStart', 'PreToolUse', 'PostCompact']}})
    settings = run / 'settings.json'
    probe.dump(settings, {'disableAllHooks': False})
    mcp = run / 'empty-mcp.json'
    probe.dump(mcp, {'mcpServers': {}})
    for source in plugin.rglob('*'):
        if source.is_file():
            dest = evidence / 'fixture' / source.relative_to(plugin)
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, dest)
    for source in [Path(__file__), probe.HERE / 'probe.py', probe.HERE / 'inline_probe.py']:
        shutil.copyfile(source, evidence / 'fixture' / (source.stem + '-used.py'))
    probe.publish_json(evidence / 'identities.json', {
        'at': datetime.now(timezone.utc).isoformat(),
        'host': probe.execute([str(args.claude), '--version'], repo, env),
        'authenticated': True, 'profile': str(profile), 'archive_sha256': probe.ARCHIVE,
        'source_sha256': {p.name: probe.digest(p) for p in probe.HERE.iterdir() if p.is_file()},
        'runtime_preparation_actor': 'observer restored existing renamed interpreter, not host-tool setup',
        'documentation': probe.DOCS + ['https://code.claude.com/docs/en/sessions']})
    log = Path(config['event_log'])
    base = [str(args.claude), '--setting-sources', 'user', '--settings', str(settings),
            '--plugin-dir', str(plugin), '--strict-mcp-config', '--mcp-config', str(mcp)]

    def invoke(name, prompt, session, resume=False):
        offset = len(probe.events(log))
        debug = run / (name + '.debug.txt')
        argv = base + ['-p', prompt, '--tools', '', '--permission-mode', 'manual',
            '--permission-prompts', 'none', '--max-turns', '1', '--max-budget-usd', '0.50',
            '--output-format', 'stream-json', '--verbose', '--include-hook-events',
            '--debug-file', str(debug), '--resume' if resume else '--session-id', session]
        result = probe.execute(argv, repo, env, timeout=100)
        if debug.exists():
            probe.publish_capture(debug, evidence / debug.name)
        actual_events = probe.events(log)[offset:]
        probe.publish_json(evidence / (name + '.json'), {'command': result, 'events': actual_events})
        message = result_message(result)
        print(json.dumps({'step': name, 'exit': result['exit'], 'timeout': result['timeout'],
                          'subtype': message.get('subtype'), 'is_error': message.get('is_error'),
                          'result': message.get('result'), 'events': [r['event'] for r in actual_events]}), flush=True)
        return result, actual_events, message

    marker = 'CONTEXT-' + str(uuid.uuid4())
    governance.write_text('PROBE-CONTEXT-ID: ' + marker + '\nObservation fixture; no governance authority granted.\n', encoding='utf-8')
    first_digest = probe.digest(governance)
    prompt = 'Return only the current PROBE-CONTEXT-ID value from your SessionStart hook context. Do not guess or use tools.'
    sessions = [str(uuid.uuid4()), str(uuid.uuid4())]
    observations = [invoke('C03-first', prompt, sessions[0]), invoke('C03-second', prompt, sessions[1])]
    passed = all(completed_successfully(r) and m.get('result', '').strip() == marker
                 and any(e.get('event') == 'SessionStart' and e.get('source') == 'startup' for e in es)
                 for r, es, m in observations)
    probe.save_case(evidence / 'C03', [o[0] for o in observations],
        'Two real fresh conversations repeat context supplied only by the startup hook.',
        {'expected_marker': marker, 'source_sha256': first_digest,
         'events': [o[1] for o in observations], 'messages': [o[2] for o in observations]},
        'pass' if passed else 'fail', identity_evidence=(evidence / 'identities.json').relative_to(probe.ROOT).as_posix())
    new_marker = 'CONTEXT-' + str(uuid.uuid4())
    governance.write_text('PROBE-CONTEXT-ID: ' + new_marker + '\nObservation fixture; no governance authority granted.\n', encoding='utf-8')
    resumed = invoke('C04-resume', prompt, sessions[0], resume=True)
    probe.save_case(evidence / 'C04', [resumed[0]], 'Resume and compaction reload fresh current governance.',
        {'old_source_sha256': first_digest, 'new_source_sha256': probe.digest(governance),
         'expected_marker': new_marker, 'events': resumed[1], 'message': resumed[2],
         'resume_observed': resumed[2].get('result', '').strip() == new_marker,
         'compact': 'not attempted by this no-tools session runner'}, 'unavailable',
        identity_evidence=(evidence / 'identities.json').relative_to(probe.ROOT).as_posix())
    probe.publish_json(run / 'continuation.json', {'base': base, 'repo': str(repo), 'profile': str(profile),
        'sessions': sessions, 'evidence': str(evidence), 'governance': str(governance), 'event_log': str(log),
        'expected_marker': new_marker})
    if log.exists():
        probe.publish_capture(log, evidence / 'events.jsonl')
    probe.publish_json(evidence / 'isolation.json', {'normal_profile_before': before,
        'normal_profile_after': probe.metadata(watched), 'normal_profile_metadata_equal': before == probe.metadata(watched),
        'governed_target_sha256': probe.digest(target), 'governed_target_unchanged': target.read_text() == 'unchanged\n',
        'credential_contents_read_or_copied': False, 'runtime_left_prepared': True})
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
