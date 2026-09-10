import hashlib, json, os, pathlib, subprocess

out = pathlib.Path(__file__).resolve().parent
oracle = json.loads((out/'oracle.json').read_bytes())
source = out.parent/'se-harness-plugin-evidence-path-fix'
argv = ['git','-c','safe.directory='+source.as_posix(),'-C',str(source),'cat-file','--batch']
inputs = ''.join(oracle['preserved_candidate']+':'+p+'\n' for p in oracle['selected_evidence_paths']).encode()
env = dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1', GIT_OPTIONAL_LOCKS='0')
result = subprocess.run(argv,input=inputs,capture_output=True,env=env,timeout=60)
def save(name,data):
    path=out/name
    if path.exists(): raise RuntimeError('Refusing overwrite')
    path.write_bytes(data)
save('candidate-source.py',pathlib.Path(__file__).read_bytes())
save('o05-candidate.stdout',result.stdout);save('o05-candidate.stderr',result.stderr)
save('o05-candidate.json',(json.dumps(dict(argv=argv,returncode=result.returncode,stdin=inputs.decode()),indent=2)+'\n').encode())
assert result.returncode == 0
cursor=0;checks=[]
for path in oracle['selected_evidence_paths']:
    end=result.stdout.index(b'\n',cursor)
    oid,kind,size=result.stdout[cursor:end].decode().split();size=int(size)
    data=result.stdout[end+1:end+1+size];cursor=end+size+2
    digest=hashlib.sha256(data).hexdigest(); original=oracle['original_inventory'][path]
    checks.append(dict(path=path,bytes=size,sha256=digest,git_blob=oid,matches_g=digest==original['sha256'] and size==original['bytes']))
assert cursor == len(result.stdout)
passed=all(c['matches_g'] for c in checks)
save('candidate-selected.json',(json.dumps(dict(passed=passed,selected_paths=95,candidate=oracle['preserved_candidate'],source_commit=oracle['source_commit'],checks=checks),indent=2)+'\n').encode())
assert passed
print('All 95 selected evidence files have identical bytes at original C and G.')
