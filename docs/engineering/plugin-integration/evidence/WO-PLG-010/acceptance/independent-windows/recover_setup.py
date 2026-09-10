"""Execute the setup reference's exact Windows snippet in disposable data."""
import hashlib
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess

root = Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--repo-name',default='behavior-repository')
parser.add_argument('--label',default='chg10-setup')
parser.add_argument('--reuse',action='store_true')
opts=parser.parse_args()
source = root.parents[1]/'se-harness-plugin-change-skill'
reference = source/'plugins/verity-plane/common/skills/setup/references/environment.md'
blocks = dict(re.findall(r'<!-- snippet:([a-z]+) -->\n```[^\n]+\n(.*?)\n```', reference.read_text(), re.S))
data = root/'plugin-data'
data.mkdir(exist_ok=opts.reuse)
values = dict(SetupPython=str(root.parents[1]/'se-harness-plugin-eval-016/Scripts/python.exe'),
              Repo=str(root/opts.repo_name), Data=str(data), EnvDir=str(data/'evaluator-016'),
              Wheel=str(root.parents[1]/'plugin-evaluator-wheels/se_harness-0.16.0-py3-none-any.whl'),
              Version='0.16.0', Payload='51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c',
              Archive='a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae',
              IdentityFile=str(data/(opts.label+'-identity.json')), PrerequisiteCheck=blocks['prerequisites'],
              InputCheck=blocks['inputs'], EntryCheck=blocks['entry'], AcceptIdentity=blocks['accept'])
quote = lambda v: "'"+v.replace("'", "''")+"'"
script = root/'behavior-evidence'/(opts.label+'.ps1')
script.write_text('\n'.join('$'+k+'='+quote(v) for k,v in values.items())+'\n'+blocks['powershell']+'\n', encoding='utf8')
shell = shutil.which('pwsh') or shutil.which('powershell')
argv = [shell, '-NoProfile', '-NonInteractive', '-File', str(script)]
run = subprocess.run(argv, cwd=root, capture_output=True, timeout=60)
record = {'argv': argv, 'exit_code': run.returncode, 'stdout': run.stdout.decode('utf8','replace'),
          'stderr': run.stderr.decode('utf8','replace'), 'reference_sha256': hashlib.sha256(reference.read_bytes()).hexdigest(),
          'method': 'Exact Windows setup command block; offline disposable installation; no native host activation.'}
(root/'behavior-evidence'/(opts.label+'.json')).write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record, indent=2))
