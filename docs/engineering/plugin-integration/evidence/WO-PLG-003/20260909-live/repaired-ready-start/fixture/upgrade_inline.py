"""Update only the declared disposable marketplace, using the real plugin CLI.

Keep the original fixture and command results; never edit installed hook trust.
"""
import argparse
import json
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import INLINE_GUARD, digest, isolated_environment, retain, run, write
from sanitize_output import sanitize_value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--codex', type=Path, required=True)
    parser.add_argument('--from-version', default='0.0.1')
    parser.add_argument('--to-version', default='0.0.2')
    parser.add_argument('--diagnostic', action='store_true', help='Echo only the documented plugin root/data locations')
    parser.add_argument('--native-inline', action='store_true', help='Use the inline native guard without a nested PowerShell process')
    parser.add_argument('--readiness', action='store_true', help='Use real released readiness observations and an exact test-only sentinel refusal')
    parser.add_argument('--evidence-name', default='inline-upgrade')
    args = parser.parse_args()
    checkout = Path(__file__).resolve().parents[3]
    sandbox = args.sandbox.resolve()
    allowed = checkout.parent / 'plugin-probe-sandboxes/codex'
    if allowed not in sandbox.parents:
        parser.error('Use an existing task-owned Codex probe sandbox.')
    plugin = sandbox / 'marketplace with spaces/plugins/codex-probe'
    manifest = plugin / '.codex-plugin/plugin.json'
    metadata = json.loads(manifest.read_text())
    if metadata.get('name') != 'codex-probe' or metadata.get('version') != args.from_version:
        parser.error('The fixture version must match --from-version before this recorded update.')
    if Path(args.evidence_name).name != args.evidence_name:
        parser.error('Evidence name must be one directory name.')
    destination = checkout / 'docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live' / args.evidence_name / 'change'
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(plugin, destination / 'before')
    shutil.copy2(__file__, destination / 'upgrade_inline-used.py')
    metadata['version'] = args.to_version
    write(manifest, json.dumps(metadata, indent=2) + '\n')
    command = 'powershell.exe -NoProfile -NonInteractive -Command "' + INLINE_GUARD + '"'
    if args.diagnostic:
        command = 'cmd.exe /d /c "echo CODEX_PROBE_DIAGNOSTIC_003 & echo PROBE_ROOT=%PLUGIN_ROOT% & echo PROBE_DATA=%PLUGIN_DATA%"'
    if args.native_inline:
        command = INLINE_GUARD
    if args.readiness:
        command = INLINE_GUARD.replace('observe_runtime.py', 'observe_ready_runtime.py')
        command = command.replace('do not perform governed writes.',
            'ordinary governed writes remain prohibited. The exact CODEX_PROBE_DENY_SENTINEL negative-test command may be attempted once only to observe its hook refusal; never retry or bypass that refusal. Authorized setup commands remain permitted.')
        sentinel = ("if($event.hook_event_name -eq 'PreToolUse' -and "
            "(($event.tool_input|ConvertTo-Json -Depth 20 -Compress) -like '*CODEX_PROBE_DENY_SENTINEL*')){"
            "[Console]::Error.WriteLine('CODEX_PROBE_DENY_SENTINEL: exact test-only write refused; not a production policy decision'); exit 2}; ")
        command = command.replace("$pointer=Join-Path", sentinel + "$pointer=Join-Path")
    hooks = {'SessionStart': [{'matcher': 'startup|resume|clear|compact',
                              'hooks': [{'type': 'command', 'command': command, 'timeout': 10}]}],
             'PreToolUse': [{'hooks': [{'type': 'command', 'command': command, 'timeout': 10}]}]}
    write(plugin / 'hooks/hooks.json', json.dumps({'hooks': hooks}, indent=2) + '\n')
    shutil.copy2(Path(__file__).with_name('observe_runtime.py'), plugin / 'observe_runtime.py')
    if args.readiness:
        shutil.copy2(Path(__file__).with_name('observe_ready_runtime.py'), plugin / 'observe_ready_runtime.py')
        write(plugin / 'skills/setup/SKILL.md',
            '---\nname: setup\ndescription: Disposable Codex probe setup marker; no production authority.\n---\n\n'
            'Report CODEX_PROBE_SKILL_003. Do not install Python. If supplied Python is missing, older than 3.11, '
            'or lacks venv/ensurepip, report that prerequisite and stop setup. No readiness may be claimed before '
            'fresh released evaluator checks. Ordinary governed writes remain prohibited while unready. '
            'The exact CODEX_PROBE_DENY_SENTINEL negative test may be attempted once only to observe hook refusal; '
            'never retry or bypass it. Authorized disposable environment setup and repair remain permitted.\n')
    shutil.copytree(plugin, destination / 'after')
    write(destination / 'source-digests.json', json.dumps({
        'before': {str(p.relative_to(destination / 'before')): digest(p)
                   for p in (destination / 'before').rglob('*') if p.is_file()},
        'after': {str(p.relative_to(plugin)): digest(p) for p in plugin.rglob('*') if p.is_file()},
        'actor': 'observer', 'changes': 'Disposable marketplace fixture only; hook trust unchanged by this script.'
    }, indent=2) + '\n')
    env = isolated_environment(sandbox / 'profile')
    for name, arguments in [('plugin-add', ['plugin', 'add', 'codex-probe@codex-probe-local', '--json']),
                            ('plugin-list', ['plugin', 'list', '--json'])]:
        result = run([str(args.codex), *arguments], sandbox / 'repo', env, timeout=30)
        retain(destination, name, sanitize_value(result))
        print(json.dumps({'step': name, 'exit_status': result['exit_status'], 'stdout': result['stdout']}))
        if result['exit_status'] != 0 or result['timed_out']:
            raise SystemExit('Plugin CLI step failed; retained evidence is incomplete.')


if __name__ == '__main__':
    main()
