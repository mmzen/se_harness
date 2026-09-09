"""Record one actual Codex app-server conversation in an existing probe profile.

Uses only generated request schemas. Does not grant trust, answer approvals,
weaken sandboxing, expose login output, or simulate host events.
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import digest, isolated_environment, run, write
from processes import spawn, stop_owned_tree
from sanitize_output import sanitize_text, sanitize_value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', type=Path, required=True)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--resume', help='Actual previously persisted thread id')
    parser.add_argument('--compact', action='store_true')
    args = parser.parse_args()
    sandbox, destination = args.sandbox.resolve(), args.evidence.resolve()
    checkout = Path(__file__).resolve().parents[3]
    evidence_root = checkout / 'docs/engineering/plugin-integration/evidence/WO-PLG-003'
    if sandbox == checkout or checkout in sandbox.parents:
        parser.error('The disposable sandbox must remain outside the checkout.')
    if evidence_root not in destination.parents or destination.exists():
        parser.error('Use a new evidence directory within WO-PLG-003 evidence.')
    env = isolated_environment(sandbox / 'profile')
    status = run([str(args.codex), 'login', 'status'], sandbox / 'repo', env, timeout=20)
    if status['exit_status'] != 0 or status['timed_out']:
        parser.error('Isolated sign-in is required. No session or evidence was created.')
    schema_root = sandbox / 'schemas'
    methods = {'initialize', 'hooks/list', 'skills/list', 'thread/start', 'thread/resume',
               'turn/start', 'thread/compact/start', 'thread/read'}
    client_schema = json.loads((schema_root / 'ClientRequest.json').read_text())
    schema_text = json.dumps(client_schema)
    if any('"' + method + '"' not in schema_text for method in methods):
        parser.error('A required method is absent from this host schema.')
    destination.mkdir(parents=True)
    version = run([str(args.codex), '--version'], sandbox / 'repo', env)
    source_files = list(Path(__file__).parent.glob('*.py'))
    write(destination / 'identity.json', json.dumps(sanitize_value({
        'host_version': version, 'sandbox': str(sandbox),
        'schemas': {str(p.relative_to(schema_root)): digest(p) for p in [
            schema_root / 'ClientRequest.json', schema_root / 'v2/TurnStartParams.json',
            schema_root / 'v2/HookCompletedNotification.json']},
        'source_sha256': {p.name: digest(p) for p in source_files},
        'authenticated_status': 'signed_in', 'normal_profile_used': False,
        'capture_policy': 'Sanitized session observations only; login output is excluded.'
    }), indent=2) + '\n')
    for source in source_files:
        target = destination / 'fixture' / source.name
        target.parent.mkdir(exist_ok=True)
        target.write_bytes(source.read_bytes())
    process = spawn([str(args.codex), 'app-server', '--stdio'], cwd=sandbox / 'repo',
                    env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, text=True, encoding='utf8', errors='replace')
    records, errors = [], []
    sequence = 0
    started = time.monotonic()

    def stdout_reader():
        for line in process.stdout:
            try:
                message = json.loads(line)
            except ValueError:
                message = {'unparsed_stdout': line}
            if str(message.get('method', '')).startswith('account/'):
                message = {'method': message['method'], 'capture_omission': 'account event fields excluded'}
            records.append({'received_at': time.time(), 'message': sanitize_value(message)})

    def stderr_reader():
        for line in process.stderr:
            errors.append(sanitize_text(line))

    readers = [threading.Thread(target=stdout_reader, daemon=True),
               threading.Thread(target=stderr_reader, daemon=True)]
    for reader in readers:
        reader.start()

    def wait_for(predicate, first=0, timeout=60):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            for entry in records[first:]:
                if 'received_at' in entry and predicate(entry['message']):
                    return entry['message']
            if process.poll() is not None:
                break
            time.sleep(.05)
        return {'observer_timeout': True}

    def request(method, params):
        nonlocal sequence
        sequence += 1
        identifier = sequence
        message = {'id': identifier, 'method': method, 'params': params}
        first = len(records)
        records.append({'sent_at': time.time(), 'message': sanitize_value(message)})
        process.stdin.write(json.dumps(message) + '\n')
        process.stdin.flush()
        return wait_for(lambda value: value.get('id') == identifier, first, timeout=30)

    outcome = {'whole_case_conclusion': 'unassessed', 'production_readiness': False}
    try:
        request('initialize', {'clientInfo': {'name': 'codex-live-probe', 'version': '0.0.1'},
                               'capabilities': {'experimentalApi': True}})
        process.stdin.write('{"method":"initialized","params":{}}\n')
        process.stdin.flush()
        request('hooks/list', {'cwds': [str(sandbox / 'repo')]})
        request('skills/list', {'cwds': [str(sandbox / 'repo')], 'forceReload': True})
        params = {'cwd': str(sandbox / 'repo'), 'sandbox': 'read-only', 'approvalPolicy': 'on-request'}
        if args.resume:
            params['threadId'] = args.resume
        else:
            params['ephemeral'] = False
        result = request('thread/resume' if args.resume else 'thread/start', params)
        thread_id = result.get('result', {}).get('thread', {}).get('id')
        outcome['thread_id'] = thread_id
        if thread_id:
            first = len(records)
            request('turn/start', {'threadId': thread_id, 'input': [{'type': 'text',
                'text': 'Reply with the single word READY. Do not use tools or change files.'}]})
            outcome['turn_completion'] = wait_for(lambda value:
                value.get('method') == 'turn/completed' and value.get('params', {}).get('threadId') == thread_id,
                first, timeout=90)
            if args.compact and not outcome['turn_completion'].get('observer_timeout'):
                first = len(records)
                request('thread/compact/start', {'threadId': thread_id})
                outcome['compact_completion'] = wait_for(lambda value:
                    value.get('params', {}).get('threadId') == thread_id and (
                        value.get('method') == 'thread/compacted' or (
                        value.get('method') == 'item/completed' and
                        value.get('params', {}).get('item', {}).get('type') == 'contextCompaction')), first, timeout=90)
                if not outcome['compact_completion'].get('observer_timeout'):
                    # SessionStart(compact) can precede the next model request.
                    # Preserve that real hook/result before closing the server.
                    first = len(records)
                    request('turn/start', {'threadId': thread_id, 'input': [{'type': 'text',
                        'text': 'Reply with the single word READY. Do not use tools or change files.'}]})
                    outcome['post_compact_turn_completion'] = wait_for(lambda value:
                        value.get('method') == 'turn/completed' and
                        value.get('params', {}).get('threadId') == thread_id, first, timeout=90)
            request('thread/read', {'threadId': thread_id, 'includeTurns': True})
    finally:
        try:
            process.stdin.close()
        except (OSError, BrokenPipeError):
            pass
        cleanup = stop_owned_tree(process)
        for reader in readers:
            reader.join(timeout=3)
        outcome.update(seconds=round(time.monotonic() - started, 3), cleanup=cleanup,
                       reader_complete=[not reader.is_alive() for reader in readers])
        write(destination / 'transcript.json', json.dumps(sanitize_value(records), indent=2) + '\n')
        write(destination / 'stderr.txt', sanitize_text(''.join(errors)))
        write(destination / 'observations.json', json.dumps(sanitize_value(outcome), indent=2) + '\n')
        print(json.dumps({'evidence': str(destination), 'thread_id': outcome.get('thread_id'),
                          'turn_observed': 'turn_completion' in outcome and not outcome['turn_completion'].get('observer_timeout'),
                          'compact_observed': 'compact_completion' in outcome and not outcome['compact_completion'].get('observer_timeout')}))


if __name__ == '__main__':
    main()
