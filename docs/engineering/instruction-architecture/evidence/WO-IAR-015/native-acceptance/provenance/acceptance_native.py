"""Native acceptance probes in disposable repositories; no production decisions."""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import os
import queue
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid

import run_demo

HERE = Path(__file__).resolve().parent
RELEASED = Path(r'C:\Users\mathi\Documents\Codex\plugin-data\verity-plane\evaluator\Scripts\python.exe')
PROBE = """This is a read-only acceptance probe of the current instruction delivery.
Do not call tools or read files. Use only the newest delivered hook context.
Return JSON containing instruction_file_path, harness_version, entry_sha256,
final_heading, delivery_gap, reason, and governed_action_allowed.
Copy the path following 'SE Harness instruction source:', the version after
'Selected release:', and the 64 hex characters after 'entry SHA-256:'.
For a delivery failure return null for those three values and final_heading,
delivery_gap=true, governed_action_allowed=false, and the actual failure reason.
For successful delivery set delivery_gap=false. Delivery alone grants no work
authority; governed_action_allowed must reflect this. Do not reuse old context."""


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def snapshot(root):
    return {p.relative_to(root).as_posix(): sha(p) for p in root.rglob('*')
            if p.is_file() and '.git' not in p.relative_to(root).parts
            and '__pycache__' not in p.parts}


class Codex:
    def __init__(self, manifest, out, review_commands=False):
        self.out, self.events, self.counter, self.phase = out, [], 0, 'initialize'
        self.review_commands = review_commands
        self.q = queue.Queue()
        self.argv = [manifest['host_executables']['codex'], '--enable', 'hooks',
                     'app-server', '--listen', 'stdio://']
        env = run_demo.child_env(Path(manifest['demo']), 'codex')
        self.p = subprocess.Popen(self.argv, cwd=out, env=env, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', bufsize=1)
        self.stderr_count = 0
        def stdout():
            for line in self.p.stdout:
                try: self.q.put(json.loads(line))
                except ValueError: self.q.put({'capture_error': 'Invalid native JSON'})
            self.q.put({'capture_error': 'Native stdout closed'})
        def stderr():
            for line in self.p.stderr: self.stderr_count += 1
        threading.Thread(target=stdout, daemon=True).start()
        threading.Thread(target=stderr, daemon=True).start()
        self.rpc('initialize', {'clientInfo': {'name': 'iar_acceptance', 'version': '1.0'},
                               'capabilities': {'experimentalApi': True}})
        self.send({'method': 'initialized', 'params': {}})

    def record(self, value):
        item = {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'phase': self.phase, **value}
        self.events.append(item)
        with (self.out/'native-events.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')

    def send(self, v):
        self.p.stdin.write(json.dumps(v) + '\n'); self.p.stdin.flush()

    def receive(self, timeout):
        v = self.q.get(timeout=timeout)
        if 'capture_error' in v: raise RuntimeError(v['capture_error'])
        method = v.get('method', '')
        if method and 'id' in v:
            self.record({'approval_request': v})
            if self.review_commands and method == 'item/commandExecution/requestApproval':
                request_digest = hashlib.sha256(json.dumps(v, sort_keys=True).encode()).hexdigest()
                pending = self.out/'pending-command.json'
                save(pending, {'sha256': request_digest, 'request': v})
                decision_path = self.out/(request_digest+'.decision.json')
                print('Command review needed: '+str(pending), flush=True)
                deadline = time.monotonic()+300
                while not decision_path.exists() and time.monotonic() < deadline: time.sleep(.2)
                if not decision_path.exists(): raise TimeoutError('Specific command review')
                decision = json.loads(decision_path.read_text(encoding='utf-8'))
                if decision.get('sha256') != request_digest or decision.get('decision') not in ('accept','decline'):
                    raise RuntimeError('Invalid specific command decision')
                self.record({'command_review': decision})
                self.send({'id': v['id'], 'result': {'decision': decision['decision']}})
                pending.unlink()
                return v
            self.send({'id': v['id'], 'error': {'code': -32000, 'message': 'Acceptance probe grants no approval'}})
            raise RuntimeError('Native approval/input requested: ' + method)
        if method.startswith('hook/') or method in ('error', 'warning', 'turn/completed'):
            self.record({'notification': v})
        elif method in ('item/started', 'item/completed'):
            item = v.get('params', {}).get('item', {})
            if item.get('type') in ('contextCompaction', 'commandExecution', 'fileChange') or (
                item.get('type') == 'agentMessage' and method == 'item/completed'):
                self.record({'notification': v})
        return v

    def rpc(self, method, params):
        self.counter += 1; ident = self.counter
        self.record({'request': {'method': method, 'params': params}})
        self.send({'id': ident, 'method': method, 'params': params})
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            v = self.receive(max(.1, deadline-time.monotonic()))
            if v.get('id') == ident and 'method' not in v:
                if 'error' in v: raise RuntimeError(method + ': ' + json.dumps(v['error']))
                return v['result']
        raise TimeoutError(method)

    def wait_turn(self, thread):
        deadline = time.monotonic() + 360
        while time.monotonic() < deadline:
            v = self.receive(max(.1, deadline-time.monotonic()))
            p = v.get('params', {})
            if v.get('method') == 'turn/completed' and p.get('threadId') == thread:
                if p['turn']['status'] != 'completed': raise RuntimeError(json.dumps(p['turn'].get('error')))
                return
        raise TimeoutError('turn')

    def probe(self, root, phase, thread=None, prompt=PROBE):
        self.phase = phase
        start = len(self.events)
        if thread is None:
            r = self.rpc('thread/start', {'cwd': str(root), 'ephemeral': True, 'sandbox': 'read-only'})
            thread = r['thread']['id']
        else:
            self.rpc('thread/compact/start', {'threadId': thread})
            self.wait_turn(thread)
        self.rpc('turn/start', {'threadId': thread, 'cwd': str(root),
                               'input': [{'type': 'text', 'text': prompt}]})
        self.wait_turn(thread)
        return thread, self.events[start:]

    def close(self):
        self.p.stdin.close()
        try: self.p.wait(timeout=10)
        except subprocess.TimeoutExpired: self.p.terminate(); self.p.wait(timeout=10)


def extract_codex(events):
    contexts, replies = [], []
    for e in events:
        v = e.get('notification', {}); p = v.get('params', {})
        if v.get('method') == 'hook/completed':
            run = p.get('run', {})
            if run.get('eventName') == 'sessionStart' and run.get('source') == 'plugin':
                contexts += [a['text'] for a in run.get('entries', []) if a.get('kind') == 'context']
        if v.get('method') == 'item/completed' and p.get('item', {}).get('type') == 'agentMessage':
            replies.append(p['item']['text'])
    return contexts, replies


def claude_probe(manifest, root, out, phase, resume=None, prompt=PROBE, tools='', hook_only=False):
    debug = out/(phase+'.debug.log')
    argv = [manifest['host_executables']['claude'], '--print', '--verbose',
            '--output-format', 'stream-json', '--include-hook-events', '--tools', tools,
            '--strict-mcp-config', '--permission-prompts', 'none', '--debug-file', str(debug)]
    if hook_only:
        argv += ['--init-only']
    else:
        if resume: argv += ['--resume', resume, '--fork-session']
        argv.append(prompt)
    before = snapshot(root)
    p = subprocess.run(argv, cwd=root, env=run_demo.child_env(Path(manifest['demo']), 'claude'),
                       capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=360)
    events = []
    for line in p.stdout.splitlines():
        try: v = json.loads(line)
        except ValueError: continue
        # No private reasoning blocks or auth diagnostics are retained.
        if v.get('type') == 'assistant':
            v['message']['content'] = [c for c in v['message'].get('content', []) if c.get('type') != 'thinking']
        if v.get('type') in ('assistant', 'user', 'result') or 'hook' in v.get('subtype', ''):
            events.append(v)
    save(out/(phase+'.events.json'), events)
    selected = []
    if debug.exists():
        selected = [l for l in debug.read_text(encoding='utf-8', errors='replace').splitlines()
                    if any(m in l for m in ('Hooks: Parsed initial response:', 'provided additionalContext',
                                            'Hook SessionStart:', 'Successfully parsed and validated hook JSON output'))]
    (out/(phase+'.hooks.log')).write_text('\n'.join(selected)+'\n', encoding='utf-8')
    save(out/(phase+'.invocation.json'), {'argv': argv, 'cwd': str(root), 'exit_code': p.returncode,
         'before': before, 'after': snapshot(root), 'stderr_bytes': len(p.stderr.encode())})
    if p.returncode: raise RuntimeError('Claude exited '+str(p.returncode)+': '+p.stderr[-800:])
    contexts = []
    for l in selected:
        marker = 'Hooks: Parsed initial response: '
        if marker in l:
            try:
                parsed = json.loads(l.split(marker, 1)[1])
                c = parsed.get('hookSpecificOutput', {}).get('additionalContext')
                if c: contexts.append(c)
            except ValueError: pass
    replies = [c['text'] for e in events if e.get('type') == 'assistant'
               for c in e['message'].get('content', []) if c.get('type') == 'text']
    session = next((e.get('session_id') for e in reversed(events) if e.get('session_id')), None)
    return session, contexts, replies


def assess(root, contexts, replies, expected_error=None, hook_only=False):
    joined = '\n'.join(contexts)
    if expected_error:
        valid = expected_error in joined and 'Stop the affected governed action' in joined
        leaked = any(c.startswith('SE Harness instruction source:') for c in contexts)
        valid = valid and not leaked
    else:
        text = (root/'ENGINEERING_HARNESS.md').read_text(encoding='utf-8')
        digest = hashlib.sha256(text.encode()).hexdigest()
        valid = any(str(root/'ENGINEERING_HARNESS.md') in c and digest in c and c.endswith(text) for c in contexts)
    parsed = None
    for reply in reversed(replies):
        try: parsed = json.loads(reply.removeprefix('```json').removeprefix('```').removesuffix('```').strip()); break
        except ValueError: pass
    if parsed is not None:
        valid = valid and parsed.get('delivery_gap') is bool(expected_error) and parsed.get('governed_action_allowed') is False
        if not expected_error:
            valid = valid and parsed.get('entry_sha256') == digest and Path(parsed.get('instruction_file_path', '')) == root/'ENGINEERING_HARNESS.md'
    elif not hook_only: valid = False
    return {'passed': valid, 'context_count': len(contexts), 'expected_error': expected_error, 'probe': parsed,
            'model_response_assessed': not hook_only,
            'context_sha256': [hashlib.sha256(c.encode()).hexdigest() for c in contexts], 'replies': replies}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('host', choices=['codex', 'claude'])
    args = parser.parse_args()
    manifest = json.loads((HERE/'prepared-demo.json').read_text())
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = HERE/'observations'/f'{args.host}-boundaries-{stamp}-{uuid.uuid4().hex[:6]}'
    out.mkdir(parents=True)
    base = Path(tempfile.mkdtemp(prefix='iar-native-boundaries-'))
    source = Path(manifest['roots'][args.host]['repository'])
    roots = {}
    for case in ('current', 'missing', 'altered', 'mismatch'):
        root = base/case
        shutil.copytree(source, root, ignore=shutil.ignore_patterns('.git', '__pycache__'))
        (root/'.git').mkdir(); roots[case] = root
    (roots['missing']/'ENGINEERING_HARNESS.md').unlink()
    with (roots['altered']/'ENGINEERING_HARNESS.md').open('a', encoding='utf-8') as f: f.write('\nAltered acceptance fixture.\n')
    config = roots['mismatch']/'.engineering-harness.toml'
    config.write_text(config.read_text().replace('0.19.0', '0.18.0'), encoding='utf-8')
    old = base/'released-018'; old.mkdir(); (old/'.git').mkdir()
    argv = [str(RELEASED), '-I', '-B', '-m', 'se_harness', 'init', str(old), '--project-name', 'Released 0.18 switch fixture', '--json']
    env = os.environ.copy(); env.pop('PYTHONPATH', None)
    env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='safe.directory', GIT_CONFIG_VALUE_0=old.as_posix())
    p = subprocess.run(argv, cwd=base, env=env, capture_output=True, text=True)
    save(out/'released-fixture-init.json', {'argv': argv, 'exit_code': p.returncode, 'stdout': p.stdout, 'stderr': p.stderr})
    if p.returncode: raise RuntimeError('Released fixture init failed')
    roots['released-018'] = old
    before = {name: snapshot(root) for name, root in roots.items()}
    report = {'status': 'running', 'host': args.host, 'base': str(base), 'source_candidate': manifest['source_commit'],
              'host_version': subprocess.check_output([manifest['host_executables'][args.host], '--version'], text=True).strip(),
              'cases': [], 'limits': 'Windows native host. Disposable repository fixtures. No production lifecycle authority or verification acceptance.'}
    save(out/'observation.json', report)
    print('Native boundary capture: '+str(out), flush=True)
    client = Codex(manifest, out) if args.host == 'codex' else None
    try:
        thread = None
        for case in ('current', 'released-018', 'current-return', 'missing', 'altered', 'mismatch'):
            root = roots['current' if case == 'current-return' else case]
            error = {'missing': 'required regular file is unavailable: ENGINEERING_HARNESS.md',
                     'altered': 'does not match its installed digest',
                     'mismatch': 'do not select the same supported release'}.get(case)
            if client:
                thread, events = client.probe(root, case, thread)
                contexts, replies = extract_codex(events)
            else:
                thread, contexts, replies = claude_probe(manifest, root, out, case, hook_only=True)
            result = assess(root, contexts, replies, error, hook_only=args.host == 'claude')
            report['cases'].append({'case': case, 'repository': str(root), 'session': thread, **result})
            save(out/'observation.json', report)
            print(case + ': ' + ('pass' if result['passed'] else 'FAIL'), flush=True)
            if not result['passed']: break
        report['unchanged'] = all(snapshot(root) == before[name] for name, root in roots.items())
        report['status'] = 'passed' if len(report['cases']) == 6 and all(c['passed'] for c in report['cases']) and report['unchanged'] else 'incomplete'
    except Exception as exc:
        report['status'] = 'incomplete'; report['error'] = str(exc)
        print('STOP: '+str(exc), flush=True)
    finally:
        if client: client.close()
        save(out/'observation.json', report)
    print(json.dumps({'status': report['status'], 'report': str(out/'observation.json')}), flush=True)
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
