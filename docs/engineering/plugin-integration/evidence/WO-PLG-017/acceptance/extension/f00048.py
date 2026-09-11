import argparse,hashlib,json,os,pathlib,re,subprocess,sys,tempfile,time,traceback
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from reconcile import reconcile

ap=argparse.ArgumentParser();ap.add_argument('--commit',required=True);ap.add_argument('--case',required=True);ap.add_argument('--expect',choices=['failure','success'],required=True)
a=ap.parse_args();base=pathlib.Path(__file__).resolve().parent;oracle_root=base/'attempt2';oracle=json.loads((oracle_root/'oracle.json').read_bytes())
prior=json.loads((oracle_root/'original55-oracle.json').read_bytes());source=base.parent/'se-harness-plugin-evidence-path-fix'
out=base/a.case;out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
def js(name,x):(out/name).write_bytes((json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
for f in ['run_probe.py','reconcile.py','export_worker.py']:(out/('executed-'+f)).write_bytes((base/f).read_bytes())
home=out/'home';home.mkdir();hooks=home/'hooks';hooks.mkdir()
env={k:v for k,v in os.environ.items() if not re.search(r'TOKEN|SECRET|PASSWORD|CREDENTIAL|_KEY$|^AWS_|^AZURE_|^GOOGLE_|^GIT_CONFIG_|^PYTHON',k,re.I)}
env.update(HOME=str(home),USERPROFILE=str(home),XDG_CONFIG_HOME=str(home),GIT_CONFIG_GLOBAL=str(home/'gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_ALLOW_PROTOCOL='file')
temp=pathlib.Path(tempfile.gettempdir()).resolve();scratch=pathlib.Path(tempfile.mkdtemp(prefix='p17e-',dir=temp)).resolve()
assert scratch.is_relative_to(temp)
src=scratch/'src';filler='s'*(77-len(str(scratch))-len('/repository')-1);assert filler
dest=scratch/filler/'repository';assert len(str(dest))==77 and dest.resolve().is_relative_to(scratch)
dest.mkdir(parents=True)
counter=0
def call(label,argv,expected=0,timeout=600):
    start=time.time();stdout=stderr=b'';code=None;error=None
    try:
        p=subprocess.run([str(x) for x in argv],capture_output=True,env=env,timeout=timeout)
        stdout,stderr,code=p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:stdout,stderr=e.stdout or b'',e.stderr or b'';error=dict(type='TimeoutExpired',message=str(e))
    except OSError as e:error=dict(type=type(e).__name__,message=str(e))
    (out/(label+'.stdout')).write_bytes(stdout);(out/(label+'.stderr')).write_bytes(stderr)
    js(label+'.json',dict(argv=[str(x) for x in argv],returncode=code,error=error,expected=expected,elapsed_seconds=time.time()-start,stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
    if code!=expected or error:raise RuntimeError(label+' unexpected result')
    return stdout
def git(label,*args,target=source,expected=0):
    return call(label,['git','-c','safe.directory='+source.as_posix(),'-c','core.longpaths=false','-c','core.autocrlf=false','-C',str(target),*args],expected)
result=dict(commit=a.commit,expected=a.expect,source_checkout=str(src),destination=str(dest),destination_characters=len(str(dest)),oracle_sha256=sha((oracle_root/'oracle.json').read_bytes()),passed=False)
try:
    assert os.name=='nt'
    gitdir=git('01-source-gitdir','rev-parse','--absolute-git-dir').decode().strip()
    common=git('02-source-common','rev-parse','--path-format=absolute','--git-common-dir').decode().strip()
    for i,p in enumerate([source.as_posix(),pathlib.Path(gitdir).as_posix(),pathlib.Path(common).as_posix(),src.as_posix(),dest.as_posix()]):git('03-trust-'+str(i),'config','--file',str(home/'gitconfig'),'--add','safe.directory',p)
    for i,(key,value) in enumerate([('core.longpaths','false'),('core.autocrlf','false'),('core.hooksPath',str(hooks))]):git('04-config-'+str(i),'config','--file',str(home/'gitconfig'),key,value)
    git('05-clone','clone','--no-checkout','--no-hardlinks','--no-tags','--single-branch','--branch','work/plugin-evidence-path-repair',str(source),str(src))
    git('06-checkout','checkout','--detach',a.commit,target=src)
    assert git('07-head','rev-parse','HEAD',target=src).decode().strip()==a.commit
    assert git('08-longpaths','config','--get','core.longpaths',target=src).strip()==b'false'
    for label,commit in [('c',prior['preserved_candidate']),('g',prior['source_commit']),('approved',oracle['preextension_commit'])]:git('09-ancestor-'+label,'merge-base','--is-ancestor',commit,a.commit,target=src)
    helper=src/'repository_tools/upgrade_rehearsal.py'
    original_helper=git('10-original-helper','cat-file','blob',oracle['preextension_commit']+':repository_tools/upgrade_rehearsal.py',target=src)
    assert helper.read_bytes()==original_helper
    result['exporter_sha256']=sha(original_helper)
    listed=git('11-tracked','ls-files','-z',target=src).decode().rstrip('\0').split('\0')
    result['max_full_path_at77']=max(len(str(dest/path)) for path in listed)
    call('12-actual-export',[sys.executable,'-I','-B',base/'export_worker.py','--source',src,'--destination',dest,'--output',out/'export'],expected=1 if a.expect=='failure' else 0)
    export=json.loads((out/'export/result.json').read_bytes());result['export']=export
    assert git('13-destination-longpaths','config','--get','core.longpaths',target=dest).strip()==b'false'
    if a.expect=='failure':
        assert not export['passed'] and 'git add -A' in export['error']['message'] and 'Filename too long' in export['error']['message']
        calls=[json.loads(p.read_bytes()) for p in sorted((out/'export').glob('call*.json'))]
        assert calls[-1]['argv']==['git','add','-A'] and calls[-1]['returncode']!=0
        data=(dest/oracle['extra']['original_path']).read_bytes();assert len(data)==730 and sha(data)==oracle['extra']['sha256']
        assert result['max_full_path_at77']==261
        result['expected_staging_failure_observed']=True
    else:
        assert export['passed'] and result['max_full_path_at77']<=259
        js('source-reconciliation.json',reconcile(src,oracle_root));js('export-reconciliation.json',reconcile(dest,oracle_root))
        git('14-export-commit','rev-parse','HEAD',target=dest)
        checker=src/'tests/plugin_integration/evidence-skill/check_retention_paths.py';(out/'checker-source.py').write_bytes(checker.read_bytes())
        checker_argv=[sys.executable,'-I','-B',checker,'--root',src]
        observed_paths=set(oracle['protected_preextension_files'])|{r['proposed_path'] for r in prior['mapped']}|{oracle['extra']['proposed_path'],oracle['approved_proposal_path'],oracle['staging_map_path'],'.git/index','.git/config','.git/HEAD','.git/packed-refs'}
        def snapshot():return {p:dict(bytes=(src/p).stat().st_size,sha256=sha((src/p).read_bytes())) for p in sorted(observed_paths) if (src/p).is_file()}
        before=snapshot();js('before-tampers.json',before)
        assert json.loads(call('15-checker-pass',checker_argv))['mapped_files']==56
        payload=src/oracle['extra']['proposed_path'];original=payload.read_bytes();corrupt=bytes([original[0]^1])+original[1:]
        payload.write_bytes(corrupt);js('16-payload-tamper.json',dict(path=oracle['extra']['proposed_path'],original_sha256=sha(original),corrupted_sha256=sha(corrupt),byte_offset=0))
        try:
            call('17-payload-reject',checker_argv,expected=1)
            assert 'Changed supplemental evidence payload' in (out/'17-payload-reject.stderr').read_text()
        finally:payload.write_bytes(original)
        assert payload.read_bytes()==original
        assert json.loads(call('18-payload-restored',checker_argv))['passed']
        plan_path=src/oracle['approved_proposal_path'];map_path=src/oracle['staging_map_path'];old_plan=plan_path.read_bytes();old_map=map_path.read_bytes()
        changed_plan=json.loads(old_plan);changed_plan['staging_profile']['maximum_full_path']=999
        changed_plan_bytes=(json.dumps(changed_plan,indent=2)+'\n').encode();changed_map=json.loads(old_map);changed_map['source_plan_sha256']=sha(changed_plan_bytes);changed_map_bytes=(json.dumps(changed_map,indent=2)+'\n').encode()
        plan_path.write_bytes(changed_plan_bytes);map_path.write_bytes(changed_map_bytes)
        js('19-plan-tamper.json',dict(plan_field='staging_profile.maximum_full_path',original_value=259,changed_value=999,original_plan_sha256=sha(old_plan),changed_plan_sha256=sha(changed_plan_bytes),original_map_sha256=sha(old_map),changed_map_sha256=sha(changed_map_bytes)))
        try:
            call('20-plan-reject',checker_argv,expected=1)
            assert 'Supplemental plan differs from the approved scope extension' in (out/'20-plan-reject.stderr').read_text()
        finally:plan_path.write_bytes(old_plan);map_path.write_bytes(old_map)
        assert json.loads(call('21-plan-restored',checker_argv))['passed']
        after=snapshot();js('after-tampers.json',after);assert before==after
        result.update(tampers_rejected=True,restored_hashes_equal=True,snapshot_files=len(before),checker_sha256=sha(checker.read_bytes()),mapped_files=56)
    assert not git('22-source-clean','status','--porcelain=v1','--untracked-files=all',target=src)
    result['passed']=True
except BaseException as e:
    result['error']=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc());raise
finally:
    js('result.json',result);print(json.dumps(result,indent=2))
