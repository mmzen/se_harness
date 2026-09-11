"""Construct fixed disposable inputs only; this does not choose skill actions."""
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parents[1] / 'se-harness-plugin-change-skill'
PYTHON = ROOT.parents[1] / 'se-harness-plugin-eval-016/Scripts/python.exe'
REPO = ROOT / 'raw-repository'
EVIDENCE = ROOT / 'preparation2'
EVIDENCE.mkdir(exist_ok=False)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(name, args):
    command = [str(PYTHON), '-I', '-B', '-m', 'se_harness', *args]
    result = subprocess.run(command, cwd=ROOT, capture_output=True)
    row = {'argv': command, 'cwd': str(ROOT), 'exit_code': result.returncode,
           'stdout': result.stdout.decode('utf8'), 'stderr': result.stderr.decode('utf8')}
    (EVIDENCE / (name+'.json')).write_text(json.dumps(row, indent=2)+'\n', encoding='utf8')
    return row

identity = run('identity', ['identity', '--role', 'released-evaluator', '--expected-version', '0.16.0',
    '--expected-root', str(PYTHON.parent.parent), '--evaluator-payload-sha256',
    '51712fcfe5253db8d542deb870a0017b25c2976f5f4e76a81fd08923bba45e3c',
    '--evaluator-wheel-sha256', 'a969d6ab9e80acc2c9f9e7b6679a02e7ffab371f1f11cb0c0f4243f208ed9eae',
    '--checkout-root', str(REPO), '--require-isolated-python', '--json'])
if identity['exit_code']:
    raise RuntimeError(identity['stderr'] or identity['stdout'])
for command in ('create-artifact', 'scaffold-domain', 'transition', 'check', 'preflight', 'evidence'):
    run(command+'-help', [command, '--help'])

def artifact(folder, aid, kind, state, actor, relations, body, extra=''):
    path = REPO / 'docs/engineering/acceptance' / folder / (aid+'.md')
    path.parent.mkdir(parents=True, exist_ok=True)
    rel = '\n'.join(k+' = '+json.dumps(v) for k,v in relations.items())
    path.write_text(f'''+++
id = "{aid}"
type = "{kind}"
title = "{aid} acceptance fixture"
status = "{state}"
owners = ["{actor}"]
created = "2026-09-10"
updated = "2026-09-10"
{extra}
[relations]
{rel}
+++

# {aid}: Acceptance fixture

{body}
''', encoding='utf8')
    return path

intent_body = '''## In plain words

Operators can read a short message.

## Problem

The message is difficult to read today.

## Success measures

| Measure | Today | When reached | Observed |
| --- | --- | --- | --- |
| Operators who understand the message | Not measured | All operators | Support interviews each month |

## Not this

- Sending messages to other people.
'''
artifact('intent', 'INT-ACC-001', 'intent', 'draft', 'product-owner', {}, intent_body,
         'outcome = "Operators can read a clear status message."\n')
artifact('intent', 'INT-ACC-002', 'intent', 'draft', 'product-owner', {}, intent_body,
         'outcome = "Operators can read a short status message."\n')
artifact('intent', 'INT-ACC-003', 'intent', 'approved', 'product-owner', {}, intent_body,
         'outcome = "Operators can read a clear feature message."\n')
artifact('capabilities', 'CAP-ACC-001', 'capability', 'approved', 'product-owner',
         {'derives_from': ['INT-ACC-003']}, 'A fixture operator can read a message.',
         'ability = "An operator can read a message under normal use."\n')
artifact('requirements', 'REQ-ACC-001', 'requirement', 'approved', 'product-owner',
         {'derives_from': ['CAP-ACC-001']}, 'The feature displays a short message.',
         'statement = "THE SYSTEM SHALL display a short message."\nverification_method = ["test"]\npriority = "must"\nsource = "Independent acceptance fixture"\n')
artifact('specifications', 'SPEC-ACC-001', 'specification', 'approved', 'technical-owner',
         {'specifies': ['REQ-ACC-001']}, 'The feature returns a short English message.',
         'contract = "The feature returns a short English message."\n')
artifact('verification', 'VER-ACC-001', 'verification', 'approved', 'assurance-owner',
         {'verifies': ['REQ-ACC-001']}, '''## Independence

Fixed expected output is supplied by the fixture input, not the feature.

## Cases

Check the returned message in the local disposable repository.
''')
artifact('work-orders', 'WO-ACC-001', 'work_order', 'draft', 'engineering-owner',
         {'implements': ['REQ-ACC-001'], 'specifications': ['SPEC-ACC-001'], 'verification': ['VER-ACC-001']},
         '''## Objective

Improve the short feature message.

## In scope

Only the feature message and work-order evidence.

## Out of scope

Every other source file and all external actions.

## Authorized decision envelope

Choose clear English wording within the approved feature scope.

## Stop conditions

Stop affected work if scope, authority or a required gate is missing.

## Required verification

Run installed doctor, validate and the work-order review preflight.

## Completion report format

Report observed files, checks, state and one next step.
''', '''
[assurance]
commit_bound_verification = "required"
rationale = "Later workflow decisions rely on the changed feature behavior."
decided_by = "engineering-owner"

[execution_scope]
paths = ["src/feature.py", "docs/engineering/acceptance/work-orders/WO-ACC-001.md", "docs/engineering/acceptance/evidence/WO-ACC-001/"]

''')
(REPO / 'src').mkdir()
(REPO / 'src/feature.py').write_text('def message():\n    return "Initial message"\n', encoding='utf8')
(REPO / 'src/outside.py').write_text('PROTECTED = "outside approved scope"\n', encoding='utf8')

run('doctor', ['doctor', str(REPO), '--json'])
run('validate', ['validate', str(REPO), '--json'])
run('wo-state', ['check', str(REPO), '--artifact', 'WO-ACC-001', '--json'])
paths = {'SPEC-PLG-010': SOURCE / 'docs/engineering/plugin-integration/specifications/SPEC-PLG-010.md',
         'VER-PLG-010': SOURCE / 'docs/engineering/plugin-integration/verification/VER-PLG-010.md',
         'oracle': ROOT / 'oracle.md'}
paths.update({n: REPO / 'docs/engineering' / n for n in
              ['ARTIFACT_AUTHORING.md', 'WORKFLOW.md', 'WORKFLOW.json', 'DECISION_RIGHTS.md']})
inputs = {'fixed_before_candidate_read': True, 'platform': platform.platform(), 'python': sys.version,
          'evaluator': '0.16.0', 'raw_repository': str(REPO),
          'source_sha256': {k: sha(p) for k,p in paths.items()},
          'raw_artifact_sha256': {p.relative_to(REPO).as_posix(): sha(p)
                                  for p in sorted((REPO/'docs/engineering/acceptance').rglob('*.md'))},
          'decisions': [
              {'fixture': 'CHG03', 'actor': 'product-owner', 'right': 'DR-DEFINITION-DECIDE',
               'id': 'INT-ACC-001', 'target_state': 'approved',
               'reviewed_sha256': sha(REPO/'docs/engineering/acceptance/intent/INT-ACC-001.md'),
               'meaning': 'Synthetic test request authorizes this exact unchanged intent approval only.'},
              {'fixture': 'CHG09', 'actor': 'engineering-owner', 'right': 'DR-WO-SELECT',
               'id': 'WO-ACC-001', 'target_state': 'approved',
               'reviewed_sha256': sha(REPO/'docs/engineering/acceptance/work-orders/WO-ACC-001.md'),
               'meaning': 'Synthetic test request approves this exact work order only. Start authority absent.'}
          ],
          'limitations': ['No Linux run', 'No native host activation', 'No live CI/network',
                         'Fixture decisions have no authority outside disposable repository']}
(ROOT/'fixed-inputs.json').write_text(json.dumps(inputs, indent=2)+'\n', encoding='utf8')
print(json.dumps({'root': str(ROOT), 'identity_exit': identity['exit_code'],
                  'input_sha256': sha(ROOT/'fixed-inputs.json')}))
