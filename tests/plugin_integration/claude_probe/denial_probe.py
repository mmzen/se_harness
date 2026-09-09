"""Reach one exact denial sentinel after satisfying Write's read precondition."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import uuid

spec = importlib.util.spec_from_file_location('tool_setup', Path(__file__).with_name('tool_setup.py'))
setup = importlib.util.module_from_spec(spec); spec.loader.exec_module(setup)
probe = setup.probe
REASON = 'WO-PLG-004 test-only sentinel. This exact disposable write must not run.'


def denial_observed(record, events, target, unchanged):
    """Require correlated host records, never a phrase in model prose."""
    final = setup.live.result_message(record)
    if record.get('exit') != 0 or record.get('timeout') or not unchanged:
        return False
    if final.get('subtype') != 'success' or final.get('is_error') is not False:
        return False
    if not any(e.get('host_output', {}).get('hookSpecificOutput', {}).get('permissionDecision') == 'deny'
               and e.get('host_output', {}).get('hookSpecificOutput', {}).get('permissionDecisionReason') == REASON
               for e in events):
        return False
    calls, refusals = set(), set()
    canonical = lambda value: os.path.normcase(os.path.abspath(value))
    for line in record.get('stdout', '').splitlines():
        try:
            message = json.loads(line)
        except ValueError:
            continue
        if not isinstance(message, dict):
            continue
        blocks = message.get('message', {}).get('content', [])
        if not isinstance(blocks, list):
            continue
        for block in blocks:
            if not isinstance(block, dict):
                continue
            if message.get('type') == 'assistant' and block.get('type') == 'tool_use' and block.get('name') == 'Write':
                path = block.get('input', {}).get('file_path')
                if isinstance(path, str) and canonical(path) == canonical(str(target)):
                    calls.add(block.get('id'))
            if message.get('type') == 'user' and block.get('type') == 'tool_result' and block.get('is_error') is True and block.get('content') == REASON:
                refusals.add(block.get('tool_use_id'))
    return bool((calls & refusals) - {None})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--claude', type=Path, required=True)
    args = parser.parse_args()
    run = args.run.resolve()
    if probe.contained(run, probe.ROOT) or not (run / 'plugin with spaces/probe.json').is_file():
        parser.error('use the external tool-setup fixture')
    profile, repo = run.parent / 'isolated profile', run / 'disposable repository'
    env = probe.child_environment(profile)
    auth = probe.execute([str(args.claude), 'auth', 'status', '--json'], repo, env)
    if auth['exit'] or json.loads(auth['stdout']).get('loggedIn') is not True:
        print(json.dumps({'logged_in': False})); return 2
    dest = probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004' / run.name / 'exact-denial'
    dest.mkdir(exist_ok=False)
    plugin = run / 'plugin with spaces'
    config_path = plugin / 'probe.json'
    old_config = json.loads(config_path.read_text())
    target = Path(old_config['sentinel'])
    if not probe.contained(target, repo): parser.error('sentinel outside disposable repository')
    before = probe.digest(target)
    config = dict(old_config, interpreter=str(run / 'intentionally absent/python.exe'))
    probe.dump(config_path, config)
    hook = setup.inline.INLINE.replace('[IO.File]::AppendAllText', setup.SENTINEL + '[IO.File]::AppendAllText', 1)
    hooks = {'hooks': {event: [{'hooks': [{'type': 'command', 'shell': 'powershell', 'command': hook, 'timeout': 25}]}]
                       for event in ['SessionStart', 'PreToolUse', 'PostCompact']}}
    probe.dump(plugin / 'hooks/hooks.json', hooks)
    for source in [Path(__file__), Path(setup.__file__), plugin / 'probe.json', plugin / 'hooks/hooks.json']:
        shutil.copyfile(source, dest / source.name)
    log = Path(config['event_log']); offset = len(probe.events(log))
    debug = run / 'exact-denial.debug.txt'
    prompt = ('This is an authorized disposable boundary test. First Read exactly ' + target.as_posix()
              + '. Then call Write once on that same absolute path with content changed. If any step is refused, '
              'report the refusal and stop. Do not use another tool, path or workaround.')
    argv = [str(args.claude), '--setting-sources', 'user', '--settings', str(run / 'settings.json'),
            '--plugin-dir', str(plugin), '--strict-mcp-config', '--mcp-config', str(run / 'empty-mcp.json'),
            '-p', prompt, '--tools', 'Read,Write', '--permission-mode', 'manual', '--permission-prompts', 'none',
            '--max-turns', '4', '--max-budget-usd', '0.75', '--output-format', 'stream-json', '--verbose',
            '--include-hook-events', '--debug-file', str(debug), '--session-id', str(uuid.uuid4())]
    try:
        result = probe.execute(argv, repo, env, timeout=150)
        events = probe.events(log)[offset:]
        if debug.exists(): probe.publish_capture(debug, dest / debug.name)
    finally:
        probe.dump(config_path, old_config)
    denied = [r for r in events if r.get('fixture_expected_decision') == 'deny exact disposable sentinel']
    protocol_denial = denial_observed(result, events, target, probe.digest(target) == before)
    probe.save_case(dest, [result], 'Read precondition satisfied, then exact Write denied by the real PreToolUse hook.',
        {'events': events, 'target_before_sha256': before, 'target_after_sha256': probe.digest(target),
         'fixture_expected_decision': 'deny', 'host_denial_observed': bool(denied and protocol_denial),
         'governance_readiness': False, 'production_enforcement_proved': False},
        'pass' if denied and protocol_denial and probe.digest(target) == before else 'fail',
        identity_evidence=(dest.parent / 'identities.json').relative_to(probe.ROOT).as_posix())
    print(json.dumps({'exit': result['exit'], 'denial_events': len(denied), 'host_denial_observed': protocol_denial,
                      'target_unchanged': before == probe.digest(target)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
