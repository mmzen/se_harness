"""Replay accepted native lifecycle calls through the separate released CLI.

Native files identify candidate requests; independent service receipt lookup must
confirm each acceptance. Exact immutable exports supply input Git bytes. No
service adapter computes the reference states, gates, next steps or file effects.
"""
from __future__ import annotations
import argparse
import base64
import hashlib
import json
import os
import subprocess
import tomllib
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from qualify_pilot_replay import commands, semantics


def canonical(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def semantic_assertions(value):
    # Receipt storage may sort JSON object keys; object member order is not a
    # lifecycle meaning. Preserve each exact JSON path and its complete value.
    return sorted(semantics(value),key=lambda item:item[0])


def run(args):
    for name in ('native_root','selection','credentials','evaluator_python','output'):
        setattr(args,name,getattr(args,name).absolute())
    args.output.mkdir(parents=True,exist_ok=False)
    selection=json.loads(args.selection.read_text(encoding='utf-8'))
    credentials=json.loads(args.credentials.read_text(encoding='utf-8'))
    token=next(p['token'] for p in credentials['principals'] if p['id']=='operator')
    config=json.loads(Path(selection['configuration']).read_text(encoding='utf-8'))
    events=[];cases=[];lookup=[];exports=[]

    def save(name,value):
        raw=json.dumps(value,indent=2,ensure_ascii=False)+'\n'
        assert token not in raw
        (args.output/name).write_text(raw,encoding='utf-8')

    def http(label,path,body=None):
        request=urllib.request.Request(selection['endpoint']+path,
            None if body is None else canonical(body),
            {'Authorization':'Bearer '+token,'Content-Type':'application/json'})
        try:response=urllib.request.urlopen(request,timeout=180)
        except urllib.error.HTTPError as exc:response=exc
        with response:status=response.status;value=json.loads(response.read())
        save(label+'.json',{'path':path,'request':body,'status':status,'result':value})
        return status,value

    env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','PYTHON'))}
    env.update(GIT_CONFIG_NOSYSTEM='1',GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_SYSTEM=os.devnull,
               PYTHONUTF8='1')

    def command(label,argv,cwd):
        result=subprocess.run(list(map(str,argv)),cwd=cwd,env=env,capture_output=True,timeout=180)
        event={'label':label,'argv':list(map(str,argv)),'cwd':str(cwd),'exit':result.returncode,
            'stdout':result.stdout.decode('utf-8','replace'),'stderr':result.stderr.decode('utf-8','replace')}
        events.append(event);save('commands.json',events)
        return event

    def git(label,root,*argv):
        value=command(label,['git','-c','core.autocrlf=false','-c','core.hooksPath='+os.devnull,*argv],root)
        assert value['exit']==0,(label,value['stderr'])
        return value['stdout'].strip()

    def export(label,baseline):
        status,value=http(label,'/v2/projects/'+selection['project_id']+'/exports',{
            'schema':'se-harness-lifecycle-export-request/v2','test_copy':True,
            'project_id':selection['project_id'],'baseline_id':baseline,
            'client':config['client'],'expected_evaluator':config['components']['evaluator']})
        assert status==200,(label,value)
        return value

    def clone(label,value):
        directory=args.output/label;directory.mkdir()
        snapshot=value['snapshot'];bundle=directory/'history.bundle'
        raw=base64.b64decode(snapshot['git_bundle']['content_base64'],validate=True)
        assert hashlib.sha256(raw).hexdigest()==snapshot['git_bundle']['sha256']
        bundle.write_bytes(raw)
        root=directory/'repository'
        git(label+'-clone',directory,'clone','--quiet','--template=',str(bundle),str(root))
        assert git(label+'-head',root,'rev-parse','HEAD')==snapshot['head']
        git(label+'-objects',root,'fsck','--full','--no-reflogs')
        actual={p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in git(label+'-files',root,'ls-files').splitlines()}
        assert actual=={p:x['sha256'] for p,x in snapshot['files'].items()}
        candidates=[]
        for candidate in snapshot['candidates']:
            git(label+'-candidate-object',root,'cat-file','-e',candidate['test_candidate']+'^{commit}')
            records=list(root.rglob(candidate['verification_record']+'.md'))
            assert len(records)==1
            assert tomllib.loads(records[0].read_text(encoding='utf-8').split('+++',2)[1])['commit']==candidate['test_candidate']
            candidates.append(candidate)
        exports.append({'case':label,'head':snapshot['head'],'file_count':len(actual),
            'baseline_id':value['baseline']['baseline_id'],'snapshot_id':snapshot['snapshot_id'],'candidates':candidates,'exact_git_bytes':True})
        return root

    try:
        requests={}
        for path in sorted((args.native_root/'work').rglob('*.json')):
            if path.is_symlink():raise ValueError('Linked native input')
            if path.stat().st_size>4*1024*1024:continue
            try:value=json.loads(path.read_text(encoding='utf-8'))
            except (ValueError,UnicodeError):continue
            if isinstance(value,dict) and value.get('schema')=='se-harness-lifecycle-command/v2' and value.get('mode')=='apply':
                value.setdefault('client',config['client'])
                value['project_id']=selection['project_id']
                key=value['operation_key']
                # Preserve conflicting payloads under one key as distinct inputs.
                requests.setdefault(key,[]).append((path,value))
        accepted=[]
        for number,(key,variants) in enumerate(requests.items()):
            status,observed=http(f'lookup-{number:03d}','/v1/projects/'+selection['project_id']+'/operations/'+urllib.parse.quote(key,safe=''))
            lookup.append({'key':key,'status':status,'outcome':observed.get('outcome')})
            if status!=200:continue
            digest=observed['request_digest']
            matches=[(p,v) for p,v in variants if 'sha256:'+hashlib.sha256(b'se-harness-lifecycle-command/v2\n'+canonical(v)).hexdigest()==digest]
            assert matches,('No retained exact request matches accepted receipt',key)
            path,request=matches[0]
            assert observed['outcome']=='accepted' and request['project_id']==selection['project_id']
            accepted.append((observed['versions']['project']['after'],path,request,observed))
        selected=sorted(accepted)
        if args.limit:
            selected=selected[:args.limit]
        for number,(_,path,request,observed) in enumerate(selected):
            label=f'{number:03d}-{request["action"]["kind"]}'
            root=clone(label,export(label+'-input',observed['provenance']['input_baseline']))
            before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
            action=request['action']
            if action['kind']=='handoff':
                for item in action['files']:
                    target=root/item['path'];assert target.resolve().is_relative_to(root.resolve())
                    raw=base64.b64decode(item['content_base64'],validate=True)
                    assert hashlib.sha256(raw).hexdigest()==item['sha256'] and len(raw)==item['bytes']
                    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
            reference=commands(action);actual=observed['evaluator_output']['commands']
            assert len(reference)==len(actual)
            compared=[]
            for index,((name,argv),native) in enumerate(zip(reference,actual)):
                assert (name,argv)==(native['command'],native['arguments'])
                result=command(label+'-'+str(index),[args.evaluator_python,'-I','-m','se_harness',name,root,*argv,'--json'],args.output)
                assert result['exit']==native['exit']==0,(label,result)
                expected=json.loads(result['stdout'])
                assert semantic_assertions(expected)==semantic_assertions(native['result']),(label,'Semantic mismatch')
                compared.append(semantic_assertions(expected))
            after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and '.git' not in p.parts}
            changed={p for p in after if before.get(p)!=after[p]}
            assert changed=={item['path'] for item in observed['files']}
            result=export(label+'-output',observed['baseline_id'])
            assert all(result['snapshot']['files'][item['path']]['sha256']==item['sha256'] for item in observed['files'])
            cases.append({'case':label,'kind':action['kind'],'operation_key':request['operation_key'],
                'request_file':str(path),'outcome':'passed','file_effects':sorted(changed),'semantic_assertions':compared})
            save('assessment.json',{'state':'running','cases':cases,'exports':exports,'lookup':lookup})
        if args.limit:
            assert cases
            save('assessment.json',{'state':'partial_replay_only','cases':cases,'exports':exports,'lookup':lookup,
                'limits':'Diagnostic limited to the selected first operations. No full qualification or export pass.'})
            print(json.dumps({'accepted_calls':len(cases),'replay':'partial_diagnostic_passed'}))
            return
        # Hosts may use a separate exports/ directory in their bounded run root.
        # Staged input examples are not native exports and cannot satisfy this case.
        saved_exports=[p for p in args.native_root.rglob('manifest.json')
                       if 'inputs' not in p.relative_to(args.native_root).parts]
        count=0
        for path in saved_exports:
            value=json.loads(path.read_text(encoding='utf-8'))
            if value.get('schema')!='se-harness-lifecycle-export/v2':continue
            label='native-export-'+str(count);count+=1
            fresh=export(label,value['baseline']['baseline_id'])
            assert value['snapshot']['snapshot_id']==fresh['snapshot']['snapshot_id']
            for relative,item in fresh['snapshot']['files'].items():
                raw=base64.b64decode(item['content_base64'],validate=True)
                assert (path.parent/'files'/relative).read_bytes()==raw
            assert (path.parent/'history.bundle').read_bytes()==base64.b64decode(fresh['snapshot']['git_bundle']['content_base64'],validate=True)
            root=clone(label,fresh)
            checked=command(label+'-validate',[args.evaluator_python,'-I','-m','se_harness','validate',root,'--json'],args.output)
            assert checked['exit']==0
        assert cases and count>=2,('Missing accepted lifecycle or two native exports',len(cases),count)
        save('assessment.json',{'state':'accepted_calls_and_native_exports_replayed','cases':cases,'exports':exports,'lookup':lookup,
            'limits':'This check alone does not assess native autonomy, all refusal/retry cases, MCP parity or human acceptance.'})
        print(json.dumps({'accepted_calls':len(cases),'native_exports':count,'replay':'passed'}))
    except BaseException as exc:
        save('failure.json',{'type':type(exc).__name__,'message':str(exc),'cases':cases,'exports':exports,'lookup':lookup})
        raise


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('native-root','selection','credentials','evaluator-python','output'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--limit',type=int,help='Diagnostic first-operation limit; never a complete qualification claim')
    run(parser.parse_args())
