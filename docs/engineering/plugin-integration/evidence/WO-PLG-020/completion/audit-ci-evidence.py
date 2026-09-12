"""Audit passing hosted observations and retain their exact downloaded bytes."""
from collections import Counter
import ast
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent.parent / 'wo20'
EVIDENCE = ROOT / 'docs/engineering/plugin-integration/evidence/WO-PLG-020'
DEST = EVIDENCE / 'completion'
COMMIT = '9acdd08e6507d4433bc27f3888d2743d1eea13da'
CI = OUT / 'ci-main-selected'
sha = lambda raw: hashlib.sha256(raw).hexdigest()

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

def read(path):
    return json.loads(path.read_bytes())

assert git('rev-parse', 'HEAD').decode().strip() == COMMIT
assert not git('status', '--porcelain=v1')
run = read(OUT / 'github-final/candidate-run.json')
assert run['headSha'] == COMMIT and run['status'] == 'completed' and run['conclusion'] == 'success'
assert all(job['conclusion'] == 'success' for job in run['jobs'])
assert read(OUT / 'github-final/attempt-1.json')['conclusion'] == 'cancelled'
assert read(OUT / 'preflight.json')['ready']
assert read(OUT / 'validation.json')['valid']
assert all(check['passed'] for check in read(OUT / 'doctor.json')['checks'])

package = read(CI / 'candidate-package-qualification-0.17.0/candidate-package-qualification.json')
complete = read(CI / 'complete-candidate-qualification/complete-candidate.json')
assert package['passed'] and complete['passed']
assert package['target']['commit'] == complete['target']['commit'] == COMMIT
wheel_dir = CI / ('candidate-wheel-non-promotable-' + COMMIT)
wheels = list(wheel_dir.glob('*.whl'))
assert len(wheels) == 1
wheel_sha = sha(wheels[0].read_bytes())
assert wheel_sha == package['target']['wheel_sha256']
for line in (wheel_dir / 'SHA256SUMS').read_text().splitlines():
    expected, filename = line.split(maxsplit=1)
    assert sha((wheel_dir / filename.lstrip('*')).read_bytes()) == expected
test_blob = git('show', COMMIT + ':tests/test_skill_ownership.py')
assert test_blob == (ROOT / 'tests/test_skill_ownership.py').read_bytes().replace(b'\r\n', b'\n')
test_sha = sha(test_blob)
test_crlf_sha = sha(test_blob.replace(b'\n', b'\r\n'))
module = ast.parse((ROOT / 'tests/test_skill_ownership.py').read_text())
methods = {item.name: {node.name for node in item.body if isinstance(node, ast.FunctionDef) and node.name.startswith('test_')}
    for item in module.body if isinstance(item, ast.ClassDef)}
smoke_names = next(ast.literal_eval(item.value) for item in module.body
    if isinstance(item, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'SMOKE_TESTS' for target in item.targets))
assert len(methods['SkillOwnershipAcceptanceTests']) == 42
assert len(methods['OwnershipReadBoundaryTests']) == 11
selections = []
case_index = []
for platform in ('Linux', 'Windows'):
    for python, selection, expected in (('3.11', 'smoke', 8), ('3.13', 'full', 53)):
        for mode in ('source', 'package'):
            directory = CI / ('skill-ownership-' + platform) / python / mode
            runtime = read(directory / 'runtime.json')
            assert runtime['status'] == 'pass' and runtime['tests'] == expected
            assert runtime['errors'] == runtime['failures'] == 0
            assert runtime['candidate_commit'] == runtime['head_commit'] == COMMIT
            assert runtime['wheel_sha256'] == wheel_sha and not runtime['promotable']
            expected_test_sha = test_crlf_sha if platform == 'Windows' else test_sha
            assert runtime['test_module_sha256'] == expected_test_sha
            assert runtime['selection'] == selection and runtime['mode'] == mode
            assert runtime['isolated'] == (1 if mode == 'package' else 0)
            logs = (directory / 'test-output.log').read_text(errors='replace')
            assert f'Ran {expected} tests' in logs and 'FAILED' not in logs
            elapsed = re.search(r'Ran \d+ tests in ([\d.]+)s', logs)
            assert elapsed
            expected_case_names = smoke_names if selection == 'smoke' else methods['SkillOwnershipAcceptanceTests']
            skipped_names = {item['test'].split()[0] for item in runtime['skipped']}
            expected_record_names = expected_case_names - skipped_names
            if selection == 'full':
                for name in methods['OwnershipReadBoundaryTests']:
                    assert re.search(r'^' + re.escape(name) + r' \([^\n]+OwnershipReadBoundaryTests\.[^\n]+\) \.\.\. ok$', logs, re.MULTILINE)
            observed = []
            for file in sorted((directory / 'cases').glob('*.json')):
                case = read(file)
                assert case['candidate_commit'] == COMMIT
                assert case['case_outcome'] in ('passed', 'skipped'), (file, case['case_outcome'])
                assert 'released_017' not in case['test']
                if mode == 'package':
                    assert case['evaluator']['archive_sha256'] == wheel_sha
                name = case['test'].rsplit('.', 1)[-1]
                assert (case['case_outcome'] == 'skipped') == (name in skipped_names)
                observed.append(name)
                case_index.append({'path': file.relative_to(CI).as_posix(), 'test': case['test'],
                    'outcome': case['case_outcome'], 'sha256': sha(file.read_bytes()),
                    'event_count': len(case.get('events', []))})
            assert len(observed) == len(set(observed))
            assert expected_record_names <= set(observed) <= expected_case_names
            assert all(name in observed for name in (
                'test_own07_candidate_dashboard_output_preserves_installed_workflow',
                'test_own07_candidate_qualification_output_preserves_retired_skill',
                'test_own07_unsupported_old_lock_refuses_before_writes'))
            selections.append({'platform': platform, 'python': python, 'mode': mode,
                'tests': expected, 'skipped': runtime['skipped'], 'seconds': float(elapsed.group(1)),
                'retained_case_records': len(observed), 'read_boundary_unit_tests': 11 if selection == 'full' else 0,
                'runtime': directory.relative_to(CI).as_posix() + '/runtime.json',
                'test_module_sha256': runtime['test_module_sha256'],
                'test_module_transport': 'Git LF-to-CRLF only' if platform == 'Windows' else 'identical Git LF bytes',
                'run_attempt': runtime['run_attempt']})

replays = []
for platform in ('Linux', 'Windows'):
    for number in (1, 2):
        path = CI / ('upgrade-rehearsal-' + platform) / f'rehearsal-result-{number}/upgrade-rehearsal-result.json'
        replay = read(path)
        assert replay['overall_result'] == 'pass' and replay['failure'] is None
        assert all(step['outcome'] == 'pass' for step in replay['steps'])
        replays.append({'platform': platform, 'replay': number, 'semantic_sha256': replay['semantic_sha256']})
assert len({item['semantic_sha256'] for item in replays}) == 1
log = (OUT / 'github-final/workflow.log').read_text(errors='replace')
match = re.search(r'Ran (1240) tests in ([\d.]+)s[^\n]*\n(?:.*\n){0,3}?.*?OK(?: \(skipped=(\d+)\))?', log)
assert match, 'source runner verdict not found'
summary = {'candidate_commit': COMMIT, 'candidate_tree': complete['target']['tree'],
    'workflow_run': run['url'], 'workflow_attempt': read(OUT / 'github-final/run-api.json')['run_attempt'],
    'wheel_sha256': wheel_sha, 'test_module_git_blob_sha256': test_sha,
    'test_module_crlf_sha256': test_crlf_sha, 'source_tests': int(match.group(1)),
    'source_seconds': float(match.group(2)), 'source_skips': int(match.group(3) or 0),
    'ownership_selections': selections, 'ownership_test_executions': sum(item['tests'] for item in selections),
    'case_count': len(case_index),
    'case_outcomes': dict(Counter(case['outcome'] for case in case_index)),
    'upgrade_replays': replays, 'governing_evaluator_version': '0.17.0',
    'old_017_migration_acceptance': 'excluded by explicit approved scope; historical failures preserved',
    'first_attempt': 'cancelled and incomplete; not acceptance',
    'candidate_ci_passed': True, 'scope': 'WO-PLG-020 only',
    'limits': ['No native-host qualification, macOS acceptance, release, adoption or live WO-PLG-009 migration.',
        'C10/C11 accepted enforcement limitation remains.',
        'Installed wheel is non-promotable; source observations are candidate-controlled.']}
DEST.mkdir()
(OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')
(DEST / 'acceptance-summary.json').write_bytes((OUT / 'summary.json').read_bytes())
(DEST / 'case-index.json').write_text(json.dumps(case_index, indent=2) + '\n', encoding='utf-8')

def archive_tree(name, groups):
    members = {}
    for prefix, source in groups:
        for path in source.rglob('*'):
            if path.is_file() and path.suffix not in ('.whl', '.gz'):
                members[prefix + '/' + path.relative_to(source).as_posix()] = path.read_bytes()
    archive = DEST / name
    with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as stream:
        for name, raw in sorted(members.items()):
            stream.writestr(name, raw)
    with zipfile.ZipFile(archive) as stream:
        assert stream.testzip() is None
        assert all(stream.read(name) == raw for name, raw in members.items())
    index = {'archive': archive.name, 'sha256': sha(archive.read_bytes()), 'bytes': archive.stat().st_size,
        'members': {name: {'bytes': len(raw), 'sha256': sha(raw)} for name, raw in sorted(members.items())}}
    (archive.with_suffix('.json')).write_text(json.dumps(index, indent=2) + '\n', encoding='utf-8')

archive_tree('merged-candidate-ci.zip', [('artifacts', CI), ('github', OUT / 'github-final')])
archive_tree('cancelled-attempt.zip', [('artifacts', OUT / 'ci-main-initial'), ('github', OUT / 'github-resumed')])
for name in ('preflight', 'doctor', 'validation'):
    for suffix in ('.json', '-command.json', '.stderr.log'):
        shutil.copyfile(OUT / (name + suffix), DEST / (name + suffix))
shutil.copyfile(OUT / 'retain_evidence.py', DEST / 'audit-ci-evidence.py')
print(json.dumps(summary, indent=2))
