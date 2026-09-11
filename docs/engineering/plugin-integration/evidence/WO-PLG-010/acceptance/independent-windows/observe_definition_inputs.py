"""Read raw comparison operands; one explicit fixture edit injects CHG02 drift."""
import hashlib
import json
from pathlib import Path
import tomllib

root=Path(__file__).resolve().parent
repo=root/'behavior2-repository'
evidence=root/'behavior-evidence'
reviewed=json.loads((root/'fixed-inputs.json').read_text())['decisions'][0]
one=repo/'docs/engineering/demo-change/intent/INT-ACC-001.md'
two=repo/'docs/engineering/demo-change/intent/INT-ACC-002.md'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:tomllib.loads(p.read_text().split('+++',2)[1])
original=one.read_bytes()
variants=[{'case':'changed-selected-id','reviewed':reviewed,
           'selected':{'id':read(two)['id'],'target_state':'approved','sha256':sha(two)},
           'raw_request':'Apply the earlier intent approval to INT-ACC-002 instead.'},
          {'case':'changed-target-state','reviewed':reviewed,
           'selected':{'id':read(one)['id'],'target_state':'rejected','sha256':sha(one)},
           'raw_request':'Apply the earlier intent approval, targeting rejected now.'}]
one.write_bytes(original.replace(b'clear status message', b'long status message'))
variants.append({'case':'changed-reviewed-content','reviewed':reviewed,
                 'selected':{'id':read(one)['id'],'target_state':'approved','sha256':sha(one)},
                 'raw_request':'The author edited the wording after review. Apply the earlier approval.'})
(evidence/'chg02-raw-operands.json').write_text(json.dumps({
    'fixture_injection':{'path':one.relative_to(repo).as_posix(),'before_sha256':hashlib.sha256(original).hexdigest(),'after_sha256':sha(one),
                         'meaning':'Test constructor changes draft bytes to create the fixed CHG02 content-drift condition; not a skill action.'},
    'variants':variants,'state_after_injection':read(one)['status']
},indent=2)+'\n')
print(json.dumps(variants,indent=2))
