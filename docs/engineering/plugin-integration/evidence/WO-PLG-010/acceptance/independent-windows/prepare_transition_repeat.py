"""Fresh fixture and existing exact decision for lost transition receipt."""
import hashlib
import json
from pathlib import Path
import shutil
root=Path(__file__).resolve().parent
repo=root/'transition-repository'
shutil.copytree(root/'raw-repository',repo)
old,new=repo/'docs/engineering/acceptance',repo/'docs/engineering/demo-change'
assert old.resolve().is_relative_to(repo.resolve()) and new.resolve().is_relative_to(repo.resolve())
old.rename(new)
wo=new/'work-orders/WO-ACC-001.md'
wo.write_text(wo.read_text().replace('docs/engineering/acceptance/','docs/engineering/demo-change/'),encoding='utf8')
intent=new/'intent/INT-ACC-001.md'
decision=json.loads((root/'fixed-inputs.json').read_text())['decisions'][0]
assert hashlib.sha256(intent.read_bytes()).hexdigest()==decision['reviewed_sha256']
(root/'behavior-evidence/chg08-transition-inputs.json').write_text(json.dumps({
    'fixture_only':True,'request':'Apply the exact existing intent approval. If the tool receipt is lost, resume the same request from actual files and history.',
    'decision':decision,'repo':str(repo),'interruption':'Suppress receipt after actual process exit; not an in-flight transaction crash.',
    'initial_sha256':hashlib.sha256(intent.read_bytes()).hexdigest()
},indent=2)+'\n')
print(repo)
