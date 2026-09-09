"""Bounded Windows Claude activation observations; no installed-profile mutation.

The live host runner deliberately does not log in, copy credentials, approve
tools, install Python, or implement a production governance handler.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ARCHIVE = 'a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae'
PAYLOAD = '51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c'
DOCS = ['https://code.claude.com/docs/en/cli-reference',
        'https://code.claude.com/docs/en/plugins-reference',
        'https://code.claude.com/docs/en/hooks',
        'https://code.claude.com/docs/en/settings',
        'https://code.claude.com/docs/en/authentication#credential-management']


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


REDACTED = '[REDACTED]'
SECRET_KEY = re.compile(r'(?i)^[a-z0-9_-]*(?:token|password|secret|api[_-]?key|authorization|cookie|set-cookie)$')
SECRET_ASSIGNMENT = re.compile(
    r'''(?ix)(?<![a-z0-9])[a-z0-9_-]*
    (?:token|password|secret|api[_-]?key|authorization|cookie)
    ["'\\]*\s*[:=]\s*\S''')
PRIVATE_KEY = re.compile(r'-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----', re.S)


def sanitize_value(value):
    """Remove credential fields without altering recorded verdicts or digests."""
    if isinstance(value, dict):
        return {key: REDACTED if SECRET_KEY.fullmatch(key) else sanitize_value(item)
                for key, item in value.items()}
    if isinstance(value, list):
        result = []
        redact_next = False
        for item in value:
            result.append(REDACTED if redact_next else sanitize_value(item))
            redact_next = isinstance(item, str) and item.startswith('--') and bool(SECRET_KEY.fullmatch(item[2:]))
        return result
    if isinstance(value, str):
        return sanitize_text(value)
    return value


def sanitize_text(text):
    """Sanitize JSON/JSONL and diagnostic text; never return an IPC auth example.

    Non-JSON lines containing credentials are removed whole, since quoting in
    shell/JavaScript examples is not a reliable boundary for replacing a value.
    This deliberately sacrifices that line's detail instead of retaining a
    partially masked credential. Raw captures stay only in the local sandbox.
    """
    text = PRIVATE_KEY.sub('[REDACTED: private key]', text)
    try:
        document = json.loads(text)
    except (ValueError, TypeError):
        document = None
    if isinstance(document, (dict, list)):
        cleaned = sanitize_value(document)
        return text if cleaned == document else json.dumps(cleaned, ensure_ascii=False) + ('\n' if text.endswith('\n') else '')
    result = []
    for line in text.splitlines(keepends=True):
        ending = '\r\n' if line.endswith('\r\n') else '\n' if line.endswith('\n') else ''
        try:
            parsed = json.loads(line)
        except (ValueError, TypeError):
            parsed = None
        if isinstance(parsed, (dict, list)):
            cleaned = sanitize_value(parsed)
            result.append(line if cleaned == parsed else json.dumps(cleaned, ensure_ascii=False) + ending)
            continue
        normalized = line.replace('\\"', '"').replace("\\'", "'")
        if '[uds-messaging]' in line and ('Inject messages' in line or 'auth' in line.lower()):
            result.append('[REDACTED: IPC authentication example]' + ending)
        elif SECRET_ASSIGNMENT.search(normalized) or re.search(r'(?i)\bBearer\s+\S+|\bsk-ant-[a-z0-9_-]+', normalized):
            result.append('[REDACTED: sensitive output line]' + ending)
        else:
            result.append(line)
    return ''.join(result)


def publish_text(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(sanitize_text(text), encoding='utf-8')


def publish_json(path, value):
    dump(path, sanitize_value(value))


def publish_capture(source, destination):
    publish_text(destination, source.read_text(encoding='utf-8-sig', errors='replace'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def contained(child, parent):
    try:
        Path(child).resolve().relative_to(Path(parent).resolve())
        return True
    except ValueError:
        return False


def metadata(paths):
    """Inventory names/stat only, including credential files; never their bytes."""
    result = {}
    for path in paths:
        path = Path(path)
        try:
            stat = path.stat()
            result[str(path)] = {'exists': True, 'size': stat.st_size,
                                 'mtime_ns': stat.st_mtime_ns}
        except FileNotFoundError:
            result[str(path)] = {'exists': False}
        except PermissionError:
            result[str(path)] = {'inventory': 'unavailable: access denied'}
    return result


def child_environment(profile):
    # Do not inherit token/provider/helper configuration or user Python settings.
    keep = ['SystemRoot', 'WINDIR', 'SystemDrive', 'ComSpec', 'PATHEXT',
            'TEMP', 'TMP', 'USERPROFILE', 'HOMEDRIVE', 'HOMEPATH',
            'LOCALAPPDATA', 'APPDATA', 'PROGRAMDATA', 'PROGRAMFILES',
            'PROGRAMFILES(X86)', 'COMMONPROGRAMFILES', 'PROCESSOR_ARCHITECTURE']
    result = {key: os.environ[key] for key in keep if key in os.environ}
    result['PATH'] = os.pathsep.join([str(Path(os.environ['SystemRoot']) / 'System32'),
                                    r'C:\Program Files\Git\bin'])
    result.update(CLAUDE_CONFIG_DIR=str(profile),
                  CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1',
                  CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL='1')
    return result


def execute(argv, cwd, env, timeout=35):
    start = time.monotonic()
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding='utf-8', errors='replace')
    expired = False
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        expired = True
        # Kill only this probe process and its descendants, never a named app.
        subprocess.run(['taskkill.exe', '/PID', str(proc.pid), '/T', '/F'],
                       capture_output=True, timeout=10)
        out, err = proc.communicate(timeout=10)
    return {'argv': argv, 'cwd': str(cwd), 'exit': proc.returncode,
            'timeout': expired, 'seconds': round(time.monotonic() - start, 3),
            'stdout': out, 'stderr': err}


def events(path):
    return [json.loads(line) for line in path.read_text(encoding='utf-8-sig').splitlines()] if path.exists() else []


def classify_start(result, records, handler):
    """Independent evidence check: command success alone cannot prove delivery."""
    selected = [r for r in records if r.get('event') == 'SessionStart']
    if result['timeout'] or result['exit'] != 0 or not selected:
        return 'incompatible'
    if any(r.get('handler_invoked') != handler for r in selected):
        return 'fail'
    return 'observed'


def create_plugin(path, config, powershell, version='0.0.1'):
    dump(path / '.claude-plugin/plugin.json', {
        'name': 'verity-plane-probe', 'version': version,
        'author': {'name': 'SE Harness compatibility probe'},
        'description': 'Disposable observation fixture for WO-PLG-004'})
    skill = path / 'skills/setup/SKILL.md'
    skill.parent.mkdir(parents=True)
    skill.write_text('---\nname: setup\ndescription: Report the disposable probe prerequisites.\n---\n'
                     'This is an observation fixture. Report that setup needs supplied Python 3.11+, '
                     'venv and ensurepip. Do not install Python or claim governed readiness.\n', encoding='utf-8')
    entries = {}
    for event, mode in [('SessionStart', 'session'), ('PreToolUse', 'tool'), ('PostCompact', 'observe')]:
        entries[event] = [{'hooks': [{'type': 'command', 'command': powershell,
            'args': ['-NoProfile', '-NonInteractive', '-File', '${CLAUDE_PLUGIN_ROOT}/guard.ps1', mode],
            'timeout': 25}]}]
    dump(path / 'hooks/hooks.json', {'hooks': entries})
    dump(path / 'probe.json', config)
    for name in ['guard.ps1', 'handler.py']:
        shutil.copyfile(HERE / name, path / name)


def save_case(destination, records, expectation, observed, conclusion):
    destination.mkdir(parents=True, exist_ok=True)
    publish_json(destination / 'commands.json', records)
    publish_text(destination / 'actions.txt', '\n'.join(json.dumps(r['argv']) for r in records) + '\n')
    for stream in ['stdout', 'stderr']:
        publish_text(destination / f'{stream}.txt', '\n'.join(f'COMMAND {n + 1}\n{r[stream]}' for n, r in enumerate(records)))
    publish_json(destination / 'observations.json', {'expected': expectation, 'observed': observed,
        'conclusion': conclusion, 'production_support': 'unqualified',
        'exit_status': [r['exit'] for r in records],
        'host_identity_evidence': 'docs/engineering/plugin-integration/evidence/WO-PLG-004/identities.json',
        'capture_policy': 'sanitized-public-v1; credential fields and sensitive diagnostic lines redacted',
        'source_evidence': ['commands.json', 'stdout.txt', 'stderr.txt']})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['sandbox', 'evidence', 'claude', 'python', 'wheel']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    sandbox, evidence = args.sandbox.resolve(), args.evidence.resolve()
    if contained(sandbox, ROOT) or sandbox.exists():
        parser.error('sandbox must be a fresh directory outside the checkout')
    expected_evidence = ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-004'
    if evidence != expected_evidence.resolve():
        parser.error('evidence must be the declared WO-PLG-004 directory')
    if digest(args.wheel) != ARCHIVE:
        parser.error('wheel does not match the independently recorded released archive')
    sandbox.mkdir(parents=True)
    evidence.mkdir(parents=True, exist_ok=True)
    profile = sandbox / 'isolated profile'
    profile.mkdir()
    repo = sandbox / 'disposable repository'
    repo.mkdir()
    governance = repo / 'governance.txt'
    governance.write_text('PROBE GOVERNANCE CONTEXT version one; no authority granted.\n')
    target = repo / 'governed-target.txt'
    target.write_text('unchanged\n')
    env = child_environment(profile)
    powershell = str(Path(os.environ['SystemRoot']) / 'System32/WindowsPowerShell/v1.0/powershell.exe')
    normal = Path(os.environ['USERPROFILE'])
    watched = [normal / '.claude.json', normal / '.claude/settings.json',
               normal / '.claude/.credentials.json', normal / '.claude/plugins/installed_plugins.json',
               normal / '.claude/plugins/known_marketplaces.json', normal / '.config/git/ignore']
    before = metadata(watched)
    publish_json(evidence / 'normal-profile-before.json', before)
    settings = sandbox / 'settings.json'
    dump(settings, {'disableAllHooks': False})
    empty_mcp = sandbox / 'empty-mcp.json'
    dump(empty_mcp, {'mcpServers': {}})
    runtime = sandbox / 'selected evaluator'
    interpreter = runtime / 'Scripts/python.exe'
    config = {'interpreter': str(interpreter), 'event_log': str(sandbox / 'events.jsonl'),
              'governance': str(governance), 'archive': ARCHIVE, 'payload': PAYLOAD}
    plugin = sandbox / 'plugin with spaces'
    create_plugin(plugin, config, powershell)

    def base(path=plugin):
        return [str(args.claude), '--setting-sources', 'user', '--settings', str(settings),
                '--plugin-dir', str(path), '--strict-mcp-config', '--mcp-config', str(empty_mcp)]

    def run(argv, timeout=35):
        return execute(argv, repo, env, timeout)

    def startup(label, path=plugin):
        result = run(base(path) + ['--debug-file', str(sandbox / f'{label}.debug.txt'), '--init-only'])
        debug = sandbox / f'{label}.debug.txt'
        if debug.exists():
            publish_capture(debug, evidence / f'{label}.debug.txt')
        return result

    identities = [run([str(args.claude), '--version']),
                  run([str(args.python), '-I', '-c', 'import sys,platform,venv,ensurepip; print(sys.version); print(platform.platform()); print(sys.executable); print(ensurepip.version())'])]
    publish_json(evidence / 'identities.json', {'at': datetime.now(timezone.utc).isoformat(),
        'commands': identities, 'wheel': str(args.wheel), 'archive_sha256': ARCHIVE,
        'source_files': {p.name: digest(p) for p in HERE.iterdir() if p.is_file()},
        'documentation': DOCS, 'platforms': {'Windows': 'tested', 'Linux': 'unavailable', 'macOS': 'unavailable'},
        'isolated_profile': str(profile), 'environment_variable_names': sorted(env)})
    c01 = [run([str(args.claude), 'plugin', 'validate', str(plugin), '--json', '--strict']),
           run([str(args.claude), '--setting-sources', 'user', '--settings', str(settings), '--plugin-dir', str(plugin), 'plugin', 'list', '--json']),
           run([str(args.claude), '--setting-sources', 'user', '--settings', str(settings), '--plugin-dir', str(plugin), 'plugin', 'details', 'verity-plane-probe']), startup('C01-start')]
    first_events = events(Path(config['event_log']))
    save_case(evidence / 'C01', c01, 'Discover the setup skill and observe a shell guard before evaluator setup.',
              {'startup': classify_start(c01[-1], first_events, False), 'events': first_events,
               'resume_compact': 'unavailable: no authenticated persisted conversation'}, 'unavailable')

    # A real absent provided interpreter is observed; old/no-venv profiles are
    # deliberately not simulated as live Python installations.
    missing = execute([powershell, '-NoProfile', '-NonInteractive', '-Command',
        "if (Test-Path -LiteralPath $env:PROBE_PYTHON) { exit 9 }; Write-Output 'Provided Python unavailable; install Python 3.11+ with venv/ensurepip. No setup performed.'"],
        repo, dict(env, PROBE_PYTHON=str(sandbox / 'missing/python.exe')))
    save_case(evidence / 'C02', [missing], 'Missing, old and unusable provided Python produce guidance without installation.',
        {'missing_python': 'observed by host-shell prerequisite check; not a Claude tool invocation',
         'old_python': 'unavailable: no such interpreter supplied', 'missing_venv_ensurepip': 'unavailable: no such interpreter supplied',
         'target_unchanged': digest(target)}, 'unavailable')

    # Preparation is executed by this observer, not mislabelled as Claude setup.
    prepared = [run([str(args.python), '-I', '-m', 'venv', str(runtime)], 55)]
    if prepared[0]['exit'] == 0:
        prepared.append(run([str(interpreter), '-I', '-m', 'pip', 'install', '--no-index', '--no-deps', str(args.wheel)], 55))
    c03 = prepared + [startup('C03-first'), startup('C03-second')]
    save_case(evidence / 'C03', c03, 'Two fresh startups invoke the selected evaluator and capture context bytes.',
        {'events': events(Path(config['event_log'])), 'preparation_actor': 'probe observer, not Claude tool',
         'context_in_model': 'unavailable without authenticated conversation'}, 'unavailable')

    prior = digest(governance)
    governance.write_text('PROBE GOVERNANCE CONTEXT version two; no authority granted.\n')
    # A bounded real prompt records the authentication limitation. No tool can
    # execute, and no existing conversation or credential is copied.
    auth_attempt = run(base() + ['-p', 'Return only PROBE_OK. Do not use tools.', '--tools', '',
        '--permission-mode', 'manual', '--permission-prompts', 'none', '--max-turns', '1',
        '--max-budget-usd', '0.10', '--output-format', 'stream-json', '--verbose',
        '--include-hook-events', '--no-session-persistence'], 25)
    save_case(evidence / 'C04', [auth_attempt], 'Actual resume/compact delivers fresh governance after a change.',
        {'prior_sha256': prior, 'new_sha256': digest(governance),
         'resume': 'not executed: no authorized authenticated saved session',
         'compact': 'not executed: no authorized authenticated conversation',
         'attempt': 'bounded no-tools authentication availability trial, not resume/compact evidence'}, 'unavailable')

    count_before = len(events(Path(config['event_log'])))
    dump(settings, {'disableAllHooks': True})
    off = startup('C05-disabled')
    count_off = len(events(Path(config['event_log'])))
    dump(settings, {'disableAllHooks': False})
    on = startup('C05-enabled')
    save_case(evidence / 'C05', [off, on], 'Disabled hooks emit no fixture event; re-enabled hooks emit an event.',
        {'events_before': count_before, 'after_disabled': count_off,
         'after_enabled': len(events(Path(config['event_log']))),
         'interactive_trust': 'unavailable: print/init-only is not an interactive trust test'}, 'unavailable')

    plugin2 = sandbox / 'updated plugin with spaces'
    create_plugin(plugin2, config, powershell, '0.0.2')
    updated = startup('C06-updated', plugin2)
    if interpreter.exists():
        # Only the fresh, task-owned env executable is renamed; supplied Python
        # and the operator's evaluator remain untouched.
        if not contained(interpreter, sandbox):
            raise RuntimeError('interpreter escaped disposable root')
        interpreter.rename(interpreter.with_suffix('.removed'))
    removed = startup('C06-removed', plugin2)
    save_case(evidence / 'C06', [updated, removed], 'Spaced paths, version restart, stable plugin data and missing interpreter are observed.',
        {'events': events(Path(config['event_log'])),
         'reload': 'restart tested; interactive /reload-plugins unavailable',
         'normal_interpreter_removed': False}, 'unavailable')
    save_case(evidence / 'C07', [auth_attempt], 'Actual Claude shell tools perform authorized setup/repair and the unready governed-write trial.',
        {'setup': 'not executed by Claude', 'repair': 'not executed by Claude',
         'governed_write': 'not attempted; authentication unavailable', 'target_sha256': digest(target),
         'governance_readiness': False, 'external_observer_venv_is_not_C07': True}, 'unavailable')
    after = metadata(watched)
    publish_json(evidence / 'normal-profile-after.json', after)
    publish_json(evidence / 'isolation.json', {'metadata_only': True, 'readable_normal_profile_metadata_unchanged': before == after,
        'unavailable_inventory_paths': [path for path, value in before.items() if 'inventory' in value],
        'target_sha256': digest(target), 'sandbox': str(sandbox),
        'credential_files_opened_by_probe': False, 'credentials_copied': False,
        'public_capture_policy': 'sanitized-public-v1',
        'host_authentication_not_established': True})
    publish_capture(Path(config['event_log']), evidence / 'events.jsonl') if Path(config['event_log']).exists() else None
    print(json.dumps({'evidence': str(evidence), 'sandbox': str(sandbox),
                      'readable_normal_profile_metadata_unchanged': before == after, 'case_conclusions': 'unavailable; inspect partial live observations'}))


if __name__ == '__main__':
    main()
