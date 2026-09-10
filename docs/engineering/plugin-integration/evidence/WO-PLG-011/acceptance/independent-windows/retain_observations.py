"""Copy explicitly named observed results into the selected authorized packet."""
import argparse, hashlib, json, subprocess
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
ap.add_argument('--trace',type=Path,required=True);ap.add_argument('--record',action='append',required=True)
ns=ap.parse_args()
head=subprocess.run(['git','-C',str(ns.repo),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
observations=[]
for label in ns.record:
    path=ns.trace/(label+'.json');row=json.loads(path.read_text())
    observations.append({k:row[k] for k in ('label','argv','cwd','exit_code','stdout','stderr')})
    observations[-1]['raw_trace_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
body='# Retained observed evidence\n\nThese are local fixture observations, not assurance or release decisions.\n\nTested committed input: '+head+'\n\n'
body+='The injected wrong-expectation failure and missing probe test evidence retention; they are not acceptance requirements for the greeting.\n\n'
body+='```json\n'+json.dumps({'observations':observations,'missing_observation':{'argv':['inspect_fixture.py','--expect','NeverRun'],'status':'not run; no exit status or output exists'},'candidate_source':{'path':'src/feature.py','sha256':hashlib.sha256((ns.repo/'src/feature.py').read_bytes()).hexdigest()}},indent=2)+'\n```\n'
dest=ns.repo/'docs/engineering/evidence-demo/evidence/WO-EVD-001/observations.md'
dest.write_text(body,encoding='utf8');print(body)
