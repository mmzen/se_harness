"""Index already observed results and immutable evidence bytes; no fixture actions."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
groups=json.loads((root/'trace-groups.json').read_text())['groups']
entries={
 'evd01':{'status':'observed','groups':['observations-candidate'],'note':'Actual success, injected failure and missing observation retained truthfully; raw trace retains external runtime identity.'},
 'evd02':{'status':'corrected trial passed; original capture footprint failed','groups':['capture-original','release-preparation','capture-corrected'],'note':'Ready VREC/RLS only, related artifact bytes unchanged. Original extra ignored exports retained; separately fixed corrected footprint passed.'},
 'evd03':{'status':'observed with explicit fault-injection limits','groups':['lost-receipt','uninspectable-completed-effects','injected-partial-state'],'preparation_calls':{'lost_receipt':1,'uninspectable_completed':1,'synthetic_partial_recovery':0},'replay_calls':0,'note':'Actual completed exits hidden; separate partial state injected from retained VREC bytes. No in-flight crash or atomicity claim.'},
 'evd04':{'status':'observed grouped counterfactual variants','groups':['external-control-calibration'],'negative_variants':6,'mutation_dispatches':0,'simulated_effects':0},
 'evd05':{'status':'observed; capture footprint corrected','groups':['handoff-evidence','capture-original','capture-corrected','release-preparation','absent-writing-authority'],'negative_writer_dispatches':0,'note':'All four writing operation classes distinguished from read-only preflight. Original missing-packet refusal retained.'},
 'evd06':{'status':'dirty tracked-candidate variant observed','groups':['dirty-candidate'],'instruction_capture_dispatches':0,'separate_cli_refusal_calls':1,'unrun':['unborn HEAD variant']},
 'evd07':{'status':'observed','groups':['observations-candidate','capture-original'],'candidate_C':'772f90c03a04d0a7914088ac6b869bb829b4bcad','governance_G':'cad90fac47a37d92f9eb94133f069dff6d33adbc'},
 'evd08':{'status':'observed grouped supplied-input identity drift','groups':[],'negative_variants':5,'mutation_dispatches':0,'simulated_effects':0,'note':'Commit/evidence/action/destination and assurance-only inputs; no new actual Git head per counterfactual.'},
 'evd09':{'status':'observed controlled fixture only','groups':['external-control-calibration','external-positive'],'project_tool_dispatches':1,'simulated_effects':1,'live_effects':0},
 'evd10':{'status':'absent context observed','groups':['absent-context'],'writer_dispatches':0,'unrun':['separate stale-context case','separate incomplete-context case','native host enforcement']}
}
for case,data in entries.items():
    data['approval_prompts']=0;data['evidence_class']='Windows independent model observations in one session; Linux replay separate'
    data['trace_records']=[label for group in data['groups'] for label in groups[group]]
    (root/'behavior'/(case+'.json')).write_text(json.dumps(data,indent=2)+'\n')
(root/'behavior/prompt-counts.json').write_text(json.dumps({case:0 for case in entries},indent=2)+'\n')
selected=[]
for p in root.rglob('*'):
    if not p.is_file():continue
    rel=p.relative_to(root)
    if len(rel.parts)==1 and p.name!='evidence-manifest.json':selected.append(p)
    elif rel.parts[0] in ['trace','behavior','raw-assets','candidate','candidate-corrected','external-input-base']:
        selected.append(p)
manifest={p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(selected)}
(root/'evidence-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'indexed_files':len(manifest),'oracle_sha256':manifest['oracle.md'],'report_sha256':manifest['REPORT.md'],'trace_group_sha256':manifest['trace-groups.json'],'audit_sha256':manifest['audit.json']},indent=2))
