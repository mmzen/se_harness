"""Bind a synthetic raw release-preparation request to the actual fixture bytes."""
import hashlib,json,tomllib
from pathlib import Path
root=Path(__file__).resolve().parent;repo=root/'release-repository'
v='docs/engineering/evidence-demo/verification-records/VREC-EVD-001.md'
m=tomllib.loads((repo/v).read_text().split('+++',2)[1])
paths=[v,m['evaluator_evidence_path'],*m['evidence_paths'],'docs/engineering/evidence-demo/release/REL-EVD-001.md','docs/engineering/evidence-demo/work-orders/WO-EVD-001.md']
out={'schema':'fixed-synthetic-release-input-v1','candidate':m['commit'],'work_order':'WO-EVD-001','verification_record':'VREC-EVD-001','release_contract':'REL-EVD-001','record':'RLS-EVD-001','version':'1.2.3','domain':'evidence-demo','owner':'release-owner','right':'DR-RLS-PREPARE','input_sha256':{p:hashlib.sha256((repo/p).read_bytes()).hexdigest() for p in paths},'supplied_decision':'EVD02-rls raw request: synthetic release-owner authorizes these exact preparation inputs only. No release or external action decision.','preexisting_assurance_input':'Fixture setup only: VREC-EVD-001 was previously verified at candidate C by fixture-assurance-owner. This is not a live or tested assurance transition.'}
dest=root/'release-inputs.json'
if dest.exists():raise FileExistsError(dest)
dest.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
