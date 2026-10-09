"""Record a native agent session; do not select or execute its workflow steps.

Inputs are operator-selected local paths and a task file. The optional loopback
proxy drops the first accepted lifecycle reply. It never performs recovery.
Provider authentication stays in the native host's normal credential store.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import socket
import subprocess
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from native_call import contained, instructions, lookup_file


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


class ReplyFault:
    """Forward local traffic and retain evidence of one discarded reply."""

    def __init__(self, endpoint, output):
        parsed = urllib.parse.urlsplit(endpoint)
        if parsed.scheme != 'http' or parsed.hostname != '127.0.0.1' or parsed.path:
            raise ValueError('Use an explicit loopback HTTP service without a path')
        self.events = []
        self.dropped = False
        self.lock = threading.Lock()
        fault = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def forward(self):
                size = int(self.headers.get('Content-Length', '0'))
                if size > 4 * 1024 * 1024:
                    self.send_error(413)
                    return
                body = self.rfile.read(size) if size else None
                headers = {k: v for k, v in self.headers.items()
                           if k.lower() not in ('host', 'connection', 'content-length')}
                request = urllib.request.Request(endpoint+self.path, body, headers, method=self.command)
                try:
                    response = urllib.request.urlopen(request, timeout=180)
                except urllib.error.HTTPError as exc:
                    response = exc
                with response:
                    raw = response.read(2 * 1024 * 1024 + 1)
                    status = response.status
                    content_type = response.headers.get('Content-Type', 'application/json')
                try:
                    sent, received = json.loads(body or b'null'), json.loads(raw)
                except ValueError:
                    sent, received = None, None
                with fault.lock:
                    drop = (not fault.dropped and isinstance(sent, dict)
                            and sent.get('schema') == 'se-harness-lifecycle-command/v2'
                            and sent.get('mode') == 'apply' and isinstance(received, dict)
                            and received.get('outcome') == 'accepted')
                    if drop:
                        fault.dropped = True
                        fault.events.append({'status': status, 'operation_key': sent['operation_key'],
                                             'result': received, 'reply_dropped': True})
                        save(output/'reply-fault.json', fault.events)
                if drop:
                    self.close_connection = True
                    self.connection.shutdown(socket.SHUT_RDWR)
                    self.connection.close()
                    return
                self.send_response(status)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(raw)))
                self.end_headers()
                self.wfile.write(raw)

            do_POST = forward
            do_GET = forward

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.endpoint = 'http://127.0.0.1:' + str(self.server.server_port)

    def close(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()


def prepare_output(output, prepared_inputs=False):
    if not prepared_inputs:
        output.mkdir(parents=True, exist_ok=False)
        return
    if output.is_symlink() or output.is_junction() or not output.is_dir():
        raise ValueError('Prepared output must be an existing ordinary directory')
    if {p.name for p in output.iterdir()} != {'inputs', 'work'}:
        raise ValueError('Prepared output must contain only inputs and empty work')
    for child in (output/'inputs', output/'work'):
        if child.is_symlink() or child.is_junction() or not child.is_dir():
            raise ValueError('Prepared inputs and work must be ordinary directories')
    if any((output/'work').iterdir()):
        raise ValueError('Prepared work directory must be empty')


def instruction_entry(root, settings, selectors):
    """Copy operator-selected canonical sections and manifest pointers, not answers."""
    view = instructions(root, settings, selectors)
    manifest_path = contained(root, settings['source_manifest'])
    name = manifest_path.relative_to(root / 'inputs').as_posix()
    manifest_entry = lookup_file(root, settings, name)['file']
    manifest = json.loads(manifest_path.read_bytes())
    artifacts = manifest['artifacts']
    if not isinstance(artifacts, list) or len(artifacts) > 100:
        raise ValueError('Entry requires at most 100 exact source-manifest pointers')
    pointers, ids = [], set()
    for artifact in artifacts:
        item = lookup_file(root, settings, 'source/' + artifact['path'])['file']
        if (artifact['artifact_id'] in ids or item['bytes'] != artifact['bytes']
                or item['sha256'] != artifact['raw_sha256']):
            raise ValueError('Source-manifest identity differs from its staged input')
        ids.add(artifact['artifact_id'])
        pointers.append({'id': artifact['artifact_id'], 'path': item['path'],
                         'sha256': item['sha256']})
    packet = {'instruction_view': view, 'source_manifest': manifest_entry,
              'artifact_pointers': pointers,
              'claim': 'Explicit task inputs, not automatic startup-delivery evidence. '
                       'Pointers are not artifact content reads.'}
    parts = ['## Selected instruction entry\n\n'
             'The following complete canonical sections are already supplied in this context. '
             'Apply them before commentary and actions. Reuse them while unchanged and retained; '
             'read additional references only when their conditions apply. '
             'After compaction, recover this entry from task.md. '
             + packet['claim'] + '\n']
    for resource in view['resources']:
        parts.append('\nSource: ' + json.dumps({k: resource[k] for k in
                     ('resource', 'path', 'release', 'sha256')}) + '\n')
        for section in resource['sections']:
            if 'content' in section:
                parts.append('\n' + section['content'])
    parts.append('\n## Existing artifact pointers\n\n'
                 'These records are available for inspection. Their presence does not '
                 'establish that they cover this request. Select and read the applicable '
                 'records before making content claims.\n\n' + json.dumps(pointers) + '\n')
    text = ''.join(parts)
    if len(text.encode('utf-8')) > 64 * 1024:
        raise ValueError('Selected instruction entry exceeds 64 KiB; select narrower sections')
    return packet, text


def write_prompt(stream, prompt):
    """Do not translate canonical LF or CRLF sections on Windows stdin."""
    stream.reconfigure(newline='')
    stream.write(prompt)
    stream.close()


def prompt_pointer(path):
    """Deliver the task once, through a file read that is visible in the capture."""
    return (f'Read `{path}` before your first explanation or action. '
            'It contains the complete task and selected instruction entry. '
            'Apply that content directly; do not reread it while retained and unchanged. '
            'After compaction, recover from the same file. '
            'This explicit test setup is not automatic startup-delivery evidence.')


def run(args):
    output = args.output.resolve()
    prepare_output(output, args.prepared_inputs)
    settings = json.loads(args.selection.read_text(encoding='utf-8'))
    credentials = json.loads(args.credentials.read_text(encoding='utf-8'))
    secrets = [p['token'] for p in credentials['principals']]
    token = next(p['token'] for p in credentials['principals'] if p['id'] == 'operator')
    env = dict(os.environ, PYTHONUTF8='1', NO_COLOR='1', HAG_NATIVE_TEST_TOKEN=token)
    env.update(HAG_NATIVE_WORK_DIRECTORY=str(output), HAG_NATIVE_SELECTION=str(output/'selection.json'))
    settings.pop('credentials', None)
    actual_endpoint = settings['endpoint']
    fault = ReplyFault(actual_endpoint, output) if args.drop_reply else None
    if fault:
        settings['endpoint'] = fault.endpoint
    settings.update(token_variable='HAG_NATIVE_TEST_TOKEN',
                    instruction_delivery='session-local plugin' if args.host == 'claude' else 'explicit resource reads')
    save(output/'selection.json', settings)
    preparation_start = time.monotonic()
    entry = None
    prompt_prefix = ''
    if getattr(args, 'instruction_section', None):
        entry, prompt_prefix = instruction_entry(output, settings, args.instruction_section)
        save(output/'instruction-entry.json', entry)
    prompt = prompt_prefix + ('Before your first explanation, apply the supplied sections and read '
        'only the applicable plugin instructions and prerequisites still missing from context. '
        'Use the existing file tools below. This explicit test setup does not '
        'establish automatic startup instruction delivery.\n\n'
        + args.task.read_text(encoding='utf-8').replace('SELECTION_FILE', str(output/'selection.json')))
    if args.host == 'codex' and settings.get('approved_shell_argv_prefix'):
        prompt += ('\n\n## Codex file discovery\n\n'
            'If native Read is unavailable, use this existing approved helper prefix:\n\n```json\n'
            + json.dumps(settings['approved_shell_argv_prefix']) + '\n```\n'
            'Append `read-json ABSOLUTE_FILE` to read selection.json, or '
            '`read-text ABSOLUTE_FILE` for an inventoried input or work text file. '
            'Use native patch/file tools for writing. This host adaptation replaces only '
            'the unavailable native Read route; keep one helper call per invocation, '
            'normal permissions, the same selected task and all other restrictions. '
            'It supplies no workflow operation, request values, draft or decision.\n')
    (output/'task.md').write_bytes(prompt.encode('utf-8'))
    initial_prompt = prompt_pointer(output/'task.md')
    locator = None
    if args.host == 'claude':
        locator = output/'CLAUDE.md'
        # Keep operator inputs discoverable when conversation text is compacted.
        # This supplies no workflow request, state, actor or decision.
        with locator.open('x', encoding='utf-8') as stream:
            stream.write('# Disposable qualification task inputs\n\n'
                + initial_prompt + '\n'
                f'Read `{output / "selection.json"}` before acting.\n'
                'These files retain the task, selected inputs and tool boundary.\n'
                'Use the selected candidate plugin skills and their required references for the workflow.\n'
                'This file supplies no lifecycle procedure or new permission.\n')
            if settings.get('approved_shell_argv_prefix'):
                stream.write('\nThe existing approved shell prefix is this argument array:\n\n```json\n'
                    + json.dumps(settings['approved_shell_argv_prefix']) + '\n```\n')
                stream.write('\nUse one helper command per Bash call. Do not add a pipeline, a second\n'
                    'command (including echo), a shell wrapper or arbitrary Python. The tool\n'
                    'result already reports the exit status. Use native Read/Write/Edit tools\n'
                    'for files, including retained results. These are the existing tool limits.\n')
    plugin = Path(settings['plugin'])
    mcp_url = actual_endpoint + '/mcp'
    if args.host == 'codex':
        argv = [str(args.executable), '--no-daemon', 'exec', '--ephemeral', '--skip-git-repo-check',
                '--json', '-C', str(output), '--approve-for-me',
                '-c', 'plugins."verity-plane@se-harness".enabled=false',
                '-c', f'mcp_servers.hag.url={json.dumps(mcp_url)}',
                '-c', 'mcp_servers.hag.bearer_token_env_var="HAG_NATIVE_TEST_TOKEN"',
                '-c', 'mcp_servers.hag.required=true',
                '-c', 'mcp_servers.hag.tool_timeout_sec=180']
        if args.model:
            argv += ['--model', args.model]
    else:
        save(output/'mcp.json', {'mcpServers': {'hag': {'type': 'http', 'url': mcp_url,
             'headers': {'Authorization': 'Bearer ${HAG_NATIVE_TEST_TOKEN}'}, 'timeout': 180000}}})
        argv = [str(args.executable), '-p', '--no-session-persistence', '--plugin-dir', str(plugin),
                # Use only the operator's pre-approved tools. The automatic
                # classifier can allow commands outside that bounded grant.
                '--permission-mode', 'dontAsk', '--permission-prompts', 'none',
                # Keep the normal instruction-loading tool available to the
                # session-local plugin; file and command permissions still apply.
                '--tools', 'Read,Write,Edit,Bash,Skill,ToolSearch', '--mcp-config', str(output/'mcp.json'),
                '--strict-mcp-config', '--output-format', 'stream-json', '--verbose', '--include-hook-events']
        if args.permission_settings:
            argv += ['--settings', str(args.permission_settings.resolve())]
        if args.model:
            argv += ['--model', args.model]
    # A selected entry can exceed Windows' command-line limit. Both hosts accept
    # the prompt on stdin; credentials still use the existing environment route.
    if args.host == 'codex':
        argv.append('-')
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start = time.monotonic()
    timed_out = threading.Event()
    redact_count = 0
    stream_path = output/'events.jsonl'
    before = {'selection': hashlib.sha256(args.selection.read_bytes()).hexdigest(),
              'driver': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'task': hashlib.sha256(args.task.read_bytes()).hexdigest(),
              'effective_prompt': hashlib.sha256(initial_prompt.encode('utf-8')).hexdigest(),
              'task_file': hashlib.sha256(prompt.encode('utf-8')).hexdigest()}
    if args.permission_settings:
        before['permission_settings'] = hashlib.sha256(args.permission_settings.read_bytes()).hexdigest()
    if locator:
        before['task_locator'] = hashlib.sha256(locator.read_bytes()).hexdigest()
    if entry:
        before['instruction_entry'] = hashlib.sha256((output/'instruction-entry.json').read_bytes()).hexdigest()
    save(output/'invocation.json', {'host': args.host, 'argv': argv, 'cwd': str(output),
        'started_at': started, 'timeout_seconds': args.timeout, 'input_sha256': before,
        'prompt_file': str(output/'task.md'), 'prompt_transport': 'stdin-file-pointer',
        'initial_prompt': initial_prompt,
        'entry_preparation_seconds': round(start-preparation_start, 3),
        'environment_keys_added': ['PYTHONUTF8','NO_COLOR','HAG_NATIVE_TEST_TOKEN',
                                 'HAG_NATIVE_WORK_DIRECTORY','HAG_NATIVE_SELECTION'],
        'claim': 'Observed native calls only; this launcher supplies no workflow requests or decisions.'})
    try:
        with subprocess.Popen(argv, cwd=output, env=env, stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, encoding='utf-8', errors='replace') as child:
            def stop():
                timed_out.set()
                child.kill()
            timer = threading.Timer(args.timeout, stop)
            timer.start()
            try:
                write_prompt(child.stdin, initial_prompt)
                with stream_path.open('x', encoding='utf-8') as stream:
                    for line in child.stdout:
                        for secret in secrets:
                            if secret in line:
                                redact_count += line.count(secret)
                                line = line.replace(secret, '[REDACTED-SANDBOX-TOKEN]')
                        line, count = re.subn(r'sk-ant-(?:oat|ort|api)[^\s"\\]+', '[REDACTED-PROVIDER-TOKEN]', line)
                        redact_count += count
                        stream.write(line)
                        stream.flush()
                        try:
                            event = json.loads(line)
                        except ValueError:
                            continue
                        item = event.get('item', {})
                        if event.get('type') == 'item.completed':
                            print(json.dumps({'host':args.host,'type':item.get('type'),
                                'tool':item.get('tool'),'status':item.get('status'),
                                'text':item.get('text') if item.get('type')=='agent_message' else None}),flush=True)
                        if event.get('type') == 'system' and event.get('subtype') == 'init':
                            print(json.dumps({'host':args.host,'event':'init','model':event.get('model'),
                                'plugins':event.get('plugins'),'mcp_servers':event.get('mcp_servers')}),flush=True)
                        for block in event.get('message',{}).get('content',[]) if isinstance(event.get('message'),dict) else []:
                            if isinstance(block,dict) and block.get('type') == 'tool_use':
                                print(json.dumps({'host':args.host,'tool':block.get('name')}),flush=True)
                        if event.get('type') == 'result':
                            print(json.dumps({'host':args.host,'event':'result','error':event.get('is_error'),
                                'text':event.get('result')}),flush=True)
                code = child.wait()
            finally:
                timer.cancel()
    finally:
        if fault:
            fault.close()
    result = {'host':args.host,'exit':code,'timed_out':timed_out.is_set(),
        'elapsed_seconds':round(time.monotonic()-start,3),'reply_dropped':bool(fault and fault.dropped),
        'redactions':redact_count,'events_sha256':hashlib.sha256(stream_path.read_bytes()).hexdigest(),
        'outcome':'observation_retained','qualification':'requires independent assessment'}
    save(output/'session.json',result)
    print(json.dumps(result),flush=True)
    return code or int(timed_out.is_set())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host',choices=('codex','claude'),required=True)
    for name in ('executable','selection','credentials','task','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--model')
    parser.add_argument('--instruction-section', action='append',
                        help='Operator-selected canonical RESOURCE_ID#HEADING for the opening context')
    parser.add_argument('--timeout',type=int,default=2700)
    parser.add_argument('--drop-reply',action='store_true')
    parser.add_argument('--prepared-inputs',action='store_true',help='Use an operator-staged inputs directory and empty work directory')
    parser.add_argument('--permission-settings',type=Path,help='Exact separately approved Claude session-only settings file')
    raise SystemExit(run(parser.parse_args()))
