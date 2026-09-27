from pathlib import Path
import importlib.util
import hashlib
import json
import subprocess
import sys
import tempfile
from unittest.mock import patch

repo = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent / 'se_harness'
spec = importlib.util.spec_from_file_location('review_source_test', repo / 'tests/test_progressive_instruction_discovery.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
source = module.SOURCE
raw = source.read_bytes()
blob = subprocess.check_output(['git', '-c', 'safe.directory=' + repo.as_posix(), '-C', str(repo), 'show', 'HEAD:' + source.relative_to(repo).as_posix()])
lf = raw.replace(b'\r\n', b'\n')
assert blob == lf, 'Content differs beyond CRLF checkout conversion'
cases = {'git-lf': blob, 'windows-crlf': lf.replace(b'\n', b'\r\n'), 'content-change': lf + b'Unauthorized extra instruction.\n', 'whitespace-change': lf + b' ', 'bare-cr-change': lf + b'\r'}
results = []
with tempfile.TemporaryDirectory(prefix='iar-ci-identity-') as temp:
    for name, data in cases.items():
        target = Path(temp) / (name + '.md')
        target.write_bytes(data)
        case = module.ProgressiveInstructionContentTests('test_review_source_is_the_accepted_input')
        with patch.object(module, 'SOURCE', target):
            try:
                case.test_review_source_is_the_accepted_input()
                accepted = True
            except AssertionError:
                accepted = False
        expected = name in ('git-lf', 'windows-crlf')
        results.append({'case': name, 'sha256': hashlib.sha256(data).hexdigest(), 'expected_acceptance': expected, 'accepted': accepted, 'matches_expected': accepted == expected})
print(json.dumps({'method': 'Invoke the actual source-identity test with temporary input files; no source file is rewritten.', 'platform': sys.platform, 'python': sys.version, 'cases': results}, indent=2))
sys.exit(0 if all(row['matches_expected'] for row in results) else 1)
