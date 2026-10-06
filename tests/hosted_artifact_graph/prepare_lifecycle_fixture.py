"""Create a small immutable Git source fixture for the private lifecycle pilot."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tomllib
from pathlib import Path

from lifecycle_fixture import files


def prepare(python, output):
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    root = output / 'repository'
    commands = []
    env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'PYTHON'))}
    env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull)

    def run(argv, cwd=output):
        result = subprocess.run(list(map(str, argv)), cwd=cwd, env=env, capture_output=True, timeout=120)
        entry = {'argv': list(map(str, argv)), 'cwd': str(cwd), 'exit': result.returncode,
                 'stdout': result.stdout.decode('utf-8', 'replace'), 'stderr': result.stderr.decode('utf-8', 'replace')}
        commands.append(entry)
        (output / 'commands.json').write_text(json.dumps(commands, indent=2) + '\n', encoding='utf-8')
        if result.returncode:
            raise RuntimeError('Fixture command failed; inspect commands.json')
        return result.stdout

    run([python, '-I', '-m', 'se_harness', 'init', root, '--project-name', 'Disposable lifecycle rehearsal', '--integration', 'git', '--json'])
    (root / 'src').mkdir()
    (root / 'src/greeting.py').write_bytes(b"def greeting():\n    return 'Not implemented'\n")
    (root / 'REHEARSAL.txt').write_bytes(b'Synthetic test copy. No real human authority.\n')
    for name, raw in files().items():
        path = root / name.replace('-001', '-900')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw.replace(b'-001', b'-900'))
    run([python, '-I', '-m', 'se_harness', 'validate', root, '--json'])
    git = ['git', '-c', 'core.autocrlf=false', '-c', 'core.hooksPath=' + os.devnull,
           '-c', 'user.name=Rehearsal Test', '-c', 'user.email=rehearsal@example.invalid', '-c', 'commit.gpgsign=false']
    run([*git, 'init', '--quiet', '--template=', '-b', 'main'], root)
    run([*git, 'add', '--all'], root)
    run([*git, 'commit', '--quiet', '-m', 'Immutable synthetic source fixture'], root)
    commit = run([*git, 'rev-parse', 'HEAD'], root).decode().strip()
    manifest = {'schema': 'se-harness-source-manifest/v1', 'source': {
        'repository': 'https://example.invalid/private-rehearsal.git', 'object_format': 'sha1', 'commit': commit}, 'artifacts': []}
    for name in sorted(root.glob('docs/engineering/**/*.md')):
        raw = name.read_bytes()
        if not raw.startswith(b'+++'):
            continue
        record = tomllib.loads(raw.decode().split('+++', 2)[1])
        manifest['artifacts'].append({'path': name.relative_to(root).as_posix(), 'artifact_id': record['id'],
            'bytes': len(raw), 'raw_sha256': hashlib.sha256(raw).hexdigest(),
            'blob_oid': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()})
    path = output / 'manifest.json'
    path.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    stage = Path(__file__).resolve().parents[2] / 'server/scripts/stage.py'
    # parents[2] is the repository root.
    run([sys.executable, '-B', stage, root, path, output / 'staged'])
    print(json.dumps({'source_commit': commit, 'source': str(output / 'staged'), 'test_copy': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evaluator-python', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.evaluator_python.resolve(), args.output)
