"""Walk the documented connection/repair/upgrade route with real local wheels.

This writes only a new disposable output directory. It installs no host plugin
and performs no model call. Use a non-promotable candidate wheel for development.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from repository_tools.plugin_distribution import develop


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--wheel', required=True, type=Path)
    parser.add_argument('--released-wheel', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    wheel = args.wheel.resolve(strict=True)
    released = args.released_wheel.resolve(strict=True)
    develop(ROOT, wheel, output/'plugins')
    plugin = output/'plugins/codex/verity-plane'
    project = output/'project'; project.mkdir()
    owner_file = project/'owner notes.txt'
    owner_file.write_text('Keep this project content.\n', encoding='utf-8')
    data = output/'private'
    python = data/'verity-plane/evaluator'/('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    results = []

    def run(name, argv, expected=0):
        result = subprocess.run([str(a) for a in argv], cwd=output, capture_output=True, text=True, encoding='utf-8', errors='replace')
        results.append({'name':name, 'argv':[str(a) for a in argv], 'exit_code':result.returncode, 'expected':'nonzero' if expected is None else expected})
        (output/'results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
        (output/(name+'.stdout.log')).write_text(result.stdout,encoding='utf-8')
        (output/(name+'.stderr.log')).write_text(result.stderr,encoding='utf-8')
        assert result.returncode != 0 if expected is None else result.returncode == expected, result.stdout+result.stderr
        return result

    def checker(name, *argv, expected=0):
        return run(name,[python,'-I','-m','se_harness',*argv],expected)

    def setup(name, selected, expected=0):
        return run(name,[sys.executable,'-I',plugin/'scripts/setup.py','--target',project,'--data-root',data,'--wheel',selected],expected)

    # A new code project: setup prepares Python but cannot yet report a healthy harness.
    setup('new-project-setup',wheel,expected=None)
    assert python.is_file()
    assert not (project/'.engineering-harness.toml').exists()
    checker('init-preview','init',project,'--project-name','Plugin acceptance','--dry-run','--json')
    assert not (project/'.engineering-harness.toml').exists()
    checker('init','init',project,'--project-name','Plugin acceptance','--json')
    (project/'.agents/skills/harness-orient/SKILL.md').write_text('Disposable local edit.\n',encoding='utf-8')
    checker('switch-preview','skill-ownership',project,'--provider','plugin','--plugin-root',plugin,'--json')
    assert (project/'.agents/skills/harness-orient/SKILL.md').exists()
    checker('switch','skill-ownership',project,'--provider','plugin','--plugin-root',plugin,'--apply','--json')
    checker('connected-doctor','doctor',project,'--json')
    lock = json.loads((project/'.engineering-harness.lock').read_text(encoding='utf-8'))
    assert lock['skill_ownership'] == {'provider':'plugin'}
    assert not (project/'.agents/skills/harness-orient').exists()
    config_before=(project/'.engineering-harness.toml').read_bytes()
    lock_before=(project/'.engineering-harness.lock').read_bytes()
    setup('reuse',wheel)
    package = next(python.parent.parent.glob('Lib/site-packages/se_harness/__init__.py'),None)
    if package is None: package=next(python.parent.parent.glob('lib/python*/site-packages/se_harness/__init__.py'))
    package.unlink()  # Real interrupted installation; the documented rerun repairs it.
    setup('repair',wheel)
    assert package.is_file()
    assert (project/'.engineering-harness.toml').read_bytes()==config_before
    assert (project/'.engineering-harness.lock').read_bytes()==lock_before
    assert owner_file.read_text(encoding='utf-8')=='Keep this project content.\n'

    # Existing released project: install its matching wheel, then explicitly upgrade.
    existing=output/'existing-project'; existing.mkdir()
    project=existing
    setup('released-setup',released,expected=None)
    checker('released-init','init',project,'--project-name','Existing project','--json')
    checker('released-doctor','doctor',project,'--json')
    config_before=(project/'.engineering-harness.toml').read_bytes()
    setup('upgrade-checker',wheel,expected=None)
    assert (project/'.engineering-harness.toml').read_bytes()==config_before
    checker('upgrade-preview','upgrade',project,'--json')
    assert (project/'.engineering-harness.toml').read_bytes()==config_before
    checker('upgrade','upgrade',project,'--apply','--json')
    checker('existing-switch','skill-ownership',project,'--provider','plugin','--plugin-root',plugin,'--apply','--json')
    checker('upgraded-doctor','doctor',project,'--json')
    assert (project/'.engineering-harness.toml').read_bytes()!=config_before
    summary={'outcome':'passed','wheel':str(wheel),'wheel_sha256':hashlib.sha256(wheel.read_bytes()).hexdigest(),'released_wheel':str(released),'checks':len(results),'project':str(project),'python':str(python),'plugin':str(plugin),'claims':'Disposable connection/repair/upgrade commands; no native host or published plugin acceptance.'}
    (output/'summary.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,indent=2))


if __name__ == '__main__':
    main()
