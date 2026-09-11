"""Resolve a fixed raw fixture's C/digest parameters; does not infer authority."""
import hashlib,json,subprocess
from pathlib import Path
root=Path(__file__).resolve().parent;repo=root/'capture-repository'
head=subprocess.run(['git','-C',str(repo),'rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip()
paths=['docs/engineering/evidence-demo/evidence/WO-EVD-001/observations.md']
out={'schema':'fixed-synthetic-preparation-input-v1','candidate':head,'work_order':'WO-EVD-001','verification':'VER-EVD-001','record':'VREC-EVD-001','actor':'fixture-preparation-actor','right':'DR-VREC-PREPARE','domain':'evidence-demo','evidence':{p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in paths},'supplied_decision':'EVD02-vrec raw request, synthetic engineering-owner test input. Prepare this exact ready record only. No assurance/release/external right.'}
dest=root/'candidate-inputs.json'
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
