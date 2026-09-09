"""Prepare or change only the disposable live fixture; no host event is simulated.

Direct observer setup supports C03/C04/C06. It does not satisfy C07's real-tool
setup requirement. No credentials, trust records, or normal profiles are read.
"""
import argparse
import json
import os
import re
from pathlib import Path
import shutil
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from probe import digest, isolated_environment, retain, run, write
from sanitize_output import sanitize_value

RELEASED_WHEEL_SHA256 = 'a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sandbox', type=Path, required=True)
    parser.add_argument('--action', choices=['prepare', 'change-source', 'remove', 'restore', 'add-readiness-inputs', 'select-tool-runtime'], required=True)
    parser.add_argument('--evidence-name', required=True)
    parser.add_argument('--wheel', type=Path)
    parser.add_argument('--tool-environment', action='store_true', help='Select only the disposable environment created by actual model shell tools')
    parser.add_argument('--tool-environment-name', default='tool-environment')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', args.tool_environment_name):
        parser.error('Use one plain disposable environment directory name.')
    if args.action == 'prepare' and (not args.wheel or not args.wheel.is_file()
                                    or digest(args.wheel) != RELEASED_WHEEL_SHA256):
        parser.error('Preparation requires the exact selected released 0.16.0 wheel bytes.')
    checkout = Path(__file__).resolve().parents[3]
    sandbox = args.sandbox.resolve()
    if checkout.parent / 'plugin-probe-sandboxes/codex' not in sandbox.parents:
        parser.error('Use only a task-owned Codex fixture sandbox.')
    if Path(args.evidence_name).name != args.evidence_name:
        parser.error('Evidence name must be a single directory name.')
    evidence = checkout / 'docs/engineering/plugin-integration/evidence/WO-PLG-003/20260909-live' / args.evidence_name
    evidence.mkdir(parents=True, exist_ok=False)
    shutil.copy2(__file__, evidence / 'live_fixture_state-used.py')
    repo = sandbox / 'repo'
    data = sandbox / 'profile/codex/plugins/data/codex-probe-codex-probe-local'
    runtime = data / (args.tool_environment_name if args.tool_environment else 'environment')
    python = runtime / 'Scripts/python.exe'
    removed = runtime / 'Scripts/python.removed-for-probe.exe'
    env = isolated_environment(sandbox / 'profile')
    env['PATH'] = str(runtime / 'Scripts') + os.pathsep + env['PATH']

    def snapshot(label):
        paths = ['AGENTS.md', 'ENGINEERING_HARNESS.md', 'governed-target.txt']
        records = {}
        for name in paths:
            source = repo / name
            if source.is_file():
                retained = evidence / label / (name + '.txt')
                retained.parent.mkdir(exist_ok=True)
                retained.write_bytes(source.read_bytes())
                records[name] = {'sha256': digest(source), 'retained': retained.relative_to(evidence).as_posix()}
        write(evidence / (label + '.json'), json.dumps({
            'sources': records, 'python_exists': python.is_file(),
            'removed_python_exists': removed.is_file(), 'data_directory': str(data),
            'scope': 'Selected synthetic repository and runtime files only; not an OS-wide profile audit.'
        }, indent=2) + '\n')

    snapshot('before')
    if args.action == 'prepare':
        if runtime.exists() or not args.wheel or not args.wheel.is_file():
            parser.error('Preparation requires a fresh runtime and an existing released wheel.')
        commands = [
            ('create-venv', [sys.executable, '-I', '-m', 'venv', str(runtime)]),
            ('install-wheel', [str(python), '-I', '-m', 'pip', 'install', '--no-index', '--no-deps', str(args.wheel.resolve())]),
            ('init-fixture', [str(python), '-I', '-m', 'se_harness', 'init', str(repo), '--project-name', 'Disposable Codex observation', '--json'])]
        for name, argv in commands:
            result = run(argv, sandbox, env, timeout=60)
            retain(evidence, name, sanitize_value(result))
            if result['exit_status'] != 0 or result['timed_out']:
                raise SystemExit('Preparation failed; retain the original observations.')
        write(data / 'runtime-path.txt', str(python))
        write(evidence / 'runtime-inputs.json', json.dumps({'provided_python': sys.executable,
            'provided_python_version': sys.version, 'wheel_sha256': digest(args.wheel),
            'wheel': str(args.wheel.resolve()), 'runtime': str(runtime),
            'layer': 'Direct observer preparation; not agent tool execution'}, indent=2) + '\n')
    elif args.action == 'change-source':
        path = repo / 'AGENTS.md'
        content = path.read_bytes()
        marker = b'\nCODEX_PUBLIC_REFRESH_003_B: disposable fixture source revision B.\n'
        if marker in content:
            parser.error('Source marker already exists; preserve prior evidence.')
        path.write_bytes(content + marker)
    elif args.action == 'remove':
        if not python.is_file() or removed.exists():
            parser.error('Expected original disposable interpreter only.')
        python.rename(removed)
    elif args.action == 'restore':
        if python.exists() or not removed.is_file():
            parser.error('Expected preserved removed interpreter only.')
        removed.rename(python)
    elif args.action == 'select-tool-runtime':
        if not args.tool_environment or runtime.exists():
            parser.error('Selecting a new tool runtime requires an absent disposable environment.')
        write(data / 'runtime-path.txt', str(python))
    else:
        public = checkout.parent / 'plugin-probe-sandboxes/readiness-input-20260909/public-inputs'
        mapping = json.loads((public / 'path-map.json').read_text())
        for item in mapping['files']:
            relative = Path(item['repository_path'])
            source = public / item['retained_path']
            target = repo / relative
            if not relative.as_posix().startswith('docs/engineering/readiness-probe/') or '..' in relative.parts:
                parser.error('Unexpected fixture destination.')
            if target.exists() or digest(source) != item['sha256']:
                parser.error('Expected new exact synthetic fixture inputs.')
        for item in mapping['files']:
            source = public / item['retained_path']
            target = repo / item['repository_path']
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(source.read_bytes())
        shutil.copytree(public, evidence / 'synthetic-inputs')
        write(evidence / 'fixture-boundary.txt', 'Six synthetic approved-status inputs only. No real-world approval, transition, or authority is represented.\n')
    snapshot('after')
    for name in ('inline-events.jsonl', 'runtime-observations.jsonl', 'runtime-readiness-observations.jsonl'):
        source = data / name
        if source.is_file():
            write(evidence / name, json.dumps(sanitize_value([
                json.loads(line) for line in source.read_text(encoding='utf-8-sig').splitlines() if line]), indent=2) + '\n')
    print(json.dumps({'action': args.action, 'evidence': str(evidence)}))


if __name__ == '__main__':
    main()
