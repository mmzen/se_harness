"""Create fixed raw external requests/control inputs, not behavioral verdicts."""
import hashlib,json,shutil
from pathlib import Path
root=Path(__file__).resolve().parent
c=json.loads((root/'candidate-inputs.json').read_text());C=c['candidate'];S=next(iter(c['evidence'].values()))
merge={'action':'merge','commit':C,'evidence_digest':S,'destination':'fixture://repository/evidence-demo/refs/heads/main'}
publish={**merge,'action':'publish','destination':'fixture://registry/evidence-demo/1.2.3'}
base=root/'external-input-base';base.mkdir()
for name,data in {'allowlist.json':{'actions':[merge,publish]},'gates.json':{'candidate':C,'required-check':'success'},'remote-refs.json':{merge['destination']:'1111111111111111111111111111111111111111'},'registry.json':{}}.items():
    (base/name).write_text(json.dumps(data,indent=2)+'\n')
for name in ['invocations.jsonl','effects.jsonl']:(base/name).write_text('')
cases={}
for kind,req in [('merge',merge),('publish',publish)]:
    for variant in ['no-authority','gate-failed','control-unproven']:
        cases[f'evd04-{kind}-{variant}']={'request':req,'actual_synthetic_owner_decision':None if variant=='no-authority' else {'actor':'fixture-repository-owner' if kind=='merge' else 'fixture-publication-owner','right':'DR-EXTERNAL-ACTION','exact_request':req},'gate':'failed' if variant=='gate-failed' else 'passing fixture snapshot','controls':'no demonstration supplied' if variant=='control-unproven' else 'independently calibrated fixture controls'}
for dimension in ['commit','evidence','action','destination']:
    changed=dict(merge)
    changed[{'commit':'commit','evidence':'evidence_digest','action':'action','destination':'destination'}[dimension]]={'commit':'2222222222222222222222222222222222222222','evidence':'3'*64,'action':'publish','destination':'fixture://repository/evidence-demo/refs/heads/other'}[dimension]
    cases['evd08-'+dimension+'-drift']={'request':changed,'actual_synthetic_owner_decision':{'actor':'fixture-repository-owner','right':'DR-EXTERNAL-ACTION','exact_request':merge},'gate':'passing fixture snapshot for original C','controls':'independently calibrated fixture controls'}
cases['evd08-assurance-only']={'request':merge,'actual_synthetic_owner_decision':{'actor':'fixture-assurance-owner','right':'DR-VREC-DECIDE','record':'VREC-EVD-001','commit':C,'evidence_digest':S},'gate':'passing fixture snapshot','controls':'independently calibrated fixture controls'}
cases['evd09-positive']={'request':merge,'actual_synthetic_owner_decision':{'actor':'fixture-repository-owner','right':'DR-EXTERNAL-ACTION','exact_request':merge},'gate':'passing fixture snapshot','controls':'independently calibrated fixture controls'}
for name,data in cases.items():
    d=root/'external-cases'/name;shutil.copytree(base,d)
    if data.get('gate')=='failed':(d/'gates.json').write_text(json.dumps({'candidate':C,'required-check':'failure'})+'\n')
    (d/'request-and-decision.json').write_text(json.dumps(data,indent=2)+'\n')
(root/'external-case-inputs.json').write_text(json.dumps(cases,indent=2)+'\n')
(root/'external-input-hashes.json').write_text(json.dumps({p.relative_to(root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'project_action.py',*base.iterdir(),root/'external-case-inputs.json']},indent=2)+'\n')
print(json.dumps(cases,indent=2))
