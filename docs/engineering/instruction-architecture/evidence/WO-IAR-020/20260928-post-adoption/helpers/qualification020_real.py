"""Native post-adoption observations using the real host profiles."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
WORK=Path(__file__).resolve().parent
sys.path.insert(0,str(WORK/'iar-demo-tools'))
import run_demo
from acceptance_native import Codex,extract_codex,claude_probe,PROBE,snapshot
from qualification020_claude import evaluate
OUT=WORK/'qualification020-adoption'
ROOT=WORK/'se_harness'
MANIFEST=json.loads((WORK/'iar-demo-tools/prepared-demo.json').read_text(encoding='utf-8'))
MANIFEST['host_executables']={'codex':r'C:\Users\mathi\AppData\Local\OpenAI\Codex\bin\faa963e871dd422c\codex.exe','claude':r'C:\Users\mathi\.local\bin\claude.exe'}
# Native helpers normally isolate profiles. Here the exact purpose is read-only
# post-adoption observation under the current user's real profile.
run_demo.child_env=lambda base,host:os.environ.copy()

def save(name,value):
    p=OUT/(name+'.json')
    if p.exists():raise RuntimeError('Inspect existing observation before retry: '+str(p))
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

if sys.argv[1]=='state':
    label=sys.argv[2] if len(sys.argv)>2 else 'readiness-state'
    assert all(c.isalnum() or c=='-' for c in label)
    trace=OUT/('codex-'+label);trace.mkdir(exist_ok=False)
    client=Codex(MANIFEST,trace)
    try:hooks=client.rpc('hooks/list',{'cwds':[str(ROOT)]})
    finally:client.close()
    p=subprocess.run([MANIFEST['host_executables']['claude'],'auth','status','--json'],cwd=OUT,capture_output=True,text=True,encoding='utf-8',timeout=60)
    auth=json.loads(p.stdout)
    result={'codex_hooks':hooks,'claude_auth':{k:auth[k] for k in ['loggedIn','authMethod','apiProvider','subscriptionType'] if k in auth}}
    save(label,result)
    print(json.dumps(result),flush=True)
elif sys.argv[1]=='inventory':
    plan=json.loads((ROOT/'docs/engineering/instruction-architecture/acceptance/plugin-adoption/replacement.json').read_text(encoding='utf-8'))
    review={}
    for host in ['codex','claude']:
        before=json.loads((OUT/(host+'-plugins-before.json')).read_text(encoding='utf-8'))['result']
        after=json.loads((OUT/(host+'-plugins-after.json')).read_text(encoding='utf-8'))['result']
        if host=='codex':before,after=before['installed'],after['installed']
        key='pluginId' if host=='codex' else 'id'
        unrelated=lambda rows:sorted([r for r in rows if r[key]!='verity-plane@se-harness'],key=lambda r:r[key])
        assert unrelated(before)==unrelated(after)
        selected=next(r for r in after if r[key]=='verity-plane@se-harness')
        assert selected['enabled'] and selected['version']=='0.2.0'
        cache=Path.home()/('.codex' if host=='codex' else '.claude')/'plugins/cache/se-harness/verity-plane/0.2.0'
        files={rel:hashlib.sha256((cache/rel).read_bytes()).hexdigest() for rel in plan['hosts'][host]['files']}
        assert all(digest==plan['hosts'][host]['files'][rel]['sha256'] for rel,digest in files.items())
        old=json.loads((OUT/(host+'-marketplaces-before.json')).read_text(encoding='utf-8'))['result']
        new=json.loads((OUT/(host+'-marketplaces-after.json')).read_text(encoding='utf-8'))['result']
        if host=='codex':old,new=old['marketplaces'],new['marketplaces']
        except_target=lambda rows:sorted([r for r in rows if r['name']!='se-harness'],key=lambda r:r['name'])
        assert except_target(old)==except_target(new)
        review[host]={'selected':selected,'cache':str(cache),'files':files,'all_reviewed_bytes_match':True,'unrelated_plugins_and_marketplaces_unchanged':True}
    trace=OUT/'codex-hook-inventory';trace.mkdir(exist_ok=False)
    client=Codex(MANIFEST,trace)
    try:
        review['codex']['native_hooks']=client.rpc('hooks/list',{'cwds':[str(ROOT)]})
    finally:client.close()
    p=subprocess.run([MANIFEST['host_executables']['claude'],'auth','status','--json'],cwd=OUT,capture_output=True,text=True,encoding='utf-8',timeout=60)
    auth=json.loads(p.stdout)
    review['claude']['auth']={k:auth[k] for k in ['loggedIn','authMethod','apiProvider','subscriptionType'] if k in auth}
    save('post-adoption-inventory',review)
    print(json.dumps({'codex_hooks':review['codex']['native_hooks'],'claude_auth':review['claude']['auth'],'all_reviewed_bytes_match':True,'unrelated_plugins_and_marketplaces_unchanged':True}),flush=True)
elif sys.argv[1]=='codex':
    trace=OUT/'codex-native';trace.mkdir(exist_ok=False)
    client=Codex(MANIFEST,trace)
    before=snapshot(ROOT);report={'status':'incomplete','profile':'real','repository':str(ROOT),'cases':[]}
    try:
        thread=None
        for phase in ['startup','compact']:
            thread,events=client.probe(ROOT,phase,thread,prompt=PROBE+'\nReturn only JSON, without a code fence or extra prose.')
            contexts,replies=extract_codex(events)
            result=evaluate(ROOT,contexts,replies)
            report['cases'].append({'phase':phase,**result})
            print(json.dumps({'phase':phase,'passed':result['passed'],'probe':result.get('probe')}),flush=True)
            if not result['passed']:break
        report['unchanged']=snapshot(ROOT)==before
        if len(report['cases'])==2 and all(c['passed'] for c in report['cases']) and report['unchanged']:report['status']='passed'
    except Exception as exc:report['error']=str(exc)
    finally:client.close();save('codex-native-assessment',report)
    print(json.dumps({'status':report['status'],'error':report.get('error')}),flush=True)
elif sys.argv[1] in ['claude-startup','claude-compact','claude-after-compact','claude-startup-opus','claude-compact-opus','claude-after-compact-opus']:
    phase=sys.argv[1]
    suffix='-opus' if phase.endswith('-opus') else ''
    stage=phase.removesuffix(suffix) if suffix else phase
    trace=OUT/phase;trace.mkdir(exist_ok=False)
    session=None;prompt=PROBE+'\nReturn only the JSON object.'
    if stage=='claude-compact':
        session=json.loads((OUT/('claude-startup'+suffix+'-assessment.json')).read_text(encoding='utf-8'))['session_id'];prompt='/compact'
    elif stage=='claude-after-compact':session=json.loads((OUT/('claude-compact'+suffix+'-assessment.json')).read_text(encoding='utf-8'))['session_id']
    before=snapshot(ROOT)
    session,contexts,replies=claude_probe(MANIFEST,ROOT,trace,phase,resume=session,prompt=prompt,model='opus' if suffix else None)
    result={'session_id':session,'unchanged':snapshot(ROOT)==before,'session_model_override':'opus' if suffix else None,'saved_model_setting_changed':False}
    if stage=='claude-compact':
        events=json.loads((trace/(phase+'.events.json')).read_text(encoding='utf-8'))
        callbacks=[e for e in events if e.get('subtype')=='hook_response' and e.get('hook_name')=='SessionStart:compact']
        text=(ROOT/'ENGINEERING_HARNESS.md').read_text(encoding='utf-8');digest=hashlib.sha256(text.encode()).hexdigest()
        full=[]
        for callback in callbacks:
            payload=json.loads(callback['output'])['hookSpecificOutput']['additionalContext']
            full.append(callback.get('exit_code')==0 and payload.endswith(text) and digest in payload and str(ROOT/'ENGINEERING_HARNESS.md') in payload)
        result.update(passed=bool(full) and all(full) and result['unchanged'],native_compact_callbacks=len(callbacks),each_payload_is_full_current_root=full,entry_sha256=digest)
    else:result.update(evaluate(ROOT,contexts,replies));result['passed'] &= result['unchanged']
    save(phase+'-assessment',result)
    print(json.dumps(result),flush=True)
