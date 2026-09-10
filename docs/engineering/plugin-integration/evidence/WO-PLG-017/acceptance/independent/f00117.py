import hashlib,json,pathlib
base=pathlib.Path(__file__).resolve().parent
source=base.parent/'plugin-probe-control/se-harness-plugin-evidence-path-fix/ci/ed31a520-failed'
out=base/'ci-context';out.mkdir(exist_ok=False)
mapping=[]
for name in ['result.json','j11.json','j11.log','j04.json','j04.log','commands.json']:
    data=(source/name).read_bytes();(out/name).write_bytes(data)
    mapping.append(dict(source=str(source/name),retained=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
source_job=json.loads((out/'j11.json').read_bytes());windows_job=json.loads((out/'j04.json').read_bytes())
assert source_job['head_sha']==windows_job['head_sha']=='ed31a520964f81627c9c5b428b68968caa6282e7'
assert source_job['conclusion']=='success' and windows_job['conclusion']=='failure'
assert b'Ran 1134 tests' in (out/'j11.log').read_bytes() and b'OK (skipped=4)' in (out/'j11.log').read_bytes()
assert b'Filename too long' in (out/'j04.log').read_bytes()
(out/'source-map.json').write_text(json.dumps(mapping,indent=2)+'\n',encoding='utf-8')
(base/'source-suite-not-run.json').write_text(json.dumps(dict(status='not_run',launched=False,
    planned_argv=['python3','scripts/run_tests.py'],reason='Parent withdrew redundant local source-suite request after exact-head CI source suite passed.',
    actual_source_evidence_job=source_job['id'],actual_source_summary='Ran 1134 tests; OK (skipped=4)',
    actual_upgrade_windows_job=windows_job['id'],repair_remains_blocked=True),indent=2)+'\n',encoding='utf-8')
print('Retained actual CI1134/4 pass and separate Windows upgrade failure; local suite not launched.')
