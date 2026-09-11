import hashlib,json,pathlib,platform,sys,time,traceback
base=pathlib.Path(__file__).resolve().parent;sys.path.insert(0,str(base))
from reconcile import reconcile
after=json.loads((base/'after-extension/result.json').read_bytes())
assert after['export']['passed'] and after['commit']=='28b4d2e22477067a17544e8275a37cecf22575f0'
windows_path=after['destination'].replace('\\','/')
assert windows_path.startswith('C:/Users/mathi/AppData/Local/Temp/p17e-')
target=pathlib.Path('/mnt/c/'+windows_path[3:])
out=base/'linux-readability';out.mkdir(exist_ok=False)
sha=lambda b:hashlib.sha256(b).hexdigest()
for p in [pathlib.Path(__file__),base/'reconcile.py']:(out/('executed-'+p.name)).write_bytes(p.read_bytes())
result=dict(passed=False,argv=[sys.executable,*sys.argv],platform=platform.platform(),python=sys.version,
    source_commit=after['commit'],input_export=str(target),input_kind='Actual staged Windows export, read natively through WSL; no new evaluator or model replay',
    checker_status_separate=after['passed'],
    oracle_sha256=sha((base/'attempt2/oracle.json').read_bytes()),reconciler_sha256=sha((base/'reconcile.py').read_bytes()))
start=time.time()
try:
    observed=reconcile(target,base/'attempt2')
    expected=json.loads((base/'after-extension/export-reconciliation.json').read_bytes())
    assert observed==expected
    (out/'reconciliation.json').write_bytes((json.dumps(observed,indent=2,sort_keys=True)+'\n').encode())
    result.update(passed=True,returncode=0,mapped_files=56,protected_files=len(observed['protected_files']),
        unchanged_original_files=len(observed['unchanged_original_files']),selected_unchanged_files=len(observed['selected_original_unchanged']))
except BaseException as e:
    result.update(returncode=1,error=dict(type=type(e).__name__,message=str(e),traceback=traceback.format_exc()));raise
finally:
    result['elapsed_seconds']=time.time()-start
    (out/'result.json').write_bytes((json.dumps(result,indent=2,sort_keys=True)+'\n').encode());print(json.dumps(result,indent=2))
