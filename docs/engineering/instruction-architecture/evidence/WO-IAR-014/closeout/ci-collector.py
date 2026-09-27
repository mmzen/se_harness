import json, subprocess, datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'work/iar-closeout-ci'
OUT.mkdir(exist_ok=True)
GH=r'C:\Program Files\GitHub CLI\gh.exe'
def run(args,name):
    p=subprocess.run([GH,*args],capture_output=True)
    (OUT/(name+'.stdout')).write_bytes(p.stdout)
    (OUT/(name+'.stderr')).write_bytes(p.stderr)
    (OUT/(name+'.invocation.json')).write_text(json.dumps({'argv':[GH,*args],'cwd':str(ROOT),'exit_code':p.returncode,'observed_at':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2)+'\n',encoding='utf-8')
    if p.returncode: raise SystemExit(p.stderr.decode(errors='replace'))
    return p.stdout
r=json.loads(run(['run','view','36334454733','--repo','mmzen/se_harness','--json','headSha,status,conclusion,jobs,url'],'run'))
assert r['headSha']=='17dc41eea39368a92614011e8c341a61e0c93609' and r['conclusion']=='success'
assert all(j['conclusion']=='success' for j in r['jobs'])
run(['api','repos/mmzen/se_harness/actions/runs/36334454733/artifacts'],'artifacts')
for name in ['candidate-source-raw','complete-candidate-qualification','candidate-package-qualification-0.18.0','upgrade-rehearsal-Windows','upgrade-rehearsal-Linux']:
    run(['run','download','36334454733','--repo','mmzen/se_harness','--name',name,'--dir',str(OUT/name)],'download-'+name)
print(json.dumps({'head':r['headSha'],'jobs':[(j['name'],j['conclusion']) for j in r['jobs']], 'directory':str(OUT)}))
