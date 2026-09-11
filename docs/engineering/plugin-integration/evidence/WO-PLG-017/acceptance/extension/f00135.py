import hashlib,json,os,pathlib,subprocess

OUT=pathlib.Path(__file__).resolve().parent
SRC=OUT.parent/'se-harness-plugin-evidence-path-fix'
PREV=OUT.parent/'plugin-path-repair-independent-20260911'
sha=lambda b:hashlib.sha256(b).hexdigest()
env=dict(os.environ,GIT_CONFIG_GLOBAL=os.devnull,GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0')
def save(name,data):
    p=OUT/name
    if p.exists():raise RuntimeError('Refusing overwrite')
    p.write_bytes(data)
def js(name,data):save(name,(json.dumps(data,indent=2,sort_keys=True)+'\n').encode())
def git(name,*args,stdin=None):
    argv=['git','-c','safe.directory='+SRC.as_posix(),'-C',str(SRC),*args]
    p=subprocess.run(argv,input=stdin,capture_output=True,env=env,timeout=60)
    save(name+'.stdout',p.stdout);save(name+'.stderr',p.stderr)
    if stdin is not None:save(name+'.stdin',stdin)
    js(name+'.json',dict(argv=argv,returncode=p.returncode,stdout_sha256=sha(p.stdout),stderr_sha256=sha(p.stderr)))
    assert p.returncode==0
    return p.stdout
save('freeze-source.py',pathlib.Path(__file__).read_bytes())
prior_bytes=(PREV/'oracle.json').read_bytes()
assert sha(prior_bytes)=='51370c2582f8360b2bc5530b677c3f41b181a8d8f3d44c99e44e166ae29cc378'
save('original55-oracle.json',prior_bytes);prior=json.loads(prior_bytes)
commit=git('01-approved-head','rev-parse','e9c256eb^{commit}').decode().strip()
prefix='docs/engineering/plugin-integration/'
proposal_path=prefix+'evidence/WO-PLG-017/scope-extension-plan.json'
proposal_bytes=git('02-approved-proposal','show',commit+':'+proposal_path)
assert sha(proposal_bytes)=='1927a7d61c7d6357e61047f427c0d2f1fb8e456d32dd1698efc01c7bba6f9538'
proposal=json.loads(proposal_bytes);assert len(proposal['files'])==1
row=proposal['files'][0]
assert row['bytes']==730 and row['sha256']=='730e0507e7c4992b183122e91fda0369d610a499d76545b463d725c22dcaf263'
assert row['original_path'] not in prior['selected_evidence_paths']
payload=git('03-original-payload','show',commit+':'+row['original_path'])
assert len(payload)==730 and sha(payload)==row['sha256']
save('original0056.json',payload);save('approved-proposal.json',proposal_bytes)
tree=git('04-approved-tree','ls-tree','-r','-z',commit)
entries={}
for raw in tree.split(b'\0'):
    if not raw:continue
    meta,path=raw.split(b'\t',1);mode,kind,oid=meta.decode().split()
    entries[path.decode()]=dict(mode=mode,type=kind,oid=oid)
immutable=[prefix+'evidence/WO-PLG-017/path-plan.json',prefix+'evidence/WO-PLG-011/native-path-map.json']
immutable+=sorted(p for p in entries if ('/verification-records/VREC-' in p or p.rsplit('/',1)[-1].startswith('VREC-') and p.endswith('-evaluator.json')))
immutable=sorted(set(immutable))
objects=git('05-immutable-objects','cat-file','--batch',stdin=''.join(commit+':'+p+'\n' for p in immutable).encode())
cursor=0;protected={};contents={}
for path in immutable:
    end=objects.index(b'\n',cursor);oid,kind,size=objects[cursor:end].decode().split();size=int(size)
    data=objects[end+1:end+1+size];cursor=end+size+2
    assert oid==entries[path]['oid'] and kind=='blob'
    protected[path]=dict(bytes=size,sha256=sha(data),git_blob=oid);contents[path]=data
assert cursor==len(objects)
plan_path=prefix+'evidence/WO-PLG-017/path-plan.json';map_path=prefix+'evidence/WO-PLG-011/native-path-map.json'
save('original55-plan.json',contents[plan_path]);save('original55-map.json',contents[map_path])
assert sha(contents[plan_path])==prior['governing_plan_sha256']
assert json.loads(contents[map_path])['files']==[{k:r[k] for k in ('original_path','sha256','bytes')}|{'retained_path':r['proposed_path']} for r in prior['mapped']]
for p in [prior['vrec_path'],prior['evaluator_path']]:
    assert protected[p]['sha256']==prior['original_inventory'][p]['sha256']
git('06-c-ancestor','merge-base','--is-ancestor',prior['preserved_candidate'],commit)
git('07-g-ancestor','merge-base','--is-ancestor',prior['source_commit'],commit)
oracle=dict(schema='wo017-extension-independent-v1',preextension_commit=commit,
    original55_oracle_sha256=sha(prior_bytes),approved_proposal_path=proposal_path,approved_proposal_sha256=sha(proposal_bytes),
    extra=row,staging_map_path=proposal['retention_map_destination'],protected_preextension_files=protected,
    staging_root_characters=77,staging_max_full_path=259,preextension_max_full_path=261,ordinary_checkout_budget=250,
    expectations=['Invoke unchanged repository_tools.upgrade_rehearsal.export_tracked_tree at a fresh exact77-character Windows repository path.',
      'Preextension e9c256eb must fail at git add -A for the183-character file with core.longpaths=false.',
      'Approved repaired commit must export and stage successfully at the same77-character depth.',
      'Reconcile all56 moves against fixed original bytes and approved maps; no old paths remain.',
      'Original55 plan/map, historical VREC/sidecar bytes and original source manifests stay unchanged.',
      'Supplemental one-byte corruption and coordinated supplemental plan/map tamper must be rejected, then restored exactly.',
      'Linux readability only; no fresh source suite or model behavior claim.'],updated_checker_read=False)
js('oracle.json',oracle)
js('freeze.json',dict(oracle_sha256=sha((OUT/'oracle.json').read_bytes()),preextension_commit=commit,
    protected_file_count=len(protected),payload_sha256=sha(payload),updated_checker_read=False))
print((OUT/'freeze.json').read_text())
