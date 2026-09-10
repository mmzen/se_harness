"""New input fixture repairs a reserved domain name; no candidate behavior."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

root = Path(__file__).resolve().parent
repo = root/'behavior2-repository'
shutil.copytree(root/'raw-repository', repo)
old, new = repo/'docs/engineering/acceptance', repo/'docs/engineering/demo-change'
assert old.resolve().is_relative_to(repo.resolve()) and new.resolve().is_relative_to(repo.resolve())
old.rename(new)
wo = new/'work-orders/WO-ACC-001.md'
wo.write_text(wo.read_text().replace('docs/engineering/acceptance/', 'docs/engineering/demo-change/'), encoding='utf8')
commands = []
for args in [['init','-b','main'],['add','--all'],['-c','user.name=Fixture Owner','-c','user.email=fixture@example.invalid','commit','-m','Fixed disposable baseline'],['update-ref','refs/remotes/origin/main','HEAD']]:
    argv = ['git','-C',str(repo),*args]
    run = subprocess.run(argv, cwd=root, capture_output=True)
    commands.append({'argv': argv, 'exit_code': run.returncode, 'stdout': run.stdout.decode('utf8','replace'), 'stderr': run.stderr.decode('utf8','replace')})
    if run.returncode:
        raise RuntimeError(commands[-1])
decision = {'fixture': 'CHG09-corrected', 'actor': 'engineering-owner', 'right': 'DR-WO-SELECT',
            'id': 'WO-ACC-001', 'target_state': 'approved', 'reviewed_sha256': hashlib.sha256(wo.read_bytes()).hexdigest(),
            'meaning': 'Synthetic test input approves only this exact corrected draft. No start authority is provided.'}
(root/'behavior-evidence/fixture-repair.json').write_text(json.dumps({
    'reason': 'Original fixture incorrectly selected reserved domain slug acceptance; preserved failed attempt as fixture defect.',
    'input_changes': ['New repository with valid demo-change domain', 'WO scoped paths corrected', 'New exact synthetic reviewed decision fixed before test retry'],
    'candidate_changed': False, 'setup_commands': commands, 'decision': decision,
    'baseline': {p.relative_to(repo).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in repo.rglob('*') if p.is_file() and '.git' not in p.parts}
}, indent=2)+'\n')
print(json.dumps(decision, indent=2))
