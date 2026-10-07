"""Installed-client lifecycle walkthrough against a real private sandbox."""
from __future__ import annotations
import argparse, base64, copy, hashlib, json, os, subprocess, sys, time, tomllib, uuid
from pathlib import Path


class Pilot:
    def __init__(self, args):
        self.args = args
        self.output = args.output.resolve(); self.output.mkdir(parents=True, exist_ok=False)
        self.config = json.loads(args.configuration.read_text())
        self.credentials = json.loads(args.credentials.read_text())
        self.source = json.loads(args.source_manifest.read_text())
        self.events = []; self.sequence = 0; self.version = 0; self.context = None
        self.prefix = uuid.uuid4().hex
        sys.path.insert(0, str(args.repository / 'tests/hosted_artifact_graph'))
        from lifecycle_fixture import files
        self.drafts = files()

    def save(self, name, value):
        (self.output / name).write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')

    def cli(self, label, operation, request=None, *, expected=0, principal='operator', extra=()):
        self.sequence += 1
        label = f'{self.sequence:03}-{label}'
        argv = [str(self.args.client_python), '-I', '-m', 'se_harness', 'remote', operation,
                '--endpoint', self.args.endpoint, '--project', self.config['project_id'], '--token-env', 'HAG_TEST_TOKEN', '--json', *extra]
        if request is not None:
            self.save(label + '-request.json', request)
            argv += ['--request', str(self.output / (label + '-request.json'))]
        if operation in ('import','draft-open','create-artifact','revise-artifact','freeze','rehearse','export'):
            argv += ['--client-wheel', str(self.args.client_wheel)]
        if operation in ('rehearse', 'export'):
            argv += ['--test-copy']
        token = next(p['token'] for p in self.credentials['principals'] if p['id'] == principal)
        start = time.monotonic()
        result = subprocess.run(argv, cwd=self.output, env=dict(os.environ, HAG_TEST_TOKEN=token), capture_output=True, timeout=180)
        out, err = result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
        assert token not in out + err
        event = {'label': label, 'argv': argv, 'cwd': str(self.output), 'exit': result.returncode,
                 'stdout': out, 'stderr': err, 'seconds': round(time.monotonic()-start, 3)}
        self.save(label + '.json', event); self.events.append(label + '.json')
        print(json.dumps({'step': label, 'exit': result.returncode}), flush=True)
        assert result.returncode == expected, label + ': inspect actual retained result'
        return json.loads(out if result.returncode != 2 else err)

    def command(self, operation, **fields):
        return {'schema': 'se-harness-remote-command/v1', 'operation': operation,
            'operation_key': self.prefix + '-' + str(self.sequence), 'project_id': self.config['project_id'],
            'expected_evaluator': self.config['components']['evaluator'], 'client': self.config['client'],
            'expected_project_version': self.version, **fields}

    def accepted(self, label, request):
        result = self.cli(label, request['operation'], request)
        assert result['outcome'] == 'accepted'
        self.version = result['versions']['project']['after']
        if result.get('view', {}).get('kind') == 'context': self.context = result['view']
        return result

    def action(self, action, mode='preview'):
        return {'schema': 'se-harness-lifecycle-command/v2', 'operation': 'rehearse', 'test_copy': True,
            'operation_key': self.prefix + '-' + str(self.sequence), 'project_id': self.config['project_id'],
            'expected_evaluator': self.config['components']['evaluator'], 'client': self.config['client'],
            'expected_project_version': self.version, 'context_id': self.context['context_id'],
            'expected_context_version': self.context['context_version'], 'mode': mode, 'preview_digest': None, 'action': action}

    def apply(self, label, action):
        request = self.action(action)
        preview = self.cli(label + '-preview', 'rehearse', request)
        assert preview['outcome'] == 'previewed' and preview['test_copy'] is True and preview['receipt_id'] is None
        request.update(mode='apply', preview_digest=preview['preview_digest'])
        result = self.accepted(label + '-apply', request)
        assert result['test_copy'] is True
        repeated = self.cli(label + '-retry', 'rehearse', request)
        assert repeated == result
        self.last_request = request; self.last_result = result
        return result

    def transition(self, label, ids, state, actor='test-owner'):
        return self.apply(label, {'kind': 'transition', 'assignments': [{'artifact': i, 'state': state, 'actor': actor,
            'reason': 'Synthetic rehearsal only; no real human decision or external authority.'} for i in ids]})

    def read(self, operation, **fields):
        result = self.cli('read-' + operation, 'read', {'schema': 'se-harness-graph-read/v1', 'project_id': self.config['project_id'],
            'operation': operation, 'view': self.context, 'budget': {'rows': 500, 'bytes': 2097152, 'depth': 8}, **fields})
        assert result['test_copy'] is True and result['schema'] == 'se-harness-graph-read/v2'
        return result

    def export(self, label, baseline):
        destination = self.output / label
        result = self.cli(label, 'export', {'schema': 'se-harness-lifecycle-export-request/v2', 'test_copy': True,
            'project_id': self.config['project_id'], 'baseline_id': baseline, 'client': self.config['client'],
            'expected_evaluator': self.config['components']['evaluator']}, extra=('--destination', str(destination)))
        assert result['baseline_id'] == baseline and not (destination / '.incomplete').exists()
        return destination

    def run(self):
        status = self.cli('ready', 'status')
        assert status['ready'] and status['test_copy'] and status['schema_revision'] == 2
        self.version = status['project_version']
        if self.args.resume_definitions:
            resumed = json.loads(json.loads(self.args.resume_definitions.read_text())['stdout'])
            assert resumed['versions']['project']['after'] == self.version
            self.context = resumed['view']
            return self.after_definitions(resumed)
        if self.args.resume_drafts:
            resumed = json.loads(json.loads(self.args.resume_drafts.read_text())['stdout'])
            assert resumed['versions']['project']['after'] == self.version
            self.context = resumed['view']
            return self.after_drafts()
        imported = self.accepted('import', self.command('import', source_manifest=self.source))
        self.accepted('context', self.command('draft-open', base_baseline_id=imported['view']['baseline_id'], work_order_id='WO-P3-900'))
        for name, raw in self.drafts.items():
            doc = tomllib.loads(raw.decode().split('+++', 2)[1])
            created = self.accepted('create-' + doc['id'], self.command('create-artifact', context_id=self.context['context_id'],
                expected_context_version=self.context['context_version'], domain='lifecycle-pilot', artifact_type=doc['type'], artifact_id=doc['id']))
            revision = created['affected_artifacts'][0]
            self.accepted('complete-' + doc['id'], self.command('revise-artifact', context_id=self.context['context_id'],
                expected_context_version=self.context['context_version'], artifact_id=doc['id'], expected_revision_id=revision['revision_id'],
                document_base64=base64.b64encode(raw).decode()))
        return self.after_drafts()

    def after_drafts(self):
        wrong = {'kind': 'transition', 'assignments': [{'artifact': 'WO-P3-001', 'state': 'verified', 'actor': 'test-owner', 'reason': 'Synthetic refusal test.'}]}
        unsupported = self.cli('refuse-unsupported-edge', 'rehearse', self.action(wrong), expected=1)
        assert unsupported['error']['code'] == 'HAG_REMOTE_EVALUATOR_REFUSED'
        wrong['assignments'][0].update(artifact='WO-P3-900', state='approved')
        imported_refusal = self.cli('refuse-imported-state', 'rehearse', self.action(wrong), expected=1)
        assert imported_refusal['error']['code'] == 'HAG_REMOTE_PROTECTED_FIELD'
        arbitrary = self.action({'kind': 'validate'}, 'inspect'); arbitrary['action']['test_command'] = ['never-run-this']
        bad = self.cli('refuse-arbitrary-command', 'rehearse', arbitrary, expected=1)
        assert bad['error']['code'] == 'HAG_REMOTE_MALFORMED'
        first = self.transition('approve-definitions', ['INT-P3-001','CAP-P3-001','REQ-P3-001','SPEC-P3-001','VER-P3-001','REL-P3-001'], 'approved')
        return self.after_definitions(first)

    def after_definitions(self, first):
        early = self.export('early-export', first['baseline_id'])
        replay = self.output / 'initial-history'
        result = subprocess.run(['git', '-c', 'core.autocrlf=false', '-c', 'core.hooksPath=' + os.devnull, 'clone', '--quiet', '--template=', '--branch', 'rehearsal', str(early / 'history.bundle'), str(replay)], capture_output=True)
        assert result.returncode == 0, result.stderr.decode()
        base = subprocess.check_output(['git','rev-list','--max-parents=0','HEAD'], cwd=replay).decode().strip()
        self.transition('approve-work', ['WO-P3-001'], 'approved')
        self.cli('start-preflight', 'rehearse', self.action({'kind': 'preflight', 'work_order': 'WO-P3-001', 'phase': 'start'}, 'inspect'))
        self.transition('start-work', ['WO-P3-001'], 'in_progress', 'test-executor')
        denied = b'outside the selected test scope\n'
        failed_gate = self.cli('refuse-outside-scope', 'rehearse', self.action({'kind':'handoff','work_order':'WO-P3-001','from_git':base,
            'files':[{'path':'outside-scope.txt','bytes':len(denied),'sha256':hashlib.sha256(denied).hexdigest(),
                      'content_base64':base64.b64encode(denied).decode()}]}), expected=1)
        assert failed_gate['error']['code'] == 'HAG_REMOTE_EVALUATOR_REFUSED'
        self.apply('raise-risk', {'kind':'raise-risk', 'domain':'lifecycle-pilot','id':'RISK-P3-001','title':'Incorrect test greeting',
            'description':'A test implementation could return a different greeting.','action':'Run the independent exact-string assertion.',
            'owner':'test-owner','raised_by':'test-executor','threatens':['WO-P3-001'],'decision_id':'DEC-P3-001','recommend':'mitigate'})
        self.apply('decide-risk', {'kind':'decide','artifact':'DEC-P3-001','decision':'test-owner','reason':'Synthetic risk treatment; no real risk acceptance.',
            'option':'mitigate','disposition':'decide','mitigated_by':['WO-P3-001']})
        code = b"def greeting():\n    return 'Hello rehearsal'\n"
        source = self.output / 'greeting.py'; source.write_bytes(code)
        test_argv = [str(self.args.client_python), '-I', '-c', "import runpy,sys;assert runpy.run_path(sys.argv[1])['greeting']()=='Hello rehearsal';print('exact greeting passed')", str(source)]
        tested = subprocess.run(test_argv, cwd=self.output, capture_output=True)
        test_evidence = {'argv':test_argv,'cwd':str(self.output),'exit':tested.returncode,'stdout':tested.stdout.decode(),'stderr':tested.stderr.decode()}
        assert tested.returncode == 0
        evidence_bytes = (json.dumps(test_evidence, indent=2) + '\n').encode()
        evidence = 'docs/engineering/lifecycle-pilot/evidence/WO-P3-001/assertion.json'
        files = [{'path': p,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest(),'content_base64':base64.b64encode(raw).decode()} for p,raw in [('src/greeting.py',code),(evidence,evidence_bytes)]]
        self.apply('handoff', {'kind':'handoff','work_order':'WO-P3-001','from_git':base,'files':files})
        self.transition('complete-work', ['WO-P3-001'], 'implemented', 'test-executor')
        capture = {'kind':'capture-verification','id':'VREC-P3-001','domain':'lifecycle-pilot','work_orders':['WO-P3-001'],
                   'verifications':['VER-P3-001'],'evidence':[evidence],'owner':'quality-owner'}
        self.save('capture-request.json', self.action(capture))
        self.apply('capture', capture)
        self.transition('verify', ['VREC-P3-001'], 'verified', 'quality-owner')
        self.apply('prepare-release', {'kind':'prepare-release','id':'RLS-P3-001','domain':'lifecycle-pilot','release_contract':'REL-P3-001',
            'verification_record':'VREC-P3-001','work_orders':['WO-P3-001'],'version':'0.0.1','tag':'rehearsal-0.0.1','owner':'release-owner'})
        final = self.transition('release', ['RLS-P3-001'], 'released', 'release-owner')
        self.read('check', artifact_id='RLS-P3-001')
        self.read('work-context', work_order_id='WO-P3-001')
        self.read('cypher', query='MATCH (r:Revision) WHERE r.artifact_id = $id RETURN r.artifact_id AS id LIMIT 5', parameters={'id':'WO-P3-001'})
        final_export = self.export('final-export', final['baseline_id'])
        old_again = self.export('old-export-again', first['baseline_id'])
        assert (early/'history.bundle').read_bytes() == (old_again/'history.bundle').read_bytes()
        for p in (early/'files').rglob('*'):
            if p.is_file(): assert p.read_bytes() == (old_again/'files'/p.relative_to(early/'files')).read_bytes()
        self.save('walkthrough.json', {'state':'installed_client_sequence_passed','test_copy':True,'source':self.source['source'],
            'project_version':self.version,'context':self.context,'first_baseline':first['baseline_id'],'final_baseline':final['baseline_id'],
            'final_export':str(final_export),'last_request':self.last_request,'last_result':self.last_result,'events':self.events,
            'remaining':['independent semantic comparison','faults/concurrency','restart/restore','packaged documentation review']})


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('client-python','client-wheel','configuration','credentials','source-manifest','repository','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--endpoint',required=True)
    parser.add_argument('--resume-drafts',type=Path,help='exact retained last draft-authoring response; no replay of accepted writes')
    parser.add_argument('--resume-definitions',type=Path,help='exact retained first definition approval; resume remaining test work')
    args=parser.parse_args(); pilot=Pilot(args)
    try: pilot.run()
    except BaseException as exc:
        pilot.save('walkthrough-failure.json',{'outcome':'failed','type':type(exc).__name__,'message':str(exc),'events':pilot.events})
        raise
