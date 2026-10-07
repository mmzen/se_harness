"""Independent released-command comparison from exact hosted input Git bytes.

Run inside the qualification container. No service adapter creates reference
answers: ordinary clones and the separately installed public CLI do that.
"""
import argparse
import base64
import hashlib
import json
import os
import subprocess
import tomllib
from pathlib import Path


def commands(action):
    a=action; kind=a['kind']
    if kind=='transition':
        argv=[]
        for item in a['assignments']:
            for flag,key in (('set','state'),('decision','actor'),('reason','reason')):
                argv += ['--'+flag,item['artifact']+'='+item[key]]
        return [('transition',argv),('transition',argv+['--apply'])]
    if kind=='raise-risk':
        argv=[]
        for key in ('domain','id','title','description','action','owner','raised_by','stage','category','likelihood','impact','recommend'):
            if key in a: argv += ['--'+key.replace('_','-'),str(a[key])]
        for ident in a['threatens']: argv += ['--threatens',ident]
        if 'decision_id' in a: argv += ['--with-decision','--decision-id',a['decision_id']]
        return [('raise-risk',argv+['--dry-run']),('raise-risk',argv)]
    if kind=='decide':
        argv=['--artifact',a['artifact'],'--decision',a['decision'],'--reason',a['reason']]
        for key in ('option','authority_owner','revisit'):
            if key in a: argv += ['--'+key.replace('_','-'),a[key]]
        for key in ('scope','mitigated_by','avoided_by'):
            for ident in a.get(key,[]): argv += ['--'+key.replace('_','-'),ident]
        if a['disposition']!='decide': argv += ['--'+a['disposition']]
        return [('decide',argv),('decide',argv+['--apply'])]
    if kind=='handoff':
        paths=sorted(x['path'] for x in a['files'])
        return [('check',['--artifact',a['work_order'],'--checkpoint','scope','--changes-complete',
                         *[v for p in paths for v in ('--changed-path',p)]]),
                ('preflight',['--work-order',a['work_order'],'--phase','review']),
                ('evidence',['--artifact',a['work_order'],'--checkpoint','handoff']),
                ('check',['--artifact',a['work_order'],'--checkpoint','handoff','--from-git',a['from_git']])]
    if kind=='capture-verification':
        argv=['--id',a['id'],'--domain',a['domain'],'--owner',a['owner']]
        for key,flag in (('work_orders','work-order'),('verifications','verification'),('evidence','evidence')):
            for item in a[key]: argv += ['--'+flag,item]
        return [(kind,argv)]
    if kind=='prepare-release':
        argv=[]
        for key in ('id','domain','release_contract','verification_record','version','owner','tag'):
            argv += ['--'+key.replace('_','-'),a[key]]
        for item in a['work_orders']: argv += ['--work-order',item]
        return [(kind,argv)]
    raise ValueError('No independent reference for '+kind)


def semantics(value):
    """Only declared semantic assertions; raw results and exact bytes are retained."""
    found=[]
    def walk(node,path=''):
        if isinstance(node,dict):
            for key,item in node.items():
                if key in ('state','current_lifecycle_state'):
                    found.append([path+'/'+key,item])
                elif key=='next' and isinstance(item,dict):
                    found.append([path+'/next',{k:item.get(k) for k in ('procedure_id','step_id')}])
                elif key in ('predicate_id','gate_id'):
                    found.append([path+'/'+key,item,node.get('status'),node.get('result')])
                elif key=='id' and isinstance(item,str) and item.startswith(('QGP-','QG-')):
                    found.append([path+'/id',item,node.get('status'),node.get('result')])
                else: walk(item,path+'/'+key)
        elif isinstance(node,list):
            for i,item in enumerate(node):walk(item,path+'/'+str(i))
    walk(value)
    return found


def run(args):
    from hosted_artifact_graph.service import Service
    args.output.mkdir(parents=True,exist_ok=False)
    service=Service(json.loads(args.config.read_text()),json.loads(args.credentials.read_text()))
    principal=next(p for p in service.credentials['principals'] if p['id']=='operator')
    events=[]; cases=[]; inputs={}
    def command(label,argv,cwd):
        env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','PYTHON'))}
        env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull)
        child=subprocess.run(list(map(str,argv)),cwd=cwd,env=env,capture_output=True,timeout=180)
        event={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'exit':child.returncode,
            'stdout':child.stdout.decode('utf-8','replace'),'stderr':child.stderr.decode('utf-8','replace')}
        events.append(event);(args.output/'commands.json').write_text(json.dumps(events,indent=2)+'\n')
        return event
    def git(label,root,*argv):
        value=command(label,['git','-c','core.autocrlf=false','-c','core.hooksPath=/dev/null',*argv],root)
        assert value['exit']==0,(label,value['stderr'])
        return value['stdout'].strip()
    def export(baseline):
        return service.export_test(principal,{'schema':'se-harness-lifecycle-export-request/v2','test_copy':True,
            'project_id':service.project_id,'baseline_id':baseline,'client':service.config['client'],
            'expected_evaluator':service.config['components']['evaluator']})
    def clone(label,value):
        directory=args.output/label;directory.mkdir()
        snapshot=value['snapshot']; bundle=directory/'history.bundle'
        bundle.write_bytes(base64.b64decode(snapshot['git_bundle']['content_base64']))
        root=directory/'repository'
        git(label+'-clone',directory,'clone','--quiet','--template=',str(bundle),str(root))
        assert git(label+'-head',root,'rev-parse','HEAD')==snapshot['head']
        git(label+'-objects',root,'fsck','--full','--no-reflogs')
        actual={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in git(label+'-files',root,'ls-files').splitlines()}
        assert actual=={p:x['sha256'] for p,x in snapshot['files'].items()}
        for candidate in snapshot['candidates']:
            git(label+'-candidate-object',root,'cat-file','-e',candidate['test_candidate']+'^{commit}')
            record=root/'docs/engineering/lifecycle-pilot/verification-records'/ (candidate['verification_record']+'.md')
            assert tomllib.loads(record.read_text().split('+++',2)[1])['commit']==candidate['test_candidate']
        return root
    try:
        for path in sorted(args.walkthrough.glob('*-apply-request.json')):
            request=json.loads(path.read_text())
            if request.get('schema')!='se-harness-lifecycle-command/v2':continue
            observed=json.loads(json.loads(path.with_name(path.name.replace('-request','')).read_text())['stdout'])
            if observed.get('outcome')!='accepted':continue
            label=path.stem.replace('-request','')
            root=clone(label,export(observed['provenance']['input_baseline']))
            inputs[request['action']['kind']]=observed['provenance']['input_baseline']
            if not cases: inputs['initial']=observed['provenance']['input_baseline']
            before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
            action=request['action']
            if action['kind']=='handoff':
                for item in action['files']:
                    target=root/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(base64.b64decode(item['content_base64']))
            expected_commands=commands(action)
            actual_commands=observed['evaluator_output']['commands']
            assert len(expected_commands)==len(actual_commands)
            compared=[]
            for i,((name,argv),actual) in enumerate(zip(expected_commands,actual_commands)):
                assert (name,argv)==(actual['command'],actual['arguments'])
                outcome=command(label+'-'+str(i),[service.evaluator.python,'-I','-m','se_harness',name,root,*argv,'--json'],args.output)
                assert outcome['exit']==actual['exit']==0,(label,outcome)
                expected=json.loads(outcome['stdout'])
                assert semantics(expected)==semantics(actual['result']),(label,semantics(expected),semantics(actual['result']))
                compared.append(semantics(expected))
            after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
            changed={p for p in after if before.get(p)!=after[p]}
            assert changed=={item['path'] for item in observed['files']}
            output=export(observed['baseline_id'])
            assert all(output['snapshot']['files'][item['path']]['sha256']==item['sha256'] for item in observed['files'])
            cases.append({'case':label,'kind':action['kind'],'outcome':'passed','file_effects':sorted(changed),'semantic_assertions':compared})
            (args.output/'parity.json').write_text(json.dumps({'state':'running','cases':cases},indent=2)+'\n')
        assert len(cases)==11,len(cases)
        for marker,baseline in (('refuse-unsupported-edge',inputs['initial']),('refuse-outside-scope',inputs['raise-risk'])):
            path=next(args.walkthrough.glob('*'+marker+'-request.json'))
            request=json.loads(path.read_text())
            observed=json.loads(json.loads(path.with_name(path.name.replace('-request','')).read_text())['stdout'])
            root=clone(marker,export(baseline));action=request['action']
            if action['kind']=='handoff':
                for item in action['files']:
                    target=root/item['path'];target.parent.mkdir(parents=True,exist_ok=True)
                    target.write_bytes(base64.b64decode(item['content_base64']))
            name,argv=commands(action)[0]
            actual=observed['evaluator_output']['commands'][-1]
            outcome=command(marker,[service.evaluator.python,'-I','-m','se_harness',name,root,*argv,'--json'],args.output)
            assert outcome['exit']==actual['exit']!=0
            expected=json.loads(outcome['stdout'])
            assert semantics(expected)==semantics(actual['result'])
            cases.append({'case':marker,'outcome':'passed','semantic_assertions':semantics(expected)})
        state=json.loads((args.walkthrough/'walkthrough.json').read_text())
        for label,baseline in (('early',state['first_baseline']),('final',state['final_baseline'])):
            root=clone(label,export(baseline))
            checked=command(label+'-validate',[service.evaluator.python,'-I','-m','se_harness','validate',root,'--json'],args.output)
            assert checked['exit']==0
            if label=='final':
                for ident in ('WO-P3-001','VREC-P3-001','RLS-P3-001'):
                    checked=command(label+'-'+ident,[service.evaluator.python,'-I','-m','se_harness','check',root,'--artifact',ident,'--json'],args.output)
                    assert checked['exit']==0
        result={'state':'independent_released_parity_and_export_passed','cases':cases,'commands':'commands.json',
            'comparison':'Exact command arguments, exits, selected states, gate predicates, next typed actions and complete changed path sets.',
            'incidental_exclusions':['generated timestamps','temporary absolute paths','hashes of records containing those incidental bytes'],
            'exact_bytes':'No stored/exported bytes normalized; each retained command-output file digest equals the selected export and its ordinary Git tree.'}
        (args.output/'parity.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({'state':result['state'],'operations':len(cases)}))
    finally:service.store.driver.close()


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=Path('/run/config/config.json'))
    parser.add_argument('--credentials',type=Path,default=Path('/run/secrets/sandbox_credentials'))
    parser.add_argument('--walkthrough',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    run(parser.parse_args())
