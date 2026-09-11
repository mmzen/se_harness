import hashlib,json,pathlib
base=pathlib.Path(__file__).resolve().parent;out=base/'payloads';out.mkdir(exist_ok=False)
oracle=json.loads((base/'attempt2/oracle.json').read_bytes());prior=json.loads((base/'attempt2/original55-oracle.json').read_bytes())
case=json.loads((base/'after-extension/result.json').read_bytes());assert case['export']['passed']
source=pathlib.Path(case['destination']);sha=lambda b:hashlib.sha256(b).hexdigest();records=[]
for n,row in enumerate(prior['mapped']+[oracle['extra']],1):
    data=(source/row['proposed_path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256']
    dest='p%04d%s'%(n,pathlib.Path(row['proposed_path']).suffix);(out/dest).write_bytes(data)
    records.append(dict(original_path=row['original_path'],retained_repository_path=row['proposed_path'],file=dest,bytes=len(data),sha256=sha(data)))
prefix='docs/engineering/plugin-integration/evidence/'
for name,path in [('original55-plan.json',prefix+'WO-PLG-017/path-plan.json'),('original55-map.json',prefix+'WO-PLG-011/native-path-map.json'),('extension-plan.json',oracle['approved_proposal_path']),('extension-map.json',oracle['staging_map_path'])]:
    data=(source/path).read_bytes();(out/name).write_bytes(data)
    records.append(dict(retained_repository_path=path,file=name,bytes=len(data),sha256=sha(data)))
(out/'manifest.json').write_bytes((json.dumps(dict(source_commit=case['commit'],source_export=str(source),payload_files=56,maps_and_plans=4,files=records),indent=2,sort_keys=True)+'\n').encode())
print('Retained56 exact payload files and4 exact maps/plans.')
