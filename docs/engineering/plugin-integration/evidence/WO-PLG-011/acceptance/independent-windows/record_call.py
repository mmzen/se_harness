"""Transparent explicit-argv recorder. No authority or workflow policy."""
import argparse, hashlib, json, os, subprocess, time
from pathlib import Path

def snapshot(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()}

def statefiles(root):
    out = {}
    for p in sorted(root.rglob('*')):
        if p.is_file() and '.git' not in p.parts and p.suffix in ('.md', '.json', '.py'):
            value = p.read_text(encoding='utf8', errors='replace')
            if value.startswith('+++') or p.suffix != '.md':
                out[p.relative_to(root).as_posix()] = value
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--python',required=True)
    ap.add_argument('--repo',type=Path,required=True)
    ap.add_argument('--evidence',type=Path,required=True)
    ap.add_argument('--label',required=True)
    ap.add_argument('--native',action='store_true')
    ap.add_argument('--suppress-receipt',action='store_true')
    ap.add_argument('--stdin-file',type=Path)
    ap.add_argument('argv',nargs=argparse.REMAINDER)
    ns=ap.parse_args()
    args=ns.argv[1:] if ns.argv[:1]==['--'] else ns.argv
    args=[str(ns.repo.resolve()) if x=='{repo}' else x for x in args]
    command=args if ns.native else [ns.python,'-I','-B','-m','se_harness',*args]
    env=os.environ.copy(); env.pop('PYTHONPATH',None)
    env['PATH']=str(Path(ns.python).parent)+os.pathsep+env.get('PATH','')
    env['GIT_CONFIG_NOSYSTEM']='1'; env['GIT_CONFIG_GLOBAL']=os.devnull
    ns.evidence.mkdir(parents=True,exist_ok=True)
    dest=ns.evidence/(ns.label+'.json')
    if dest.exists(): raise FileExistsError(dest)
    before, bs, started=snapshot(ns.repo),statefiles(ns.repo),time.time()
    inp=ns.stdin_file.read_bytes() if ns.stdin_file else None
    run=subprocess.run(command,cwd=Path(__file__).resolve().parent,env=env,input=inp,capture_output=True,timeout=60)
    after=snapshot(ns.repo)
    row={'label':ns.label,'argv':command,'cwd':str(Path(__file__).resolve().parent),'stdin':inp.decode() if inp else None,
         'started_unix':started,'duration_seconds':time.time()-started,'exit_code':run.returncode,
         'stdout':run.stdout.decode('utf8','replace'),'stderr':run.stderr.decode('utf8','replace'),
         'before':before,'after':after,'before_statefiles':bs,'after_statefiles':statefiles(ns.repo),
         'changed_paths':[p for p in sorted(before.keys()|after.keys()) if before.get(p)!=after.get(p)],
         'receipt_suppressed_after_exit':ns.suppress_receipt}
    dest.write_text(json.dumps(row,indent=2)+'\n',encoding='utf8')
    if ns.suppress_receipt:
        print(json.dumps({'fault_injection':'Tool receipt lost after process exit. Inspect existing effects before retry. Observer retained actual result.','record':str(dest)})); return
    print(json.dumps({'record':str(dest),'exit_code':run.returncode,'changed_paths':row['changed_paths']}))
    try:
        result=json.loads(row['stdout'])
        selected={k:result[k] for k in ('schema','operation','outcome','state','findings','restitution','context','changes') if k in result}
        print(json.dumps(selected or result,indent=2))
    except ValueError: print(row['stdout'])
    if row['stderr']: print(row['stderr'])

if __name__=='__main__': main()
