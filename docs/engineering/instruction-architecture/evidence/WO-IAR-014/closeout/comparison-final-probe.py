"""Transient acceptance probe; all mutations below target disposable test inputs."""
import json,sys,subprocess,os,hashlib,shutil,datetime
from pathlib import Path
from evolution_cli import REPO,ROOT,PY

OUT=ROOT/'work/iar-lifecycle-comparison-v2'
OUT.mkdir(exist_ok=True)
candidate=json.loads((ROOT/'work/ci19-package.json').read_text())
CPY=Path(candidate['python'])
git=['git','-c','safe.directory='+REPO.as_posix(),'-C',str(REPO)]
assert not subprocess.check_output(git+['diff','--name-only',candidate['package_source_commit'],'HEAD','--','se_harness','templates','pyproject.toml','MANIFEST.in'])
assert hashlib.sha256(Path(candidate['wheel']).read_bytes()).hexdigest()==candidate['sha256']
env=os.environ.copy();env['PYTHONIOENCODING']='utf-8'
def invoke(label,py,args):
 p=subprocess.run([str(py),'-I','-B','-m','se_harness',*args],cwd=ROOT,env=env,capture_output=True)
 (OUT/(label+'.stdout')).write_bytes(p.stdout);(OUT/(label+'.stderr')).write_bytes(p.stderr)
 (OUT/(label+'.invocation.json')).write_text(json.dumps({'argv':[str(py),'-I','-B','-m','se_harness',*args],'cwd':str(ROOT),'exit_code':p.returncode,'time':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n',encoding='utf-8')
 try:r=json.loads(p.stdout)
 except ValueError:r={'raw':p.stdout.decode(errors='replace')}
 return p.returncode,r
sys.path.insert(0,str(REPO))
from tests.artifact_support import create_base_chain,record_execution_approval
fixtures=OUT/'formal-inputs'
assert not fixtures.exists(),'Inspect earlier effects before rerunning'
create_base_chain(fixtures,work_order_status='draft',operating_contract_status='draft')
# The shared legacy fixture ID is not eligible for released start preflight.
# Rename only synthetic inputs; preserve the initial refusal observation.
for fp in list(fixtures.rglob('*')):
 if fp.is_file():
  fp.write_text(fp.read_text(encoding='utf-8').replace('WO-001','WO-CMP-001'),encoding='utf-8')
  if 'WO-001' in fp.name: fp.rename(fp.with_name(fp.name.replace('WO-001','WO-CMP-001')))
wo=fixtures/'docs/engineering/product/work-orders/WO-CMP-001.md'
text=wo.read_text(encoding='utf-8').replace('[relations]','[assurance]\ncommit_bound_verification = "required"\nrationale = "Synthetic comparison fixture."\ndecided_by = "test-owner"\n\n[execution_scope]\npaths = ["src/"]\n\n[relations]',1)
wo.write_text(text,encoding='utf-8')
roots={}
for label,py in [('baseline',PY),('candidate',CPY)]:
 root=OUT/label
 code,r=invoke(label+'-init',py,['init',str(root),'--project-name','Lifecycle comparison'])
 assert code==0,(label,r)
 shutil.copytree(fixtures/'docs/engineering/product',root/'docs/engineering/product')
 code,r=invoke(label+'-doctor',py,['doctor',str(root),'--json']);assert code==0,(label,r)
 roots[label]=(root,py)
def semantic(code,r):
 c=r.get('compliance',{})
 return {'exit_code':code,'state':r.get('state'),'operation':r.get('operation'),
  'status':c.get('status'),'checkpoint':c.get('checkpoint'),'workflow_rule_id':c.get('workflow_rule_id'),
  'gates':[{'id':g['id'],'status':g['status'],'predicates':[{'id':p['id'],'status':p['status']} for p in g.get('predicates',[])]} for g in c.get('gates',[])],
  'procedure':r.get('procedure'),'restitution':r.get('restitution')}
comparisons=[]
for state in ['draft','approved','in_progress','implemented']:
 for root,py in roots.values():
  wp=root/'docs/engineering/product/work-orders/WO-CMP-001.md'
  wp.write_text(text.replace('status = "draft"',f'status = "{state}"',1),encoding='utf-8')
  record_execution_approval(wp)
 a=(roots['baseline'][0]/'docs/engineering/product/work-orders/WO-CMP-001.md').read_bytes()
 assert a==(roots['candidate'][0]/'docs/engineering/product/work-orders/WO-CMP-001.md').read_bytes()
 cases=[('projection',[])]
 if state=='approved':cases += [('start',['--checkpoint','start'])]
 if state=='in_progress':cases += [('scope-pass',['--checkpoint','scope','--changes-complete','--changed-path','src/example.py']),('scope-refusal',['--checkpoint','scope','--changes-complete','--changed-path','outside.py']),('handoff-missing-evidence',['--checkpoint','handoff','--changes-complete','--changed-path','src/example.py'])]
 for name,extra in cases:
  results={}
  for label,(root,py) in roots.items():
   code,r=invoke(label+'-'+state+'-'+name,py,['check',str(root),'--artifact','WO-CMP-001',*extra,'--json'])
   results[label]=semantic(code,r)
  same=results['baseline']==results['candidate']
  comparisons.append({'state':state,'case':name,'formal_wo_sha256':hashlib.sha256(a).hexdigest(),'equal':same,'results':results})
summary={'claim':'Actual isolated released 0.18.0 and candidate 0.19.0 on separately valid installations with byte-identical synthetic formal records. No real source artifact is modified.',
 'candidate_package':candidate,'cases':comparisons,
 'excluded':'Installation/runtime identity, formal snapshot/result digests, reading manifests and additive instruction_discovery are intentionally version-specific; lifecycle fields, complete procedure operands, gate and predicate verdicts, effects, decision rights and next actions are compared.'}
(OUT/'comparison.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'cases':[(c['state'],c['case'],c['equal']) for c in comparisons]},indent=2))
assert all(c['equal'] for c in comparisons),'Inspect retained baseline/candidate difference'
