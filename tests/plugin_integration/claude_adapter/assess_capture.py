"""Independent re-assessment of retained native wire captures, without host calls."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def messages(text):
    result=[]
    for line in text.splitlines():
        try:
            value=json.loads(line)
            if isinstance(value,dict): result.append(value)
        except ValueError:
            pass
    return result


def hooks(row,event=None):
    found=[]
    for message in messages(row['stdout']):
        if message.get('subtype')!='hook_response' or (event and message.get('hook_event')!=event):
            continue
        try:
            output=json.loads(message.get('stdout',''))['hookSpecificOutput']
        except (ValueError,KeyError,TypeError):
            output={}
        records=messages(message.get('stderr',''))
        guard=next((r for r in records if r.get('adapter')=='verity-plane-claude-v1'),{})
        found.append({'id':message.get('hook_id'),'name':message.get('hook_name'),'event':message.get('hook_event'),
                      'outcome':message.get('outcome'),'exit':message.get('exit_code'),'output':output,'guard':guard,
                      'handler':[r for r in records if 'checks' in r]})
    return found


def edit(row):
    wire=messages(row['stdout'])
    uses=[b for m in wire for b in m.get('message',{}).get('content',[]) if isinstance(b,dict) and b.get('type')=='tool_use' and b.get('name')=='Write']
    results=[b for m in wire for b in m.get('message',{}).get('content',[]) if isinstance(b,dict) and b.get('type')=='tool_result' and b.get('tool_use_id') in {u['id'] for u in uses}]
    correlated=[h for h in hooks(row,'PreToolUse') if h['guard'].get('tool_use_id') in {u['id'] for u in uses}]
    prompt=row['argv'][row['argv'].index('-p')+1]
    requested=re.search(r'First use Read once on (.*?) to satisfy.*?content ("(?:\\.|[^"\\])*")\.',prompt)
    exact=bool(requested and uses and all(u.get('input')=={'file_path':requested.group(1),'content':json.loads(requested.group(2))} for u in uses))
    target_key=Path(requested.group(1)).name if requested else None
    expected_sha=hashlib.sha256(json.loads(requested.group(2)).encode('utf8')).hexdigest() if requested else None
    target_changed=(row.get('target_before',{}).get(target_key)!=row.get('target_after',{}).get(target_key))
    expected_effect=bool(expected_sha and target_changed and row.get('target_after',{}).get(target_key)==expected_sha)
    decisions=[]
    for h in correlated:
        reason=h['output'].get('permissionDecisionReason')
        denied=(h['outcome']=='success' and h['exit']==0 and h['output'].get('permissionDecision')=='deny' and isinstance(reason,str) and bool(reason.strip()) and
                any(r.get('tool_use_id')==h['guard']['tool_use_id'] and r.get('is_error') is True and reason in str(r.get('content')) for r in results))
        starts=[x['received_monotonic'] for x in row.get('timeline',[]) if x.get('hook_id')==h['id'] and x.get('subtype')=='hook_started']
        ends=[x['received_monotonic'] for x in row.get('timeline',[]) if x.get('hook_id')==h['id'] and x.get('subtype')=='hook_response']
        result_times=[x['received_monotonic'] for x in row.get('timeline',[]) if any(t.get('tool_use_id')==h['guard']['tool_use_id'] for t in x.get('tools',[]))]
        decisions.append({'tool_use_id':h['guard']['tool_use_id'],'denied':bool(denied),'hook':h,
            'host_elapsed_seconds':ends[0]-starts[0] if starts and ends else None,
            'hook_precedes_tool_result':bool(ends and result_times and ends[0]<=result_times[0])})
    native_hooks=[]
    for hook in hooks(row,'PreToolUse'):
        if hook['name']!='PreToolUse:Write': continue
        start=[t['received_monotonic'] for t in row.get('timeline',[]) if t.get('subtype')=='hook_started' and t.get('hook_id')==hook['id']]
        end=[t['received_monotonic'] for t in row.get('timeline',[]) if t.get('subtype')=='hook_response' and t.get('hook_id')==hook['id']]
        native_hooks.append({'id':hook['id'],'outcome':hook['outcome'],'exit':hook['exit'],'output':hook['output'],
                             'elapsed_seconds':end[0]-start[0] if start and end else None})
    return {'uses':uses,'results':results,'decisions':decisions,'exact_requested_write':exact,
            'native_Write_hooks':native_hooks,'target_key':target_key,'expected_sha256':expected_sha,'expected_target_effect':expected_effect,
            'successful_Write_results':sum(r.get('is_error') is not True for r in results),
            'final_target_hashes_before':row.get('target_before'),'final_target_hashes_after':row.get('target_after')}


def assess(case, *, rows=None, original=None):
    if rows is None:
        rows=json.loads((case/'commands.json').read_text(encoding='utf8'))
    if original is None:
        original=json.loads((case/'observations.json').read_text(encoding='utf8'))
    name=case.name
    found={'source':'native system/hook_response stdout+stderr and correlated tool_use/tool_result objects',
           'qualification':False,'case':name}
    if name=='C03':
        observations=[edit(r) for r in rows]
        yes,no=observations
        passed=(len(yes['uses'])==len(no['uses'])==1 and yes['exact_requested_write'] and no['exact_requested_write'] and yes['successful_Write_results']==1 and yes['expected_target_effect'] and
            any(d['hook_precedes_tool_result'] and any(x.get('status')=='checked' for x in d['hook']['handler']) for d in yes['decisions']) and
            no['successful_Write_results']==0 and no['final_target_hashes_before']==no['final_target_hashes_after'] and
            any(d['denied'] and d['hook_precedes_tool_result'] for d in no['decisions']))
        found.update(observations=observations,conclusion='pass' if passed else 'fail')
    elif name=='C05':
        observations=[hooks(r,'SessionStart') for r in rows]
        passed=not observations[0] and any(h['guard'].get('script_exit')==4 and h['guard'].get('status')=='unready' and h['output'].get('additionalContext','').startswith('UNREADY:') for h in observations[1])
        found.update(observations=observations,conclusion='pass' if passed else 'fail')
    elif name=='C06':
        observations=hooks(rows[-1],'PreToolUse')
        passed=any(h['guard'].get('tool_name')=='Read' and h['guard'].get('interpreter_invoked') is False and
                   h['output'].get('additionalContext','').startswith('UNREADY COVERAGE GAP:') and 'permissionDecision' not in h['output'] for h in observations)
        found.update(observations=observations,conclusion='pass' if passed else 'unavailable')
    elif name=='C08':
        observations=[hooks(r,'SessionStart') for r in rows]
        missing=lambda hs:any(h['guard'].get('interpreter_invoked') is False and 'SETUP REQUIRED' in h['output'].get('additionalContext','') for h in hs)
        wrong=any(h['guard'].get('interpreter_invoked') is True and any('released evaluator identity refused' in x.get('error','') for x in h['handler']) for h in observations[1])
        ready=any(any(x.get('status')=='complete-output-prepared' for x in h['handler']) for h in observations[2])
        found.update(observations=observations,correction='Wrong identity is an identity refusal, not setup-required. Earlier debug-substring flags are superseded by these actual hook outputs.',conclusion='pass' if len(observations)==4 and missing(observations[0]) and wrong and ready and missing(observations[3]) else 'fail')
    elif name in ('C09','C10','C11','C12'):
        observations=[edit(r) for r in rows]
        if name=='C09':
            faults=original['observed']['faults']
            cleanup=[]
            for observation,fault in zip(observations,faults):
                records=[h for d in observation['decisions'] for h in d['hook']['handler']]
                replaced=[(h,c) for h in records for c in h.get('checks',[]) if c.get('fault_replaced_argv')]
                clean=bool(replaced) and all(c.get('cleanup',{}).get('active_processes')==0 and
                    c.get('cleanup_started_monotonic',float('inf'))<=c.get('cleanup_finished_monotonic',-1)<=h.get('response_written_monotonic',-1)
                    for h,c in replaced)
                mode=fault['mode']
                fault_verified=any(('deadline' in c.get('error','').lower() if mode=='stalled' else c.get('exit_status')=={'failed':3,'interrupted':15}[mode]) for _,c in replaced)
                outer=bool(fault['child_pids']) and set(fault['child_pids'])==set(fault['children_alive']) and all(v is False for v in fault['children_alive'].values())
                cleanup.append({'mode':mode,'inner_fault_verified':fault_verified,'cleanup_before_shared_response':clean,'outer_children_stopped':outer,
                    'parent_child_pids':fault['child_pids'],'fault_checks':[{k:v for k,v in c.items() if k not in ('argv','result','stderr','fault_replaced_argv')} for _,c in replaced]})
            passed=len(observations)==len(cleanup)==3 and all(len(o['uses'])==1 and o['exact_requested_write'] and o['successful_Write_results']==0 and o['final_target_hashes_before']==o['final_target_hashes_after'] and
                any(d['denied'] and d['hook_precedes_tool_result'] and d['host_elapsed_seconds'] is not None and d['host_elapsed_seconds']<60 and
                    any(x.get('checks') for x in d['hook']['handler']) for d in o['decisions']) for o in observations) and all(c['inner_fault_verified'] and c['cleanup_before_shared_response'] and c['outer_children_stopped'] for c in cleanup)
            found['cleanup']=cleanup
            conclusion='pass' if passed else 'fail'
        elif name in ('C10','C11'):
            conclusion='fail' if any(o['exact_requested_write'] and o['uses'] and not any(d['denied'] for d in o['decisions']) for o in observations) else 'unavailable'
        else:
            started=all(any(x.get('subtype')=='hook_started' and x.get('hook_name')=='PreToolUse:Write' for x in r.get('timeline',[])) for r in rows)
            bindings=original['observed']['bindings']
            rejected=all(b['eligible_for_live_assessment'] is False and b['qualified'] is False for b in bindings)
            loaded=[]
            for binding in bindings:
                data=json.loads((case/(binding['loaded_field']+'-loaded-hooks.json')).read_text(encoding='utf8'))
                hook=data['hooks']['PreToolUse'][0]['hooks'][0]
                loaded.append(hook.get(binding['loaded_field'])==binding['loaded_value'])
            found['loaded_mutation_and_static_rejection']=bool(rejected and all(loaded))
            conclusion='pass' if started and len(bindings)==len(observations)==2 and all(loaded) and rejected and all(len(o['uses'])==1 and o['exact_requested_write'] for o in observations) else 'unavailable'
        found.update(observations=observations,conclusion=conclusion)
    else:
        found.update(conclusion='not-reassessed',note='Use independent case-specific context/protocol assessment.')
    return found


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('case',type=Path)
    args=parser.parse_args()
    print(json.dumps(assess(args.case),ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
