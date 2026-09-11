"""Disposable observations for WO-PLG-006. Never installed with the adapter."""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import threading

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ADAPTER = ROOT / 'plugins/verity-plane/claude-code'
COMMON = ROOT / 'plugins/verity-plane/common'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


binding = load('claude_binding', ADAPTER / 'scripts/binding.py')
probe = load('claude_probe_observation', HERE.parent / 'claude_probe/probe.py')
fault_observer = load('shared_fault_observer', HERE.parent / 'tool_action/run_acceptance.py')
PYTHON = ROOT.parent / 'se-harness-plugin-eval-016/Scripts/python.exe'
CLAUDE = Path.home() / '.local/bin/claude.exe'
PROFILE = ROOT.parent / 'plugin-probe-sandboxes/claude/run-20260908-02/isolated profile'


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def json_lines(raw):
    result = []
    for line in raw.splitlines():
        try:
            value = json.loads(line)
            if isinstance(value, dict):
                result.append(value)
        except ValueError:
            pass
    return result


def run(argv, cwd, env=None, raw=None, timeout=90):
    start = time.monotonic()
    process = subprocess.Popen([str(a) for a in argv], cwd=cwd, env=env,
                               stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               creationflags=subprocess.CREATE_NO_WINDOW)
    expired = False
    try:
        out, err = process.communicate(raw, timeout=timeout)
    except subprocess.TimeoutExpired:
        expired = True
        subprocess.run(['taskkill.exe', '/PID', str(process.pid), '/T', '/F'], capture_output=True)
        out, err = process.communicate(timeout=15)
    return {'argv': [str(a) for a in argv], 'cwd': str(cwd), 'exit': process.returncode,
            'timeout': expired, 'started_monotonic': start, 'finished_monotonic': time.monotonic(),
            'stdout': out.decode('utf8', 'replace'), 'stderr': err.decode('utf8', 'replace')}


def run_stream(argv, cwd, env, timeout=150):
    """Timestamp actual streamed host events outside the adapter process."""
    started = time.monotonic()
    proc = subprocess.Popen([str(a) for a in argv], cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    captured = {'stdout': [], 'stderr': []}
    timeline = []
    def receive(stream, name):
        for raw in iter(stream.readline, b''):
            stamp = time.monotonic()
            captured[name].append(raw)
            if name == 'stdout':
                try:
                    value = json.loads(raw)
                except ValueError:
                    continue
                item = {k: value[k] for k in ('type', 'subtype', 'hook_id', 'hook_name', 'hook_event', 'outcome', 'exit_code') if k in value}
                blocks = value.get('message', {}).get('content', [])
                item['tools'] = [{k:b[k] for k in ('type','id','name','tool_use_id','is_error') if k in b}
                                 for b in blocks if isinstance(b,dict) and b.get('type') in ('tool_use','tool_result')]
                if item.get('subtype','').startswith('hook_') or item['tools']:
                    item['received_monotonic'] = stamp
                    timeline.append(item)
    threads = [threading.Thread(target=receive, args=(getattr(proc,name),name),daemon=True) for name in captured]
    for thread in threads:
        thread.start()
    expired = False
    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        expired = True
        subprocess.run(['taskkill.exe','/PID',str(proc.pid),'/T','/F'],capture_output=True)
        proc.wait(timeout=15)
    for thread in threads:
        thread.join(15)
    return {'argv':[str(a) for a in argv],'cwd':str(cwd),'exit':proc.returncode,'timeout':expired,
            'started_monotonic':started,'finished_monotonic':time.monotonic(),'timeline':timeline,
            **{name:b''.join(raw).decode('utf8','replace') for name,raw in captured.items()}}


def create_fixture(space, *, initialize=True):
    space = Path(space).resolve()
    space.mkdir(parents=True, exist_ok=False)
    repo = space / 'disposable repository'
    setup = []
    if initialize:
        setup.append(run([PYTHON, '-I', '-B', '-m', 'se_harness', 'init', repo,
                          '--project-name', 'claude-adapter-fixture', '--json'], space))
        if setup[-1]['exit']:
            raise RuntimeError('released fixture initialization failed: ' + setup[-1]['stderr'])
        source = ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live/readiness-fixture-inputs/synthetic-inputs'
        for path in source.rglob('*.md.txt'):
            target = repo / path.relative_to(source).as_posix().removesuffix('.txt')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(path.read_bytes())
        wo = repo / 'docs/engineering/readiness-probe/work-orders/WO-PROBE-001.md'
        wo.write_text(wo.read_text().replace('status = "approved"', 'status = "in_progress"', 1), encoding='utf8')
        setup.append(run([PYTHON, '-I', '-B', '-m', 'se_harness', 'evidence', repo,
                          '--artifact', 'WO-PROBE-001', '--checkpoint', 'pre-action', '--json'], space))
    else:
        repo.mkdir()
    for name in ('governed-target.txt', 'outside-scope.txt'):
        (repo / name).write_text('initial fixture target\n', encoding='utf8')
    plugin = space / 'plugin with spaces'
    shutil.copytree(ADAPTER, plugin)
    shutil.copytree(COMMON / 'scripts', plugin / 'scripts', dirs_exist_ok=True)
    shutil.copytree(COMMON / 'skills', plugin / 'skills')
    config = {'schema': 'verity-plane-claude-binding-v1', **binding.PROFILE, **binding.BUDGET,
              'host_executable': str(CLAUDE), 'host_sha256': sha(CLAUDE),
              'repo': str(repo), 'environment': str(PYTHON.parent.parent), 'artifact': 'WO-PROBE-001',
              'context_limit': 32768, 'read_limit': 0}
    config_path = space / 'private binding.json'
    dump(config_path, config)
    env = probe.child_environment(PROFILE)
    env.update(VERITY_PLANE_CLAUDE_BINDING=str(config_path), CLAUDE_PLUGIN_ROOT=str(plugin))
    return {'space': space, 'repo': repo, 'plugin': plugin, 'config': config,
            'config_path': config_path, 'env': env, 'setup': setup}


def direct(fixture, event, *, kind=None, command=None):
    kind = kind or (event.get('hook_event_name', 'SessionStart') if isinstance(event, dict) else 'PreToolUse')
    hooks = json.loads((fixture['plugin'] / 'hooks/hooks.json').read_text())
    command = command or hooks['hooks'][kind][0]['hooks'][0]['command']
    raw = json.dumps(event, ensure_ascii=False).encode() if isinstance(event, dict) else event
    result = run([Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe',
                  '-NoProfile', '-NonInteractive', '-Command', command], fixture['space'], fixture['env'], raw)
    result['event_input'] = raw.decode('utf8', 'replace')
    return result


def event(fixture, kind='SessionStart', tool='Write', path='governed-target.txt'):
    value = {'hook_event_name': kind, 'cwd': str(fixture['repo'])}
    if kind == 'SessionStart':
        value['source'] = 'startup'
    else:
        value.update(tool_name=tool, tool_use_id='fixed-fixture-id',
                     tool_input={'file_path': str(fixture['repo'] / path), 'content': 'observed fixture effect\n'})
    return value


def response(result):
    try:
        return json.loads(result['stdout']).get('hookSpecificOutput', {})
    except ValueError:
        return {}


def denied(result):
    return response(result).get('permissionDecision') == 'deny'


def guard_record(result):
    return next((x for x in reversed(json_lines(result['stderr'])) if x.get('adapter')), {})
