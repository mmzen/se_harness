"""Observe released evaluator readiness and deliver its exact fixture manifest."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


root = Path(os.environ['CLAUDE_PLUGIN_ROOT'])
config = json.loads((root / 'probe.json').read_text())
repo = Path(config['governance']).parent.resolve()


def run(arguments):
    argv = [sys.executable, '-I', '-m', 'se_harness', *arguments]
    result = subprocess.run(argv, cwd=repo.parent, capture_output=True, text=True, encoding='utf-8', timeout=20)
    try:
        output = json.loads(result.stdout)
    except ValueError:
        output = None
    return {'argv': argv, 'exit': result.returncode, 'stdout': result.stdout,
            'stderr': result.stderr, 'result': output}


identity_call = subprocess.run([sys.executable, '-I', str(root / 'identity_observer.py')],
                               capture_output=True, text=True, encoding='utf-8', timeout=20)
observation = json.loads(identity_call.stdout)
observation['probe_only'] = True
observation['governance_readiness'] = False
observation['readiness_source'] = 'Released harnessctl preflight of explicitly synthetic test inputs; no lifecycle decision.'
observation['context'] = 'The disposable fixture has not established evaluator readiness. No authority is granted.'
if observation.get('identity_exit') == 0 and observation.get('identity', {}).get('passed') is True:
    checks = {'doctor': run(['doctor', str(repo), '--json']),
              'preflight': run(['preflight', str(repo), '--work-order', config['work_order'], '--phase', 'start', '--json']),
              'check': run(['check', str(repo), '--artifact', config['work_order'], '--json'])}
    observation['released_checks'] = checks
    if all(c['exit'] == 0 for c in checks.values()):
        check = checks['check']['result']
        manifest = check['context']['reading_manifest']
        files, parts = [], []
        for relative in manifest:
            path = (repo / relative).resolve()
            path.relative_to(repo)
            source = path.read_bytes()
            files.append({'path': relative, 'sha256': hashlib.sha256(source).hexdigest(), 'bytes': len(source)})
            parts.append('FILE: ' + relative + '\n' + source.decode('utf-8'))
        payload = '\n\n'.join(parts)
        observation['manifest_files'] = files
        observation['manifest_payload_sha256'] = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        observation['governance_readiness'] = checks['preflight']['result'].get('ready') is True
        observation['context'] = ('Disposable test inputs only. The evaluator reports preflight ready=' +
                                  str(observation['governance_readiness']).lower() +
                                  '. No real lifecycle transition or operator approval is recorded by this probe.\n\n' + payload)
print(json.dumps(observation))
