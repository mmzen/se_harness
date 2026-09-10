import hashlib, json, os, pathlib, shutil, subprocess, sys, time

base = pathlib.Path(__file__).resolve().parent
checked = json.loads((base/'linux-final/result.json').read_bytes())
assert checked['passed'] and checked['commit'] == 'ed31a520964f81627c9c5b428b68968caa6282e7'
repo = pathlib.Path(checked['checkout'])
out = base/'source-suite'; out.mkdir(exist_ok=False)
home = out/'home'; home.mkdir()
env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(home), GIT_CONFIG_GLOBAL=os.devnull,
    GIT_CONFIG_NOSYSTEM='1', GIT_OPTIONAL_LOCKS='0', GIT_TERMINAL_PROMPT='0', GIT_ALLOW_PROTOCOL='file')
env.pop('PYTHONPATH',None); env.pop('SE_HARNESS_TEST_SCALE',None)
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,b):
    p=out/name
    if p.exists():raise RuntimeError('Refusing overwrite')
    p.write_bytes(b)
def js(name,x):save(name,(json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
def call(name,argv,timeout=60):
    started=time.time();stdout=stderr=b'';code=None;error=None
    try:
        p=subprocess.run(argv,cwd=repo,env=env,capture_output=True,timeout=timeout)
        stdout,stderr,code=p.stdout,p.stderr,p.returncode
    except subprocess.TimeoutExpired as e:
        stdout,stderr=e.stdout or b'',e.stderr or b'';error={'type':'TimeoutExpired','message':str(e)}
    except OSError as e:error={'type':type(e).__name__,'message':str(e)}
    save(name+'.stdout',stdout);save(name+'.stderr',stderr)
    result=dict(argv=argv,cwd=str(repo),returncode=code,error=error,elapsed_seconds=time.time()-started,
        stdout_sha256=sha(stdout),stderr_sha256=sha(stderr))
    js(name+'.json',result)
    return result,stdout,stderr
save('runner-source.py',pathlib.Path(__file__).read_bytes())
save('suite-source.py',(repo/'scripts/run_tests.py').read_bytes())
python=shutil.which('python3');assert python
call('01-python-version',[python,'--version'])
git=['git','-c','safe.directory='+repo.as_posix(),'-C',str(repo)]
r,head,_=call('02-head',git+['rev-parse','HEAD']);assert r['returncode']==0 and head.decode().strip()==checked['commit']
r,status,_=call('03-status-before',git+['status','--porcelain=v1','--untracked-files=all']);assert r['returncode']==0 and not status
r,stdout,stderr=call('04-source-suite',[python,'scripts/run_tests.py'],timeout=3600)
call('05-status-after',git+['status','--porcelain=v1','--untracked-files=all'])
timings=repo/'target/test-timings.json'
if timings.exists():save('test-timings.json',timings.read_bytes())
js('result.json',dict(passed=r['returncode']==0 and r['error'] is None,commit=checked['commit'],
    command=r,python=python,scale='default full; no additional skips or source changes',
    suite_source_sha256=sha((repo/'scripts/run_tests.py').read_bytes())))
print(json.dumps(r,indent=2))
print(stdout.decode(errors='replace')[-3000:]);print(stderr.decode(errors='replace')[-3000:])
raise SystemExit(0 if r['returncode']==0 and r['error'] is None else 1)
