"""Replay WO-HAG-003 against an installed wheel and disposable records only.

Run with that environment's Python -I. No repository imports or guard mocks.
The program creates and removes its own temporary fixture; it never accepts a
live repository path. Output contains actual commands, exits and CLI results.
"""
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import tomllib

import se_harness


def main():
    assert sys.flags.isolated, "Use the installed environment's Python -I"
    report = {"platform": platform.platform(), "python": sys.version,
              "executable": sys.executable, "module": se_harness.__file__,
              "version": se_harness.__version__, "observations": [], "checks": []}
    with tempfile.TemporaryDirectory(prefix="hag003-installed-") as directory:
        cwd = Path(directory)
        root = cwd / "fixture"

        def cli(command, *args, expected=0):
            argv = [sys.executable, '-I', '-m', 'se_harness', command, str(root), *args, '--json']
            result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, encoding='utf-8', timeout=120)
            item = {'argv': argv, 'cwd': str(cwd), 'exit_code': result.returncode,
                    'stdout': result.stdout, 'stderr': result.stderr}
            report['observations'].append(item)
            assert result.returncode == expected, item
            return json.loads(result.stdout)

        def formal(folder, artifact, kind, relations, extra='', status='draft', owner='engineering-owner'):
            lines = ['+++', f'id = "{artifact}"', f'type = "{kind}"', f'title = "Synthetic {artifact}"',
                     f'status = "{status}"', 'owners = '+json.dumps([owner]),
                     'created = "2026-10-04"', 'updated = "2026-10-04"', extra, '[relations]']
            lines += [name+' = '+json.dumps(values) for name, values in relations.items()]
            text = '\n'.join(lines) + '\n+++\n\n# Synthetic installed-package test\n'
            path = root / 'docs/engineering/probe' / folder / (artifact + '.md')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8', newline='\n')
            return path

        def snapshot():
            return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in root.rglob('*') if p.is_file()}

        def metadata(path):
            return tomllib.loads(path.read_text(encoding='utf-8').split('+++', 2)[1])

        try:
            cli('init', '--project-name', 'Disposable decision attribution probe')
            formal('intent', 'INT-PRB-001', 'intent', {})
            formal('capabilities', 'CAP-PRB-001', 'capability', {'derives_from': ['INT-PRB-001']})
            formal('requirements', 'REQ-PRB-001', 'requirement', {'derives_from': ['CAP-PRB-001']},
                   'statement = "THE SYSTEM SHALL retain the human decision."\nverification_method = ["test"]')
            formal('specifications', 'SPEC-PRB-001', 'specification', {'specifies': ['REQ-PRB-001']})
            formal('verification', 'VER-PRB-001', 'verification', {'verifies': ['REQ-PRB-001']})
            work = formal('work-orders', 'WO-PRB-001', 'work_order', {'implements': ['REQ-PRB-001'],
                          'specifications': ['SPEC-PRB-001'], 'verification': ['VER-PRB-001']})
            decision = formal('decisions', 'DEC-PRB-001', 'decision',
                              {'concerns': ['WO-PRB-001'], 'blocks': ['WO-PRB-001']},
                              'kind = "question"\nquestion = "Keep this definition?"\nraised_by = "test-agent"\n'
                              'recommendation = "keep"\n[[options]]\nid = "keep"\nlabel = "Keep."\n'
                              '[[options]]\nid = "stop"\nlabel = "Stop."', status='open', owner='mmzen')
            cli('validate')
            base = ('--artifact', 'DEC-PRB-001', '--option', 'keep', '--decision', 'mmzen', '--reason', '  Recorded test answer.  ')
            before = snapshot()
            refused = cli('decide', *base, '--apply', expected=1)
            assert 'WEX201' in json.dumps(refused) and snapshot() == before
            report['checks'].append('actual human without explicit binding refuses; no bytes changed')
            for owner in ('unrelated', '', 'x' * 129, 'engineering-owner\n'):
                cli('decide', *base, '--authority-owner', owner, '--apply', expected=1)
                assert snapshot() == before
            report['checks'].append('invalid or unrelated binding refuses; no bytes changed')
            cli('decide', *base, '--authority-owner', 'engineering-owner')
            assert snapshot() == before
            report['checks'].append('valid preview writes nothing')
            cli('decide', *base, '--authority-owner', 'engineering-owner', '--apply')
            meta = metadata(decision)
            assert meta['disposition']['decided_by'] == 'mmzen'
            assert meta['disposition']['authority_owner'] == 'engineering-owner'
            assert meta['disposition']['reason'] == '  Recorded test answer.  '
            assert meta['lifecycle_events'][-1]['decided_by'] == 'mmzen'
            assert snapshot()[work.relative_to(root).as_posix()] == before[work.relative_to(root).as_posix()]
            after = snapshot()
            assert {p for p in after if after[p] != before.get(p)} == {decision.relative_to(root).as_posix()}
            cli('validate')
            cli('decide', *base, '--authority-owner', 'engineering-owner', '--apply', expected=1)
            assert snapshot() == after
            report['checks'].append('apply records actual human and owner; terminal replay refuses; blocked work unchanged')
            paired = cli('raise-risk', '--domain', 'probe', '--title', 'Synthetic threat',
                         '--description', 'The test observes paired-risk attribution.', '--action', 'Review it.',
                         '--owner', 'engineering-owner', '--threatens', 'WO-PRB-001', '--id', 'RISK-PRB-001',
                         '--with-decision', '--decision-id', 'DEC-PRB-002')
            cli('decide', '--artifact', 'DEC-PRB-002', '--decision', 'mmzen', '--authority-owner', 'engineering-owner',
                '--option', 'accept', '--reason', 'Test acceptance until v9.', '--revisit', 'v9', '--apply')
            risk = root / 'docs/engineering/probe/risks/RISK-PRB-001.md'
            assert metadata(risk)['disposition']['decided_by'] == 'mmzen'
            assert metadata(risk)['lifecycle_events'][-1]['decided_by'] == 'mmzen'
            cli('validate')
            report['checks'].append('paired risk and decision retain actual human through the installed mutation guard')
            report['result'] = 'pass'
        except Exception as error:
            report['result'] = 'fail'
            report['error'] = str(error)
        print(json.dumps(report, indent=2))
        return 0 if report['result'] == 'pass' else 1


if __name__ == '__main__':
    raise SystemExit(main())
