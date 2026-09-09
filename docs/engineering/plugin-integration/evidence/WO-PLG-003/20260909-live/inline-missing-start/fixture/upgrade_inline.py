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
    args = parser.parse_args()
    checkout = Path(__file__).resolve().parents[3]
    sandbox = args.sandbox.resolve()
    allowed = checkout.parent / 'plugin-probe-sandboxes/codex'
    if allowed not in sandbox.parents:
        parser.error('Use an existing task-owned Codex probe sandbox.')
    plugin = sandbox / 'marketplace with spaces/plugins/codex-probe'
    manifest = plugin / '.codex-plugin/plugin.json'
    metadata = json.loads(manifest.read_text())
    if metadata.get('name') != 'codex-probe' or metadata.get('version') != '0.0.1':
        parser.error('This recorded update expects the original codex-probe 0.0.1 fixture.')
    destination = checkout / 'docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live/inline-upgrade/change'
    destination.mkdir(parents=True, exist_ok=False)
    shutil.copytree(plugin, destination / 'before')
    shutil.copy2(__file__, destination / 'upgrade_inline-used.py')
    metadata['version'] = '0.0.2'
    write(manifest, json.dumps(metadata, indent=2) + '\n')
    command = 'powershell.exe -NoProfile -NonInteractive -Command "' + INLINE_GUARD + '"'
    hooks = {'SessionStart': [{'matcher': 'startup|resume|clear|compact',
                              'hooks': [{'type': 'command', 'command': command, 'timeout': 10}]}],
             'PreToolUse': [{'hooks': [{'type': 'command', 'command': command, 'timeout': 10}]}]}
    write(plugin / 'hooks/hooks.json', json.dumps({'hooks': hooks}, indent=2) + '\n')
    shutil.copy2(Path(__file__).with_name('observe_runtime.py'), plugin / 'observe_runtime.py')
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
