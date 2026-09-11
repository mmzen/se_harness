"""New raw WO fixture for complete CHG10 state projection coverage."""
import hashlib
import json
from pathlib import Path
import shutil

root=Path(__file__).resolve().parent
repo=root/'readiness-repository'
shutil.copytree(root/'raw-repository', repo)
old,new=repo/'docs/engineering/acceptance',repo/'docs/engineering/demo-change'
assert old.resolve().is_relative_to(repo.resolve()) and new.resolve().is_relative_to(repo.resolve())
old.rename(new)
wo=new/'work-orders/WO-ACC-001.md'
wo.write_text(wo.read_text().replace('docs/engineering/acceptance/','docs/engineering/demo-change/'),encoding='utf8')
decision=json.loads((root/'behavior-evidence/fixture-repair.json').read_text())['decision']
assert hashlib.sha256(wo.read_bytes()).hexdigest()==decision['reviewed_sha256']
(root/'behavior-evidence/chg10-repeat-inputs.json').write_text(json.dumps({
    'fixture_only':True,'request':'Apply the supplied exact WO approval using the change skill. Preserve this unchanged decision through readiness recovery.',
    'decision':decision,'unready_variants':['No delivery for newly selected repository','Only a prior repository delivery is available','An interrupted delivery omits END VERIFIED GOVERNANCE'],
    'repo':str(repo),'initial_state':'draft','initial_wo_sha256':hashlib.sha256(wo.read_bytes()).hexdigest(),
    'expected_from_fixed_oracle':'No mutation before complete verified context; after recovery apply exactly approval and no start.'
},indent=2)+'\n')
prior=json.loads((root/'behavior-evidence/corrected-repeat-context.json').read_text())
context=json.loads(prior['stdout'])['hookSpecificOutput']['additionalContext']
print('Observed stale source:', prior['event']['cwd'])
print('Injected incomplete delivery follows; its ending is intentionally absent:')
print(context[:250])
