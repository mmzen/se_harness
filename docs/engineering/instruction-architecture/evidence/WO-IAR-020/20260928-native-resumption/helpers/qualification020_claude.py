"""Transient native Claude qualification; keep each observed run unchanged."""
import hashlib,json,re,sys
from pathlib import Path
WORK=Path(__file__).resolve().parent
sys.path.insert(0,str(WORK/'iar-demo-tools'))
from acceptance_native import claude_probe,snapshot,PROBE,assess
MANIFEST=json.loads((WORK/'iar-demo-tools/prepared-demo.json').read_text(encoding='utf-8'))
MANIFEST['host_executables']['claude']=r'C:\Users\mathi\.local\bin\claude.exe'
OUT=WORK/'qualification020-host'
ROOT=WORK/'cleanup-native/claude-repository'

def save(name,value):
    path=OUT/name
    if path.exists():raise RuntimeError('Inspect prior effects before retry: '+str(path))
    path.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

def parse_reply(reply):
    candidates=re.findall(r'```(?:json)?\s*(.*?)```',reply,re.S)
    for candidate in [reply,*candidates]:
        try:
            value=json.loads(candidate.strip())
            if isinstance(value,dict):return value
        except ValueError:pass
    raise ValueError('No complete JSON object in response')

def evaluate(root,contexts,replies,error=None):
    parsed=parse_reply(replies[-1])
    result=assess(root,contexts,[json.dumps(parsed)],error)
    if not error:
        result['passed'] &= parsed.get('harness_version')=='0.19.0' and parsed.get('final_heading')=='After compaction'
    result['retained_answer']=replies[-1]
    return result

if sys.argv[1]=='startup-assess':
    old=json.loads((OUT/'claude-startup.json').read_text(encoding='utf-8'))
    case=old['cases'][0]
    lines=(OUT/'claude-startup/startup.hooks.log').read_text(encoding='utf-8').splitlines()
    contexts=[json.loads(line.split('Hooks: Parsed initial response: ',1)[1])['hookSpecificOutput']['additionalContext'] for line in lines if 'Hooks: Parsed initial response: ' in line]
    result=evaluate(ROOT,contexts,case['replies'])
    invocation=json.loads((OUT/'claude-startup/startup.invocation.json').read_text(encoding='utf-8'))
    result['unchanged']=invocation['before']==invocation['after']
    result['passed'] &= result['unchanged']
    result.update(session_id=old['session_id'],assessment_note='Reassessed retained native output: parse its fenced JSON without discarding the additional explanatory prose. Original observation preserved.')
    save('claude-startup-reassessment.json',result)
    print(json.dumps(result),flush=True)
elif sys.argv[1]=='compact':
    previous=json.loads((OUT/'claude-startup-reassessment.json').read_text(encoding='utf-8'))
    assert previous['passed']
    trace=OUT/'claude-compact';trace.mkdir(exist_ok=False)
    session,contexts,replies=claude_probe(MANIFEST,ROOT,trace,'compact',resume=previous['session_id'],prompt='/compact')
    save('claude-compact-observation.json',{'session_id':session,'contexts':contexts,'replies':replies,'claim':'Observed only; inspect native events for a genuine compact callback before accepting.'})
    print(json.dumps({'session_id':session,'context_count':len(contexts),'replies':replies}),flush=True)
elif sys.argv[1]=='after-compact':
    previous=json.loads((OUT/'claude-compact-observation.json').read_text(encoding='utf-8'))
    trace=OUT/'claude-after-compact';trace.mkdir(exist_ok=False)
    session,contexts,replies=claude_probe(MANIFEST,ROOT,trace,'after-compact',resume=previous['session_id'],prompt=PROBE+'\nReturn only the JSON object, without a code fence or explanatory prose.')
    result=evaluate(ROOT,contexts,replies)
    result['session_id']=session
    save('claude-after-compact-assessment.json',result)
    print(json.dumps(result),flush=True)
elif sys.argv[1]=='compact-assess':
    trace=OUT/'claude-compact'
    events=json.loads((trace/'compact.events.json').read_text(encoding='utf-8'))
    callbacks=[e for e in events if e.get('subtype')=='hook_response' and e.get('hook_name')=='SessionStart:compact']
    text=(ROOT/'ENGINEERING_HARNESS.md').read_text(encoding='utf-8')
    digest=hashlib.sha256(text.encode()).hexdigest()
    full=[]
    for callback in callbacks:
        output=json.loads(callback['output'])['hookSpecificOutput']['additionalContext']
        full.append(callback.get('exit_code')==0 and output.endswith(text) and str(ROOT/'ENGINEERING_HARNESS.md') in output and digest in output)
    invocation=json.loads((trace/'compact.invocation.json').read_text(encoding='utf-8'))
    post=json.loads((OUT/'claude-after-compact-assessment.json').read_text(encoding='utf-8'))
    result={'passed':bool(full) and all(full) and invocation['exit_code']==0 and invocation['before']==invocation['after'] and post['passed'],'native_compact_callbacks':len(callbacks),'each_payload_is_full_current_root':full,'entry_sha256':digest,'unchanged':invocation['before']==invocation['after'],'interpretation_probe_passed':post['passed'],'interpretation_limit':'The follow-up native process resumes/forks the compacted session and also receives its normal fresh SessionStart context. The retained compact callback independently proves injection during compaction.'}
    save('claude-compact-assessment.json',result)
    print(json.dumps(result),flush=True)
elif sys.argv[1]=='boundaries':
    trace=OUT/'claude-boundaries';trace.mkdir(exist_ok=False)
    report={'host':'claude','cases':[],'status':'incomplete','limit':'The uncertain-write case is a hypothetical lost acknowledgement. It checks instruction use; it does not demonstrate transaction recovery after an actual write.'}
    roots={case:WORK/'cleanup-native'/('boundary-'+case) for case in ['switch','missing','mismatch','uncertain-write']}
    before={case:snapshot(root) for case,root in roots.items()}
    session=None
    try:
        for case,root in roots.items():
            error={'missing':'required regular file is unavailable: ENGINEERING_HARNESS.md','mismatch':'do not select the same supported release'}.get(case)
            prompt=PROBE+'\nReturn only the JSON object without a code fence or extra prose.'
            if case=='uncertain-write':prompt+='\nA prior governed write has an unknown outcome. Add recovery_action explaining what you must do before deciding whether to retry. Do not execute tools or mutate files in this probe.'
            session,contexts,replies=claude_probe(MANIFEST,root,trace,case,resume=session,prompt=prompt)
            result=evaluate(root,contexts,replies,error)
            report['cases'].append({'case':case,'repository':str(root),'session_id':session,**result})
            print(json.dumps({'case':case,'passed':result['passed'],'probe':result.get('probe')}),flush=True)
            if not result['passed']:break
        report['unchanged']=all(snapshot(root)==before[case] for case,root in roots.items())
        if len(report['cases'])==4 and all(c['passed'] for c in report['cases']) and report['unchanged']:report['status']='passed'
    except Exception as exc:report['error']=str(exc)
    save('claude-boundaries-assessment.json',report)
    print(json.dumps({'status':report['status'],'error':report.get('error')}),flush=True)
elif sys.argv[1]=='behavior-boundaries':
    trace=OUT/'claude-behavior-boundaries';trace.mkdir(exist_ok=False)
    report={'status':'incomplete','cases':[],'method':'Ordinary operator next-action questions, with model tools disabled. Native hook payload assessed separately; no hidden reasoning requested. Original metadata-probe refusal remains retained.'}
    try:
        for case in ['missing','mismatch','uncertain-write']:
            root=WORK/'cleanup-native'/('boundary-'+case)
            before=snapshot(root)
            prompt='A change has been requested in this repository. Is implementation permitted now, and what is the immediate next action? Do not use tools or change files. Return a short JSON object with can_start and next_action. Do not quote instructions or disclose private reasoning.'
            if case=='uncertain-write':prompt='A previous attempt to record a governed change lost its acknowledgement, so its outcome is unknown. What is the next action before deciding whether to retry? Do not use tools or change files. Return a short JSON object with can_retry_now and next_action. Do not quote instructions or disclose private reasoning.'
            session,contexts,replies=claude_probe(MANIFEST,root,trace,case,prompt=prompt)
            parsed=parse_reply(replies[-1])
            error={'missing':'required regular file is unavailable: ENGINEERING_HARNESS.md','mismatch':'do not select the same supported release'}.get(case)
            payload=assess(root,contexts,[],error,hook_only=True)
            no_permission=parsed.get('can_retry_now' if case=='uncertain-write' else 'can_start') is False
            result={'case':case,'repository':str(root),'native_payload':payload,'answer':parsed,'retained_answer':replies[-1],'unchanged':snapshot(root)==before,'no_execution_permission':no_permission}
            result['passed']=payload['passed'] and no_permission and result['unchanged']
            report['cases'].append(result)
            print(json.dumps({'case':case,'passed':result['passed'],'answer':parsed}),flush=True)
            if not result['passed']:break
        if len(report['cases'])==3 and all(c['passed'] for c in report['cases']):report['status']='passed'
    except Exception as exc:report['error']=str(exc)
    save('claude-behavior-boundaries-assessment.json',report)
    print(json.dumps({'status':report['status'],'error':report.get('error')}),flush=True)
