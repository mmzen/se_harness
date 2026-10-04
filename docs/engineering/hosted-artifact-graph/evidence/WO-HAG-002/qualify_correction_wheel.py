"""EV-08: only invoke the installed wheel, isolated and outside source."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import time

p = argparse.ArgumentParser()
p.add_argument('--python', type=Path, required=True)
p.add_argument('--wheel', type=Path, required=True)
p.add_argument('--commit', required=True)
a = p.parse_args()
base = Path(__file__).resolve().parent
root = base / 'correction-wheel-projection'
assert not root.exists()
records = []

def run(label, args, expected=0, module=True):
    argv = [str(a.python), '-I', '-B', *(['-m', 'se_harness'] if module else []), *args]
    start = time.monotonic()
    r = subprocess.run(argv, cwd=base, capture_output=True, text=True, encoding='utf-8')
    record = {'case': label, 'argv': argv, 'cwd': str(base), 'exit_code': r.returncode,
              'stdout': r.stdout, 'stderr': r.stderr, 'seconds': time.monotonic()-start, 'expected_exit_code': expected}
    records.append(record)
    (base / 'correction-installed-cases.json').write_text(json.dumps(records, indent=2), encoding='utf-8')
    assert r.returncode == expected, record
    return json.loads(r.stdout)

identity = run('installed-payload', ['-c', 'import json,platform,sys; from se_harness.evaluator_identity import installed_evaluator_identity; import se_harness; print(json.dumps({"identity":installed_evaluator_identity().to_lock(),"python":sys.version,"platform":platform.platform(),"module":se_harness.__file__,"isolated":sys.flags.isolated}))'], module=False)
assert identity['isolated'] == 1
assert Path(identity['module']).resolve().is_relative_to(a.python.resolve().parent.parent)
assert identity['identity']['archive_sha256'] == hashlib.sha256(a.wheel.read_bytes()).hexdigest()
run('candidate-package-identity', ['identity', '--role', 'candidate-package', '--expected-version', '0.22.1',
    '--expected-root', str(a.python.resolve().parent.parent), '--checkout-root', str(base.parent / 'se_harness'),
    '--candidate-commit', a.commit, '--require-isolated-python', '--json'])
run('initialize-disposable-projection', ['init', str(root), '--project-name', 'draft-qualification', '--json'])
run('generate-requirement', ['create-artifact', str(root), '--domain', 'demo', '--type', 'requirement', '--id', 'REQ-DEMO-001', '--json'])
selected = root / 'docs/engineering/demo/requirements/REQ-DEMO-001.md'
original = selected.read_bytes()

def snapshot():
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}

def check(label, expected):
    before = snapshot()
    result = run(label, ['validate-draft', str(root), '--artifact', 'REQ-DEMO-001', '--json'], expected)
    assert before == snapshot(), 'query wrote files'
    assert result['schema'] == 'se-harness-draft-validation-v1'
    assert result['admissible'] == (expected == 0)
    return result

assert check('canonical-template', 0)['incomplete']
for prefix, kind in [('CAP', 'capability'), ('RLS', 'release_record')]:
    path = root / ('docs/engineering/demo/' + prefix + '-FIXTURE-001.md')
    path.write_text('+++\nid = "' + prefix + '-FIXTURE-001"\ntype = "' + kind +
        '"\ntitle = "Synthetic endpoint"\nstatus = "draft"\nowners = ["fixture"]\ncreated = "2026-10-04"\nupdated = "2026-10-04"\n[relations]\n+++\n\nSynthetic qualification input.\n', encoding='utf-8')
selected.write_bytes(original.replace(b'CAP-xxx', b'CAP-FIXTURE-001'))
check('correct-capability-endpoint', 0)
selected.write_bytes(original.replace(b'CAP-xxx', b'RLS-FIXTURE-001'))
wrong = check('wrong-release-endpoint', 1)
assert any(e.get('target') == 'RLS-FIXTURE-001' and e['code'] == 'E011' for e in wrong['errors'])
normal = run('normal-validator-wrong-endpoint', ['validate', str(root), '--json'], 1)
assert any(e['code'] == 'E011' and e['path'].endswith('REQ-DEMO-001.md') for e in normal['errors'])
selected.write_bytes(original.replace(b'["CAP-xxx"]', b'["CAP-xxx", "RLS-FIXTURE-001"]'))
assert check('mixed-placeholder-and-wrong-endpoint', 1)['incomplete']
selected.write_bytes(original.replace(b'[relations]', b'lifecycle_events = []\n[relations]'))
check('lifecycle-history-refusal', 1)
selected.write_bytes(b'+++\nid = [\n+++\n')
check('malformed-toml-refusal', 1)
summary = {'candidate_commit': a.commit, 'wheel': a.wheel.name,
           'wheel_sha256': hashlib.sha256(a.wheel.read_bytes()).hexdigest(),
           'observed_identity': identity, 'cases': len(records), 'passed': True,
           'authority': 'candidate qualification only; no release or governor adoption'}
(base / 'correction-installed-summary.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
print(json.dumps(summary))
