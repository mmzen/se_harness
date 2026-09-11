"""Read-only fixture readback or one independently expected feature assertion."""
import argparse, json, runpy, subprocess, tomllib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--expect');ap.add_argument('--id');ns=ap.parse_args()
if ns.expect is not None:
    actual=runpy.run_path(str(ns.repo/'src/feature.py'))['greeting']()
    print(json.dumps({'actual':actual,'expected':ns.expect,'passed':actual==ns.expect}))
    raise SystemExit(0 if actual==ns.expect else 1)
records=[]
for p in sorted((ns.repo/'docs/engineering').rglob('*.md')):
    text=p.read_text(encoding='utf8')
    if not text.startswith('+++'):continue
    data=tomllib.loads(text.split('+++',2)[1])
    if ns.id and data.get('id')!=ns.id:continue
    records.append({'path':p.relative_to(ns.repo).as_posix(),'metadata':data})
print(json.dumps({'records':records,'head':subprocess.run(['git','-C',str(ns.repo),'rev-parse','HEAD'],capture_output=True,text=True).stdout.strip(),'status':subprocess.run(['git','-C',str(ns.repo),'status','--porcelain=v1'],capture_output=True,text=True).stdout},indent=2,default=str))
