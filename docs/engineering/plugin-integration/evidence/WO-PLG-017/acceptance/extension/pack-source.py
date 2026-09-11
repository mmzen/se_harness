import gzip,hashlib,json,pathlib

base=pathlib.Path(__file__).resolve().parent;out=base.parent/'plugin-path-extension-flat-20260911'
sha=lambda b:hashlib.sha256(b).hexdigest()
read=lambda p:json.loads((base/p).read_bytes())
before=read('before-extension/result.json');after=read('after-extension/result.json');corrected=read('checker-correction/result.json');linux=read('linux-archive-readability/result.json')
assert before['passed'] and before['expected_staging_failure_observed'] and after['export']['passed'] and corrected['passed'] and linux['passed']
assert before['destination_characters']==after['destination_characters']==77
assert before['max_full_path_at77']==261 and after['max_full_path_at77']==259
assert before['exporter_sha256']==after['exporter_sha256']
out.mkdir(exist_ok=False)
special={'attempt2/oracle.json':'oracle.json','attempt2/approved-proposal.json':'approved-plan.json',
    'before-extension/result.json':'before.json','after-extension/result.json':'after.json',
    'checker-correction/result.json':'checker-fixed.json','linux-archive-readability/result.json':'linux.json',
    'payloads/manifest.json':'payloads.json'}
for p in (base/'payloads').iterdir():
    if p.is_file() and p.name!='manifest.json':special['payloads/'+p.name]=p.name
omitted=[];omit_set=set()
for case in ['before-extension','after-extension']:
    record=read(case+'/export/call01.json');commit=read(case+'/result.json')['commit']
    stream=record['stdout'];rel=case+'/export/'+stream['path'];stored=(base/rel).read_bytes();raw=gzip.decompress(stored)
    assert sha(raw)==stream['sha256'] and len(raw)==stream['bytes'] and sha(stored)==stream['stored_sha256']
    omit_set.add(rel)
    omitted.append(dict(source_path=rel,omitted_from_package=True,reason='Whole-repository archive recursively contains prior acceptance packages; retained externally and reproducible from immutable Git commit.',
        source_commit=commit,actual_archive_argv=record['argv'],actual_archive_cwd=record['cwd'],
        stdout_bytes=len(raw),stdout_sha256=sha(raw),external_stored_bytes=len(stored),external_stored_sha256=sha(stored),
        external_retention_path=str(base/rel),reproduction_argv=['git','-c','core.autocrlf=false','archive','--format=tar',commit],
        reproduction_context='Run in the preserved source repository containing this immutable commit. HEAD in the actual argv was recorded as source_commit.'))
rows=[];dedup={};index=0;call_audit=[]
for p in sorted(base.rglob('*')):
    if not p.is_file() or p.name=='pack_evidence.py':continue
    rel=p.relative_to(base).as_posix()
    if rel in omit_set:continue
    data=p.read_bytes();digest=sha(data);key=(digest,rel if rel in special else '')
    if key in dedup:name=dedup[key]
    else:
        index+=1;compressed=len(data)>1000000 and rel not in special
        name=special.get(rel,'f%05d%s'%(index,'.gz' if compressed else (p.suffix or '.bin')))
        stored=gzip.compress(data,mtime=0) if compressed else data
        (out/name).write_bytes(stored);dedup[key]=name
    stored=(out/name).read_bytes();encoding='gzip' if name.endswith('.gz') and not p.name.endswith('.gz') else 'identity'
    restored=gzip.decompress(stored) if encoding=='gzip' else stored;assert restored==data
    rows.append(dict(source_path=rel,retained_path=name,source_bytes=len(data),source_sha256=digest,stored_bytes=len(stored),stored_sha256=sha(stored),encoding=encoding))
    if p.suffix=='.json':
        try:r=json.loads(data)
        except (ValueError,UnicodeError):continue
        if isinstance(r,dict) and 'argv' in r and 'returncode' in r:
            streams={}
            for channel in ['stdout','stderr']:
                if channel+'_sha256' in r:
                    q=p.with_suffix('.'+channel);streams[channel]=q.exists() and sha(q.read_bytes())==r[channel+'_sha256']
                elif isinstance(r.get(channel),dict) and 'path' in r[channel]:
                    channel_info=r[channel];q=p.parent/channel_info['path'];blob=q.read_bytes()
                    raw=gzip.decompress(blob) if channel_info['encoding']=='gzip' else blob
                    streams[channel]=sha(raw)==channel_info['sha256'] and len(raw)==channel_info['bytes']
            assert all(streams.values())
            call_audit.append(dict(source_path=rel,returncode=r['returncode'],stream_hashes_pass=streams))
def js(name,x):(out/name).write_bytes((json.dumps(x,indent=2,sort_keys=True)+'\n').encode())
assert read('checker-correction/before.json')==read('checker-correction/after.json')
js('source-path-map.json',dict(schema='wo017-extension-flat-v1',source_root=str(base),files=rows,explicit_bulk_omissions=omitted,
    excluded='Disposable source/export repositories, native Linux temp extraction and runtime environments are outside this package. Only the two listed bulk archive streams are omitted from retained output files.'))
js('bulk-omissions.json',dict(files=omitted,retained_actual_payload_count=56,plans_and_maps_retained=4))
js('audit.json',dict(retention_audit_passed=True,scoped_checks_passed=True,completion_claimed=False,assurance_claimed=False,
    oracle_sha256=sha((base/'attempt2/oracle.json').read_bytes()),preextension=before,repaired_staging=after['export'],
    corrected_checker=corrected,linux=linux,source_suite='Not run; full source/hosted CI qualification remains with parent task.',
    checked_records=call_audit,archive_streams_omitted=omitted,
    limitations=['Actual staging candidates are e9c256eb and28b4d2e2; corrected checker source is e5b48a16 against unchanged28b history/payload inputs.',
      'Linux read the exact captured Git archive in a fresh native directory after a direct Windows Temp ACL refusal; no evaluator/model replay.',
      'Hosted Windows upgrade and downstream/full CI outcomes are separate from these local observations.']))
report=f'''# Independent WO-PLG-017 extension checks

The actual pre-extension exporter failed at Git staging; the repaired exporter succeeded at the same directory depth. Both disposable Windows repository paths are exactly 77 characters and use an isolated Git configuration with core.longpaths=false.

| Observation | Immutable source | Result |
| --- | --- | --- |
| Real export_tracked_tree, archive/extract/init/config/git add | `{before['commit']}` | Expected failure: specified path is 261 characters; git add -A reports Filename too long. |
| Same unchanged exporter through git add and disposable commit | `{after['commit']}` | Pass: maximum full path 259 characters. |
| Corrected checker and supplemental tamper tests | `{corrected['checker_commit']}` checker bytes, unchanged `{corrected['repository_commit']}` repository inputs | Pass; byte and plan/map changes rejected, then restored. |
| Native Linux extraction/readability of actual captured archive | `{linux['source_commit']}` | Pass for all 56 payloads, 366 protected files and 1,084 original files. |

The frozen oracle is `a809a6bd7940daf6d7cef9b8036e01924c1036ddfcbada333f4b3939a2cc52f3`, fixed before the updated checker was read. It binds approved proposal `1927a7d61c7d6357e61047f427c0d2f1fb8e456d32dd1698efc01c7bba6f9538` and the extra 730-byte payload `730e0507e7c4992b183122e91fda0369d610a499d76545b463d725c22dcaf263`, and reuses the original independent 55-file oracle. All 56 paths reconcile one-to-one; old paths are absent. Original55 plan/map, historical VREC/sidecar/source-manifest bytes, 94 selected unchanged paths and the original README prefix remain intact. C and G remain ancestors.

The unchanged exporter is `{after['exporter_sha256']}`. A transparent subprocess recorder calls the real subprocess implementation and returns its actual results without replacement. It captures the actual archive bytes and Git argv/status/stdio. Binary streams stay binary; text streams preserve the text returned by the unchanged helper. The successful staging created only the exporter's ordinary throwaway commit, not a source-repository or lifecycle commit.

The first 28b checker run failed because Git show tried to stat a long revision/path expression under the isolated configuration. Its raw failure and direct readback remain retained. The parent changed four reads to git cat-file blob in e5; the observed Git diff contains only that checker file. Corrected checker SHA-256 `{corrected['checker_sha256']}` then passed against the unchanged 28b repository/history. One byte in native/0056.json was altered and rejected. Separately, the supplemental plan's staging maximum was changed from 259 to 999 and the map digest updated to match; the pinned plan check rejected it. Both were restored, passing checker calls followed each restoration, and all 428 observed file/Git metadata hashes matched afterward. No later staging result is inferred for e5; hosted qualification at the corrected head remains separate.

The initial oracle Git show lookup failure is retained; cat-file recovered the exact original object. A first Linux attempt could not read Windows Temp files because of the cross-account ACL; no permissions were changed. The passing Linux attempt extracted the exact SHA-bound real Git archive into a fresh native temporary directory, verified its embedded commit identity and reconciled the same frozen bytes. This is file retention/readability evidence, not model behavior or evaluator replay. No source suite was run.

The package retains 56 actual payload files and four actual plan/map files. It explicitly omits the two whole-repository archive stdout streams to avoid recursively packaging earlier evidence. Their source commits, actual argv, raw sizes/hashes, external locations and immutable-commit reproduction commands are in bulk-omissions.json; the call records still bind them. All other recorded output, source snapshots, original failures and results are mapped by source-path-map.json to short flat names. inventory.json binds this package. Completion, assurance and full hosted CI are not claimed by this subtask.
'''
(out/'REPORT.md').write_text(report,encoding='utf-8',newline='\n');(out/'pack-source.py').write_bytes(pathlib.Path(__file__).read_bytes())
files=[]
for p in sorted(out.iterdir()):
    data=p.read_bytes();files.append(dict(path=p.name,bytes=len(data),sha256=sha(data)))
js('inventory.json',dict(files=files,payload_files=len(files),total_bytes=sum(x['bytes'] for x in files),mapped_sources=len(rows),bulk_omitted_count=len(omitted),longest_filename=max(len(x['path']) for x in files)))
print(json.dumps(dict(output=str(out),payload_files=len(files),bytes=sum(x['bytes'] for x in files),mapped_sources=len(rows),omitted_bulk_streams=len(omitted),inventory_sha256=sha((out/'inventory.json').read_bytes())),indent=2))
