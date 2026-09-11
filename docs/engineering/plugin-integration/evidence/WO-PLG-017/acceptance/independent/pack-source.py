import gzip, hashlib, json, pathlib, re

base=pathlib.Path(__file__).resolve().parent
out=base.parent/'plugin-path-repair-flat-20260911'
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads((base/p).read_bytes())
windows=read('windows-final/result.json');linux=read('linux-final/result.json');suite=read('source-suite-not-run.json')
assert windows['passed'] and linux['passed']
out.mkdir(exist_ok=False)
rows=[];retained={};index=0
special={'oracle.json':'oracle.json','oracle.md':'oracle.md','approved-path-plan.json':'path-plan.json',
 'windows-final/result.json':'windows.json','linux-final/result.json':'linux.json',
 'source-suite-not-run.json':'suite-not-run.json','candidate-selected.json':'c-vs-g.json',
 'ci-context/j11.log':'ci-source.log','ci-context/j11.json':'ci-source.json',
 'ci-context/j04.log':'ci-windows.log','ci-context/j04.json':'ci-windows.json'}
sources=[]
for p in sorted(base.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(base).as_posix()
    if 'repo' in p.relative_to(base).parts or p.name=='pack_evidence.py':continue
    sources.append((rel,p))
for rel,p in sources:
    data=p.read_bytes();digest=sha(data)
    key=(digest,rel if rel in special else '')
    if key in retained:
        destination=retained[key]
    else:
        index+=1
        compressed=len(data)>1_000_000
        destination=special.get(rel,'f%05d%s'%(index,'.gz' if compressed else (p.suffix or '.bin')))
        stored=gzip.compress(data,compresslevel=9,mtime=0) if compressed and rel not in special else data
        (out/destination).write_bytes(stored)
        retained[key]=destination
    stored=(out/destination).read_bytes()
    encoding='gzip' if destination.endswith('.gz') else 'identity'
    assert (gzip.decompress(stored) if encoding=='gzip' else stored)==data
    rows.append(dict(source_path=rel,retained_path=destination,source_bytes=len(data),source_sha256=digest,
        stored_bytes=len(stored),stored_sha256=sha(stored),encoding=encoding))
def writejson(name,x):(out/name).write_bytes((json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
writejson('source-path-map.json',dict(schema='wo017-flat-retention-v1',source_root=str(base),files=rows,
    excluded=['Disposable checkout directories named repo, their .git trees, Windows Temp checkouts, and runtime environments.'],
    compression='Files larger than one million bytes are retained losslessly as gzip; original/stored byte hashes are both recorded.'))
call_audit=[]
for rel,p in sources:
    if p.suffix!='.json':continue
    try:record=json.loads(p.read_bytes())
    except (ValueError,UnicodeError):continue
    if isinstance(record,dict) and 'argv' in record and 'returncode' in record:
        checks={}
        for channel in ('stdout','stderr'):
            adjacent=p.with_suffix('.'+channel)
            if channel+'_sha256' in record:
                checks[channel]=adjacent.exists() and sha(adjacent.read_bytes())==record[channel+'_sha256']
        call_audit.append(dict(source=rel,returncode=record['returncode'],stream_hashes=checks))
assert all(all(c['stream_hashes'].values()) for c in call_audit)
counts={}
for case in ['windows-attempt3','windows-final','linux-final']:
    r=read(case+'/result.json')
    before=read(case+'/13-before-checker.json');after=read(case+'/20-after-restore.json')
    assert before==after
    if case!='windows-attempt3':assert before==read(case+'/26-after-plan-restore.json')
    counts[case]=dict(commit=r['commit'],passed=r['passed'],runner_sha256=r['runner_sha256'],
        archived_runner_matches=sha((base/case/'runner-source.py').read_bytes())==r['runner_sha256'],
        snapshot_file_count=len(before),snapshot_restore_equal=True)
assert all(c['archived_runner_matches'] for c in counts.values())
historical=read('candidate-selected.json');mismatches=[x for x in historical['checks'] if not x['matches_g']]
assert len(mismatches)==1 and mismatches[0]['path'].endswith('WO-PLG-011-handoff.md')
suite_summary=suite['actual_source_summary']
writejson('audit.json',dict(passed=False,retention_audit_passed=True,scoped_checks_passed=windows['passed'] and linux['passed'],
    repair_completion_claimed=False,external_blocker={'source':'Parent-retained exact-head PR449 CI log; raw copy archived in ci-context',
      'stage':'upgrade_rehearsal export_tracked_tree git add -A',
      'path':'docs/engineering/plugin-integration/evidence/WO-PLG-011/acceptance/linux-replay-attempt2/external-control-state/external-cases/evd04-publish-control-unproven/request-and-decision.json',
      'reason':'Actual Git filename-too-long error for the 183-character relative path during nested upgrade rehearsal; outside the approved 55 moves',
      'root_limit':'The full temporary root is absent from the CI log; a 77-character rehearsal root against a 259-character ceiling is a separate derived explanation.'},
    oracle_sha256=windows['oracle_sha256'],
    final_commit=windows['commit'],windows=windows,linux=linux,source_suite=suite,source_suite_summary=suite_summary,executed_versions=counts,
    call_records=call_audit,original_failures_preserved=['o01 ownership refusal','Windows clone ownership refusals attempts1 and2',
       'Candidate-vs-G all-equal supplemental assertion: handoff already changed between C and G'],
    fixed_inputs='Original G oracle is unchanged; no product/helper/evaluator behavior rerun is claimed.'))
report=f'''# Independent WO-PLG-017 acceptance

Commit `{windows['commit']}` passed the scoped Windows and Linux checkout, byte reconciliation, readability and controlled corruption checks. The repair remains incomplete: PR449 CI failed in upgrade_rehearsal export_tracked_tree, where git add -A encounters the 183-character request-and-decision.json path under a deeper Temp/upgrade-rehearsal-xxxxxxxx/repository root. That path is outside the approved 55 moves. This report claims neither full CI success nor completion, and no additional relocation was performed. The actual parent-retained CI job metadata and full failure log are copied here as ci-windows.json and ci-windows.log.

The CI log does not record the full temporary root. The parent's 77-character rehearsal-root calculation against a 259-character ceiling explains the observed failure as a derivation; it is not a recorded absolute checkout path. A later scope-extension proposal is outside these tests, which remain bound to ed31a520.

The independently frozen oracle is `51370c2582f8360b2bc5530b677c3f41b181a8d8f3d44c99e44e166ae29cc378`; it was fixed from approved path-plan and Git G before the repair checker was read.

Both platforms reconciled all 55 relocated files one-to-one with original Git blob bytes, lengths and SHA-256; every old path is absent. Another 1,085 original evidence/test files are unchanged, including original manifests, VREC-PLG-008 and its evaluator sidecar. All 94 selected paths other than the allowed README are unchanged from G. The README preserves its original bytes as a prefix and appends 488 bytes. Both C and G remain ancestors.

The fresh Windows checkout explicitly set and read back `core.longpaths=false`. It contains {windows['tracked_files']} tracked files, with maximum relative length {windows['max_relative_path']} and maximum actual full path {windows['actual_root_max_windows_full_path'][0]}, below the fixed 250 budget. At the stated CI root, the maximum is {windows['ci_root_max_windows_full_path'][0]}. These are observations for those roots, not arbitrary checkout locations. The checker itself uses longpaths=true for its read-only Git queries; that did not perform checkout or weaken the actual false checkout test.

Final checker `{windows['checker_sha256']}` passed on both platforms. A one-byte payload corruption was rejected. Separately, changing the disposable plan's preserved candidate and the map's matching plan digest, while retaining payload bytes, was rejected. Each tamper was confined to disposable files, restored exactly, and followed by a passing checker call. Complete checkout, ignored and Git file-byte snapshots match after restoration. Linux parsed/read all 55 retained native files and verified original retained replay inputs; this is retention verification, not fresh model behavior or an evaluator-command replay.

The first repaired commit `c3c74334d1d780c112525b6d2b9043e5239f5425` also passed Windows checks and payload tamper. Its original checker and driver snapshots remain retained. Final checks use the later pinned-plan checker. Windows attempts1/2 failed before checkout because the local clone child did not receive command-scope ownership trust; the correction used only an isolated Git config with exact source/admin paths. No user/global config or source repository was changed.

A supplemental initial assumption that all 95 selected files were identical between C and G failed for one preexisting handoff. Its raw objects and diff remain retained: only formal_snapshot_sha256 and rebound_at changed at G. The repair oracle stays bound to G and requires its handoff bytes; VREC-PLG-008 continues binding original C bytes. This historical distinction is not a repair failure.

The requested duplicate local Linux source suite was not launched. The parent withdrew that request after the exact-head CI source job passed: {suite_summary}. Its actual metadata and full log are retained as ci-source.json and ci-source.log. The unexecuted local recorder source and suite-not-run.json remain explicit; they are not evidence of another test run. CI's source pass remains separate from its failed Windows upgrade and skipped dependent jobs.

`source-path-map.json` maps every retained byte stream and source snapshot to short flat names, with stored and original hashes. Large streams are losslessly gzip-compressed; disposable repositories, .git contents and runtime environments are excluded from packaging, while their recorded hash snapshots are retained. `audit.json` checks command stream digests, executed runner identities and restored snapshots. `inventory.json` binds the resulting package.
'''
(out/'REPORT.md').write_text(report,encoding='utf-8',newline='\n')
(out/'pack-source.py').write_bytes(pathlib.Path(__file__).read_bytes())
inventory=[]
for p in sorted(out.iterdir()):
    data=p.read_bytes();inventory.append(dict(path=p.name,bytes=len(data),sha256=sha(data)))
writejson('inventory.json',dict(schema='wo017-package-inventory-v1',files=inventory,payload_files=len(inventory),
    total_bytes=sum(x['bytes'] for x in inventory),mapped_source_files=len(rows),longest_flat_name=max(len(x['path']) for x in inventory)))
print(json.dumps(dict(output=str(out),files=len(inventory),bytes=sum(x['bytes'] for x in inventory),
    inventory_sha256=sha((out/'inventory.json').read_bytes())),indent=2))
