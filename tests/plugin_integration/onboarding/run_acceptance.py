"""Exercise local host loading and documented checker commands in fresh profiles.

Requires installed Codex and Claude Code CLIs plus a local development wheel.
No credentials are copied and no model request is made. Native skill discovery
and direct command execution are recorded separately; this is not an agent run.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from repository_tools.plugin_distribution import develop


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    hosts = {name: shutil.which(name) for name in ('codex', 'claude')}
    assert all(hosts.values()), 'Install the Codex and Claude Code CLIs before this optional walkthrough.'
    wheel = args.wheel.resolve(strict=True)
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    market = output/'packages'
    develop(ROOT, wheel, market)
    catalog = market/'.agents/plugins/marketplace.json'
    catalog.parent.mkdir(parents=True)
    catalog.write_text(json.dumps({'name':'verity-local', 'plugins':[{
        'name':'verity-plane', 'source':{'source':'local', 'path':'./codex/verity-plane'},
        'policy':{'installation':'AVAILABLE', 'authentication':'ON_INSTALL'},
        'category':'Productivity'}]}, indent=2)+'\n', encoding='utf-8')
    results = []
    observations = []

    for host, executable in hosts.items():
        home = output/host/'profile'
        project = output/host/'project'
        project.mkdir(parents=True)
        env = {k:os.environ[k] for k in ('SYSTEMROOT', 'WINDIR', 'COMSPEC', 'PATHEXT',
               'NUMBER_OF_PROCESSORS', 'PROCESSOR_ARCHITECTURE') if k in os.environ}
        env.update(HOME=str(home), USERPROFILE=str(home), CODEX_HOME=str(home/'codex'),
                   CLAUDE_CONFIG_DIR=str(home/'claude'), APPDATA=str(home/'AppData/Roaming'),
                   LOCALAPPDATA=str(home/'AppData/Local'), TEMP=str(home/'tmp'), TMP=str(home/'tmp'),
                   PATH=os.pathsep.join([str(Path(sys.executable).parent),
                        os.path.join(os.environ.get('SYSTEMROOT', '/'), 'System32'),
                        r'C:\Program Files\Git\cmd']), NO_COLOR='1')
        for key in ('CODEX_HOME', 'CLAUDE_CONFIG_DIR', 'APPDATA', 'LOCALAPPDATA', 'TEMP'):
            Path(env[key]).mkdir(parents=True, exist_ok=True)
        (home/'codex/config.toml').write_text('cli_auth_credentials_store = "file"\ncheck_for_update_on_startup = false\n', encoding='utf-8')

        def run(name, argv, missing_harness=False):
            name = host+'-'+name
            result = subprocess.run([str(a) for a in argv], cwd=project, env=env,
                capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=90)
            results.append({'name':name, 'argv':[str(a) for a in argv],
                            'exit_code':result.returncode, 'expected':'missing harness' if missing_harness else 0})
            (output/'results.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
            (output/(name+'.stdout.log')).write_text(result.stdout, encoding='utf-8')
            (output/(name+'.stderr.log')).write_text(result.stderr, encoding='utf-8')
            print(name, result.returncode, flush=True)
            if missing_harness:
                assert result.returncode != 0 and not (project/'.engineering-harness.toml').exists(), result.stdout+result.stderr
            else:
                assert result.returncode == 0, result.stdout+result.stderr
            return result.stdout

        version = run('version', [executable, '--version']).strip()
        if host == 'codex':
            run('marketplace', [executable, 'plugin', 'marketplace', 'add', market, '--json'])
            installed = json.loads(run('install', [executable, 'plugin', 'add', 'verity-plane@verity-local', '--json']))
            plugin = Path(installed['installedPath'])
            discovery = run('discovery', [executable, 'debug', 'prompt-input', 'Use verity-plane:setup to connect this disposable project.'])
            assert 'verity-plane:setup' in discovery and '/setup/SKILL.md' in discovery.replace('\\', '/')
        else:
            plugin = market/'claude/verity-plane'
            discovery = run('discovery', [executable, '--plugin-dir', plugin, 'plugin', 'details', 'verity-plane'])
            assert 'setup' in discovery and 'harness-orient' in discovery
        data = home/'plugin-data'
        python = data/'verity-plane/evaluator'/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        run('setup', [sys.executable, '-I', plugin/'scripts/setup.py', '--target', project,
                     '--data-root', data, '--wheel', plugin/'packages'/wheel.name], missing_harness=True)
        assert python.is_file()
        checker = [python, '-I', '-m', 'se_harness']
        checker_version = run('checker-version', [*checker, '--version']).strip()
        run('init-preview', [*checker, 'init', project, '--project-name', 'Plugin walkthrough', '--dry-run', '--json'])
        assert not (project/'.engineering-harness.toml').exists()
        run('init', [*checker, 'init', project, '--project-name', 'Plugin walkthrough', '--json'])
        run('provider-preview', [*checker, 'skill-ownership', project, '--provider', 'plugin', '--plugin-root', plugin, '--json'])
        run('provider', [*checker, 'skill-ownership', project, '--provider', 'plugin', '--plugin-root', plugin, '--apply', '--json'])
        run('doctor', [*checker, 'doctor', project, '--json'])
        lock = json.loads((project/'.engineering-harness.lock').read_text(encoding='utf-8'))
        assert lock['skill_ownership'] == {'provider':'plugin'}
        observations.append({'host':host, 'version':version, 'checker':checker_version, 'plugin':str(plugin),
            'project':str(project), 'load_route':'local marketplace installation' if host == 'codex' else 'session --plugin-dir',
            'outcome':'native discovery and direct setup/connection/doctor passed'})

    summary = {'outcome':'passed', 'platform':sys.platform, 'python':sys.version.split()[0],
        'wheel':str(wheel), 'wheel_sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),
        'hosts':observations, 'commands':len(results),
        'limits':'Development packages in fresh profiles; no model-driven session, public installation or other-platform claim.'}
    (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
