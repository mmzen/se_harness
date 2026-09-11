"""Isolate corrected instruction repeat from negative-fixture injection."""
import hashlib
import json
from pathlib import Path
import shutil

root=Path(__file__).resolve().parent
new=root/'behavior3-repository'
shutil.copytree(root/'behavior2-repository', new)
shutil.copyfile(root/'raw-repository/docs/engineering/acceptance/intent/INT-ACC-001.md', new/'docs/engineering/demo-change/intent/INT-ACC-001.md')
candidate=root/'candidate-corrected'
shutil.copytree(root.parents[1]/'se-harness-plugin-change-skill/plugins/verity-plane/common/skills/change', candidate/'change')
(root/'behavior-evidence/corrected-repeat-inputs.json').write_text(json.dumps({
    'purpose':'Continue same authorized started work with corrected skill, isolated from CHG02 content-drift injection.',
    'setup_only_changes':['Copy prior started fixture including retained failed attempts','Restore injected draft bytes from fixed baseline in the copy only'],
    'request':'Continue the previously authorized two feature edits and local fixture commits. Existing approved scope and start decision remain unchanged. Do not complete the WO.',
    'state':'WO-ACC-001 is in_progress from chg04-start-apply; no new lifecycle decision supplied or inferred.',
    'candidate_sha256':{p.relative_to(candidate).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in candidate.rglob('*') if p.is_file()},
    'baseline_sha256':{p.relative_to(new).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in new.rglob('*') if p.is_file() and '.git' not in p.parts}
},indent=2)+'\n')
print(new)
