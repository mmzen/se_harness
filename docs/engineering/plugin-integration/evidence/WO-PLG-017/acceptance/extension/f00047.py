"""Independent file-byte oracle; usable on Windows and Linux without evaluator calls."""
import hashlib,json,pathlib
sha=lambda b:hashlib.sha256(b).hexdigest()
def reconcile(root,oracle_root):
    oracle_bytes=(oracle_root/'oracle.json').read_bytes()
    assert sha(oracle_bytes)=='a809a6bd7940daf6d7cef9b8036e01924c1036ddfcbada333f4b3939a2cc52f3'
    oracle=json.loads(oracle_bytes);prior=json.loads((oracle_root/'original55-oracle.json').read_bytes())
    all_rows=prior['mapped']+[oracle['extra']]
    old={r['original_path'] for r in all_rows};new={r['proposed_path'] for r in all_rows}
    assert len(old)==len(new)==56
    observed=[]
    for r in all_rows:
        data=(root/r['proposed_path']).read_bytes()
        assert len(data)==r['bytes'] and sha(data)==r['sha256'],r['proposed_path']
        assert not (root/r['original_path']).exists(),r['original_path']
        if r['proposed_path'].endswith('.json'):json.loads(data)
        else:data.decode('utf-8')
        observed.append(dict(path=r['proposed_path'],bytes=len(data),sha256=sha(data)))
    protected=[]
    for p,expected in oracle['protected_preextension_files'].items():
        data=(root/p).read_bytes();assert len(data)==expected['bytes'] and sha(data)==expected['sha256'],p
        protected.append(p)
    originals=[];readme=prior['only_allowed_original_evidence_edit']
    for p,expected in prior['original_inventory'].items():
        if p in old or p==readme:continue
        data=(root/p).read_bytes();assert len(data)==expected['bytes'] and sha(data)==expected['sha256'],p
        originals.append(p)
    readme_data=(root/readme).read_bytes();size=prior['original_inventory'][readme]['bytes']
    assert sha(readme_data[:size])==prior['original_inventory'][readme]['sha256']
    proposal_bytes=(root/oracle['approved_proposal_path']).read_bytes()
    assert sha(proposal_bytes)==oracle['approved_proposal_sha256']
    proposal=json.loads(proposal_bytes);mapping=json.loads((root/oracle['staging_map_path']).read_bytes())
    row=oracle['extra'];expected={('retained_path' if k=='proposed_path' else k):v for k,v in row.items()}
    assert mapping['files']==[expected]
    assert mapping['source_plan_sha256']==oracle['approved_proposal_sha256'] and mapping['source_commit']==proposal['source_commit']
    actual_new={p.relative_to(root).as_posix() for p in (root/'docs/engineering/plugin-integration/evidence/WO-PLG-011/native').iterdir() if p.is_file()}
    assert actual_new==new
    return dict(passed=True,mapped_files=56,observed=observed,protected_files=protected,unchanged_original_files=originals,
        selected_original_unchanged=[p for p in prior['selected_evidence_paths'] if p!=readme],original_readme_prefix_preserved=True,
        readable_native_files=56,scope='Readability and exact retained bytes, not a model/evaluator behavior replay')
