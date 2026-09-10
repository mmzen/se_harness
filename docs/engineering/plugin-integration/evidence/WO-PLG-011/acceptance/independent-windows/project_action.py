"""Fixture-only project tool with independent fixed external-action controls.

No harness policy or authority decisions live here. Inputs are a separate
immutable allowlist and fixture gate snapshot. Effects are JSON simulation only.
"""
import argparse,json,sys
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--control-dir',type=Path,required=True)
ap.add_argument('--action',required=True);ap.add_argument('--commit',required=True)
ap.add_argument('--evidence-digest',required=True);ap.add_argument('--destination',required=True)
ns=ap.parse_args();root=ns.control_dir
request={'action':ns.action,'commit':ns.commit,'evidence_digest':ns.evidence_digest,'destination':ns.destination}
log=root/'invocations.jsonl'
with log.open('a',encoding='utf8') as f:f.write(json.dumps({'argv':sys.argv,'request':request})+'\n')
allowed=json.loads((root/'allowlist.json').read_text())
gate=json.loads((root/'gates.json').read_text())
if request not in allowed['actions']:
    print(json.dumps({'simulation_only':True,'outcome':'blocked','reason':'Exact request is outside the independent fixture control allowlist.'}));raise SystemExit(17)
if gate!={'candidate':ns.commit,'required-check':'success'}:
    print(json.dumps({'simulation_only':True,'outcome':'blocked','reason':'Independent fixture gate snapshot does not pass for candidate.'}));raise SystemExit(18)
statepath=root/('remote-refs.json' if ns.action=='merge' else 'registry.json')
state=json.loads(statepath.read_text());state[ns.destination]=ns.commit
statepath.write_text(json.dumps(state,indent=2)+'\n')
with (root/'effects.jsonl').open('a',encoding='utf8') as f:f.write(json.dumps({'simulation_only':True,'statefile':statepath.name,'request':request})+'\n')
print(json.dumps({'simulation_only':True,'outcome':'applied','request':request,'statefile':statepath.name}))
