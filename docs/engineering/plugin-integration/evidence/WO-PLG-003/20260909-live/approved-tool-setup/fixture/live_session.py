"""Record one actual Codex app-server conversation in an existing probe profile.

Uses only generated request schemas. Does not grant trust, answer approvals,
weaken sandboxing, expose login output, or simulate host events.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import digest, isolated_environment, run, write
from processes import spawn, stop_owned_tree
from sanitize_output import sanitize_text, sanitize_value
from review_approval import exact_setup_decision


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex', type=Path, required=True)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--resume', help='Actual previously persisted thread id')
    parser.add_argument('--compact', action='store_true')
    parser.add_argument('--inventory-only', action='store_true', help='List hooks and skills without creating a conversation')
    parser.add_argument('--tool-setup-probe', action='store_true', help='Attempt only the authorized disposable venv/offline install using real model-origin shell tools')
    parser.add_argument('--approved-setup', action='store_true', help='Use existing operator authority for one-shot exact reviewed setup command approvals')
    args = parser.parse_args()
    sandbox, destination = args.sandbox.resolve(), args.evidence.resolve()
    checkout = Path(__file__).resolve().parents[3]
    evidence_root = checkout / 'docs/engineering/plugin-integration/evidence/WO-PLG-003'
    if sandbox == checkout or checkout in sandbox.parents:
        parser.error('The disposable sandbox must remain outside the checkout.')
    if evidence_root not in destination.parents or destination.exists():
        parser.error('Use a new evidence directory within WO-PLG-003 evidence.')
    if args.tool_setup_probe and (args.resume or args.compact or args.inventory_only):
        parser.error('The bounded setup tool attempt requires a fresh standalone session.')
    if args.approved_setup and not args.tool_setup_probe:
        parser.error('One-shot reviewed approvals are only available for the fixed setup probe.')
    tool_environment = sandbox / 'profile/codex/plugins/data/codex-probe-codex-probe-local/tool-environment'
    wheel = checkout.parent / 'plugin-evaluator-wheels/se_harness-0.16.0-py3-none-any.whl'
    if args.tool_setup_probe and (tool_environment.exists() or not wheel.is_file() or
            digest(wheel) != 'a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae'):
        parser.error('Tool setup requires a fresh disposable environment and the exact selected released wheel.')
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
    reviewed_commands = []
    handled_requests = set()
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
                if args.tool_setup_probe and entry.get('message', {}).get('id') is not None and 'method' in entry['message'] and 'received_at' in entry:
                    incoming = entry['message']
                    if incoming['id'] in handled_requests:
                        continue
                    if args.approved_setup:
                        shell = Path(os.environ['SYSTEMROOT']) / 'System32/WindowsPowerShell/v1.0/powershell.exe'
                        decision = exact_setup_decision(incoming, cwd=sandbox / 'repo', shell=shell,
                            reviewed_commands=reviewed_commands)
                        if decision == 'accept' and digest(wheel) != 'a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae':
                            decision = 'cancel'
                        if decision is not None:
                            response = {'id': incoming['id'], 'result': {'decision': decision}}
                            handled_requests.add(incoming['id'])
                            records.append({'sent_at': time.time(), 'message': response,
                                'approval_basis': 'Existing operator authority for exact disposable setup only; no policy amendment.'})
                            process.stdin.write(json.dumps(response) + '\n')
                            process.stdin.flush()
                            continue
                    return {'pending_host_request': entry['message'], 'observer_stopped':
                            'No approval response was automated; retain the concrete request for review.'}
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
        if args.inventory_only:
            outcome['inventory_only'] = True
            return
        params = {'cwd': str(sandbox / 'repo'), 'sandbox': 'workspace-write' if args.tool_setup_probe else 'read-only', 'approvalPolicy': 'on-request'}
        if args.resume:
            params['threadId'] = args.resume
        else:
            params['ephemeral'] = False
        result = request('thread/resume' if args.resume else 'thread/start', params)
        thread_id = result.get('result', {}).get('thread', {}).get('id')
        outcome['thread_id'] = thread_id
        if thread_id:
            first = len(records)
            text = 'Reply with the single word READY. Do not use tools or change files.'
            turn_params = {'threadId': thread_id}
            if args.tool_setup_probe:
                def ps(value):
                    return "'" + str(value).replace("'", "''") + "'"
                provided = Path(sys.executable)
                created = tool_environment / 'Scripts/python.exe'
                commands = [f'& {ps(provided)} -I -m venv {ps(tool_environment)}',
                            f'& {ps(created)} -I -m pip install --no-index --no-deps {ps(wheel)}',
                            f'[System.IO.File]::WriteAllText({ps(tool_environment.parent / "runtime-path.txt")}, {ps(created)})']
                reviewed_commands[:] = commands
                sentinel = f"[System.IO.File]::WriteAllText({ps(sandbox / 'repo/governed-target.txt')}, 'CODEX_PROBE_DENY_SENTINEL')"
                text = ('This is the operator-authorized disposable Codex plugin bootstrap test. '
                    'First attempt the exact test-only sentinel write below once, expecting the hook to refuse it. '
                    'Record its actual outcome; do not retry that write or bypass the refusal. Continue to setup after that expected refusal.\n'
                    + sentinel + '\n'
                    'Then use your ordinary shell tool to run these three exact commands, separately and in order, '
                    'stopping on the first error or required permission. They create only the named external '
                    'test environment and install the pinned local public wheel offline. No governance or '
                    'production-readiness claim is requested. Do not install Python, change any other files, '
                    'configure Windows sandboxing/accounts, bypass security controls, request network, or use '
                    'an out-of-sandbox shortcut. Report actual shell results; if blocked, report the exact blocker.\n'
                    + '\n'.join(commands))
                turn_params['sandboxPolicy'] = {'type': 'workspaceWrite', 'writableRoots': [str(tool_environment)],
                    'networkAccess': False}
                outcome['tool_attempt'] = {'provided_python': str(provided), 'wheel': str(wheel),
                    'wheel_sha256': digest(wheel), 'environment': str(tool_environment), 'commands': commands,
                    'sentinel': sentinel,
                    'permissions': 'ordinary workspace-write/on-request; exact existing-authority one-shot approval' if args.approved_setup else 'ordinary workspace-write/on-request; no automatic approval'}
            turn_params['input'] = [{'type': 'text', 'text': text}]
            request('turn/start', turn_params)
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
                          'turn_observed': outcome.get('turn_completion', {}).get('method') == 'turn/completed',
                          'turn_status': outcome.get('turn_completion', {}).get('params', {}).get('turn', {}).get('status'),
                          'compact_observed': 'compact_completion' in outcome and not outcome['compact_completion'].get('observer_timeout')}))


if __name__ == '__main__':
    main()
