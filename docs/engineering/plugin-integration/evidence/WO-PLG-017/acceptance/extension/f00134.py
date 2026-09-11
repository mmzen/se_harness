import hashlib,json,os,pathlib,re,subprocess,sys,time,traceback
base=pathlib.Path(__file__).resolve().parent;out=base/'checker-correction';out.mkdir(exist_ok=False)
previous=json.loads((base/'after-extension/result.json').read_bytes());assert previous['export']['passed']
src=pathlib.Path(previous['source_checkout']);source=base.parent/'se-harness-plugin-evidence-path-fix'
oracle=json.loads((base/'attempt2/oracle.json').read_bytes());prior=json.loads((base/'attempt2/original55-oracle.json').read_bytes())
commit='e5b48a16be2e5e59ecd17d7d28d24409ff5ce519';sha=lambda b:hashlib.sha256(b).hexdigest()
env={k:v for k,v in os.environ.items() if not re.search(r'TOKEN|SECRET|PASSWORD|CREDENTIAL|_KEY$|^AWS_|^AZURE_|^GOOGLE_|^GIT_CONFIG_|^PYTHON',k,re.I)}
env.update(GIT_CONFIG_GLOBAL=str(base/'after-extension/home/gitconfig'),GIT_CONFIG_NOSYSTEM='1',GIT_OPTIONAL_LOCKS='0',GIT_TERMINAL_PROMPT='0',GIT_ALLOW_PROTOCOL='file')
def js(name,x):(out/name).write_bytes((json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
def call(name,argv,expected=0):
    start=time.time();stdout=stderr=b'';code=None;error=None
    try:
        p=subprocess.run([str(x) for x in argv],capture_output=True,env=env,timeout=180);stdout,stderr,code=p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:stdout,stderr=e.stdout or b'',e.stderr or b'';error=dict(type='TimeoutExpired',message=str(e))
    except OSError as e:error=dict(type=type(e).__name__,message=str(e))
    (out/(name+'.stdout')).write_bytes(stdout);(out/(name+'.stderr')).write_bytes(stderr)
    js(name+'.json',dict(argv=[str(x) for x in argv],returncode=code,error=error,expected=expected,elapsed_seconds=time.time()-start,stdout_sha256=sha(stdout),stderr_sha256=sha(stderr)))
    if code!=expected or error:raise RuntimeError(name+' failed')
    return stdout
(out/'runner-source.py').write_bytes(pathlib.Path(__file__).read_bytes())
result=dict(passed=False,checker_commit=commit,repository_commit=previous['commit'],staging_commit=previous['commit'],repository=str(src),
    scope='Corrected checker bytes from new commit against unchanged original staged candidate/history inputs; no new staging claim')
try:
    argv=['git','-c','safe.directory='+source.as_posix(),'-C',str(source)]
    data=call('01-checker-blob',argv+['cat-file','blob',commit+':tests/plugin_integration/evidence-skill/check_retention_paths.py'])
    checker=out/'checker-e5.py';checker.write_bytes(data);result['checker_sha256']=sha(data)
    changed=call('02-commit-diff',argv+['diff','--name-only',previous['commit'],commit]).decode().splitlines()
    assert changed==['tests/plugin_integration/evidence-skill/check_retention_paths.py'],changed
    g=['git','-c','safe.directory='+src.as_posix(),'-C',str(src)]
    assert call('03-head',g+['rev-parse','HEAD']).decode().strip()==previous['commit']
    assert call('04-longpaths',g+['config','--get','core.longpaths']).strip()==b'false'
    assert not call('05-clean-before',g+['status','--porcelain=v1','--untracked-files=all'])
    observed=set(oracle['protected_preextension_files'])|{r['proposed_path'] for r in prior['mapped']}|{oracle['extra']['proposed_path'],oracle['approved_proposal_path'],oracle['staging_map_path'],'.git/index','.git/config','.git/HEAD','.git/packed-refs'}
    def snapshot():return {p:dict(bytes=(src/p).stat().st_size,sha256=sha((src/p).read_bytes())) for p in sorted(observed) if (src/p).is_file()}
    before=snapshot();js('before.json',before)
    command=[sys.executable,'-I','-B',checker,'--root',src]
    assert json.loads(call('06-corrected-positive',command))['mapped_files']==56
    payload=src/oracle['extra']['proposed_path'];original=payload.read_bytes();corrupt=bytes([original[0]^1])+original[1:]
    payload.write_bytes(corrupt);js('07-payload-tamper.json',dict(path=oracle['extra']['proposed_path'],byte_offset=0,original_sha256=sha(original),corrupted_sha256=sha(corrupt)))
    try:
        call('08-payload-reject',command,expected=1)
        assert 'Changed supplemental evidence payload' in (out/'08-payload-reject.stderr').read_text()
    finally:payload.write_bytes(original)
    assert payload.read_bytes()==original
    assert json.loads(call('09-payload-restored',command))['passed']
    plan=src/oracle['approved_proposal_path'];mapping=src/oracle['staging_map_path'];original_plan=plan.read_bytes();original_map=mapping.read_bytes()
    changed_plan=json.loads(original_plan);changed_plan['staging_profile']['maximum_full_path']=999
    changed_plan_bytes=(json.dumps(changed_plan,indent=2)+'\n').encode();changed_map=json.loads(original_map);changed_map['source_plan_sha256']=sha(changed_plan_bytes)
    changed_map_bytes=(json.dumps(changed_map,indent=2)+'\n').encode();plan.write_bytes(changed_plan_bytes);mapping.write_bytes(changed_map_bytes)
    js('10-plan-tamper.json',dict(field='staging_profile.maximum_full_path',original_value=259,changed_value=999,original_plan_sha256=sha(original_plan),changed_plan_sha256=sha(changed_plan_bytes),original_map_sha256=sha(original_map),changed_map_sha256=sha(changed_map_bytes)))
    try:
        call('11-plan-reject',command,expected=1)
        assert 'Supplemental plan differs from the approved scope extension' in (out/'11-plan-reject.stderr').read_text()
    finally:plan.write_bytes(original_plan);mapping.write_bytes(original_map)
    assert json.loads(call('12-plan-restored',command))['passed']
    after=snapshot();js('after.json',after);assert before==after
    assert not call('13-clean-after',g+['status','--porcelain=v1','--untracked-files=all'])
    result.update(passed=True,one_byte_rejected=True,coordinated_plan_map_rejected=True,restored_hashes_equal=True,snapshot_files=len(before))
except BaseException as e:result['error']=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc());raise
finally:js('result.json',result);print(json.dumps(result,indent=2))
