"""Observe the selected evaluator and context; never calculate authority."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

config = json.loads((Path(os.environ['CLAUDE_PLUGIN_ROOT']) / 'probe.json').read_text())
engine = Path(sys.prefix)
argv = [sys.executable, '-I', '-m', 'se_harness', 'identity',
        '--role', 'released-evaluator', '--expected-version', '0.16.0',
        '--expected-root', str(engine), '--checkout-root', str(Path(config['governance']).parent),
        '--require-isolated-python',
        '--entry-point', str(Path(sys.prefix) / 'Scripts' / 'harnessctl.exe'),
        '--require-entry-point', '--evaluator-payload-sha256', config['payload'],
        '--evaluator-wheel-sha256', config['archive'], '--json']
result = subprocess.run(argv, capture_output=True, text=True, timeout=15)
source = Path(config['governance']).read_bytes()
print(json.dumps({'probe_only': True, 'governance_readiness': False,
                  'argv': argv, 'identity_exit': result.returncode,
                  'identity': json.loads(result.stdout),
                  'source_sha256': hashlib.sha256(source).hexdigest(),
                  'context': source.decode('utf-8')}))
