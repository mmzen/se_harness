"""Observe real resume and /compact for an existing isolated fixture session."""
import argparse
import importlib.util
import json
from pathlib import Path
import shutil
import uuid

spec = importlib.util.spec_from_file_location('live_sessions', Path(__file__).with_name('live_sessions.py'))
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)
probe = live.probe


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run', type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--missing-runtime', action='store_true')
    args = parser.parse_args()
    run = args.run.resolve()
    if probe.contained(run, probe.ROOT) or Path(args.label).name != args.label:
        parser.error('use an external existing run and a single fresh label')
    data = json.loads((run / 'continuation.json').read_text())
    repo, profile = Path(data['repo']), Path(data['profile'])
    if not probe.contained(repo, run) or profile != run.parent / 'isolated profile':
        parser.error('run context does not match its isolated profile/repository')
    evidence_root = Path(data['evidence'])
    if not probe.contained(evidence_root, probe.ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004'):
        parser.error('evidence outside work order')
    dest = evidence_root / args.label
    dest.mkdir(exist_ok=False)
    private = run / args.label
    private.mkdir(exist_ok=False)
    shutil.copyfile(__file__, dest / 'runner-used.py')
    env = probe.child_environment(profile)
    auth = probe.execute([data['base'][0], 'auth', 'status', '--json'], repo, env)
    if auth['exit'] != 0 or json.loads(auth['stdout']).get('loggedIn') is not True:
        print(json.dumps({'logged_in': False}))
        return 2
    config_path = run / 'plugin with spaces/probe.json'
    original_config = json.loads(config_path.read_text())
    if args.missing_runtime:
        probe.dump(config_path, dict(original_config, interpreter=str(run / 'not installed/python.exe')))
    log = Path(data['event_log'])
    governance = Path(data['governance'])
    session = str(uuid.uuid4()) if args.missing_runtime else data['sessions'][1]
    records, all_events = [], []

    def invoke(name, prompt, resume=True):
        offset = len(probe.events(log))
        debug = private / (name + '.debug.txt')
        argv = data['base'] + ['-p', prompt, '--tools', '', '--permission-mode', 'manual',
            '--permission-prompts', 'none', '--max-turns', '1', '--max-budget-usd', '0.50',
            '--output-format', 'stream-json', '--verbose', '--include-hook-events',
            '--debug-file', str(debug), '--resume' if resume else '--session-id', session]
        result = probe.execute(argv, repo, env, timeout=100)
        records.append(result)
        observed = probe.events(log)[offset:]
        all_events.extend(observed)
        if debug.exists():
            probe.publish_capture(debug, dest / debug.name)
        message = live.result_message(result)
        probe.publish_json(dest / (name + '.json'), {'command': result, 'events': observed})
        print(json.dumps({'step': name, 'exit': result['exit'], 'result': message.get('result'),
                          'events': [r.get('event') + ':' + str(r.get('source')) for r in observed]}), flush=True)
        return result

    old_digest = probe.digest(governance)
    governance.write_text('Fixture revision: resume-' + str(uuid.uuid4()) + '\nObservation fixture; no authority granted.\n', encoding='utf-8')
    resume_digest = probe.digest(governance)
    if args.missing_runtime:
        invoke('startup', '/verity-plane-live-probe:setup', resume=False)
    invoke('resume', 'Say ready. Do not use tools.')
    governance.write_text('Fixture revision: compact-' + str(uuid.uuid4()) + '\nObservation fixture; no authority granted.\n', encoding='utf-8')
    compact_digest = probe.digest(governance)
    compact = invoke('compact', '/compact')
    boundaries = []
    for line in compact['stdout'].splitlines():
        try:
            value = json.loads(line)
        except ValueError:
            continue
        if value.get('type') == 'system' and value.get('subtype') == 'compact_boundary':
            boundaries.append(value)
    if not boundaries and 'Not enough messages' in compact['stdout']:
        invoke('seed-history', 'Explain the purpose of a software smoke test in three short sentences. Do not use tools.')
        compact = invoke('compact-retry', '/compact')
        boundaries = [json.loads(line) for line in compact['stdout'].splitlines()
                      if line.startswith('{') and json.loads(line).get('subtype') == 'compact_boundary']
    startup = [r for r in all_events if r.get('event') == 'SessionStart']
    resumed = [r for r in startup if r.get('source') == 'resume']
    compacted = [r for r in startup if r.get('source') == 'compact']
    postcompact = [r for r in all_events if r.get('event') == 'PostCompact']
    ready_context = lambda rows, expected: any(json.loads(r.get('handler_output', '{}')).get('source_sha256') == expected
                                              and r.get('host_output', {}).get('hookSpecificOutput', {}).get('additionalContext') for r in rows)
    if args.missing_runtime:
        passed = bool(resumed and compacted and postcompact and boundaries) and all(r.get('handler_invoked') is False for r in all_events)
    else:
        passed = bool(boundaries and postcompact) and ready_context(resumed, resume_digest) and ready_context(compacted, compact_digest)
    probe.save_case(dest, records, 'Actual resume and compaction deliver current hook events/context, or missing-runtime guidance.',
        {'mode': 'missing-runtime' if args.missing_runtime else 'prepared-runtime', 'events': all_events,
         'old_source_sha256': old_digest, 'resume_source_sha256': resume_digest,
         'compact_source_sha256': compact_digest, 'compact_boundaries': boundaries,
         'governance_readiness': False, 'session': session,
         'documentation': 'https://code.claude.com/docs/en/agent-sdk/slash-commands#compact-history-with-compact'},
        'pass' if passed else 'fail', identity_evidence=(evidence_root / 'identities.json').relative_to(probe.ROOT).as_posix())
    probe.dump(config_path, original_config)
    probe.publish_capture(log, evidence_root / 'events.jsonl')
    print(json.dumps({'conclusion': 'pass' if passed else 'fail', 'evidence': str(dest)}))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
