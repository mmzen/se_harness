"""Capture the actual shared handler's output; this does not assert receipt."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import subprocess

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument('--repo-name', default='behavior2-repository')
parser.add_argument('--label', default='corrected-fixture-context')
opts = parser.parse_args()
repo = root/opts.repo_name
python = root/'plugin-data/evaluator-016/Scripts/python.exe'
handler = root.parents[1]/'se-harness-plugin-change-skill/plugins/verity-plane/common/scripts/session-context.py'
args = [str(python), '-I', '-B', str(handler), '--repo', str(repo), '--environment', str(python.parent.parent),
        '--version', '0.16.0', '--payload-sha256', '51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c',
        '--archive-sha256', 'a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae',
        '--host', 'codex', '--context-limit', '32768', '--read-limit', '32768']
event = {'hook_event_name': 'SessionStart', 'source': 'resume', 'cwd': str(repo)}
env = os.environ.copy()
env.pop('PYTHONPATH', None)
env['PATH'] = str(python.parent)+os.pathsep+env.get('PATH','')
snap = lambda: {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in repo.rglob('*') if p.is_file()}
before = snap()
result = subprocess.run(args, input=json.dumps(event).encode(), capture_output=True, cwd=root, env=env, timeout=60)
row = {'argv': args, 'event': event, 'exit_code': result.returncode,
       'stdout': result.stdout.decode('utf8'), 'stderr': result.stderr.decode('utf8'),
       'before': before, 'after': snap(), 'native_host_delivery': False}
(root/'behavior-evidence'/(opts.label+'.json')).write_text(json.dumps(row, indent=2)+'\n', encoding='utf8')
print(row['stdout'])
