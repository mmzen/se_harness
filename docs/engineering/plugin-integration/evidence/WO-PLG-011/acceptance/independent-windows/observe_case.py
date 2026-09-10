"""Record supplied model observation and whole fixture hashes; no policy engine."""
import argparse,hashlib,json
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True)
ap.add_argument('--output',type=Path,required=True);ap.add_argument('--case',required=True)
ap.add_argument('--phase',choices=['before','after'],required=True)
ap.add_argument('--observation',default='');ap.add_argument('--prompts',type=int,default=0)
ap.add_argument('--local-root',type=Path)
ns=ap.parse_args();files={p.relative_to(ns.root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ns.root.rglob('*')) if p.is_file()}
dest=ns.output/(ns.case+'-'+ns.phase+'.json');ns.output.mkdir(parents=True,exist_ok=True)
if dest.exists():raise FileExistsError(dest)
row={'case':ns.case,'phase':ns.phase,'root':str(ns.root),'file_hashes':files,'model_observation':ns.observation,'approval_prompts':ns.prompts}
if ns.local_root:
    row['local_root']=str(ns.local_root)
    row['local_file_hashes']={p.relative_to(ns.local_root).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(ns.local_root.rglob('*')) if p.is_file()}
for name in ['invocations.jsonl','effects.jsonl','remote-refs.json','registry.json']:
    row[name]=[(p.relative_to(ns.root).as_posix(),p.read_text()) for p in ns.root.rglob(name)]
dest.write_text(json.dumps(row,indent=2)+'\n');print(json.dumps({'case':ns.case,'phase':ns.phase,'file_count':len(files),'model_observation':ns.observation,'approval_prompts':ns.prompts}))
