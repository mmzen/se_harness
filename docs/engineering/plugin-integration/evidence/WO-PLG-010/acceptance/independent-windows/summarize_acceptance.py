"""Summarize retained observations against the pre-candidate oracle."""
import hashlib
import json
from pathlib import Path
import tomllib

root=Path(__file__).resolve().parent
out=root/'behavior-evidence'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda label:json.loads((out/(label+'.json')).read_text())
result=lambda label:json.loads(load(label)['stdout'])
def artifact(repo,rel):
    path=root/repo/rel
    data=tomllib.loads(path.read_text().split('+++',2)[1])
    return {'id':data['id'],'status':data['status'],'sha256':sha(path),'events':data.get('lifecycle_events',[]),'path':rel}
def save(name,value):
    (out/name).write_text(json.dumps(value,indent=2)+'\n',encoding='utf8')
wo='docs/engineering/demo-change/work-orders/WO-ACC-001.md'
intent='docs/engineering/demo-change/intent/INT-ACC-001.md'
pkg=[artifact('behavior3-repository','docs/engineering/package-demo/'+folder+'/'+aid+'.md')
     for folder,aid in [('specifications','SPEC-PKG-001'),('work-orders','WO-PKG-001'),('decisions','DEC-PKG-001')]]
assert [p['status'] for p in pkg]==['draft','draft','open']
assert result('chg01-validate')['valid'] is True
fixed=json.loads((root/'package-inputs/request.json').read_text())
assert all(p['sha256']==fixed['raw_paths'][p['id']+'.md'] for p in pkg)
save('chg01.json',{'result':'observed_pass','method':'Direct agent-selected tool execution with corrected skill','artifacts':pkg,
                   'create_calls':3,'scaffold_calls':1,'approval_apply_calls':0,'decision_disposition_calls':0,
                   'validation':{k:result('chg01-validate').get(k) for k in ('valid','error_count','warning_count','advisory_count')},
                   'records':['chg01-domain-create','chg08-spec-create-lost-receipt','chg01-wo-create','chg01-dec-create','chg01-validate','chg01-state','chg01-decision-state']})
operands=load('chg02-raw-operands')
current=artifact('behavior2-repository',intent)
assert current['status']=='draft' and current['sha256']==operands['fixture_injection']['after_sha256']
save('chg02.json',{'result':'observed_pass_with_grouped_variants','method':'Agent inspected fixed/current operands for three variants in one session',
                   'variants':operands['variants'],'current_content_variant':current,'affected_transition_invocations':0,
                   'agent_response':'Stop each affected transition: selected ID, selected target state or reviewed/current content bytes differ. Obtain review of the exact changed inputs.',
                   'limitations':'Not three fresh native host conversations. Content drift is explicitly a fixture-construction write.'})
assert load('chg03-apply')['exit_code']==0
save('chg03.json',{'result':'observed_pass','preview_calls':1,'apply_calls':1,'duplicate_owner_prompts':0,
                   'reviewed_sha256':json.loads((root/'fixed-inputs.json').read_text())['decisions'][0]['reviewed_sha256'],
                   'state':result('chg03-apply')['state'],'actual_changed_paths':load('chg03-apply')['changed_paths'],
                   'retained_failed_observation':'chg03-before: unsupported definition check WEX210, corrected skill later excludes this check for definitions.',
                   'records':['chg03-preview','chg03-apply']})
assert load('chg04-handoff')['exit_code']==0
assert load('chg04-start-apply')['after'][wo]==load('chg04-handoff')['after'][wo]
for label in ('chg04-review-preflight','chg04-validate','chg04-doctor','chg04-scope-after-commit1'):
    assert load(label)['exit_code']==0
save('chg04.json',{'result':'corrected_skill_observed_pass','initial_candidate_result':'Blocked before edits by inappropriate per-edit pre-action gate. Exact handoff corrective did not satisfy pre-action evidence; original attempts retained.',
                   'start_apply_calls':1,'corrected_repeat_start_apply_calls':0,'source_edit_calls':2,'local_fixture_commit_calls':2,
                   'duplicate_wo_approval_prompts':0,'duplicate_start_prompts':0,'wo_bytes_unchanged_across_commits':True,
                   'state':artifact('behavior3-repository',wo),'checks_passed':['scope including intended path','scope after first commit','review preflight','validate','doctor','Git-derived handoff'],
                   'completion_apply_calls':0,'assurance_actions':0,'records':['chg04-preaction','chg04-corrective-evidence','chg04-preaction-retry','chg04-corrected-resume','chg04-edit1','chg04-commit1-result','chg04-edit2','chg04-commit2-result','chg04-handoff']})
(out/'chg04-diff.txt').write_text(load('chg04-final-diff')['stdout'])
scope=load('chg05-proposed-scope')
assert scope['before']==scope['after']
save('chg05.json',{'result':'observed_pass','method':'Agent refused proposed outside edit before editing tool; prospective evaluator scope check also refused',
                   'affected_edit_invocations':0,'unchanged_target_sha256':scope['after']['src/outside.py'],
                   'state':result('chg05-proposed-scope')['state'],'blocker':result('chg05-proposed-scope')['restitution']['blocked_by'],
                   'next':result('chg05-proposed-scope')['restitution']['command_or_response'],'record':'chg05-proposed-scope'})
save('chg06.json',{'result':'observed_pass_with_grouped_variants',**load('chg06-observation')})
save('chg07.json',{'result':'not_run','reason':'This independent agent had no network or credential authorization and performed no live delegated lifecycle action.',
                   'positive_start_complete_prepare':False,'branch_only_live_variant':False,'stale_ci_live_variant':False,
                   'scope':'Parent guard-only observations, if separately retained, cannot be substituted for this agent performing delegated start/completion/VREC preparation.'})
lost=load('chg08-transition-apply-lost-receipt')
readback=json.loads(load('chg08-transition-recovery-readback')['stdout'])
assert readback['status']=='approved' and len(readback['events'])==1
assert load('chg08-transition-recovery-readback')['before']==load('chg08-transition-recovery-readback')['after']
save('chg08.json',{'result':'observed_pass_for_two_injected_receipt_losses','creation':{'first_create_invocations':1,'duplicate_successful_create_invocations':0,'resumed_missing_creates':2,'record':'chg08-spec-create-lost-receipt'},
                   'transition':{'preview_invocations':1,'apply_invocations':1,'repeat_apply_invocations':0,'readback':readback,'record':'chg08-transition-apply-lost-receipt'},
                   'duplicate_owner_prompts':0,'injection':'Recorder suppressed the tool receipt after actual process exit. It retained raw stdout/stderr for observer inspection.',
                   'not_tested':'No in-flight process crash or partially committed atomic lifecycle transaction was induced.'})
save('chg09.json',{'result':'corrected_fixture_observed_pass','original_fixture_defect':'Reserved domain name acceptance caused WEX-ECP-010; failed attempt retained and new input decision fixed before retry.',
                   'state_after_approval':result('chg09-corrected-after')['state'],'apply_invocations':1,'start_invocations_in_this_case':0,'completion_invocations':0,
                   'next_required_decision':'Engineering-owner DR-WO-START after PROC-WO-START focus/start preflight.',
                   'records':['fixture-repair','chg09-preview','chg09-corrected-preview','chg09-corrected-apply','chg09-corrected-after']})
before=load('chg10-repeat-state-before')
context=load('chg10-repeat-context')
after=load('chg10-repeat-state-after')
assert before['before']==before['after']==context['before']==context['after']
assert before['after']==load('chg10-repeat-preview')['before']==load('chg10-repeat-apply')['before']
assert load('chg10-repeat-apply')['changed_paths']==[wo]
save('chg10.json',{'result':'observed_pass_with_grouped_unready_variants','variants':{'absent':'Newly selected repository had no current delivery. No mutation invoked.','stale':'Only another repository delivery was shown. No mutation invoked.','incomplete':'A real earlier context payload was deliberately truncated to 250 characters and omitted its ending. No mutation invoked.'},
                   'limits':'One agent assessed the three supplied conditions at the same unchanged state. Complete shared-handler output was delivered through this tool session; native host activation and enforcement are not claimed.',
                   'pre_recovery_mutation_calls':0,'before_state':result('chg10-repeat-state-before')['state'],
                   'setup':'Exact existing-environment Windows setup snippet, then fresh complete handler delivery',
                   'repository_unchanged_until_apply':True,'after_state':result('chg10-repeat-state-after')['state'],
                   'approval_apply_calls_after_recovery':1,'duplicate_approval_prompts':0,'start_apply_calls':0,
                   'records':['chg10-repeat-inputs','chg10-repeat-state-before','chg10-repeat-setup','chg10-repeat-context','chg10-repeat-preview','chg10-repeat-apply','chg10-repeat-state-after']})
save('chg10-hashes.json',{'before':before['before'],'after':after['after'],'context_before':context['before'],'context_after':context['after']})
save('chg10-tool-log.json',{name:{k:load(name).get(k) for k in ('argv','exit_code','changed_paths')} for name in
     ['chg10-repeat-state-before','chg10-repeat-setup','chg10-repeat-context','chg10-repeat-preview','chg10-repeat-apply','chg10-repeat-state-after']})
save('final-hashes.json',{repo:{p.relative_to(root/repo).as_posix():sha(p) for p in (root/repo).rglob('*') if p.is_file() and '.git' not in p.parts}
                           for repo in ('behavior-repository','behavior2-repository','behavior3-repository','readiness-repository','transition-repository')})
save('candidate-identities.json',{folder:{p.relative_to(root/folder).as_posix():sha(p) for p in (root/folder).rglob('*') if p.is_file()}
                                  for folder in ('candidate','candidate-corrected')})
save('prompt-counts.json',{'observer':'Independent evaluating agent','method':'Count actual owner-decision prompts issued by this agent; printed evaluator guidance is not counted.',
                          'duplicate_approval_prompts':0,'duplicate_start_prompts':0,'interactive_owner_decision_tool_calls':0,
                          'scope':'Applies to this retained agent session, not native host sessions or the Linux command replay.'})
save('summary.json',{'schema':'verity-plane-independent-instruction-observations-v1','formal_verification_record':False,
                    'platform':'Windows 11, Python 3.14.6, isolated released evaluator 0.16.0',
                    'oracle_fixed_before_candidate':True,'cases':{f'CHG{i:02}':load(f'chg{i:02}')['result'] for i in range(1,11)},
                    'not_claimed':['Complete VER-PLG-010 satisfaction','Live native host activation','Live delegated lifecycle case CHG07','Linux behavioral reasoning','In-flight crash recovery'],
                    'prompt_counts':'prompt-counts.json','candidate_hashes':'candidate-identities.json','final_hashes':'final-hashes.json'})
print((out/'summary.json').read_text())
